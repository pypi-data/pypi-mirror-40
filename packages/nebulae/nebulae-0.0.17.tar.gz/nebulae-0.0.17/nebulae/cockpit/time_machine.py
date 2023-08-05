#!/usr/bin/env python
'''
time_machine
Created by Seria at 23/12/2018 8:34 PM
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
from tensorflow.python.framework import graph_util
import os

class TimeMachine(object):
    def __init__(self, param):
        '''
        Time Machine saves current states or restores saved states
        '''
        self.param = param
        if not param['ckpt_path'] is None:
            if param['ckpt_scope'] is None:
                to_be_restored = tf.global_variables()
            else:
                to_be_restored = tf.global_variables(scope=param['ckpt_scope'])
            self.restorer = tf.train.Saver(to_be_restored)
        if not param['save_path'] is None:
            if param['save_scope'] is None:
                to_be_saved = tf.global_variables()
            else:
                to_be_saved = tf.global_variables(scope=param['save_scope'])
            self.saver = tf.train.Saver(to_be_saved, max_to_keep=1)

    def dateBack(self):
        if os.path.isfile(self.param['ckpt_path']):
            ckpt = self.param['ckpt_path']
        else:
            ckpt = tf.train.latest_checkpoint(self.param['ckpt_path'])
        self.restorer.restore(self.param['sess'], ckpt)

    def saveCkpt(self, step):
        self.saver.save(self.param['sess'], self.param['save_path'], global_step=step, write_meta_graph=True)

    def freezeTheMoment(self, moment):
        out_graph_def = graph_util.convert_variables_to_constants(self.param['sess'],
                                                                  self.param['sess'].graph_def, moment)
        tf.train.write_graph(out_graph_def, os.path.abspath(self.param['frozen_path']),
                             os.path.basename(self.param['frozen_path']), as_text=False)