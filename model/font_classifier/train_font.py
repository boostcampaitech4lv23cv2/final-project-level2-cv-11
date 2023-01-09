import argparse
import glob
import json
import multiprocessing
import os
import random
import re
from importlib import import_module
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
import wandb

from scheduler import scheduler_module
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from PIL import Image
from loss import create_criterion
from torchmetrics import ConfusionMatrix, F1Score
from torchmetrics.classification import MulticlassF1Score, MulticlassAccuracy
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# 경고 off
import warnings
warnings.filterwarnings(action='ignore')


# 재현성
def seed_everything(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if use multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']
    
# 자동 경로 추가
def increment_path(path, exist_ok=False):
    """ Automatically increment path, i.e. runs/exp --> runs/exp0, runs/exp1 etc.
    Args:
        path (str or pathlib.Path): f"{model_dir}/{args.name}".
        exist_ok (bool): whether increment path (increment if False).
    """
    path = Path(path)
    if (path.exists() and exist_ok) or (not path.exists()):
        return str(path)
    else:
        dirs = glob.glob(f"{path}*")
        matches = [re.search(rf"%s(\d+)" % path.stem, d) for d in dirs]
        i = [int(m.groups()[0]) for m in matches if m]
        n = max(i) + 1 if i else 2
        return f"{path}{n}"
    
    
# -- train
def train(data_dir, model_dir, args):
    seed_everything(args.seed)
    
    save_dir = increment_path(os.path.join(model_dir, args.name))
    
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    
    
    dataset_module = getattr(import_module("dataset_font"), args.dataset)
    dataset_train = dataset_module(
        data_dir=data_dir,
        val_ratio = args.val_ratio,
        is_train = True
    )
    
    num_classes = len(os.listdir(args.data_dir)) # font의 개수
    
    # -- augmentation
    transform_module = getattr(import_module("dataset_font"), args.train_augmentation)  # default: BaseAugmentation
    transform = transform_module(
        resize=args.resize,
        mean=(0.548, 0.504, 0.479), 
        std=(0.237, 0.247, 0.246)
    )
    
    # -- data_loader & sampler
    dataset_train.set_transform(transform)
    
    dataset_val = dataset_module(
        data_dir=data_dir,
        val_ratio = args.val_ratio,
        is_train = False
    )
    dataset_val.set_transform(transform)
    
    
    transform = transform_module(
        resize=args.resize,
        mean=(0.548, 0.504, 0.479), 
        std=(0.237, 0.247, 0.246)
    )
    
    
    train_loader = DataLoader(
        dataset_train,
        batch_size=args.batch_size,
        num_workers=multiprocessing.cpu_count() // 2,
        shuffle=True,
        pin_memory=use_cuda,
        drop_last=True
    )
    
    val_loader = DataLoader(
        dataset_val,
        batch_size=args.valid_batch_size,
        num_workers=multiprocessing.cpu_count() // 2,
        shuffle=False,
        pin_memory=use_cuda,
        drop_last=False,
    )
    
    model_module = getattr(import_module("model_font"), args.model)  # default: ResNet50
    model = model_module(num_classes=num_classes).to(device)
    model = torch.nn.DataParallel(model)
    
    # --loss
    criterion = create_criterion(args.criterion)  # default: cross_entropy
    if args.optimizer == "AdamP":
        opt_module = getattr(import_module("adamp"), args.optimizer)
    else:
        opt_module = getattr(import_module("torch.optim"), args.optimizer)  # default: Adam
    
    # --optimizer
    optimizer = opt_module(
        model.parameters(),
        lr=args.lr,
        weight_decay=5e-4
    )
    
    # --scheduler
    if args.scheduler != "None":
        scheduler = scheduler_module.get_scheduler(scheduler_module,args.scheduler, optimizer)
    
    for epoch in tqdm(range(args.epochs)):
        
        # -- train loop
        model.train()
        loss_value = 0
        matches = 0
        loss_value_sum = 0
        train_acc_sum = 0
        for idx, train_batch in enumerate(train_loader):
            inputs, labels = train_batch
            inputs = inputs.to(device)
            labels = labels.to(device)
        
            outs = model(inputs)
            loss = criterion(outs, labels)
        
            optimizer.zero_grad()
        
            loss.backward()
            optimizer.step()
        
            loss_value += loss.item()
            preds = torch.argmax(outs, dim=-1)
            matches += (preds == labels).sum().item()
            if (idx + 1) % args.log_interval == 0:
                train_loss = loss_value / (idx +1)
                train_acc = matches / args.batch_size / (idx +1)
                current_lr = get_lr(optimizer)
                print(
                    f"Epoch[{epoch}/{args.epochs}]({idx + 1}/{len(train_loader)}) || "
                    f"training loss {train_loss:4.4} || training accuracy {train_acc:4.2%} || lr {current_lr}"
                )
                # logs
                wandb.log({
                    "Train/loss": train_loss,
                    "Train/accuracy": train_acc,
                    "step" : epoch * len(train_loader) + idx + 1
                    })

                
        loss_value_sum = loss_value / args.log_interval
        train_acc_sum =  matches / args.batch_size / len(train_loader)
        wandb.log({
            "Train/loss_epoch": loss_value_sum,
            "Train/accuracy_epcoh": train_acc_sum,
            "lr": current_lr,
            "epoch": epoch
            })
        
        
        # val loop
        with torch.no_grad():
            print("Calculating validation results...")
            model.eval()
            val_loss_items = []
            val_acc_items = []
            preds_expand = torch.tensor([])
            labels_expand = torch.tensor([])
            
            for val_batch in val_loader:
                inputs, labels = val_batch
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                outs = model(inputs)
                loss = criterion(outs, labels)
                # -- calculate metrics(loss, acc, f1)
                preds = torch.argmax(outs, dim=-1)
                loss_item = criterion(outs, labels).item()
                acc_item = (labels == preds).sum().item()
                val_loss_items.append(loss_item)
                val_acc_items.append(acc_item)
                
                preds_expand = torch.cat((preds_expand, preds.detach().cpu()),-1)
                labels_expand = torch.cat((labels_expand, labels.detach().cpu()),-1)
                
            # -- evaluation
            f1 = MulticlassF1Score(num_classes=num_classes)
            f1_score = f1(preds_expand.type(torch.LongTensor), labels_expand.type(torch.LongTensor)).item()
            val_loss = np.sum(val_loss_items) / len(dataset_val)
            val_acc = np.sum(val_acc_items) / len(dataset_val)
            
            print(f"[Val] acc : {val_acc:4.2%}, loss: {val_loss:4.2}, f1: {f1_score:4.4} ")
            
            wandb.log({
                "Val/loss": val_loss,
                "Val/accuracy": val_acc,
                "Val/f1_score": f1_score
            })
            
        if (epoch + 1) % args.save_interval == 0:
            # model save
            torch.save(model, f"{save_dir}/{epoch}.pth")
            
        # --scheduler
        if args.scheduler != "None":
            scheduler.step()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Data and model checkpoints directories
    parser.add_argument('--seed', type=int, default=42, help='random seed (default: 42)')
    parser.add_argument('--epochs', type=int, default=200, help='number of epochs to train (default: 200)')
    parser.add_argument('--dataset', type=str, default='FontDataset', help='dataset augmentation type (default: Ma skBaseDataset)') 
    parser.add_argument('--train_augmentation', type=str, default='BaseAugmentation', help='data augmentation type (default: BaseAugmentation)')
    parser.add_argument('--val_augmentation', type=str, default='BaseAugmentation', help='data augmentation type (default: BaseAugmentation)')
    parser.add_argument("--resize", nargs="+", type=int, default=[256, 256], help='resize size for image when training')
    parser.add_argument('--batch_size', type=int, default=64, help='input batch size for training (default: 64)')
    parser.add_argument('--valid_batch_size', type=int, default=10, help='input batch size for validing (default: 1000)')
    parser.add_argument('--model', type=str, default='ResNet50', help='model type (default: ResNet50)')
    parser.add_argument('--optimizer', type=str, default='Adam', help='optimizer type (default: Adam)')
    parser.add_argument('--lr', type=float, default=1e-3, help='learning rate (default: 1e-3)')
    parser.add_argument('--val_ratio', type=float, default=0.01, help='ratio for validaton (default: 0.2)')
    parser.add_argument('--criterion', type=str, default='cross_entropy', help='criterion type (default: cross_entropy)')
    parser.add_argument('--log_interval', type=int, default=20, help='how many batches to wait before logging training status')
    parser.add_argument('--name', default='exp', help='model save at {SM_MODEL_DIR}/{name}')
    parser.add_argument('--scheduler', type=str, default='None', help='scheduler(default:None), scheduler list in scheduler.py')
    parser.add_argument('--save_interval', type=int, default=5, help='how many epochs to wait before save pth')
    
    # Container environment
    parser.add_argument('--data_dir', type=str, default='/opt/level3_productserving-level3-cv-11/data/words/ko/typical_images') 
    parser.add_argument('--model_dir', type=str, default = './experiment/classifier')
    
    # wandb
    parser.add_argument('--tags', default= None, nargs='+',type=str, help = "프로젝트 태그 할당")
    args = parser.parse_args()
    print(args)

    data_dir = args.data_dir
    model_dir = args.model_dir
    
    wandb.init(entity = "miho",
               project = "Final-Project",
               sync_tensorboard=True,
               name = args.name,
               tags = args.tags)
    wandb.config.update(args)
    
    train(data_dir, model_dir, args)