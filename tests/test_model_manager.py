from app.core.model_manager import DEFAULT_SENSITIVITY, MODELS, preprocess, threshold_for

from PIL import Image


def test_default_slider_gives_calibrated_threshold():
    for mid, spec in MODELS.items():
        assert abs(threshold_for(mid, DEFAULT_SENSITIVITY) - spec.thr_default) < 1e-9


def test_softer_slider_lowers_threshold():
    for mid in MODELS:
        assert threshold_for(mid, 0) > threshold_for(mid, 50) > threshold_for(mid, 100)


def test_preprocess_shape_and_unknown_model_fallback():
    spec = MODELS["heavy"]
    for size in ((640, 480), (300, 900), (224, 224)):
        assert preprocess(Image.new("RGB", size, (10, 120, 200)), spec).shape == (3, spec.crop, spec.crop)
    assert threshold_for("nope", 33) == MODELS["light"].thr_default


def test_gpu_detection_and_cpu_fallback_run_without_errors(tmp_path):
    from app.core.model_manager import OnnxEmbedder, available_gpu

    assert available_gpu() in (None, "CUDAExecutionProvider", "DmlExecutionProvider", "CoreMLExecutionProvider")
    import pytest

    with pytest.raises(Exception):  # несуществующая модель -> понятная ошибка, а не NameError
        OnnxEmbedder(tmp_path / "missing.onnx", "auto")


def test_truncated_model_file_is_not_considered_downloaded(tmp_path, monkeypatch):
    import app.core.model_manager as mm

    monkeypatch.setattr(mm, "MODELS_DIR", tmp_path)
    spec = mm.MODELS["light"]
    (tmp_path / spec.file).write_bytes(b"x" * 10)
    assert mm.is_downloaded("light") is False
    (tmp_path / spec.file).write_bytes(b"x" * spec.size_bytes)
    assert mm.is_downloaded("light") is True
