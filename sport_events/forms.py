from django import forms
from django.utils import timezone
from .models import Match
from users.models import CustomUser
from django.db.models import Q


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = "__all__" # for Django 1.8+


    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        if self.instance:
            if self.instance.participant_2 is None:
                self.fields['winner'].queryset = CustomUser.objects.filter(pk=self.instance.participant_1.pk) 
            else:
                self.fields['winner'].queryset = CustomUser.objects.filter(Q(pk=self.instance.participant_1.pk) | Q(pk=self.instance.participant_2.pk) )


