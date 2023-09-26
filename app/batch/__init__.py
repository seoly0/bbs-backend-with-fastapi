import sys

from celery import Celery

from settings import ENV, ROOT
from utils.moduleUtils import collect_module_name

sys.path.insert(0, ROOT)

REDIS_URL = f"redis://:{ENV.REDIS_PASSWORD}@{ENV.REDIS_HOST}:{ENV.REDIS_PORT}"
REDIS_CELERY = f"{REDIS_URL}/{ENV.REDIS_CELERY}"
TASK_MODULES = collect_module_name(__file__, str(__package__))

app = Celery(ENV.APP_NAME, broker=REDIS_CELERY, backend=REDIS_CELERY)
app.conf.broker_connection_retry_on_startup = True
app.conf.worker_log_format = "[%(levelname)-8s] :: %(asctime)s :: %(processName)s >> %(message)s"
app.conf.worker_task_log_format = (
    "[%(levelname)-8s] :: %(asctime)s :: %(processName)s :: %(task_name)s[%(task_id)s] >> %(message)s"
)

app.autodiscover_tasks(TASK_MODULES)

# celery -A app.batch worker --loglevel=info --beat
