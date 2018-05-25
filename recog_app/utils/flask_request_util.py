from recog_app.app import InfraLog as Ilg
from recog_app.utils.common import is_private_ip
import traceback


def get_real_ip_from_flask_request(flask_request):
    real_ip = None
    try:
        real_ip = flask_request.environ.get("HTTP_X_REAL_IP")
        if not real_ip:
            real_ips = flask_request.environ.get("HTTP_X_FORWARDED_FOR", "")
            if real_ips:
                for real_ip in real_ips.split(","):
                    if not is_private_ip(real_ip):
                        return real_ip
            real_ip = flask_request.environ.get("REMOTE_ADDR")
    except:
        Ilg.Write(Ilg.PRI_ERROR, traceback.format_exc())
    return real_ip


def get_request_data(flask_request):
    request_data = dict(
        url=flask_request.url,
        form=flask_request.form,
        view_args=flask_request.view_args,
        files=serialize_request_files(flask_request.files),
        real_ip=get_real_ip_from_flask_request(flask_request=flask_request),
        host_url=flask_request.host_url
    )
    return request_data


def serialize_request_files(files):
    files_data = dict()
    files_data.iteritems()
    for key, raw_file_data in files.iteritems():
        file_data = dict(
            content_type=raw_file_data.content_type,
            filename=raw_file_data.filename
        )
        files_data[key] = file_data
    return files_data
