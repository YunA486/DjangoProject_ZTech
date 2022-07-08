from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('inner/', views.inner, name='inner'),
    path('saving/', views.saving, name='saving'),
    path('investment/', views.investment, name='investment'),
]