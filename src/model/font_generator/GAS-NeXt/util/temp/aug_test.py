import albumentations as A
import cv2
from PIL import Image
import numpy as np
import os
import random
import torch
import torchvision.transforms as transforms
from albumentations.pytorch import ToTensorV2
#from options.train_options import TrainOptions

#from data.base_dataset import BaseDataset

'''class FontDataset(BaseDataset):
    def __init__(self): 
        BaseDataset.__init__(self, opt)
        self.data = '/opt/test/GAS-NeXt/datasets/font/train/korean/꽃소금체'
        max_dataset_size = float("inf")
        self.paths = sorted(
            self.make_dataset(self.data, max_dataset_size)
        )  # get image paths
        self.transform = A.Compose([
            A.OneOf([
                A.Affine(rotate=[-45, 45], shear=(-35, 35), 
                        mode=cv2.BORDER_CONSTANT, cval=255),
                A.ElasticTransform(border_mode=cv2.BORDER_CONSTANT,
                                    value=255),
                A.OpticalDistortion(border_mode=cv2.BORDER_CONSTANT,
                                    value=255),
            ], p=0.3),
            A.Normalize(mean=(0.5,), std=(0.5,)),
            ToTensorV2()
        ])
        self.img_size = 286
    
    def __getitem__(self, index):
        # get content path and corresbonding stlye paths
        gt_path = self.paths[index]
        parts = gt_path.split(os.sep)
        #style_paths = self.get_style_paths(parts)
        #content_path = self.get_content_path(parts)
        # load and transform images
        content_image = self.load_image(content_path)
        gt_image = self.load_image(gt_path)
        style_image = torch.cat(
            [self.load_image(style_path) for style_path in style_paths], 0
        )
        return {
            "gt_images": gt_image,
            "content_images": content_image,
            "style_images": style_image,
            "style_image_paths": style_paths,
            "image_paths": gt_path,
        }
        
    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.paths)
    
    def load_image(self, path):
        #print("path")
        image = Image.open(path)
        image = np.array(image)
        image = self.transform(image=image)
        return image["image"]
    
    def make_dataset(root, max_dataset_size=float("inf")):
        images = []
        assert os.path.isdir(root), "%s is not a valid directory" % root
        fnames = os.listdir(root)
        for fname in fnames:
            if is_image_file(fname):
                path = os.path.join(root, fname)
                images.append(path)
        return images[: min(max_dataset_size, len(images))]

class CustomDatasetDataLoader:
    """Wrapper class of Dataset class that performs multi-threaded data loading"""

    def __init__(self, opt):
        """Initialize this class
        Step 1: create a dataset instance given the name [dataset_mode]
        Step 2: create a multi-threaded data loader.
        """
        self.dataset = FontDataset()
        self.batch_size = 1
        print("dataset [%s] was created" % type(self.dataset).__name__)
        self.dataloader = torch.utils.data.DataLoader(
            self.dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=int(8),
        )
        self.max_dataset_size = float("inf")

    def load_data(self):
        return self

    def __len__(self):
        """Return the number of data in the dataset"""
        return min(len(self.dataset), self.max_dataset_size)

    def __iter__(self):
        """Return a batch of data"""
        for i, data in enumerate(self.dataloader):
            if i * self.batch_size >= self.max_dataset_size:
                break
            yield data    '''

from torchvision.utils import save_image

if __name__ == "__main__": 
    #data_loader = CustomDatasetDataLoader(opt)
    #dataset = FontDataset()
    dataroot = '/opt/test/GAS-NeXt/datasets/font/train/korean/꽃소금체'
    images = os.listdir(dataroot)
    '''transform = A.Compose([
        A.OneOf([
            A.OneOf([
                A.Affine(rotate=[-45, 45],  
                    mode=cv2.BORDER_CONSTANT, cval=255),
                A.Affine(shear=(-35, 35), 
                    mode=cv2.BORDER_CONSTANT, cval=255),
            ], p=1),
            A.ElasticTransform(alpha=0.5, sigma=0.25,
                           alpha_affine=5,
                           border_mode=cv2.BORDER_CONSTANT,
                           value=255),
            A.OpticalDistortion(distort_limit=0.2, border_mode=cv2.BORDER_CONSTANT,
                                value=255),
        ], p=0.3),
        A.Normalize(mean=(0.5,), std=(0.5,)),
        ToTensorV2()
    ])'''  # 120, affine *0.03, sigma*0.05
    transform = A.Compose([ 
        A.OpticalDistortion(distort_limit=0.2,
                            border_mode=cv2.BORDER_CONSTANT,
                                value=255, p=1),
        A.Normalize(mean=(0.5,), std=(0.5,)),
        ToTensorV2()
    ])
    img_size = 286
    output_path = './results/'
    for image in images: 
        img = Image.open(os.path.join(dataroot, image))
        img = np.array(img)
        img = transform(image=img)
        save_image(img["image"], os.path.join(output_path, image))
        print(f"{image} saved!!")
        #print(type(image["image"]))
    