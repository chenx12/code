# -*- encoding:utf-8 -*-
from flask import Flask, request, g
from psycopg2 import connect
from psycopg2.extras import RealDictCursor

from multiprocessing import Process
import threading
import time
from threading import Thread
import  datetime
import traceback
import json
import calendar
import redis
import re
import logging

app = Flask(__name__)

if __name__ == '__main__':
    thread = Process(target=run)
    thread.start()   
    app.run(host='0.0.0.0', port=9002, debug=False)
