# coding: utf-8
from __future__ import print_function, division, unicode_literals, absolute_import

import os
import sys
import math
import numpy
import time
import copy
import ctypes
import sklearn.metrics

try:
    from .mesh import Mesh
except ImportError:
    from mesh import Mesh


class MLP(Mesh):
    def __init__(self, params={}, **kwargs):
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

        self.iteration_log_ = None
        self.iteration_check_ = None

        self.epoch_size = None

        self.score_table_ = []
        self.best_score_ = None
        self.best_estimator_ = None
        self.best_model_ = None

        self.no_better_count_ = 0

        self.mesh_init(dtype=self.params_.get('dtype', 'float64'))

    def get_params(self, deep=False):
        return self.params_

    def set_params(self, **kwargs):
        self.params_.update(kwargs)

        if self.initialized_:
            self.mlp_init(**self.params_)
        return self

    def renew_estimator(self):
        if self.best_estimator_ is None:
            self.best_estimator_ = MLP(self.get_params())
            self.best_estimator_.fit()

        self.best_estimator_.rate_ = self.rate_
        self.best_estimator_.loss_ = self.loss_
        self.best_estimator_.best_score_ = self.best_score_

        self.best_estimator_.score_table_ = self.score_table_.copy()

        self.best_model_ = self.save_model()

        self.best_estimator_.load_model(self.best_model_)

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

                 importance_out=False,
                 loss_mul=0.001,

                 tol_value=1e-4,
                 tol_rounds=5,

                 epoch_log=1,
                 epoch_check=1,
                 epoch_train=1,
                 epoch_size=None,

                 rate_init=0.06,
                 rate_decay=0.9,

                 shuffle=True,

                 verbose=1,
                 ):

        self.tol_value = tol_value
        self.tol_rounds = tol_rounds

        self.epoch_log = epoch_log
        self.epoch_check = epoch_check
        self.epoch_train = epoch_train

        if epoch_size is not None:
            self.epoch_size = epoch_size

        self.rate_init = rate_init
        self.rate_decay = rate_decay
        self.importance_out = importance_out
        self.loss_mul = loss_mul
        self.shuffle = shuffle
        self.output_range = output_range

        self.verbose = verbose

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
                'WeightRate': weight_rate,
                'Dropout': dropout,
                'Leaky': leaky,
                'Activation': activation,
                'Op': op,
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
        if not isinstance(arr, numpy.ndarray):
            if hasattr(arr, 'toarray'):
                arr = arr.toarray()
            arr = numpy.array(arr, self.DTYPE)

        if arr.dtype != self.DTYPE:
            arr = arr.astype(self.DTYPE)
        if arr.ndim == 1:
            arr = arr.reshape((-1, 1))
        if not arr.flags['C_CONTIGUOUS']:
            arr = numpy.ascontiguousarray(arr)
        return arr

    def get_score(self, eval_set, metric='accuracy'):
        if metric == 'accuracy':
            y_pred = self.predict(eval_set[0])
            self.set_conf({'IsTrain': True})
            score = sklearn.metrics.accuracy_score(eval_set[1], y_pred)
            return score
        elif metric == 'neg_mean_squared_error':
            y_pred = self.predict(eval_set[0])
            self.set_conf({'IsTrain': True})
            score = sklearn.metrics.mean_squared_error(eval_set[1], y_pred)
            return score * -1.0
        else:
            print(sorted(sklearn.metrics.SCORERS.keys()))
            raise NotImplementedError()

    def fit(self, in_arr=None, target_arr=None, eval_set=None, eval_metric=None):
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

        if eval_set is None:
            eval_set = (in_arr, target_arr)
        else:
            eval_set[0] = self.check_arr(eval_set[0])
            eval_set[1] = self.check_arr(eval_set[1])

            assert len(eval_set[0]) == len(eval_set[1])

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
            if self.iteration_check_ is None:
                self.iteration_check_ = int(self.epoch_check * self.epoch_size)

            if self.rate_ is None:
                self.rate_ = self.rate_init

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

                if (self.count_ % self.iteration_check_ == 0 or
                        self.count_ >= self.total_):
                    score = self.get_score(eval_set, eval_metric)
                    self.score_table_.append(score)

                    if self.best_score_ is not None:
                        if score > (self.best_score_ + self.tol_value):
                            self.no_better_count_ = 0
                        else:
                            self.no_better_count_ += 1

                    if (self.best_score_ is None or
                            self.best_score_ < score):
                        self.best_score_ = score
                        self.renew_estimator()

                    if self.no_better_count_ >= self.tol_rounds:
                        self.no_better_count_ = 0
                        self.rate_ *= self.rate_decay
                        self.load_model(self.best_model_)
                        self.loss_ = self.best_estimator_.loss_

                if self.verbose > 0:
                    if (self.count_ % self.iteration_log_ == 0 or
                            self.count_ >= self.total_):

                        if self.verbose > 0:
                            print("Iteration %g/%g\tEpoch %g/%g" % (
                                self.count_ % self.epoch_size, self.epoch_size,
                                self.count_ // self.epoch_size, self.epoch_train))

                            print("    rate: %g loss: %g score: %s" %
                                  (self.rate_, self.loss_, 
                                    str(self.best_score_)))
                        sys.stdout.flush()

                if self.count_ >= self.total_:
                    break

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

        for idx in range(arr_size):
            self.predict_one(in_arr[idx], out_arr[idx])

        if self.output_range is not None:
            out_arr = numpy.clip(
                out_arr,
                a_min=self.output_range[0],
                a_max=self.output_range[1]
            )

        return out_arr

    def predict_proba(self, in_arr, out_arr=None):
        out_arr = self.feed(in_arr, out_arr)

        return out_arr

    def predict(self, in_arr, out_arr=None):
        out_arr = self.feed(in_arr, out_arr)

        loss_type = self.tensors[-1]['LossType']
        if loss_type in ["softmax", "hardmax"]:
            return out_arr.argmax(axis=1)

        if out_arr.ndim == 2 and out_arr.shape[1] == 1:
            out_arr = out_arr.reshape(-1)

        return out_arr

    def train_one(self, in_buf, target_buf, rate, importance_out):
        self.clear_tensor(-1, self.FLAG_V | self.FLAG_DV)
        self.clear_filter(-1, self.FLAG_DV)
        self.input(0, in_buf)

        self.forward()

        loss = self.cal_loss(len(self.tensors) - 1, target_buf)

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
    mlp = MLP(layer_size=[2, 1],  op="fc")
    mlp.fit()
    print(mlp.mi_)

    mem = mlp.save_model()
    print(len(mem), mem[-5:])

    # mlp_copy = mlp_clone(mlp)
    # print(mlp_copy.mi_)
    # mem1 = mlp_copy.save_model()
    # print(len(mem1), mem1[-5:])

    # mlp.run_filler()

    # mem = mlp.save_model()
    # print(len(mem), mem[-5:])

    # # mlp_copy = clone(mlp)
    # print(mlp_copy.mi_)
    # mem1 = mlp_copy.save_model()
    # print(len(mem1), mem1[-5:])

    # print("appname:", m.info("appname"))
    # sys.stdout.flush()

    # m.fit()
    # m.set_tensor(0,
    #              {'Shape': [1, 2], 'Regularization': 0.1})

    # m.show_conf()
    # m.show_tensor()
    # m.show_filter()
    # m.destroy()
