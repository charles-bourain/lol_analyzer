from django.shortcuts import render

from django.views.generic import TemplateView, FormView
from .forms import HeroForm
from matches.models import Player
from .manager import NetworkManager
from django.http import HttpResponse


class BrainView(FormView):
    template_name = 'brain/main.html'
    form_class = HeroForm
    success_url = ''

    def form_valid(self, form):
            ally_list = []
            enemy_list = []

            for i in form.cleaned_data:
                if i.startswith('ally'):
                    ally_list.append(form.cleaned_data[i])
                else:
                    enemy_list.append(form.cleaned_data[i])

            NN_network = NetworkManager(hidden_layers = 2, ally_champ_obj_list = ally_list, enemy_champ_obj_list = enemy_list)
            raw_win_rate = NN_network.train_network()
            NN_prediction = NN_network.run_network()

            print NN_prediction

            return HttpResponse("Raw Win Rate = {}  :  Prediction = {}".format(raw_win_rate, NN_prediction))






