from django.urls import path
from .views import (trip_ , CalendarView,index ,add_location,new_flight)

# app_name = 'trip'
urlpatterns = [
    # url(r'^index/$', views.index, name='index'),

    path('', CalendarView.as_view(), name='calendar'),
    path('index/', index, name='index'),
    path('new/', trip_, name='trip_new'),
	path('edit/<int:trip_id>/', trip_, name='trip_edit'),
	path('add_location/', add_location, name='add_location'),
	path('new_flight/', new_flight, name='new_flight'),
]
 