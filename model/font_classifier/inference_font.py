import argparse
import multiprocessing
import os
from importlib import import_module

import pandas as pd
import torch
from torch.utils.data import DataLoader

from dataset_font import FontDataset

# 경고 off
import warnings
warnings.filterwarnings(action='ignore')


@torch.no_grad()
def inference(data_dir, args):
    """
    """
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    
    model = torch.load(args.model_path, map_location = device)
    model.eval()

    img_root = os.path.join(data_dir, 'test')
    image_names = os.listdir(img_root)

    img_paths = [os.path.join(img_root, img_id) for img_id in image_names]
    dataset = getattr(import_module("dataset_font"), args.dataset)(img_paths, args.resize)
    loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=args.batch_size,
        num_workers=multiprocessing.cpu_count() // 2,
        shuffle=False,
        pin_memory=use_cuda,
        drop_last=False,
    )

    print("Calculating inference results..")
    preds = []
    values = []
    with torch.no_grad():
        for idx, images in enumerate(loader):
            images = images.to(device)
            predict = model(images)
            #pred = predict.argmax(dim=-1)
            pred_topk = torch.topk(predict, k= 2, dim = -1)
            pred = pred_topk.indices
            value = pred_topk.values
            preds.extend(pred.cpu().numpy())
            values.extend(value.cpu().numpy())
            
    labels_list =  os.listdir(args.train_data_dir)
    print(labels_list)
    
    for i, pred in enumerate(preds):
        print(f"#{i}_{image_names[i]}")
        for j, idx in enumerate(pred):
            print(f"{labels_list[idx]}, {values[i][j]}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('model_path', type=str, help= ("best model state_dict file path"))

    # Data and model checkpoints directories
    parser.add_argument('--batch_size', type=int, default=2, help='input batch size for validing (default: 1000)')
    parser.add_argument('--resize', type=tuple, default=(256, 256), help='resize size for image when you trained (default: (96, 128))')
    parser.add_argument('--dataset', type=str, default='TestDataset', help="dataset (default: TestDataset)")

    # Container environment
    parser.add_argument('--data_dir', type=str, default='/opt/level3_productserving-level3-cv-11/data/words/ko')
    parser.add_argument('--train_data_dir', type=str, default='/opt/level3_productserving-level3-cv-11/data/words/ko/images')

    

    args = parser.parse_args()

    data_dir = args.data_dir
    #output_dir = args.output_dir

    #os.makedirs(output_dir, exist_ok=True)

    inference(data_dir, args)
    