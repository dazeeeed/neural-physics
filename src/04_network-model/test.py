import os
import numpy as np
import pandas as pd

from collections import defaultdict
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
from tensorboard.backend.event_processing import tag_types
import glob
import pandas as pd
import matplotlib.pyplot as plt
import struct

current_path = os.path.dirname(os.path.realpath("__file__"))
data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))
LOG_DIR = os.path.join(data_path, 'logs', 'hparam_tuning_2021-11-22-22-16-58')

event_path = os.path.join(LOG_DIR, 'run-0-adam-60-15', 'validation', 'events.out.tfevents.1637615868.DESKTOP-B717F5U.10160.4.v2')
# event_path = os.path.join(LOG_DIR, 'run-0-adam-60-15', 'train', 'events.out.tfevents.1637615868.DESKTOP-B717F5U.10160.4.v2')

listOutput = (glob.glob("..\\..\\data\\logs\\hparam_tuning_2021-11-15-14-03-33\\run-0-adam-50-1e-05\\*.9.v2"))

listDF = []

# Legacy aliases
COMPRESSED_HISTOGRAMS = tag_types.COMPRESSED_HISTOGRAMS
HISTOGRAMS = tag_types.HISTOGRAMS
IMAGES = tag_types.IMAGES
AUDIO = tag_types.AUDIO
SCALARS = tag_types.SCALARS
TENSORS = tag_types.TENSORS
GRAPH = tag_types.GRAPH
META_GRAPH = tag_types.META_GRAPH
RUN_METADATA = tag_types.RUN_METADATA

def parse_progress(path):
    print(path)
    if path.endswith('config'):
        return 0

    event_acc = EventAccumulator(path,
                                 size_guidance={
                                    COMPRESSED_HISTOGRAMS: 500,
                                    IMAGES: 4,
                                    AUDIO: 4,
                                    SCALARS: 10000,
                                    HISTOGRAMS: 1,
                                    TENSORS: 1000000000000,
                                },
                                compression_bps=None,
                                purge_orphaned_data=False)
    event_acc.Reload()

    tags = event_acc.Tags()
    print(tags)

    # Show all tags in the log file
    tags = event_acc.Tags()['tensors']
    tensors = event_acc.Tensors('evaluation_mean_squared_error_vs_iterations')
    print(tensors)

    wall_time, step, value = [], [], []
    for tensor in tensors:
        wall_time.append(tensor[0])
        step.append(tensor[1])
        tensor_proto = tensor[2]
        binary_val = tensor_proto.tensor_content
        decimal_val = struct.unpack('f', binary_val)[0]
        value.append(decimal_val)



    plt.plot(step, value)
    plt.show()
    # runtimes_scalar = event_acc.Scalars('runtime_ms')
    # runtimes = [runtimes_scalar[i].value for i in range(len(runtimes_scalar))]
    #
    # loss_scalar = event_acc.Scalars('loss')
    # loss = [loss_scalar[i].value for i in range(len(loss_scalar))]
    # assert len(runtimes) == len(loss)

    return 0

parse_progress(event_path)
