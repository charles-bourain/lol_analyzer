from django.shortcuts import render

from django.views.generic import TemplateView, FormView
from .forms import HeroForm
from matches.models import Match
from .manager import NetworkManager
from django.http import HttpResponse
import boto3
from pprint import pprint
from brain.utils import DataPickler


class BrainView(FormView):
    template_name = 'brain/main.html'
    form_class = HeroForm
    success_url = ''

    def form_valid(self, form):
        data_pickle_obj = DataPickler.objects.all()[0]
        client = boto3.client('machinelearning', 'us-east-1')

        record_dict = data_pickle_obj.data

        for i in form.cleaned_data:
            if i.startswith('blue'):
                key = 'blue-{}'.format(form.cleaned_data[i].name.replace("'",''))
                record_dict[key] = str(1)
            else:
                key = 'red-{}'.format(form.cleaned_data[i].name.replace("'",''))
                record_dict[key] = str(1)
        response = client.predict(
            MLModelId = 'ml-3j1aVuk32Ic',
            Record = record_dict,
            PredictEndpoint = 'https://realtime.machinelearning.us-east-1.amazonaws.com'
            )
        return HttpResponse("Chance of Blue Team Winning: "+response['Prediction']['predictedValue'])

    def form_invalid(self, form):
        return HttpResponse("Pick Teams plz")






