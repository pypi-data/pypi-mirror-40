#!/usr/bin/env python
'''
navigator
Created by Seria at 23/12/2018 11:21 AM
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
import time
from copy import deepcopy
from collections import defaultdict

class Stage(object):
    START = 'START'
    END = 'END'
    EPOCH_START = 'EPOCH START'
    EPOCH_END = 'EPOCH END'
    FORWARD = 'FORWARD'
    PREFLIGHT = 'PREFLIGHT'
    ANALYZE = 'ANALYZE'
    BREAK_DOWN = 'BREAK DOWN'
    stage_name = [START, END, EPOCH_START, EPOCH_END, FORWARD, PREFLIGHT, ANALYZE, BREAK_DOWN]
    stage_cnt = len(stage_name)

    @classmethod
    def register(cls, stages):
        for stg in stages:
            stg = stg.upper()
            if stg in cls.stage_name:
                raise Exception('%s is an existing component in warehouse.' % stg)
            exec('Stage.%s = "%s"' % (stg, stg))
            cls.stage_name.append(stg)
            cls.stage_cnt += 1



class Navigator(object):
    roman_numeral = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
    def __init__(self, engine, time_machine, fuel_depot, space_craft, dashboard):
        config = {'NG': engine.param, 'TM':time_machine.param, 'FD': {},
                  'LS': space_craft.layout_sheet.param, 'DB': dashboard.param}
        ft = fuel_depot.dataset
        for k in ft.keys():
            config['FD'][k] = ft[k].param

        self.propellants = defaultdict(list)
        self.epoch = 0
        self.mile = 0
        self.mpe = 0
        self.batch = {}
        self.destination = {}
        self.macro_stage = ''
        # start a session
        self.sess = tf.Session(config=engine.config_proto)
        self.time_machine = time_machine
        self.fuel_depot = fuel_depot
        self.space_craft = space_craft
        self.layout_sheet = space_craft.layout_sheet
        self.dashboard = dashboard
        self.feedPropellant(Stage.START, self.time_machine._setParams,
                            sess=self.sess, mile=self.space_craft.mile, scope=self.space_craft.scope, config=config)
        self.feedPropellant(Stage.START, self.time_machine.backTo)
        self.feedPropellant(Stage.END, self.layout_sheet.log)
        self.feedPropellant(Stage.END, self.dashboard.log)

    def feedPropellant(self, stage, propellant, position=None, condition='True', **kwargs):
        if isinstance(position, int):
            quantity = len(self.propellants[stage])
            if position < quantity:
                self.propellants[stage][position] = (propellant, condition, kwargs)
            else:
                for p in range(quantity, position):
                    self.propellants[stage].append((None, 'False'))
        self.propellants[stage].append((propellant, condition, kwargs))

    def _airDrop(self, stage, n, **kwargs):
        # kwargs.update(self.propellants[stage][n][2])
        self.propellants[stage][n] = self.propellants[stage][n][0:2] + (kwargs,)

    def _triggerStage(self, curr_stage):
        mile = self.mile
        epoch = self.epoch
        stage = self.macro_stage
        stats = []
        cnt = 0
        for ppl, cond, kwargs in self.propellants[curr_stage]:
            if curr_stage == stage:
                self.micro_stage = self.roman_numeral[cnt]
            if_meet = eval(cond)
            if (ppl is None) or (not if_meet):
                stats.append(None)
                cnt += 1
                continue
            stats.append(ppl(**kwargs))
            cnt += 1
        return stats

    def runAMile(self, fuel_line, pass_by=(), destination=(), interval=1):
        assert len(pass_by)+len(destination) > 0
        start = time.time()
        fl = {}
        filled_fl = {}
        quan_preflight = len(self.propellants[Stage.PREFLIGHT])
        if quan_preflight == 0: # no propellant in Preflight stage
            for i, k in enumerate(fuel_line.keys()):
                if isinstance(fuel_line[k], str):
                    fl[self.space_craft.layout[k]] = self.batch[fuel_line[k]]
                    filled_fl[k] = self.batch[fuel_line[k]]
                else:
                    fl[self.space_craft.layout[k]] = fuel_line[k]
                    filled_fl[k] = fuel_line[k]
        else:
            for i, k in enumerate(fuel_line.keys()):
                filled_fl[k] = self.batch[fuel_line[k]]
            for i in range(quan_preflight):
                self._airDrop(Stage.PREFLIGHT, i, fuel_line=filled_fl)
            temp_fl = self._triggerStage(Stage.PREFLIGHT)
            for tfl in temp_fl:
                if not tfl is None:
                    for k in tfl.keys():
                        fl[self.space_craft.layout[k]] = tfl[k]
                    break

        pb = [self.space_craft.layout[k] for k in pass_by]
        dst = [self.space_craft.layout[k] for k in destination]
        spot = self.sess.run(pb + dst, fl)
        spot = spot[len(pass_by):len(pass_by)+len(destination)]
        sp = {}
        filled_sp = {}
        for j in range(len(destination)):
            filled_sp[destination[j]] = spot[j]
        quan_analyzer = len(self.propellants[Stage.ANALYZE])
        if quan_analyzer == 0:  # no propellants in Analyze stage
            sp = deepcopy(filled_sp)
        else:
            for j in range(quan_analyzer):
                self._airDrop(Stage.ANALYZE, j, fuel_line=filled_fl, destination=filled_sp)
            temp_sp = self._triggerStage(Stage.ANALYZE)
            for tsp in temp_sp:
                if not tsp is None:
                    sp = tsp
                    break

        prefix = self.macro_stage + '-' + self.micro_stage + ':'
        for k in sp.keys():
            self.destination[prefix + k] = sp[k]
        self.dashboard._gaugeMile(self.destination.items(), self.mile, self.epoch, self.mpe,
                                  time.time()-start, interval)

    def runAnEpoch(self, fuel_tank, interval=1, miles=-1):
        start = time.time()
        self.mpe = self.fuel_depot.milesPerEpoch(fuel_tank)
        if miles < 0:
            miles = self.mpe
        for mi in range(miles):
            self.mile = mi
            self.batch = self.fuel_depot.nextBatch(fuel_tank)
            self._triggerStage(Stage.FORWARD)

        self.dashboard._gaugeEpoch(self.destination.keys(), self.epoch, self.mpe, time.time()-start, interval)
        self.destination = {}

    def launch(self, epochs=1):
        try:
            print('+' + 35 * '-' + '+')
            print('| The Spacecraft is being launched. |')
            print('+' + 35 * '-' + '+')
            self._triggerStage(Stage.START)
            if epochs < 0 or not isinstance(epochs, int):
                raise ValueError('epochs must be a non-positive integer.')
            for ep in range(epochs):
                self.epoch = ep
                self.macro_stage = Stage.EPOCH_START
                self._triggerStage(Stage.EPOCH_START)
                self.macro_stage = Stage.EPOCH_END
                self._triggerStage(Stage.EPOCH_END)
            self._triggerStage(Stage.END)
            print('+' + 44 * '-' + '+')
            print('| The Spacecraft has arrived at destination. |')
            print('+' + 44 * '-' + '+')

        except BaseException as e:
            if Stage.BREAK_DOWN in self.propellants:
                self._triggerStage(Stage.BREAK_DOWN)
            else:
                raise e