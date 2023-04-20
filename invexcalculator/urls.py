from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    # path('show', views.show_data, name='show_data')
]