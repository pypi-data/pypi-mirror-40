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
# import tensorflow as tf
# import time
# from enum import Enum
# from collections import defaultdict
#
#
# class Events(Enum):
#     EPOCH_STARTED = "epoch_started"
#     EPOCH_COMPLETED = "epoch_completed"
#     STARTED = "started"
#     COMPLETED = "completed"
#     ITERATION_STARTED = "iteration_started"
#     ITERATION_COMPLETED = "iteration_completed"
#     EXCEPTION_RAISED = "exception_raised"
#
#
# class State(object):
#     def __init__(self, **kwargs):
#         self.iteration = 0
#         self.output = None
#         self.batch = None
#         for k, v in kwargs.items():
#             setattr(self, k, v)
#
#
# class Engine(object):
#     def __init__(self, process_function):
#         self._process_function = process_function
#         self.state = None
#         self._allowed_events = []
#         self._event_handlers = defaultdict(list)
#         self.register_events(*Events)
#
#     def register_events(self, *event_names):
#         self._allowed_events.extend(event_names)
#
#     def add_event_handler(self, event_name, handler, *args, **kwargs):
#         if event_name not in self._allowed_events:
#             raise ValueError("Event {} is not a valid event for this Engine".format(event_name))
#
#         self._event_handlers[event_name].append((handler, args, kwargs))
#
#     def fire_event(self, event_name):
#         if event_name in self._allowed_events:
#             for func, args, kwargs in self._event_handlers[event_name]:
#                 func(self, *args, **kwargs)
#
#     def on(self, event_name):
#         def decorator(f):
#             self.add_event_handler(event_name, f)
#             return f
#         return decorator
#
#     def _run_once_on_dataset(self):
#         try:
#             for batch in self.state.dataloader:
#                 self.state.batch = batch
#                 self.state.iteration += 1
#                 self.fire_event(Events.ITERATION_STARTED)
#                 self.state.output = self._process_function(self, batch)
#                 self.fire_event(Events.ITERATION_COMPLETED)
#
#         except BaseException as e:
#             if Events.EXCEPTION_RAISED in self._event_handlers:
#                 self.fire_event(Events.EXCEPTION_RAISED)
#             else:
#                 raise e
#
#
#     def run(self, data, max_epochs=1):
#         self.state = State(dataloader=data, epoch=0, max_epochs=max_epochs, metrics={})
#
#         try:
#             self.fire_event(Events.STARTED)
#             while self.state.epoch < max_epochs:
#                 self.state.epoch += 1
#                 self.fire_event(Events.EPOCH_STARTED)
#                 self._run_once_on_dataset()
#                 self.fire_event(Events.EPOCH_COMPLETED)
#
#             self.fire_event(Events.COMPLETED)
#
#         except BaseException as e:
#             if Events.EXCEPTION_RAISED in self._event_handlers:
#                 self.fire_event(Events.EXCEPTION_RAISED)
#             else:
#                 raise e
#
#         return self.state
#
#
# class Navigator(object):
#     def __init__(self, config=None, ):