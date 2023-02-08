import json
from pathlib import Path
from PIL import Image
import random

import torch
from torchvision import transforms
import sys
import torch
import os
sys.path.append(str(Path(os.path.abspath(__file__)).parent))
from .models import ftgan_networks
# import models.ftgan_networks as ftgan_networks
from .datasets.utils import font2render
from glob import glob
from util.util import save_image, tensor2im
from options.test_options import TestOptions
import shutil

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")
        
def load_image(path, transform):
    image = Image.open(path).convert("L")
    image = transform(image)
    return image

def patch_instance_norm_state_dict(state_dict, module, keys, i=0):
    """Fix InstanceNorm checkpoints incompatibility (prior to 0.4)"""
    key = keys[i]
    if i + 1 == len(keys):  # at the end, pointing to a parameter/buffer
        if module.__class__.__name__.startswith("InstanceNorm") and (
            key == "running_mean" or key == "running_var"):
            if getattr(module, key) is None:
                state_dict.pop(".".join(keys))
        if module.__class__.__name__.startswith("InstanceNorm") and (
            key == "num_batches_tracked"):
            state_dict.pop(".".join(keys))
    else:
        patch_instance_norm_state_dict(
            state_dict, getattr(module, key), keys, i + 1)

def eval(source_font_list, en_list):     
    transform = transforms.Compose(
        [transforms.Resize((64, 64)), transforms.ToTensor(), transforms.Normalize(mean=(0.5,), std=(0.5,))]
    )
    
    opt = TestOptions().parse()  # get test options
    opt.num_threads = 0  # test code only supports num_threads = 1
    opt.batch_size = 1  # test code only supports batch_size = 1
    opt.display_id = (
        -1
    )  # no visdom display; the test code saves the results to a HTML file.
    device = (
        torch.device("cuda:{}".format(opt.gpu_ids[0]))
        if opt.gpu_ids
        else torch.device("cpu")
    )  # get device name: CPU or GPU  
    style_channel = 6
    dir_path = os.path.dirname(os.path.abspath(__file__))
    weight_path = os.path.join(dir_path, "checkpoints/gasnext_weight.pth")  # epoch_net_G.pth
    gen = ftgan_networks.define_G(
        opt.style_channel + 1,  # number of style image + 1 content image
        1,
        opt.ngf,
        opt.netG,
        opt.norm,
        False,  # no_dropout
        opt.init_type,
        opt.init_gain,
        opt.gpu_ids,
    ).eval()
    if isinstance(gen, torch.nn.DataParallel):
        gen = gen.module
    weight = torch.load(weight_path, map_location=str(device))
    if hasattr(weight, "_metadata"):
        del weight._metadata
        
    gen.load_state_dict(weight)  

    for idx, (source_font, en) in enumerate(zip(source_font_list, en_list)):
        ref_path = os.path.join(os.getenv("HOME"), f'tmp/img{idx}/referenced')
        extension = "png"
        batch_size = 1
        
        ref_paths = list(glob(os.path.join(ref_path, f"*.{extension}")))
        if style_channel > len(ref_paths): 
            #raise Exception("샘플 수가 적어 스타일 추출 불가! (gasnext)")
            # 랜덤 중복 추출 style_channel-ref_paths 만큼 해서 복제해주기!
            for i in range(style_channel-len(ref_paths)): 
                random_img = random.choice(ref_paths)
                ref_img_name, ext = os.path.splitext(random_img)
                shutil.copy(random_img, f'{ref_img_name}_copied_{i}{ext}')
                ref_paths.append(f'{ref_img_name}_copied_{i}{ext}')

        ref_paths = random.sample(ref_paths, style_channel)  # 6개 랜덤 추출
        ref_imgs = torch.cat(
            [load_image(ref_path, transform) for ref_path in ref_paths], 0
        )
            
        gen_chars = list(set(en))
        save_dir = os.path.join(os.getenv("HOME"), f'tmp/img{idx}/generated_gasnext')
        source_path = os.path.join(os.getenv("HOME"), 'data/font/Gulim-01.ttf')
        
        createDirectory(save_dir)
        
        for char in gen_chars:
            source_img = transform(font2render(source_path, char, size=64)).unsqueeze(0).to(device)
        
            style_img = ref_imgs.unsqueeze(0).to(device)
            #print(f"source_img type : {type(source_img)}, shape : {source_img.shape}")
            generated_images = gen((source_img, style_img))  ## 이 아웃풋 형식이 뭐지!!! 알아봐야 함
            path = os.path.join(save_dir, f"{hex(ord(char))}.png")
            
            result_img = tensor2im(generated_images)
            save_image(result_img, path)