from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout_user, name='logout'),
    path('login', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
    path('mytodo', views.mytodo, name='mytodo'),
    path('delete_task/<id>', views.delete_task, name='delete_task'),
    path('complete_task/<id>', views.complete_task, name='complete_task'),
]