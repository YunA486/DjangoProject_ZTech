from django.urls import path

from z_tech import views
from z_tech.views import TechCreateView, TechUpdateView

app_name = 'z_tech'

urlpatterns = [
    path('list2/', views.list_tech, name='list'),
    path('add/', TechCreateView.as_view(), name='add'),  # bookmark:add
    path('detail2/<int:pk>/', views.detail_tech, name='detail'),   # bookmark:detail
    path('edit/<int:pk>/', TechUpdateView.as_view(), name='edit'),      # bookmark:edit
    path('delete/<int:pk>/', views.delete_tech, name='delete'), # bookmark:delete
]