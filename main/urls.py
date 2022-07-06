from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('main/', name='main'),
    path('what/', name='what'),
    path('saving/', name='saving'),
    path('investment/', name='investment'),
]