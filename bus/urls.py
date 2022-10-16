from django.urls import path

from .views import *


urlpatterns = [
    path('', bus_index,name='bus_index'),
    path('bus/', Bus_list, name='bus_list'),
    path('bus/add', add_buss, name='add_bus'),
    path('bus/<int:pk>/remove', remove_bus, name='remove_bus'),
    path('bus/<int:pk>/edit', edit_bus, name='edit_bus'),
    path('driver/', driver_index, name='driver_index'),
    path('driver/', driver_list, name='driver_list'),
    path('driver/add', add_driver, name='add_driver'),
    path('driver/<int:pk>/remove', remove_driver, name='remove_driver'),
    path('driver/<int:pk>/edit', edit_driver, name='edit_driver'),
]
