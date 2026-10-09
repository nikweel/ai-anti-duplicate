"""Экспорт визуальной части CLIP в ONNX (запускается разработчиком, не пользователем)."""
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core.model_manager import load_model  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else "models/clip_vision.onnx")
st = load_model()
clip = st[0].model.eval().cpu()


class Vision(torch.nn.Module):
    def __init__(self, m):
        super().__init__()
        self.m = m

    def forward(self, pixel_values):
        pooled = self.m.vision_model(pixel_values=pixel_values).pooler_output
        return self.m.visual_projection(pooled)


dummy = torch.randn(2, 3, 224, 224)
torch.onnx.export(Vision(clip), (dummy,), str(out), input_names=["pixel_values"], output_names=["emb"],
                  dynamic_axes={"pixel_values": {0: "b"}, "emb": {0: "b"}}, opset_version=17, dynamo=False)
print("saved", out, out.stat().st_size // 2**20, "MB")
print(st[0].processor)
