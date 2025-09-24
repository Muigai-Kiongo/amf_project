from django import forms
from .models import Goal, Budget, Transaction, Category

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'target_amount', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'period_start', 'period_end', 'total_amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'period_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'period_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'budget', 'category', 'amount', 'date', 'description']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'budget': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category_type': forms.Select(attrs={'class': 'form-control'}),
        }