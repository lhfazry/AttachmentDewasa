#!/bin/bash
CUDA_VISIBLE_DEVICES=$CUDA_ID python tools/train.py configs/recognition/attachment/swin_small_patch244_window877_kinetics400_1k.py --cfg-options model.backbone.pretrained=pretrained/swin_small_patch4_window7_224.pth