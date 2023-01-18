import os
import random
from collections import defaultdict
from enum import Enum
from typing import Tuple, List

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset, Subset, random_split
from torchvision import transforms
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2

class FontDataset(Dataset):
    
    image_paths_train = []
    image_labels_train = []
    
    image_paths_val = []
    image_labels_val = []
    
    def __init__(self, data_dir, val_ratio=0.2, is_train = True):
        self.data_dir = data_dir
        self.transform = None
        self.is_train = is_train
        if is_train:
            self.val_ratio = val_ratio
            self.setup()
            
    
    def setup(self):
        profiles = os.listdir(self.data_dir)
        
        for idx, profile in enumerate(profiles):
            paths = os.listdir(os.path.join(self.data_dir, profile))
            image_path = []
            image_label = []
            for path in paths:
                image_path.append(os.path.join(self.data_dir,profile,path))
                image_label.append(idx)
            tmp_all = set(range(len(image_path)))
            tmp_val = set(random.sample(list(range(len(image_path))), int(len(image_path) * self.val_ratio)))
            tmp_train = tmp_all - tmp_val
        
            self.image_paths_train.extend([image_path[x] for x in tmp_train])
            self.image_labels_train.extend([image_label[x] for x in tmp_train])
            self.image_paths_val.extend([image_path[x] for x in tmp_val])
            self.image_labels_val.extend([image_label[x] for x in tmp_val])
                
    def set_transform(self, transform):
        self.transform = transform
    
    def __getitem__(self, index):
        assert self.transform is not None, ".set_tranform 메소드를 이용하여 transform 을 주입해주세요"
        
        image = self.read_image(index)
        image_transform = self.transform(image)
        
        if self.is_train:
            label = self.image_labels_train[index]
        else:
            label = self.image_labels_val[index]
            
        return image_transform.float(), label
    
    def read_image(self, index):
        if self.is_train:
            image_path = self.image_paths_train[index]
        else:
            image_path = self.image_paths_val[index]
        return Image.open(image_path).convert('RGB')
    
    def __len__(self):
        if self.is_train:
            return len(self.image_paths_train)
        else:
            return len(self.image_paths_val)
    
    
    
class TestDataset(Dataset):
    def __init__(self, img_paths, resize, mean=(0.548, 0.504, 0.479), std=(0.237, 0.247, 0.246)):
        self.img_paths = img_paths
        self.transform = transforms.Compose([
            transforms.Resize(resize, Image.BILINEAR),
            transforms.ToTensor(),
            #transforms.Normalize(mean=mean, std=std),
        ])

    def __getitem__(self, index):
        image = Image.open(self.img_paths[index]).convert('RGB')

        if self.transform:
            image = self.transform(image)
        return image

    def __len__(self):
        return len(self.img_paths)
    

class InfDataset(Dataset):
    def __init__(self, imgs, resize = (256,256)):
        self.imgs = imgs
        self.transform = transforms.Compose([
            transforms.Resize(resize, Image.BILINEAR),
            transforms.ToTensor()
        ])

    def __getitem__(self, index):
        image =  Image.fromarray(self.imgs[index]).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image

    def __len__(self):
        return len(self.imgs)
    
    
    

class BaseAugmentation:
    def __init__(self, resize, mean, std, **args):
        self.transform = transforms.Compose([
            transforms.Resize(resize, Image.BILINEAR),
            transforms.ToTensor(),
            #transforms.Normalize(mean=mean, std=std),
        ])

    def __call__(self, image):
        return self.transform(image)


class UntypicalAugmentation:
    def __init__(self, resize, mean, std, **args):
        self.transform = A.Compose([
            A.Resize(resize[0], resize[1]),
            A.Normalize(mean=mean, std=std), # normalize 먼저 적용
            A.Affine(scale=1, rotate=10, shear=3, mode=cv2.BORDER_REPLICATE),
            ToTensorV2()
        ])

    def __call__(self, image):
        return self.transform(image=np.asarray(image))["image"]


class UntypicalAugmentation_with_space:
    def __init__(self, resize, mean, std, **args):
        self.transform = A.Compose([
            A.OneOf([
                A.CenterCrop(200,200,p = 0.8),
                A.CenterCrop(150,150,p = 1),
                A.CenterCrop(130,130,p = 1),
                A.CenterCrop(105,105,p = 1)
            ],p = 1),
            A.Resize(resize[0], resize[1]),
            A.Affine(scale=1, rotate=10, shear=3, mode=cv2.BORDER_REPLICATE),
            ToTensorV2(),
        ])

    def __call__(self, image):
        return self.transform(image=np.asarray(image))["image"]