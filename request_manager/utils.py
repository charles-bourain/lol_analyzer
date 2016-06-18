from timbad.settings import REQUEST_LIMITS
from .models import Request
import datetime
from django.utils import timezone
import time
import json
import requests



class Request(object):
    last_request_time = datetime.now()
def requester(url, request_type):
    print 'REQUEST HIT'
    one_sec_time_del = datetime.timedelta(seconds = 1)
    ten_min_time_del = datetime.timedelta(seconds = 10*60)


    if request_type == 'get':
        response = requests.get(url).json()
        print 'got response'
        return response




