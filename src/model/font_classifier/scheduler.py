import torch
from importlib import import_module
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR, ReduceLROnPlateau, CyclicLR


class scheduler_module():
    
    # scheduler dict의 이름을 --scheduler 에 인자값으로 넣으면 사용가능
    # scheduler_dict안의 변수들을 바꿔서 customizing
    scheduler_dict = {
            ## torch.optim.lr_scheduler ##
            'StepLR': {'step_size': 10, 'gamma': 0.5}, # 각 step_size마다 gamma 만큼 감소
            'MultiStepLR': {'milestones': [5,10], 'gamma':0.5}, # 각 milestone마다 gamma 만큼 감소
            'ReduceLROnPlateau' : {'factor': 0.5, 'patience': 10}, # patinet 동안 개선이 없으면, 
            'CosineAnnealingLR' : {'T_max': 10, "eta_min":0.00001}, # T_max 주기마다 cos 반복
            'CyclicLR': {'base_lr': 1e-5, "max_lr": 0.01}, #  base_lr to max_lr momentum이 있는 optimizer만 사용가능
            'ExponentialLR': {"gamma": 0.95}, # step마다 gamma만큼 지수적으로 감소
            
            ##timm.scheduler.cosine_lr
            'CosineLRScheduler': {'t_initial':10, 'cycle_limit':10,'cycle_decay':0.5, 'cycle_mul':1.2, 'lr_min':1e-5, 'warmup_t':3, 'warmup_lr_init':1e-5},
            
            ## 직접구현 ##
            'WarmupConstant': {"warmup_steps": 10}, # 초반 warmup_step까지 천천히 증가,
            'SGDR_wrong':{"T_0": 10, "T_mult": 1, "eta_max": 0.002,  "T_up": 2, "gamma": 0.5} # https://gaussian37.github.io/dl-pytorch-lr_scheduler/  -> Custom CosineAnnealingWarmRestarts
            # SGDR 잘못 구현되어 있음
        }
    scheduler_list_implemented = [
            'WarmupConstant',
            'SGDR_wrong'
        ]
    scheduler_list_timm = [
        'CosineLRScheduler'
    ]
        
        
    @staticmethod
    def get_scheduler(cls, scheduler_name, optimizer):
        if scheduler_name not in cls.scheduler_dict.keys():
            raise NotImplementedError(f"{scheduler_name} is not implemented in scheduler.py")
        
        if scheduler_name in cls.scheduler_list_implemented:
            return getattr(import_module("scheduler"), scheduler_name)(optimizer, **cls.scheduler_dict[scheduler_name])
        elif scheduler_name in cls.scheduler_list_timm:
            return getattr(import_module("timm.scheduler.cosine_lr"), scheduler_name)(optimizer, **cls.scheduler_dict[scheduler_name])
        else:
            return getattr(import_module("torch.optim.lr_scheduler"), scheduler_name)(optimizer, **cls.scheduler_dict[scheduler_name])
        
    
class WarmupConstant(torch.optim.lr_scheduler.LambdaLR):
    """ Linear warmup and then constant.
        Linearly increases learning rate schedule from 0 to 1 over `warmup_steps` training steps.
        Keeps learning rate schedule equal to 1. after warmup_steps.
    """
    def __init__(self, optimizer, warmup_steps, last_epoch=-1):

        def lr_lambda(step):
            if step < warmup_steps:
                return (float(step) + 1.0)  *  (1.0 / float(max(1.0, warmup_steps)))
            return 1.

        super(WarmupConstant, self).__init__(optimizer, lr_lambda, last_epoch=last_epoch)
        


import math
from torch.optim.lr_scheduler import _LRScheduler

class SGDR_wrong(_LRScheduler):
    def __init__(self, optimizer, T_0, T_mult=1, eta_max=0.1, T_up=0, gamma=1., last_epoch=-1):
        if T_0 <= 0 or not isinstance(T_0, int):
            raise ValueError("Expected positive integer T_0, but got {}".format(T_0))
        if T_mult < 1 or not isinstance(T_mult, int):
            raise ValueError("Expected integer T_mult >= 1, but got {}".format(T_mult))
        if T_up < 0 or not isinstance(T_up, int):
            raise ValueError("Expected positive integer T_up, but got {}".format(T_up))
        self.T_0 = T_0
        self.T_mult = T_mult
        self.base_eta_max = eta_max
        self.eta_max = eta_max
        self.T_up = T_up
        self.T_i = T_0
        self.gamma = gamma
        self.cycle = 0
        self.T_cur = last_epoch
        super(SGDR_wrong, self).__init__(optimizer, last_epoch)
    
    def get_lr(self):
        if self.T_cur == -1:
            return self.base_lrs
        elif self.T_cur < self.T_up:
            return [(self.eta_max - base_lr)*self.T_cur / self.T_up + base_lr for base_lr in self.base_lrs]
        else:
            return [base_lr + (self.eta_max - base_lr) * (1 + math.cos(math.pi * (self.T_cur-self.T_up) / (self.T_i - self.T_up))) / 2
                    for base_lr in self.base_lrs]

    def step(self, epoch=None):
        if epoch is None:
            epoch = self.last_epoch + 1
            self.T_cur = self.T_cur + 1
            if self.T_cur >= self.T_i:
                self.cycle += 1
                self.T_cur = self.T_cur - self.T_i
                self.T_i = (self.T_i - self.T_up) * self.T_mult + self.T_up
        else:
            if epoch >= self.T_0:
                if self.T_mult == 1:
                    self.T_cur = epoch % self.T_0
                    self.cycle = epoch // self.T_0
                else:
                    n = int(math.log((epoch / self.T_0 * (self.T_mult - 1) + 1), self.T_mult))
                    self.cycle = n
                    self.T_cur = epoch - self.T_0 * (self.T_mult ** n - 1) / (self.T_mult - 1)
                    self.T_i = self.T_0 * self.T_mult ** (n)
            else:
                self.T_i = self.T_0
                self.T_cur = epoch
                
        self.eta_max = self.base_eta_max * (self.gamma**self.cycle)
        self.last_epoch = math.floor(epoch)
        for param_group, lr in zip(self.optimizer.param_groups, self.get_lr()):
            param_group['lr'] = lr