from django.contrib import admin
from sport_events.models import Sport,Event,Match
from .forms import MatchForm
# Register your models here.




class MatchAdmin(admin.ModelAdmin):
    form = MatchForm    


admin.site.register(Sport)
admin.site.register(Event)
admin.site.register(Match, MatchAdmin)
