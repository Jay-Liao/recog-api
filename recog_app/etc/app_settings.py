#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

# Project
PROJECT_NAME = "recog"

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# Recognition
ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg"]
RECOGNITION_POLLING_INTERVAL = 0.1
RECOGNITION_TIMEOUT = 3
MAX_NUMBER_OF_THE_SAME_PRODUCTS = 10
MODELS_FOLDER_NAME = "models"
PRODUCT_JSON_FILE_NAME = "product.json"
PRODUCT_IMAGE_FOLDER_NAME = "product_images"
IMAGE_FOLDER_NAME = "images"
RECOGNITION_HISTORY_FOLDER_NAME = "recognition_histories"

# Product Info
LATEST_MODEL_FOLDER_NAME = "latest"

print >> sys.stderr, " --------------read config done, {} ----------------".format(__file__)
