import time

import torch

from lunas.iterator import DataIterator
from lunas.reader import RangeReader, ZipReader

from lunas.readers.text import TextReader
# numpy.random.seed(1)
def get_reader():
    def ff(v):
        def f(x):
            print(v)
            return x
        return f
    r = RangeReader(10, buffer_size=1000).select(ff(1))
    r2 = RangeReader(10, buffer_size=1000).select(ff(2))
    # r = TextReader('setup.py',buffer_size=3)
    # r2 = TextReader('setup.py',buffer_size=5)
    r = ZipReader(r, r2, buffer_size=100).select(ff(3))
    # r = r.shuffle(buffer_size=10, num_threads=2)
    return r


def build_it(r):
    it = DataIterator(r, 2, cache_size=3000, sample_size_fn=lambda x: 1)
    return it


def f():
    r = get_reader()
    it = build_it(r)

    ii = it(lambda: it.step < 15)
    rv = []
    stop = 2
    for i, b in enumerate(ii):
        rv.append((it.epoch, it.step_in_epoch, it.step, b[0].samples))
        if i == stop:
            state = it.state_dict()
            torch.save(state, 'xxx')

    return rv[stop + 1:]


def g():
    r = get_reader()

    it = build_it(r)

    it.load_state_dict(torch.load('xxx'))

    ii = it(lambda: it.step < 15)
    rv = []
    for i, b in enumerate(ii):
        rv.append((it.epoch, it.step_in_epoch, it.step, b[0].samples))
    return rv


tic = time.time()
a = f()
b = g()
print(time.time() - tic)
assert a == b

# r = get_reader()
# it = build_it(r)
# for i in it.iter_epoch():
#     print(it.epoch,it.step_in_epoch,it.step,i[0].samples)
#
# for i in it.iter_epoch():
#     print(it.epoch, it.step_in_epoch, it.step, i[0].samples)
# for i in r:
#     pass