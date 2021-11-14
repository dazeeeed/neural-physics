import os
import numpy as np
import pandas as pd
from collections import defaultdict
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import glob
import matplotlib.pyplot as plt
import struct
import re

# STRUCTURE
#
# hparam_tuning/
# ├── run-0-.../
# │   ├── train/
# │   │   ├── not important things (it seems like)
# │   │   └── plugins/
# │   │       └── even more not important things
# │   └── event_file
# │   │   ├── ???
# │   │   └── tags
# │   │       ├── images
# │   │       ├── audio
# │   │       ├── ...
# │   │       └── tensors
# │   │           ├── '_hparams_/session_start_info' (not important i think)
# │   │           ├── 'batch_loss'
# │   │           │    ├── TensorEvent
# │   │           │    │   ├── TensorEvent[0] (Wall time)
# │   │           │    │   ├── TensorEvent[1] (Step)
# │   │           │    │   └── TensorEvent[2] (TensorProto)
# │   │           │    │       ├── dtype
# │   │           │    │       ├── ...
# │   │           │    │       └── tensor_content (binary value of loss)
# │   │           │    ├── ...
# │   │           │    └── TensorEvent
# │   │           ├── 'batch_mean_squared_error'
# │   │           ├── 'batch_mean_absolute_error'
# │   │           └── '_hparams_/session_end_info' (not important i think)
# │   └── event_file2
# ├── run-1-.../
# ├── run-2-.../
# └── ...



class Run():
    def __init__(self, path):
        self._path = path
        self._name = re.search("(run-.*)", path).group(0)
        values = re.search("run-(\\d+)-(\\w+)-(\\d+)-(0.\\d+)", self._name)
        self._run_number   = values[0]
        self._optimizer    = values[1]
        self._num_units1   = values[2]
        self._dropout_rate = values[3]
        self._tensor_labels = []
        self._data_dict = {}

    def __str__(self):
        # return "Name: {}\nWall time: {}\nStep: {}\nValue: {}\n".format(self.get_name())
        return "Name: {}".format(self.get_name())

    def get_name(self):
        return self._name

    def parse_progress(self):
        event_acc = EventAccumulator(self._path)
        event_acc.Reload()

        # Show all tags in the log file
        tags = event_acc.Tags()
        # print(tags)

        tensors_labels = event_acc.Tags()['tensors']
        tensors_labels.remove('_hparams_/session_start_info')
        tensors_labels.remove('_hparams_/session_end_info')
        self._tensors_labels = tensors_labels
        # tensors = event_acc.Tensors('batch_loss')
        for tensors_label in tensors_labels:
            self._data_dict[tensors_label] = {'wall_time': [], 'step': [], 'value': []}
            tensor_events = event_acc.Tensors(tensors_label)

            for tensor_event in tensor_events:
                self._data_dict[tensors_label]['wall_time'].append(tensor_event[0])
                self._data_dict[tensors_label]['step'].append(tensor_event[1])
                tensor_proto = tensor_event[2]
                binary_val = tensor_proto.tensor_content
                decimal_val = struct.unpack('f', binary_val)[0]
                self._data_dict[tensors_label]['value'].append(decimal_val)

    def get_data(self):
        return self._data_dict


current_path = os.path.dirname(os.path.realpath("__file__"))
data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))
LOG_DIR = os.path.join(data_path, 'logs', 'hparam_tuning')

run_paths = glob.glob(LOG_DIR + "/run*")

runs = []

fig, ax = plt.subplots()
for run_path in run_paths:
    run = Run(run_path)
    run.parse_progress()
    runs.append(run)
    ax.plot(run.get_data().get('batch_loss').get('step'), run.get_data().get('batch_loss').get('value'))

ax.set_yscale('log')
# print(runs[0].get_data().get('batch_loss').get('step'))
plt.show()


# def parse_progress(path):
#     event_acc = EventAccumulator(path)
#     event_acc.Reload()
#
#     # Show all tags in the log file
#     tags = event_acc.Tags()
#     # print(tags)
#
#     tensors_labels = event_acc.Tags()['tensors']
#     tensors_labels.remove('_hparams_/session_start_info')
#     tensors_labels.remove('_hparams_/session_end_info')
#     print(tensors_labels)
#     # tensors = event_acc.Tensors('batch_loss')
#     tensors = event_acc.Tensors('batch_mean_squared_error')
#
#
#     wall_time, step, value = [], [], []
#     for tensor in tensors:
#         wall_time.append(tensor[0])
#         step.append(tensor[1])
#         tensor_proto = tensor[2]
#         binary_val = tensor_proto.tensor_content
#         decimal_val = struct.unpack('f', binary_val)[0]
#         value.append(decimal_val)


    # plt.plot(step, value)
    # plt.show()
    # runtimes_scalar = event_acc.Scalars('runtime_ms')
    # runtimes = [runtimes_scalar[i].value for i in range(len(runtimes_scalar))]
    #
    # loss_scalar = event_acc.Scalars('loss')
    # loss = [loss_scalar[i].value for i in range(len(loss_scalar))]
    # assert len(runtimes) == len(loss)

    # return 0

# parse_progress(run_paths[0])
