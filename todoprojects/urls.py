from django.urls import path
from . import views 

urlpatterns = [
    path('', views.todoproject, name='todoproject'),
    path('project/<id>', views.singleproject, name='singleproject'),

    path('project_new/<project_id>', views.singleproject_new, name='singleproject_new'),
    path('project_done/<id>', views.singleproject_done, name='singleproject_done'),
    path('project_delete/<id>', views.singleproject_delete, name='singleproject_delete'),

    path('add_user', views.add_user, name='add_user'),
]