# coding: utf-8
from __future__ import print_function, division, unicode_literals, absolute_import

import sys
import os
import math
import numpy
import time

try:
    from .mesh import Mesh
    from .progress import get_eta, show_bar
except ImportError:
    from mesh import Mesh
    from progress import get_eta, show_bar


class MLP(Mesh):
    def __init__(self, params={}, **kwargs):
        self._libc = None
        self.initialized_ = False
        self.rate_ = None
        self.loss_ = None
        self.feature_importances_ = None
        self.classes_ = None
        self.params_ = {}
        self.params_.update(params)
        self.params_.update(kwargs)

        self.count_ = None
        self.total_ = None
        self.time_from_ = None
        self.iteration_log_ = None
        self.iteration_decay_ = None

        self.epoch_size = None
        self.epoch_decay = None

        self.mesh_init(dtype=self.params_.get('dtype', 'float64'))

    def get_params(self, deep=False):
        return self.params_

    def set_params(self, **kwargs):
        # print("set_params", kwargs)
        self.params_.update(kwargs)

        if self.initialized_:
            self.mlp_init(**self.params_)
        return self

    def mlp_init(self,
                 op='fc',
                 exf=[],
                 activation=[],
                 layer_size=[],
                 input_type='pointwise',
                 loss_type='mse',
                 output_range=(0, 1),
                 output_shrink=0.001,               # 0.1
                 importance_mul=0.001,
                 leaky=-0.001,
                 dropout=0,
                 bias_rate=[0.005],
                 weight_rate=[],
                 regularization=1,

                 weight_filler={'Type': 'gsfi', 'Adj': (0, 0.8)},
                 bias_filler={'Type': 'zero', 'Adj': (0, 1)},

                 epoch_log=1,
                 epoch_train=5,
                 epoch_decay=None,
                 epoch_size=None,

                 rate_init=0.06,
                 rate_decay=0.9,
                 importance_out=False,
                 loss_mul=0.001,
                 shuffle=True,

                 verbose=1,
                 verbose_feed=0,
                 ):

        self.epoch_log = epoch_log
        self.epoch_train = epoch_train

        if epoch_decay is not None:
            self.epoch_decay = epoch_decay
        if epoch_size is not None:
            self.epoch_size = epoch_size

        self.rate_init = rate_init
        self.rate_decay = rate_decay
        self.importance_out = importance_out
        self.loss_mul = loss_mul
        self.shuffle = shuffle

        self.verbose = verbose
        self.verbose_feed = verbose_feed

        self.set_conf({})

        for idx, shape in enumerate(layer_size):
            if isinstance(shape, int):
                shape = (1, 1, shape)
            assert isinstance(shape, tuple)

            arg = {'Shape': shape}
            if idx == 0:
                arg['InputType'] = input_type
                arg['ImportanceMul'] = importance_mul
            if idx == len(layer_size) - 1:
                arg['Regularization'] = regularization
                arg['LossType'] = loss_type
                arg['OutputRange'] = output_range
                arg['OutputShrink'] = output_shrink

            self.set_tensor(idx, arg)

        for idx in range(max(len(layer_size) - 1, len(exf))):
            arg = {'Tin': idx, 'Tout': idx+1}

            kv = {
                'BiasRate': bias_rate,
                'Dropout': dropout,
                'Leaky': leaky,
                'WeightRate': weight_rate,
                'Activation': activation,
                'Op': op,
                'WeightFiller': weight_filler,
                'BiasFiller': bias_filler,
            }

            for k in kv:
                if not isinstance(kv[k], list):
                    if kv[k] is not None:
                        arg[k] = kv[k]
                elif idx < len(kv[k]) and kv[k][idx] is not None:
                    arg[k] = kv[k][idx]

            if isinstance(exf, dict):
                arg.update(exf)
            elif idx < len(exf) and isinstance(exf[idx], dict):
                arg.update(exf[idx])

            self.set_filter(idx, arg)

    def check_arr(self, arr):
        if hasattr(arr, 'toarray'):
            arr = arr.toarray()

        if not isinstance(arr, numpy.ndarray):
            arr = numpy.array(arr, self.DTYPE)

        if len(arr.shape) == 1:
            arr = arr.reshape((-1, 1))
        if arr.dtype != self.DTYPE:
            arr = arr.astype(self.DTYPE)
        if not arr.flags['C_CONTIGUOUS']:
            arr = numpy.ascontiguousarray(arr)
        return arr

    def save_model(self, filepath="model.bin"):
        ret = self._libc.mesh_save_model(self.mi_, filepath.encode())
        if ret <= 0:
            raise ValueError()

    def load_model(self, filepath="model.bin"):
        if not self.initialized_:
            self.mlp_init(**self.params_)

        ret = self._libc.mesh_load_model(self.mi_, filepath.encode())
        if ret <= 0:
            raise ValueError()

    def fit(self, in_arr=None, target_arr=None):
        if not self.initialized_:
            self.initialized_ = True
            self.mlp_init(**self.params_)
            self.run_filler()
            if in_arr is None:
                return

        self.set_conf({'IsTrain': True})

        in_arr = self.check_arr(in_arr)
        target_arr = self.check_arr(target_arr)

        arr_size = len(in_arr)
        assert arr_size == len(target_arr)

        if self.total_ is None:
            if self.classes_ is None:
                self.classes_ = list(
                    range(numpy.prod(self.tensors[-1]['Shape'])))

            if self.epoch_size is None:
                self.epoch_size = arr_size

            self.total_ = int(self.epoch_size * self.epoch_train)
            self.count_ = 0

            if self.iteration_log_ is None:
                self.iteration_log_ = int(self.epoch_log * self.epoch_size)

            if self.iteration_decay_ is None and self.epoch_decay is not None:
                self.iteration_decay_ = int(self.epoch_decay * self.epoch_size)

            if self.rate_ is None:
                self.rate_ = self.rate_init

            if self.time_from_ is None:
                self.time_from_ = time.time()

        if self.shuffle:
            idx_range = numpy.arange(arr_size, dtype=numpy.int32)
        else:
            idx_range = range(arr_size)

        while self.count_ < self.total_:
            if self.shuffle:
                self.shuffle_array(idx_range)

            for idx in idx_range:
                loss = self.train_one(
                    in_arr[idx], target_arr[idx], self.rate_, self.importance_out)

                if self.loss_ is None:
                    self.loss_ = loss
                else:
                    self.loss_ += (loss - self.loss_) * self.loss_mul

                if math.isnan(self.loss_):
                    print("loss is nan", file=sys.stderr)
                    sys.exit()

                self.count_ += 1

                if self.verbose > 0:
                    if (self.count_ % self.iteration_log_ == 0 or
                            self.count_ >= self.total_):

                        if self.verbose > 1:
                            print("\nIteration %g/%g\tEpoch %g/%g" % (
                                self.count_ % self.epoch_size, self.epoch_size,
                                self.count_ // self.epoch_size, self.epoch_train))

                        show_bar(self.time_from_, self.count_ / self.total_, 
                        "rate: %-12g loss: %-12g" % (self.rate_, self.loss_))

                        if self.count_ >= self.total_:
                            sys.stdout.write("\ntime elapsed: %s\n" %
                                             get_eta(self.time_from_))
                        
                        sys.stdout.flush()

                if self.count_ >= self.total_:
                    break

                if self.iteration_decay_ is not None:
                    if self.count_ % self.iteration_decay_ == 0:
                        self.rate_ *= self.rate_decay

            if arr_size < self.epoch_size:
                break

        if self.importance_out and self.count_ >= self.total_:
            self.feature_importances_ = numpy.zeros(
                (numpy.prod(self.tensors[0]['Shape']),), dtype=self.DTYPE)
            self.read_tensor(0, self.feature_importances_, self.FLAG_EX)

        return self

    def finished(self):
        if self.total_ is None:
            return False
        return self.count_ >= self.total_

    def feed(self, in_arr, out_arr=None):
        self.set_conf({'IsTrain': False})

        in_arr = self.check_arr(in_arr)

        if out_arr is None:
            out_arr = numpy.zeros(
                (len(in_arr), numpy.prod(self.tensors[-1]['Shape'])), dtype=self.DTYPE)
        else:
            out_arr = self.check_arr(out_arr)

        arr_size = len(in_arr)
        assert arr_size == len(out_arr)

        time_from = time.time()
        for idx in range(arr_size):
            self.predict_one(in_arr[idx], out_arr[idx])

            if self.verbose_feed > 0:
                if ((idx + 1) % self.iteration_log_ == 0 or
                        (idx + 1) >= arr_size):

                    show_bar(time_from, (idx+1) / arr_size)
                    
                    if (idx + 1) >= arr_size:
                        sys.stdout.write("\ntime elapsed: %s\n" %
                                             get_eta(time_from))

                sys.stdout.flush()

        return out_arr

    def predict_proba(self, in_arr, out_arr=None):
        out_arr = self.feed(in_arr, out_arr)

        return out_arr

    def predict(self, in_arr, out_arr=None):
        out_arr = self.feed(in_arr, out_arr)

        loss_type = self.tensors[-1]['LossType']
        if loss_type in ["softmax", "hardmax"]:
            return out_arr.argmax(axis=1)

        if len(out_arr.shape) == 2 and out_arr.shape[1] == 1:
            out_arr = out_arr.reshape(-1)

        return out_arr

    def train_one(self, in_buf, target_buf, rate, importance_out):
        self.clear_tensor(-1, self.FLAG_V | self.FLAG_DV)
        self.clear_filter(-1, self.FLAG_DV)
        self.input(0, in_buf)

        self.forward()

        loss = self.cal_loss(len(self.tensors) - 1, target_buf)

        # if loss_range[1] is not None and loss > loss_range[1]:
        #     return loss
        # if loss_range[0] is not None and loss < loss_range[0]:
        #     return loss

        self.backward()
        self.renew(rate)

        if importance_out:
            self.importance(0)

        return loss

    def predict_one(self, in_buf, out_buf):
        self.clear_tensor(-1, self.FLAG_V)
        self.input(0, in_buf)
        self.forward()

        flag = self.FLAG_V
        loss_type = self.tensors[-1]['LossType']
        if loss_type in ["softmax", "hardmax"]:
            flag = self.FLAG_EX

        self.read_tensor(len(self.tensors) - 1, out_buf, flag)


if __name__ == '__main__':
    m = MLP(layer_size=[2, 1],  op="conv", initialize=True)

    print("appname:", m.info("appname"))
    sys.stdout.flush()

    m.set_tensor(0,
                 {'Shape': [1, 2], 'Regularization': 0.1})

    m.show_conf()
    m.show_tensor()
    m.show_filter()
    m.destroy()
