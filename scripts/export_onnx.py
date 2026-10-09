"""Экспорт визуальной части CLIP в ONNX (запускается разработчиком, не пользователем).

Использование: export_onnx.py <репозиторий sentence-transformers> <файл.onnx>
Пример: export_onnx.py sentence-transformers/clip-ViT-L-14 models/clip_vit_l14.onnx
"""
import sys

import torch
from sentence_transformers import SentenceTransformer

repo = sys.argv[1] if len(sys.argv) > 1 else "sentence-transformers/clip-ViT-B-32"
out = sys.argv[2] if len(sys.argv) > 2 else "models/clip_vision.onnx"
st = SentenceTransformer(repo, device="cpu")
clip = st[0].model.eval()


class Vision(torch.nn.Module):
    def __init__(self, m):
        super().__init__()
        self.m = m

    def forward(self, pixel_values):
        pooled = self.m.vision_model(pixel_values=pixel_values).pooler_output
        return self.m.visual_projection(pooled)


size = clip.config.vision_config.image_size
dummy = torch.randn(2, 3, size, size)
torch.onnx.export(Vision(clip), (dummy,), out, input_names=["pixel_values"], output_names=["emb"],
                  dynamic_axes={"pixel_values": {0: "b"}, "emb": {0: "b"}}, opset_version=17, dynamo=False)
print("saved", out, "image_size", size)
