from django.urls import path
from sport_events import views

app_name = 'sport_events'

urlpatterns = [
    path('', views.SportEventsHomeView.as_view(), name='sport_events_home'),
    
    path('active_events/', views.ActiveEventListView.as_view(), name='active_events'),
    path('closed_events/', views.ClosedEventListView.as_view(), name='closed_events'),
    path('completed_events/', views.CompletedEventListView.as_view(), name='completed_events'),
    path('my_events/', views.MyEventListView.as_view() , name='my_events'),
    
    path('event/<int:pk>/', views.EventDetailView.as_view() , name='event_detail'),
    path('event/<int:pk>/register/', views.register , name='register'),
    path('event/<int:pk>/schedule/', views.schedule , name='schedule'),

    path('match/<int:pk>/update/', views.MatchUpdateView.as_view() , name='match_update'),
]
