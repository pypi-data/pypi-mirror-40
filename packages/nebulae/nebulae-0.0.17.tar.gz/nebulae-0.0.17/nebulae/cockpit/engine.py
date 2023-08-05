#!/usr/bin/env python
'''
engine
Created by Seria at 23/11/2018 2:36 PM
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

import tensorflow as tf
from ..toolkit.utility import getAvailabelGPU

class Engine(object):
    '''
    Param:
    device: 'gpu' or 'cpu'
    available_gpus
    gpu_mem_fraction
    if_conserve
    least_mem
    '''
    def __init__(self, device, available_gpus='', gpu_mem_fraction=1, if_conserve=True, least_mem=2048):
        self.param = {'device': device, 'available_gpus': available_gpus, 'gpu_mem_fraction': gpu_mem_fraction,
                      'if_conserve': if_conserve, 'least_mem': least_mem}
        # look for available gpu devices
        config_proto = tf.ConfigProto(log_device_placement=False)
        config_proto.gpu_options.allow_growth = self.param['if_conserve']
        if self.param['device'].lower() == 'gpu':
            config_proto.gpu_options.per_process_gpu_memory_fraction = self.param['gpu_mem_fraction']
            if not self.param['available_gpus']:
                gpus = getAvailabelGPU(self.param['least_mem'])
                if gpus < 0:
                    raise Exception('No available gpu', gpus)
                else:
                    self.param['available_gpus'] = str(gpus)
            config_proto.gpu_options.visible_device_list = self.param['available_gpus']
            print('+' + (25 * '-') + '+')
            print('| Reside in Device: \033[1;36mGPU-%s\033[0m |' % self.param['available_gpus'])
            print('+' + (25 * '-') + '+')
        elif self.param['device'].lower() == 'cpu':
            print('+' + (23 * '-') + '+')
            print('| Reside in Device: \033[1;36mCPU\033[0m |')
            print('+' + (23 * '-') + '+')
        else:
            raise KeyError('Given device should be either cpu or gpu.')
        # start a session
        self.sess = tf.Session(config=config_proto)

