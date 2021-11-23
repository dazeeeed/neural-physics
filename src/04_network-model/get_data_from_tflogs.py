import os
import time
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
from tensorboard.backend.event_processing import tag_types
import glob
import struct
import re
import matplotlib.pyplot as plt
import numpy as np

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

size_guidance = {
    COMPRESSED_HISTOGRAMS: 500,
    IMAGES: 4,
    AUDIO: 4,
    SCALARS: 10000,
    HISTOGRAMS: 1,
    TENSORS: 1e20,
}


class Run:
    def __init__(self, path, does_validation_exist):
        self._path = path
        self._name = re.search("(run-.*)", path).group(0)
        # values = re.search("run-(\\d+)-(\\w+)-(\\d+)-(0.\\d+)", self._name) # for dropout name
        # values = re.search("run-(\\d+)-(\\w+)-(\\d+)-(\\d+)", self._name) # for NH1, NH2 name
        # values = re.search("run-(\\d+)-(\\w+)-(\\d+)-(\\d+)-(\\w+)", self._name) # for NH1, NH2, activation name
        #
        # try:
        #     values[4]
        # except TypeError:
        #     print("You probably have wrong filenames.")
        #
        # self._run_number = values[0]
        # self._optimizer = values[1]
        # self._num_units1 = values[2]
        # self._dropout_rate = values[3]
        # self._activation = "unknown" | values[4]
        self._data_dict = {}
        self._data_dict_val = {}
        self._does_validation_exist = does_validation_exist

    def __str__(self):
        # return "Name: {}\nWall time: {}\nStep: {}\nValue: {}\n".format(self.get_name())
        return "Name: {}".format(self.get_name())

    def get_name(self):
        return self._name

    def parse_progress(self, suffix=''):
        event_acc = EventAccumulator(os.path.join(self._path, suffix),
                                     size_guidance=size_guidance,
                                     compression_bps=None,
                                     purge_orphaned_data=False)
        event_acc.Reload()
        tags = event_acc.Tags()
        # print(tags)

        tensors_labels = event_acc.Tags()['tensors']
        labels_to_remove = ['_hparams_/session_start_info', '_hparams_/session_end_info']

        if suffix == 'validation':
            for tensors_label in tensors_labels:
                self._data_dict_val[tensors_label] = TensorLabelElement()
                tensor_events = event_acc.Tensors(tensors_label)

                for tensor_event in tensor_events:
                    self._data_dict_val[tensors_label].append_wall_time(tensor_event[0])
                    self._data_dict_val[tensors_label].append_step(tensor_event[1])
                    self._data_dict_val[tensors_label].append_value(tensor_event[2])
            return None

        for value in labels_to_remove:
            if value in tensors_labels:
                tensors_labels.remove(value)

        for tensors_label in tensors_labels:
            self._data_dict[tensors_label] = TensorLabelElement()
            tensor_events = event_acc.Tensors(tensors_label)

            for tensor_event in tensor_events:
                self._data_dict[tensors_label].append_wall_time(tensor_event[0])
                self._data_dict[tensors_label].append_step(tensor_event[1])
                self._data_dict[tensors_label].append_value(tensor_event[2])

    def parse_events(self):
        self.parse_progress()
        if self._does_validation_exist:
            self.parse_progress(suffix='validation')

    def get_train_data(self):
        return self._data_dict

    def get_val_data(self):
        return self._data_dict_val

    def does_validation_exist(self):
        return self._does_validation_exist


class TensorLabelElement:
    def __init__(self):
        self._wall_times = []
        self._steps = []
        self._values = []

    def append_wall_time(self, value: float):
        self._wall_times.append(value)

    def append_step(self, value: float):
        self._steps.append(value)

    def append_value(self, tensor_proto):
        binary_val = tensor_proto.tensor_content
        decimal_val = struct.unpack('f', binary_val)[0]
        self._values.append(decimal_val)

    def get_wall_times(self):
        return np.array(self._wall_times)

    def get_steps(self):
        return np.array(self._steps)

    def get_values(self):
        return np.array(self._values)


def smoothen(array, precision):
    """
    Parameters
    ----------
    array - list of values
    precision - number of neighbours from one side to take mean from

    Returns
    -------
    np.array - smoothed array
    """
    smoothed = np.zeros(shape=(len(array)))
    for i, value in enumerate(array):
        if i < precision or i > len(array) - precision - 1:
            smoothed[i] = value
        else:
            mean_from = array[i - precision:i + precision + 1]
            smoothed[i] = np.sum(mean_from) / len(mean_from)

    return np.array(smoothed)


def main():
    current_path = os.path.dirname(os.path.realpath("__file__"))
    data_path = os.path.abspath(os.path.join(current_path, '..', '..', 'data'))
    LOG_DIR = os.path.join(data_path, 'logs', 'hparam_tuning_2021-11-23-17-43-59')

    run_paths = glob.glob(LOG_DIR + "/run*")

    runs = []

    fig, ax = plt.subplots()
    for run_path in run_paths:
        run = Run(run_path, os.path.exists(os.path.join(run_path, 'validation')))
        run.parse_events()
        # run.parse_progress()
        runs.append(run)

    which_train_plot = ['batch_loss', 'batch_mean_squared_error', 'batch_mean_absolute_error'][1]
    which_val_plot = ['evaluation_loss_vs_iterations', 'evaluation_mean_squared_error_vs_iterations',
                      'evaluation_mean_absolute_error_vs_iterations', 'epoch_loss',
                      'epoch_mean_squared_error', 'epoch_mean_absolute_error'][0]

    for run in runs:
        # ax.plot(run.get_train_data().get(which_train_plot).get_steps(),
        #         smoothen(run.get_train_data().get(which_train_plot).get_values(), 25),
        #         label=run.get_name())
        if run.does_validation_exist():
            ax.plot(run.get_val_data().get(which_val_plot).get_steps(),
                    run.get_val_data().get(which_val_plot).get_values(),
                    label=run.get_name() + " validation")
        ax.legend()
        plt.title(which_train_plot)

    # ax.set_yscale('log')
    ax.set_ylim(0.4, 1)
    ax.set_ylabel('Mean Squared Error')
    ax.set_xlabel('Batch')
    plt.savefig(os.path.join(data_path, 'graphics', 'batch_mse.svg'))
    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

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
