# 🚀 NSFW Image Detection Service

A production-ready **REST API** for detecting NSFW (Not Safe For Work) content in images.
Built with **[nsfwjs](https://github.com/infinitered/nsfwjs)**, **TensorFlow\.js**, **Express**, and **Docker**.
Supports **CPU & GPU inference**, structured **logging (Winston)**, and provides both **multi-class** and **binary classification** endpoints.

---

## 📌 Features

* 🔎 **Classify images** into NSFW categories (`Porn`, `Hentai`, `Sexy`, `Neutral`, `Drawing`).
* ⚡ **Binary classification** → `nsfw` / `normal` with confidence.
* 🚀 **Express.js API** with `/classify` and `/classify/binary`.
* 🖼️ Handles multiple image formats with **sharp**.
* 🧠 **Automatic GPU fallback**: uses `@tensorflow/tfjs-node-gpu` if available, else CPU.
* 🐳 **Dockerized** for both CPU and GPU.
* 📜 **Structured logging** with Winston.
* 🛠️ **Health check** endpoint (`/health`).
* 🔒 File size limit: **10MB per image**.

---

## 📂 Project Structure

```
.
├── app.js              # Express server with API routes
├── util.js             # Model loading + classification logic
├── logger.js           # Winston logging config
├── Dockerfile          # CPU Dockerfile
├── Dockerfile.gpu      # GPU Dockerfile
├── Dockerfile.test     # Testing Dockerfile
├── docker-compose.yml  # Compose for CPU & GPU services
├── package.json        # Node.js dependencies
```

---

## ⚙️ Installation

### 1. Local Setup

```bash
# Clone repo
git clone <your-repo-url>
cd nsfwjs

# Install dependencies
npm install

# Start service (CPU)
npm start
```

### 2. Docker (Recommended)

#### CPU Service

```bash
docker build -t nsfwjs:cpu -f Dockerfile .
docker run -p 3000:3000 nsfwjs:cpu
```

#### GPU Service

Requires **NVIDIA Docker runtime** + drivers.

```bash
docker build -t nsfwjs:gpu -f Dockerfile.gpu .
docker run --gpus all -p 3001:3000 nsfwjs:gpu
```

#### With Docker Compose

```bash
docker compose up -d
```

This will start:

* `nsfwjs-cpu` → port **3000**
* `nsfwjs-gpu` → port **3001**

---

## 🌐 API Usage

### Health Check

```http
GET /health
```

Response:

```json
{ "status": "ok" }
```

### Multi-class Classification

```http
POST /classify
Content-Type: multipart/form-data
Body: image=<your_file>
```

Response:

```json
{
  "predictions": [
    { "className": "Porn", "probability": 0.92 },
    { "className": "Sexy", "probability": 0.05 },
    { "className": "Neutral", "probability": 0.02 },
    { "className": "Drawing", "probability": 0.01 }
  ]
}
```

### Binary Classification

```http
POST /classify/binary
Content-Type: multipart/form-data
Body: image=<your_file>
```

Response:

```json
{ "classification": "nsfw", "probability": 0.92 }
```

---

## 📝 Environment Variables

| Variable     | Default          | Description                     |
| ------------ | ---------------- | ------------------------------- |
| `PORT`       | `3000`           | Port to run the service on      |
| `MODEL_NAME` | `MobileNetV2Mid` | Model variant used (`nsfwjs`)   |
| `LOG_LEVEL`  | `info`           | Logging level (`debug`, `info`) |

---

## 📊 Logging

Uses **Winston** logger with JSON output:

```json
{
  "level": "info",
  "message": "NSFW service listening on port 3000",
  "timestamp": "2025-09-01T18:00:00.000Z"
}
```

---

## 🧪 Testing

```bash
# Run test container
docker build -t nsfwjs:test -f Dockerfile.test .
docker run nsfwjs:test
```

Or run integration test:

```bash
curl -F "image=@test.jpg" http://localhost:3000/classify/binary
```

---

## 📌 Notes

* Ensure **NVIDIA drivers** + **CUDA runtime** for GPU.
* Images >10MB are rejected.
* TensorFlow\.js automatically manages memory; explicit cleanup is optional.

---

## 📜 License

MIT License © 2025

