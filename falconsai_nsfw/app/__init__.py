from flask import Flask
from app.settings import settings
from app.logging_conf import configure_logging

def create_app() -> Flask:
    configure_logging()
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = settings.MAX_CONTENT_LENGTH

    # Register routes in app.py
    from app.app import bp as api_bp
    app.register_blueprint(api_bp)

    # Readiness/health lightweight endpoints
    @app.get("/health")
    def healthz():
        return {"status": "ok"}

    @app.get("/ready")
    def ready():
        # If model is constructed, we consider ready
        from app.model import NSFWModel
        return {"ready": NSFWModel._instance is not None}

    return app
