from django import forms
from heroes.models import Hero
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse

class HeroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(HeroForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'match_form'
        self.helper.add_input(Submit('match-submit', 'Submit'))
        self.helper.form_action = reverse('brain_view')
    
    queryset = Hero.objects.all().order_by('name')
    
    blue_1 = forms.ModelChoiceField(queryset = queryset,)
    blue_2 = forms.ModelChoiceField(queryset = queryset,)
    blue_3 = forms.ModelChoiceField(queryset = queryset, )
    blue_4 = forms.ModelChoiceField(queryset = queryset, )
    blue_5 = forms.ModelChoiceField(queryset = queryset, )
    red_1 = forms.ModelChoiceField(queryset = queryset, )
    red_2 = forms.ModelChoiceField(queryset = queryset,)
    red_3 = forms.ModelChoiceField(queryset = queryset, )
    red_4 = forms.ModelChoiceField(queryset = queryset, )
    red_5 = forms.ModelChoiceField(queryset = queryset, )