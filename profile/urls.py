from django.urls import path

from . import views

app_name = 'profile'

urlpatterns = [
    path('view/', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
]
