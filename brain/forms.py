from django import forms
from heroes.models import Hero
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class HeroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(HeroForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
    queryset = Hero.objects.all()
    ally_1 = forms.ModelChoiceField(queryset = queryset, )
    ally_2 = forms.ModelChoiceField(queryset = queryset, )
    ally_3 = forms.ModelChoiceField(queryset = queryset, )
    ally_4 = forms.ModelChoiceField(queryset = queryset, )
    ally_5 = forms.ModelChoiceField(queryset = queryset, )
    enemy_1 = forms.ModelChoiceField(queryset = queryset, )
    enemy_2 = forms.ModelChoiceField(queryset = queryset,)
    enemy_3 = forms.ModelChoiceField(queryset = queryset, )
    enemy_4 = forms.ModelChoiceField(queryset = queryset, )
    enemy_5 = forms.ModelChoiceField(queryset = queryset, )