FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for Pillow/OpenCV-ish image handling
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY gunicorn.conf.py .

# Non-root (optional hardening)
RUN useradd -m svcuser
USER svcuser

EXPOSE 8000
ENV USE_GPU=false

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:create_app()"]
