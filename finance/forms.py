from django import forms
from .models import Account, Goal, Transaction

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Name'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Starting Balance'}),
        }

class AccountTransactionForm(forms.Form):
    amount = forms.DecimalField(label="Amount", min_value=0.01)
    description = forms.CharField(label="Description", required=False)

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['account', 'name', 'target_amount', 'current_amount', 'deadline']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Goal Name'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target Amount'}),
            'current_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Current Amount'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class GoalTransactionForm(forms.Form):
    amount = forms.DecimalField(label="Amount", min_value=0.01)
    description = forms.CharField(label="Description", required=False)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'type', 'name', 'amount', 'goal', 'description']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction Name'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'goal': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description (optional)'}),
        }