#!/usr/bin/env python
'''
utility
Created by Seria at 14/11/2018 8:33 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-

import json
import numpy as np
import subprocess as subp

def toDenseLabel(labels, nclass, on_value=1, off_value=0):
    batch_size = len(labels)
    # initialize dense labels
    one_hot = off_value * np.ones((batch_size * nclass))
    indices = []
    if isinstance(labels[0], str):
        for b in range(batch_size):
            indices += [int(s) + b * nclass for s in labels[b].split(',')]
    else: # labels is a nested list
        for b in range(batch_size):
            indices += [l + b * nclass for l in labels[b]]
    one_hot[indices] = on_value
    return np.reshape(one_hot, (batch_size, nclass))


def getAvailabelGPU(least_mem):
    p = subp.Popen('nvidia-smi', stdout=subp.PIPE)
    gpu_id = 0  # next gpu we are about to probe
    flag_gpu = False
    max_occupied = least_mem
    id_best = -1  # gpu having max avialable memory
    for l in p.stdout.readlines():
        line = l.decode('utf-8').split()
        if len(line) < 1:
            break
        elif len(line) < 2:
            continue
        if line[1] == str(gpu_id):
            flag_gpu = True
            continue
        if flag_gpu:
            occupancy = int(line[8].split('M')[0])
            if occupancy < max_occupied:
                max_occupied = occupancy
                id_best = gpu_id
            gpu_id += 1
            flag_gpu = False
    return id_best

def parseConfig(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def recordConfig(config_path, config):
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)