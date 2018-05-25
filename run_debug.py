#!/usr/bin/python
# -*- utf-8 -*-
from recog_app.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, debug=True)
