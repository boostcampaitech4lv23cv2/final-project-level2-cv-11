import multiprocessing
import os
from importlib import import_module
import torch
import sys
sys.path.append(os.path.dirname(__file__))
from collections import defaultdict
from dataset_font import InfDataset



# 경고 off
import warnings
warnings.filterwarnings(action='ignore')

class Typical_FC:
    
    
    def __init__(self, type):
        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")
        self.resize = (256,256)
        self.batch_size = 2
        self.font_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data/fonts/typical")
        self.font_list = os.listdir(self.font_data_dir)
        self.model = torch.load(os.path.join(os.path.dirname(__file__),"weights",type,"weight.pth"), map_location = self.device)
        
    def classification(self, merged_boxes):
        tmp = []
        for idx, boxes in enumerate(merged_boxes):
            imgs = boxes[3]
            #dataset = getattr(import_module("dataset_font"), "InfDataset")(imgs, self.resize)
            dataset = InfDataset(imgs, self.resize)
            loader = torch.utils.data.DataLoader(
                dataset,
                batch_size=self.batch_size,
                num_workers=multiprocessing.cpu_count() // 2,
                shuffle=False,
                pin_memory=self.use_cuda,
                drop_last=False,
            )
            preds_dict = defaultdict(int)
            with torch.no_grad():
                for images in loader:
                    images = images.to(self.device)
                    predict = self.model(images)
                    pred_topk = torch.topk(predict, k= 5, dim = -1)
                    preds = pred_topk.indices
                    values = pred_topk.values
                    for pred, value in zip(preds.cpu().numpy(), values.cpu().numpy()):
                        for p,v in zip(pred, value):
                            preds_dict[p] += v
            
            sorted_dict = sorted(preds_dict.items(), key = lambda item: item[0], reverse = True)
            tmp.append(self.font_list[sorted_dict[0][0]])
        return tmp