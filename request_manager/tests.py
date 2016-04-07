from django.test import TestCase
from .models import Request
from .utils import requester
from django.utils import timezone
import datetime


class RequestTestCase(TestCase):

    def setUp(self):
        for i in [0, 10 ,599 ,601]:
            request = Request.objects.create()
            request.request_time = timezone.now() - datetime.timedelta(seconds = i)
        