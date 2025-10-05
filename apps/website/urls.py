from django.urls import path
from apps.website import views


urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('architects/', views.architects, name='architects'),
    path('projects/<int:project_id>/', views.works_progress, name='works_progress'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('api/submit-zayavka/', views.submit_zayavka, name='submit_zayavka'),
]