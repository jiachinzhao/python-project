#coding=utf-8

import os

cmd = 'gunicorn -w 4 -b localhost:5000 myflask:app'

os.system(cmd)
