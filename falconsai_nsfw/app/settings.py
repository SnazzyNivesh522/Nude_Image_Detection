import os

def env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.lower() in ("1", "true", "yes", "on")

class Settings:
    MODEL_NAME = os.getenv("MODEL_NAME", "Falconsai/nsfw_image_detection")
    MAX_CONTENT_LENGTH_MB = float(os.getenv("MAX_CONTENT_LENGTH_MB", "10"))  # upload cap
    MAX_CONTENT_LENGTH = int(MAX_CONTENT_LENGTH_MB * 1024 * 1024)

    # GPU / CPU
    USE_GPU = env_bool("USE_GPU", True)
    DEVICE_FALLBACK_TO_CPU = env_bool("DEVICE_FALLBACK_TO_CPU", True)

    # API behavior
    ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png", "bmp", "gif", "webp"])

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_JSON = env_bool("LOG_JSON", True)

settings = Settings()
