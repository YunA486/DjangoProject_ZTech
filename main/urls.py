from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name='main'),
    path('what/', views.what, name='what'),
    path('saving/', views.saving, name='saving'),
    path('investment/', views.investment, name='investment'),
]