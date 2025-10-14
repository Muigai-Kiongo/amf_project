from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.account_list, name='account-list'),
    path('accounts/create/', views.account_create, name='account-create'),
    path('accounts/<int:pk>/', views.account_detail, name='account-detail'),
    path('accounts/<int:pk>/update/', views.account_update, name='account-update'),
    path('accounts/<int:pk>/delete/', views.account_delete, name='account-delete'),

    # Add these two for deposit and withdraw!
    path('accounts/<int:pk>/deposit/', views.account_deposit, name='account_deposit'),
    path('accounts/<int:pk>/withdraw/', views.account_withdraw, name='account_withdraw'),
    

    path('goals/', views.goal_list, name='goal-list'),
    path('goals/create/', views.goal_create, name='goal-create'),
    path('goals/<int:pk>/', views.goal_detail, name='goal-detail'),
    path('goals/<int:pk>/update/', views.goal_update, name='goal-update'),
    path('goals/<int:pk>/delete/', views.goal_delete, name='goal-delete'),

    path('goals/<int:pk>/deposit/', views.goal_deposit, name='goal_deposit'),
    path('goals/<int:pk>/withdraw/', views.goal_withdraw, name='goal_withdraw'),

    path('transactions/', views.transaction_list, name='transaction-list'),
    path('transactions/create/', views.transaction_create, name='transaction-create'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction-detail'),
    path('transactions/<int:pk>/update/', views.transaction_update, name='transaction-update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction-delete'),

    path('reports/', views.reports, name='reports'),
]