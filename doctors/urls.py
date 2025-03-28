from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.home, name='home'),
    path('organ/<int:organ_id>/', views.doctor_list, name='doctor_list'),
    path('search/', views.search_doctors, name='search_doctors'),
] 