from multiprocessing import cpu_count

def get_workers():
    return cpu_count()*2 + 1

bind = '0.0.0.0:8085'
capture_output = True
workers = get_workers()
worker_class = "gevent"
#thread = 2
preload_app = True # init one instance
graceful_timeout = 60
loglevel = 'info'
accesslog = 'log/access_log.log'
access_log_format = '%({X-Real-IP}i)s %({X-Forwarded-For}i)s %({authorization}i)s | %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" **%(L)s/%(D)s**'
errorlog = 'log/error_log.log'
