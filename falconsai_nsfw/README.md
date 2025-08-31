# 🚀 NSFW Image Detection API (Flask + Hugging Face ViT)

This project provides a **production-ready, Dockerized Flask API** for NSFW image classification using [FalconsAI’s ViT-based model](https://huggingface.co/Falconsai/nsfw_image_detection).

It supports **both CPU and GPU deployments** via Docker Compose.

---

## 📂 Project Structure

```
nsfw-api-flask/
├─ app/
│  ├─ __init__.py         # Flask app factory + health endpoints
│  ├─ app.py              # API routes (/predict)
│  ├─ model.py            # Model loading + inference
│  ├─ settings.py         # Configuration via env vars
│  └─ logging_conf.py     # JSON logging setup
├─ Dockerfile             # CPU image
├─ Dockerfile.gpu         # GPU image (CUDA runtime)
├─ docker-compose.yml     # Orchestration (CPU + GPU services)
├─ gunicorn.conf.py       # Production server config
├─ requirements.txt       # Python dependencies
└─ README.md              # 📖 You are here
```

---

## ✨ Features

- ✅ **Flask REST API** with `/predict`, `/healthz`, `/ready` endpoints
- ✅ **CPU or GPU inference** (switch via env var `USE_GPU`)
- ✅ **JSON logging** (easy integration with ELK / Loki / CloudWatch)
- ✅ **Upload size limits** (`MAX_CONTENT_LENGTH_MB`)
- ✅ **Graceful error handling** (bad images, missing files, unsupported formats)
- ✅ **Dockerized for production** with Gunicorn server
- ✅ **Docker Compose setup** for running both CPU and GPU services

---

## ⚙️ Requirements

- Docker ≥ 20.x
- (Optional for GPU) NVIDIA drivers + [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

---

## 🔧 Configuration

All runtime options are controlled via **environment variables**:

| Variable                | Default                          | Description                          |
| ----------------------- | -------------------------------- | ------------------------------------ |
| `MODEL_NAME`            | `Falconsai/nsfw_image_detection` | Hugging Face model to load           |
| `USE_GPU`               | `false`                          | Set `true` to run on GPU             |
| `MAX_CONTENT_LENGTH_MB` | `10`                             | Max upload size (in MB)              |
| `LOG_LEVEL`             | `INFO`                           | Logging verbosity                    |
| `LOG_JSON`              | `true`                           | JSON logs (`false` = human-readable) |

---

## 🐳 Running with Docker Compose

### 1. Build & start services

```bash
docker compose up --build -d
```

This launches:

- **CPU service** → `http://localhost:5000`
- **GPU service** → `http://localhost:5001`

_(GPU container only works if host has NVIDIA GPU drivers + toolkit installed.)_

### 2. Check logs

```bash
docker compose logs -f nsfwpy-cpu
```

---

## 🌐 API Endpoints

### Health & Readiness

```bash
curl http://localhost:5000/health
# {"status": "ok"}

curl http://localhost:5000/ready
# {"ready": true}
```

### Prediction

```bash
curl -X POST http://localhost:5000/classify/binary \
  -F "file=@/path/to/image.jpg"
```

**Response:**

```json
{
  "classification": "nsfw",
  "probability": 0.9842,
  "scores": {
    "nsfw": 0.9842,
    "normal": 0.0158
  }
}
```

---

## 🖥️ Development (without Docker)

1. Create a virtual environment & install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run locally:

   ```bash
   gunicorn -c gunicorn.conf.py app:create_app()
   ```

   API will be available at: `http://localhost:8000`

---

## 🔒 CORS (Do You Need It?)

- If this API is **used only internally** (e.g., behind a backend or gateway), **no CORS needed**.
- If it will be **called directly from browsers** (JS apps, frontend clients), enable [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/).

Example (add in `app/__init__.py`):

```python
from flask_cors import CORS
CORS(app, resources={r"/predict": {"origins": "*"}})
```

---

## 🚀 Deployment Tips

- Scale containers with Docker Compose or Kubernetes (one process per GPU recommended).
- Place behind **NGINX / API Gateway / Load Balancer**.
- Use **API keys / auth middleware** if exposed publicly.
- Monitor logs for latency and errors.

---

## 📌 Example: Compose Override for GPU Only

If you only want GPU service, run:

```bash
docker compose up --build nsfwpy-gpu
```

Or CPU only:

```bash
docker compose up --build nsfwpy-cpu
```

---

## 📝 License

This repo is for research/educational use. The model (`Falconsai/nsfw_image_detection`) is released on Hugging Face under its respective license.
