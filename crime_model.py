# -*- coding: utf-8 -*-

import chainer
import chainer.functions as F
import chainer.links as L


class Model(chainer.Chain):
    def __init__(self, n_in=5, n_units=50, n_out=24):
        super(Model, self).__init__(
            l1=L.Linear(n_in, n_units),
            l2=L.Linear(n_units, n_units),
            l3=L.Linear(n_units, n_out),
        )

    def __call__(self, x):
        h1=F.relu(self.l1(x))
        h2=F.relu(self.l2(h1))
        y=self.l3(h2)
        return y
