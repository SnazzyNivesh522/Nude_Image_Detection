import multiprocessing
bind = "0.0.0.0:5000"
workers = max(2, multiprocessing.cpu_count() // 2)
worker_class = "gthread"          # good for I/O + light CPU
threads = 2
timeout = 60
graceful_timeout = 30
loglevel = "info"
accesslog = "-"
errorlog = "-"
