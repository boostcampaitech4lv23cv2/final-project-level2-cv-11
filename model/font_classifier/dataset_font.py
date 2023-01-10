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

class FontDataset(Dataset):
    
    image_paths = []
    image_labels = []
    
    def __init__(self, data_dir, val_ratio=0.2):
        self.data_dir = data_dir
        self.val_ratio = val_ratio

        self.transform = None
        self.setup()
    
    def setup(self):
        profiles = os.listdir(self.data_dir)
        
        for idx, profile in enumerate(profiles):
            paths = os.listdir(os.path.join(self.data_dir, profile))
            for path in paths:
                self.image_paths.append(os.path.join(self.data_dir,profile,path))
                self.image_labels.append(idx)
                
    def set_transform(self, transform):
        self.transform = transform
    
    def __getitem__(self, index):
        assert self.transform is not None, ".set_tranform 메소드를 이용하여 transform 을 주입해주세요"
        
        image = self.read_image(index)
        image_transform = self.transform(image)
        
        label = self.image_labels[index]
        return image_transform, label
    
    def read_image(self, index):
        image_path = self.image_paths[index]
        return Image.open(image_path).convert('RGB')
    
    def __len__(self):
        return len(self.image_paths)
    
    def split_dataset(self) -> Tuple[Subset, Subset]:
        """
        데이터셋을 train 과 val 로 나눕니다,
        pytorch 내부의 torch.utils.data.random_split 함수를 사용하여
        torch.utils.data.Subset 클래스 둘로 나눕니다.
        구현이 어렵지 않으니 구글링 혹은 IDE (e.g. pycharm) 의 navigation 기능을 통해 코드를 한 번 읽어보는 것을 추천드립니다^^
        """
        n_val = int(len(self) * self.val_ratio)
        n_train = len(self) - n_val
        train_set, val_set = random_split(self, [n_train, n_val])
        return train_set, val_set
    
    
    
class TestDataset(Dataset):
    def __init__(self, img_paths, resize, mean=(0.548, 0.504, 0.479), std=(0.237, 0.247, 0.246)):
        self.img_paths = img_paths
        self.transform = transforms.Compose([
            transforms.Resize(resize, Image.BILINEAR),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ])

    def __getitem__(self, index):
        image = Image.open(self.img_paths[index]).convert('RGB')

        if self.transform:
            image = self.transform(image)
        return image

    def __len__(self):
        return len(self.img_paths)
    
    
    

class BaseAugmentation:
    def __init__(self, resize, mean, std, **args):
        self.transform = transforms.Compose([
            transforms.Resize(resize, Image.BILINEAR),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ])

    def __call__(self, image):
        return self.transform(image)

import albumentations as A

class UntypicalAugmentation:
    def __init__(self, resize, mean, std, **args):
        self.transform = A.Compose([
            A.Resize(resize),
            A.pytorch.transforms.ToTensor(),
            A.Normalize(mean=mean, std=std),
            A.Affine(scale=1, rotate=10, shear=3, mode=cv2.BORDER_REPLICATE)
        ])

    def __call__(self, image):
        return self.transform(image)