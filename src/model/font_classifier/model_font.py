import torch
import torch.nn as nn
import torch.nn.functional as F

## resnet50
from torchvision.models import resnet50


class ResNet50(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.backbone = resnet50()
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
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        x = self.backbone(x)
        return x
