#coding=utf-8

import os

cmd = 'gunicorn -w 4 -b localhost:5050 weixin:app'

os.system(cmd)
