from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    # Goal URLs
    path('goals/', views.GoalListView.as_view(), name='goal-list'),
    path('goals/new/', views.GoalCreateView.as_view(), name='goal-create'),
    path('goals/<int:pk>/', views.GoalDetailView.as_view(), name='goal-detail'),
    path('goals/<int:pk>/edit/', views.GoalUpdateView.as_view(), name='goal-update'),
    path('goals/<int:pk>/delete/', views.GoalDeleteView.as_view(), name='goal-delete'),

    # Budget URLs
    path('budgets/', views.BudgetListView.as_view(), name='budget-list'),
    path('budgets/new/', views.BudgetCreateView.as_view(), name='budget-create'),
    path('budgets/<int:pk>/', views.BudgetDetailView.as_view(), name='budget-detail'),
    path('budgets/<int:pk>/edit/', views.BudgetUpdateView.as_view(), name='budget-update'),
    path('budgets/<int:pk>/delete/', views.BudgetDeleteView.as_view(), name='budget-delete'),

    # Transaction URLs
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/new/', views.TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction-update'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction-delete'),

    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
]