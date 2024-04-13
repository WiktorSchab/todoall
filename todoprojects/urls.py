from django.urls import path
from . import views 

urlpatterns = [
    path('', views.todoproject, name='todoproject'),
    path('project/<id>', views.singleproject, name='singleproject'),
    path('project_done/<id>', views.singleproject_done, name='singleproject_done'),
    path('project_delete/<id>', views.singleproject_delete, name='singleproject_delete'),
]