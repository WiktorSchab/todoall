from django.urls import path
from . import views 

urlpatterns = [
    path('', views.todoproject, name='todoproject'),
    path('project/<id>', views.singleproject, name='singleproject'),
]