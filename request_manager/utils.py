from timbad.settings import REQUEST_LIMITS
from .models import Request
import datetime
from django.utils import timezone
import time
import json
import requests

def requester(url, request_type):
    one_sec_time_del = datetime.timedelta(seconds = 1)
    ten_min_time_del = datetime.timedelta(seconds = 10*60)

    def scrub_manager():
        #Delete all Requests that were created after now + 10 minutes
        expiration_time = timezone.now()-ten_min_time_del
        expired_manager_objs = Request.objects.filter(request_time__lte=expiration_time)

        if len(expired_manager_objs) == 0:
            earliest_request_time = Request.objects.order_by('-request_time')[0].request_time

            #Stall for 10mins - earliest_time + 1 second to ensure next look at manager list will delete some managers
            stall_time = (earliest_request_time-expiration_time).total_seconds()
            time.sleep(stall_time)
            expiration_time = timezone.now()-ten_min_time_del
            expired_manager_objs = Request.objects.filter(request_time__lte=expiration_time)

        expired_manager_objs.delete()

    try:
        last_request = Request.objects.order_by("-request_time")[0].request_time
    except:
        last_request = timezone.now()-one_sec_time_del
    delta_from_last_request = timezone.now() - last_request  
    
    if delta_from_last_request < one_sec_time_del:
        print (one_sec_time_del - delta_from_last_request).total_seconds()
        #if last request was less then a second ago, wait for 1 second minus time since last request
        time.sleep((one_sec_time_del - delta_from_last_request).total_seconds())
    
    #This statement will ensure Request Manager only has 500 objects.  Once 500 is hit, a scrub occurs.    
    if Request.objects.count() >= REQUEST_LIMITS['ten_minute']:
        scrub_manager()


    if request_type == 'get':
        Request.objects.create()
        return requests.get(url).json()




