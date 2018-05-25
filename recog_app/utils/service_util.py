def is_url_available(url):
    import urllib2

    try:
        urllib2.urlopen(url, timeout=1)
        return True
    except urllib2.URLError as err:
        return False


def is_rabbitmq_available():
    from recog_app.celery_core.image_recognition_config import RABBITMQ_HOST, RABBITMQ_PORT

    return is_url_available("http://{}:{}".format(RABBITMQ_HOST, RABBITMQ_PORT))


def is_redis_available():
    from recog_app.celery_core.image_recognition_config import REDIS_HOST, REDIS_PORT

    return is_url_available("http://{}:{}".format(REDIS_HOST, REDIS_PORT))
