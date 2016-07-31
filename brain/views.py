from django.shortcuts import render

from django.views.generic import TemplateView, FormView
from .forms import BlueHeroForm, RedHeroForm
from matches.models import Match
from .manager import NetworkManager
from django.http import HttpResponse
import boto3
from pprint import pprint
from brain.utils import DataPickler
from heroes.models import Hero


class BrainView(TemplateView):
    template_name = 'brain/main.html'
    success_url = ''

    def get_context_data(self, *args, **kwargs):
        context = super(BrainView, self).get_context_data(*args, **kwargs)
        context['heroes'] = Hero.objects.all().order_by('name')
        context['blue_form'] = BlueHeroForm()
        context['red_form'] = RedHeroForm()
        red_hero_form = RedHeroForm()
        #Need to save this in settings, in case of updates
        context['league_of_legends_champion_static_data_url'] = 'http://ddragon.leagueoflegends.com/cdn/6.14.2/img/champion/'
        return context

    def post(self, *args, **kwargs):
        print self.request.POST
        blue_dict = {}
        red_dict = {}
        heroes = Hero.objects.all()
        for entry in self.request.POST:
            if entry.startswith('blue'):
                blue_dict[entry] = heroes.get(id=self.request.POST[entry])
            elif entry.startswith('red'):
                red_dict[entry] = heroes.get(id=self.request.POST[entry])
            else:
                pass
        return self.form_valid(blue_dict, red_dict)




    def form_valid(self, blue_dict, red_dict):
        data_pickle_obj = DataPickler.objects.all()[0]
        client = boto3.client('machinelearning', 'us-east-1')

        record_dict = data_pickle_obj.data

        for form in [blue_dict, red_dict]:
            for i in form:
                if i.startswith('blue'):
                    key = 'blue-{}'.format(form[i].name.replace("'",''))
                    record_dict[key] = str(1)
                else:
                    key = 'red-{}'.format(form[i].name.replace("'",''))
                    record_dict[key] = str(1)
        response = client.predict(
            MLModelId = 'ml-3j1aVuk32Ic',
            Record = record_dict,
            PredictEndpoint = 'https://realtime.machinelearning.us-east-1.amazonaws.com'
            )
        return HttpResponse(str(response['Prediction']['predictedValue']*100))







