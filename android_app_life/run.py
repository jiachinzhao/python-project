import os

os.system('gunicorn -w 4 -b localhost5050 hello:app')

