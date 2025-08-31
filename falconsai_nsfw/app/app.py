import io
import logging
import time
from PIL import Image, UnidentifiedImageError
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.settings import settings
from app.model import get_model


bp = Blueprint("api", __name__)
log = logging.getLogger(__name__)


@bp.get("/")
def index():
    return {"service": "nsfw_image_detection", "model": settings.MODEL_NAME}


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in settings.ALLOWED_EXTENSIONS
    )


@bp.post("/classify/binary")
def predict():
    started = time.time()
    if "file" not in request.files:
        return jsonify({"error": "missing file field"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename or "")
    if not filename:
        return jsonify({"error": "empty filename"}), 400
    if not allowed_file(filename):
        return jsonify({"error": "unsupported file extension"}), 400

    try:
        data = file.read()
        img = Image.open(io.BytesIO(data))
    except UnidentifiedImageError:
        return jsonify({"error": "invalid image"}), 400
    except Exception as e:
        log.exception("Failed reading image")
        return jsonify({"error": "failed to read image"}), 400

    try:
        model = get_model()
        label, confidence, scores = model.predict(img)
        took = round((time.time() - started) * 1000, 2)
        resp = {"classification": label, "probability": confidence, "scores": scores}
        log.info(f"Processed {filename} in {took}ms: {label} ({confidence})")
        return jsonify(resp)
    except Exception:
        log.exception("Inference failed")
        return jsonify({"error": "inference_failed"}), 500
