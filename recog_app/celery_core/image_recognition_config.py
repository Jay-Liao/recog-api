from recog_app.app import app
from recog_app.constants.config_constant import REDIS_URL, RABBITMQ_URL


##################################
# celery app - image_recognition_app
##################################
CELERY_DEFAULT_QUEUE = "image_recognition"
BROKER_URL = app.config[RABBITMQ_URL]
CELERY_RESULT_BACKEND = app.config[REDIS_URL]
ONE_HOUR = 3600
CELERY_TASK_RESULT_EXPIRES = ONE_HOUR

##################################
# Task name
##################################
IMAGE_RECOGNITION_TASK_NAME = "image_recognition_task"
