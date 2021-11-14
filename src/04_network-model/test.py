import os
import numpy as np
import pandas as pd

from collections import defaultdict
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import glob
import pandas as pd
import matplotlib.pyplot as plt
import struct

listOutput = (glob.glob("logs\\hparam_tuning\\run-0-adam-60-0.0001\\*"))

listDF = []


def parse_progress(path):
    print(path)
    event_acc = EventAccumulator(path)
    event_acc.Reload()

    tags = event_acc.Tags()
    # print(tags)

    # Show all tags in the log file
    tags = event_acc.Tags()['tensors']
    tensors = event_acc.Tensors('batch_loss')

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

parse_progress(listOutput[0])
