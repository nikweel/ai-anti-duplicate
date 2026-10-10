"""Экспорт DINOv2 (CLS-эмбеддинг) в ONNX. Использование: export_dinov2.py facebook/dinov2-large out.onnx"""
import sys

import torch
from transformers import AutoModel

repo, out = sys.argv[1], sys.argv[2]
m = AutoModel.from_pretrained(repo).eval()


class Wrap(torch.nn.Module):
    def __init__(self, m):
        super().__init__()
        self.m = m

    def forward(self, pixel_values):
        return self.m(pixel_values=pixel_values).pooler_output  # CLS после LayerNorm


torch.onnx.export(Wrap(m), (torch.randn(2, 3, 224, 224),), out, input_names=["pixel_values"], output_names=["emb"],
                  dynamic_axes={"pixel_values": {0: "b"}, "emb": {0: "b"}}, opset_version=17, dynamo=False)
print("saved", out)
