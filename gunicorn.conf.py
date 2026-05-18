# gunicorn 配置文件
# Railway 容器不支持 os.sendfile()，必须禁用，否则发送文件时 worker 会崩溃

sendfile = False          # 禁用 sendfile，避免 Railway 容器 SIGKILL
workers = 1               # Railway 免费层内存有限，1个worker足够
timeout = 120             # worker 超时时间（秒）
worker_class = "sync"     # 使用同步 worker
