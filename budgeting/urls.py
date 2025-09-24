from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('budget-list/', views.budget_list, name='budget_list'),
    # path('budget-create/', views.budget_create, name='budget_create'),
    # path('budget-edit/<int:pk>/', views.budget_edit, name='budget_edit'),
    # path('budget-delete/<int:pk>/', views.budget_delete, name='budget_delete'),
    # path('budget-detail/<int:pk>/', views.budget_detail, name='budget_detail'),
]