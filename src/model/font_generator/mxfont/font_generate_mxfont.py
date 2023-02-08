"""
MX-Font
Copyright (c) 2021-present NAVER Corp.
MIT license
"""

import json
from pathlib import Path
from PIL import Image

import torch
from sconf import Config
from torchvision import transforms
import sys
import torch
import os
sys.path.append(str(Path(os.path.abspath(__file__)).parent))
import models
from datasets import read_font, render
from utils import save_tensor_to_image

def createDirectory(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Failed to create the directory.")

def eval(source_font_list,en_list):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    #weight_path =os.path.join(dir_path, "result/checkpoints/last.pth")
    weight_path =os.path.join(dir_path, "mxfont_weight.pth")
    cfg = Config(os.path.join(dir_path, "cfgs/defaults.yaml"))
    
    transform = transforms.Compose(
        [transforms.Resize((128, 128)), transforms.ToTensor(), transforms.Normalize([0.5], [0.5])]
    )
    
    
    g_kwargs = cfg.get('g_args', {})
    gen = models.Generator(1, cfg.C, 1, **g_kwargs).cuda().eval()
    weight = torch.load(weight_path)
    if "generator_ema" in weight:
        weight = weight["generator_ema"]
    gen.load_state_dict(weight)
    
    for idx, (source_font, en) in enumerate(zip(source_font_list, en_list)):
        if source_font == None:
            continue
        ref_path = os.path.join(os.getenv("HOME"), f'tmp/img{idx}/referenced')
        extension = "png"
        batch_size = 3
        
        
        ref_paths = Path(ref_path).glob(f"*.{extension}")
        ref_imgs = torch.stack([transform(Image.open(str(p))) for p in ref_paths]).cuda()
        ref_batches = torch.split(ref_imgs, batch_size)
        
        
        style_facts = {}

        for batch in ref_batches:
            style_fact = gen.factorize(gen.encode(batch), 0)
        for k in style_fact:
            style_facts.setdefault(k, []).append(style_fact[k])
        
        style_facts = {k: torch.cat(v).mean(0, keepdim=True) for k, v in style_facts.items()}
        
        
        gen_chars = list(set(en))
        save_dir = os.path.join(os.getenv("HOME"), f'tmp/img{idx}/generated_mxfont')
        source_path = os.path.join(os.getenv("HOME"), 'data/font/untypical', source_font)
        
        createDirectory(save_dir)
        
        source_font = read_font(source_path)
        for char in gen_chars:
            source_img = transform(render(source_font, char)).unsqueeze(0).cuda()
            char_facts = gen.factorize(gen.encode(source_img), 1)
            
            gen_feats = gen.defactorize([style_facts, char_facts])
            out = gen.decode(gen_feats).detach().cpu()[0]            
            path = os.path.join(save_dir, f"{hex(ord(char))}.png")
            
            save_tensor_to_image(out, path)