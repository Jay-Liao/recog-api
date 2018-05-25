#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import shutil


def copytree(src, dst, symlinks=False, ignore=None):
    try:
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
    except:
        pass


def make_dirs(path):
    try:
        os.makedirs(path)
    except:
        pass


def keep_recognition_history(directory_path, request_data, response_data):
    save_dict_as_json_file(directory_path=directory_path, filename="request.json", dict_data=request_data)
    save_dict_as_json_file(directory_path=directory_path, filename="response.json", dict_data=response_data)


def save_dict_as_json_file(directory_path, filename, dict_data):
    file_path = os.path.join(directory_path, filename)
    with open(file_path, 'w') as outfile:
        json.dump(dict_data, outfile)


def remove_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


def is_valid_image_filename(filename):
    from recog_app.etc.app_settings import ALLOWED_IMAGE_EXTENSIONS

    if "." in filename:
        _, extension = filename.rsplit(".", 1)
        return extension in ALLOWED_IMAGE_EXTENSIONS
    return False
