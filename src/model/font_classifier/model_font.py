import torch
import torch.nn as nn
import torch.nn.functional as F



## efficientnet_b0
# from torchvision.models import efficientnet_b0
# class EfficientNet_B0(nn.Module):
#     def __init__(self, num_classes):
#         super().__init__()
#         self.backbone = efficientnet_b0()
#         self.backbone.classifier = nn.Sequential(
#             nn.Linear(1280, 1024),
#             nn.LeakyReLU(),
#             nn.BatchNorm1d(1024),
#             nn.Linear(1024, 512),
#             nn.LeakyReLU(),
#             nn.BatchNorm1d(512),
#             nn.Linear(512, 128),
#             nn.LeakyReLU(),
#             nn.BatchNorm1d(128),
#             nn.Linear(128, num_classes)
#         )

#     def forward(self, x):
#         output = self.backbone(x)
#         return output
    
    
    
## resnet50
from torchvision.models import resnet50
class ResNet50(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.backbone = resnet50(pretrained=False)
        self.backbone.fc = nn.Sequential(
            nn.Linear(2048, 1024),
            nn.LeakyReLU(),
            nn.BatchNorm1d(1024),
            nn.Linear(1024, 512),
            nn.LeakyReLU(),
            nn.BatchNorm1d(512),
            nn.Linear(512, 128),
            nn.LeakyReLU(),
            nn.BatchNorm1d(128),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, x):
        x = self.backbone(x)
        return x