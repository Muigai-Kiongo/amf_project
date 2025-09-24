from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Goal, Budget, Transaction, Category
from .forms import GoalForm, BudgetForm, TransactionForm, CategoryForm

# Mixin to ensure objects are owned by the current user
class UserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

@login_required
def dashboard(request):
    goals = Goal.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

    messages.info(request, "Welcome to your finance dashboard!")

    context = {
        "goals": goals,
        "budgets": budgets,
        "transactions": transactions[:5],  # latest 5
        "total_income": total_income,
        "total_expense": total_expense,
    }
    return render(request, "dashboard.html", context)

# Goal Views
class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'goal/goal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class GoalDetailView(LoginRequiredMixin, UserIsOwnerMixin, DetailView):
    model = Goal
    template_name = 'goal/goal_detail.html'

class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goal/goal_form.html'
    success_url = reverse_lazy('goal-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goal/goal_form.html'
    success_url = reverse_lazy('goal-list')

class GoalDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Goal
    template_name = 'goal/goal_confirm_delete.html'
    success_url = reverse_lazy('goal-list')

# Budget Views
class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budget/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetDetailView(LoginRequiredMixin, UserIsOwnerMixin, DetailView):
    model = Budget
    template_name = 'budget/budget_detail.html'

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BudgetUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget/budget_form.html'
    success_url = reverse_lazy('budget-list')

class BudgetDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Budget
    template_name = 'budget/budget_confirm_delete.html'
    success_url = reverse_lazy('budget-list')

# Transaction Views
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class TransactionDetailView(LoginRequiredMixin, UserIsOwnerMixin, DetailView):
    model = Transaction
    template_name = 'transaction/transaction_detail.html'

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

class TransactionDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Transaction
    template_name = 'transaction/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction-list')

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryDetailView(LoginRequiredMixin, UserIsOwnerMixin, DetailView):
    model = Category
    template_name = 'category/category_detail.html'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')