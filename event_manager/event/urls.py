from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='event-home'),
    path('event_list/', views.event_list, name='event-event_list'),
    path('top-rated/', views.top_rated_list, name='event-top-rated'),
    path('event/<int:id>/', views.view_event, name='event-view'),
    path('event/<int:id>/users', views.users_attend, name='event-users'),
    path('event/delete-comment/<int:id>/',
         views.delete_comment, name='delete_comment'),
    path('event/report-comment/<int:id>/',
         views.report_comment, name='report_comment'),
    path('event/choose-comment/<int:id>/',
         views.choose_comment, name='choose_comment'),
    path('recommended/', views.recommended_event_list,
         name='event-recommended_list'),
    path('myevents/', views.my_events, name='event-my_events'),
    path('myevents/past', views.my_events_past, name='event-my_events_past'),
    path('myevents/all', views.my_events_all, name='event-my_events_all'),
    path('myevents/<int:id>/delete', views.remove_my_event,
         name='event-remove_my_event'),
    path('calendar/', views.calendar, name='event-calendar'),
]
