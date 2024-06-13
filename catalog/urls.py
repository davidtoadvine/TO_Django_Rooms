from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('buildings/', views.building_list, name='building_list'),
    path('buildings/<int:building_id>/', views.building_detail, name='building_detail'),
    path('sections/<int:section_id>/', views.section_detail, name='section_detail'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('persons/<int:person_id>/', views.person_detail, name='person_detail'),

]
