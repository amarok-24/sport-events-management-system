from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from .models import Event,Match
from django.shortcuts import redirect
from django.urls import reverse
from django.db import transaction
from .forms import MatchForm
from django.db.models import Max
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

class ActiveEventListView(ListView):
    template_name = "sport_events/active_events_list.html"

    def get_queryset(self):
        return Event.objects.filter(status='ACTIVE')
    
    
class ClosedEventListView(ListView):
    template_name = "sport_events/closed_events_list.html"

    def get_queryset(self):
        return Event.objects.filter(status='CLOSED')


class CompletedEventListView(ListView):
    template_name = "sport_events/completed_events_list.html"

    def get_queryset(self):
        return Event.objects.filter(status='COMPLETED')


class MyEventListView(LoginRequiredMixin,ListView):
    template_name = "sport_events/my_events_list.html"

    def get_queryset(self):
        return self.request.user.event_set.all()


class EventDetailView(LoginRequiredMixin,DetailView):
    model = Event
    template_name = "sport_events/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_registered'] = False
        if self.request.user in self.object.participants.all():
            context['is_registered'] = True
        # context['is_staff'] = self.request.user.is_staff 
        context['matches'] = self.object.matches.filter(round_no=self.object.curr_round)

        if self.object.status == 'COMPLETED':
            res = self.object.matches.all().aggregate(Max('round_no'))
            winner = self.object.matches.filter(round_no=res['round_no__max'])[0].winner
            context['winner'] = winner 
            
        return context




@login_required
def register(request,pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user.is_teacher:
        user_type = 'TEACHER'
    else: 
        user_type = 'STUDENT'    

    if event.status=='ACTIVE' and event.eligible_user_type == user_type:
        event.participants.add(request.user)
        return redirect(reverse('sport_events:active_events'))        

    return redirect(reverse('sport_events:event_detail', kwargs={'pk':pk}))




class SportEventsHomeView(TemplateView):

    template_name = "sport_events/sport_events_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Odd even change remaining in scheduling
@login_required
@user_passes_test(lambda u:u.is_staff)
@transaction.atomic
def schedule(request,pk):
    event = get_object_or_404(Event, pk=pk)

    participants = []

    if event.curr_round==0:
        participants = [p for p in event.participants.all()]
    else:
        participants = [p.winner for p in event.matches.filter(round_no=event.curr_round)]
        
        for p in participants:
            if p is None:
                # set some message
                return redirect(reverse('sport_events:event_detail', kwargs={'pk':pk}))

    l = len(participants)
    
    if l==1:
        event.complete()
        event.save()
        return EventDetailView.as_view()(request, pk=pk)
        # return redirect(reverse('sport_events:event_detail', kwargs={'pk':pk}))

    event.curr_round = event.curr_round + 1
    event.save()

    i=0
    while i+1 < l:
        Match(event=event,participant_1=participants[i],participant_2=participants[i+1],
                round_no=event.curr_round).save()
        i=i+2

    if i<l:
        Match(event=event,participant_1=participants[i],
                round_no=event.curr_round).save()
    
    return redirect(reverse('sport_events:event_detail', kwargs={'pk':pk}))



@method_decorator([login_required, user_passes_test(lambda u:u.is_staff)], name='dispatch')
class MatchUpdateView(UpdateView):
    model = Match
    # fields="__all__"
    form_class = MatchForm
    template_name = "sport_events/match_update.html"
