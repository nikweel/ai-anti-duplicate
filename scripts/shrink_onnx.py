"""Хранит веса ONNX-модели в fp16, вычисления остаются fp32 (файл вдвое меньше)."""
import sys

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

src, dst = sys.argv[1], sys.argv[2]
m = onnx.load(src)
g = m.graph
casts, keep = [], []
for init in g.initializer:
    if init.data_type == TensorProto.FLOAT and np.prod(init.dims) >= 1024:
        arr = numpy_helper.to_array(init)
        if np.abs(arr).max() < 6e4:
            h = numpy_helper.from_array(arr.astype(np.float16), init.name + "_fp16")
            keep.append(h)
            casts.append(helper.make_node("Cast", [h.name], [init.name], to=TensorProto.FLOAT, name="cast_" + init.name))
            continue
    keep.append(init)
del g.initializer[:]
g.initializer.extend(keep)
nodes = list(g.node)
del g.node[:]
g.node.extend(casts + nodes)
onnx.save(m, dst)
print("saved", dst)
