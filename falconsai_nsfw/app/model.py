import logging
from typing import Tuple, Dict
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor
from app.settings import settings

log = logging.getLogger(__name__)

class NSFWModel:
    _instance = None

    def __init__(self):
        # Device selection
        device = "cuda" if (settings.USE_GPU and torch.cuda.is_available()) else "cpu"
        if device == "cuda":
            log.info("Using CUDA for inference")
        else:
            if settings.USE_GPU and not torch.cuda.is_available():
                log.warning("USE_GPU=1 but CUDA not available; using CPU")
            log.info("Using CPU for inference")

        self.device = torch.device(device)
        self.model_name = settings.MODEL_NAME
        log.info(f"Loading model: {self.model_name}")

        self.model = AutoModelForImageClassification.from_pretrained(self.model_name).to(self.device)
        self.processor = ViTImageProcessor.from_pretrained(self.model_name)

        # Warmup (optional tiny tensor to trigger lazy init)
        with torch.no_grad():
            dummy = Image.new("RGB", (32, 32), color=(0, 0, 0))
            inputs = self.processor(images=dummy, return_tensors="pt").to(self.device)
            _ = self.model(**inputs)

        # Cache label map
        self.id2label: Dict[int, str] = self.model.config.id2label

    @torch.no_grad()
    def predict(self, img: Image.Image) -> Tuple[str, float, Dict[str, float]]:
        img = img.convert("RGB")
        inputs = self.processor(images=img, return_tensors="pt").to(self.device)
        outputs = self.model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=-1).squeeze(0)
        conf, idx = torch.max(probs, dim=-1)
        label = self.id2label[int(idx.item())]
        # full probability map
        score_map = {self.id2label[i]: float(probs[i].item()) for i in range(len(probs))}
        return label, float(conf.item()), score_map

def get_model() -> NSFWModel:
    if NSFWModel._instance is None:
        NSFWModel._instance = NSFWModel()
    return NSFWModel._instance
