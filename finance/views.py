from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django import forms
from .models import Account, Goal, Transaction
from .forms import AccountForm, GoalForm, TransactionForm, GoalTransactionForm

# Deposit/Withdraw Forms
class AccountTransactionForm(forms.Form):
    amount = forms.DecimalField(label="Amount", min_value=0.01)
    description = forms.CharField(label="Description", required=False)

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    goals = Goal.objects.filter(account__user=request.user)
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    total_goal_saved = goals.aggregate(total=Sum('current_amount'))['total'] or 0

    messages.info(request, "Welcome to your finance dashboard!")

    context = {
        "accounts": accounts,
        "goals": goals,
        "transactions": transactions[:5],  # latest 5
        "total_income": total_income,
        "total_expense": total_expense,
        "total_goal_saved": total_goal_saved,
    }
    return render(request, "dashboard.html", context)

# Account Views
@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'account/account_list.html', {'accounts': accounts})

@login_required
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    return render(request, 'account/account_detail.html', {'account': account})

@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account-list')
    else:
        form = AccountForm()
    return render(request, 'account/account_form.html', {'form': form})

@login_required
def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account-list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'account/account_form.html', {'form': form})

@login_required
def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        account.delete()
        return redirect('account-list')
    return render(request, 'account/account_confirm_delete.html', {'account': account})

# Deposit/Withdraw Views
@login_required
def account_deposit(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountTransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            Transaction.objects.create(
                account=account,
                type='income',
                amount=amount,
                description=description
            )
            account.balance += amount
            account.save()
            messages.success(request, f"Deposited {amount} KES to {account.name}")
            return redirect('account-detail', pk=pk)
    else:
        form = AccountTransactionForm()
    return render(request, 'account/account_deposit_form.html', {'form': form, 'account': account})

@login_required
def account_withdraw(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountTransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            if amount > account.balance:
                messages.error(request, "Insufficient balance.")
            else:
                Transaction.objects.create(
                    account=account,
                    type='expense',
                    amount=amount,
                    description=description
                )
                account.balance -= amount
                account.save()
                messages.success(request, f"Withdrew {amount} KES from {account.name}")
                return redirect('account-detail', pk=pk)
    else:
        form = AccountTransactionForm()
    return render(request, 'account/account_withdraw_form.html', {'form': form, 'account': account})

# Goal Views
@login_required
def goal_list(request):
    goals = Goal.objects.filter(account__user=request.user)
    return render(request, 'goal/goal_list.html', {'goals': goals})

@login_required
def goal_detail(request, pk):
    goal = get_object_or_404(Goal, pk=pk, account__user=request.user)
    return render(request, 'goal/goal_detail.html', {'goal': goal})

@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save()
            return redirect('goal-list')
    else:
        form = GoalForm()
        form.fields['account'].queryset = Account.objects.filter(user=request.user)
    return render(request, 'goal/goal_form.html', {'form': form})

@login_required
def goal_update(request, pk):
    goal = get_object_or_404(Goal, pk=pk, account__user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal-list')
    else:
        form = GoalForm(instance=goal)
        form.fields['account'].queryset = Account.objects.filter(user=request.user)
    return render(request, 'goal/goal_form.html', {'form': form})

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, account__user=request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('goal-list')
    return render(request, 'goal/goal_confirm_delete.html', {'goal': goal})


@login_required
def goal_deposit(request, pk):
    goal = get_object_or_404(Goal, pk=pk, account__user=request.user)
    account = goal.account
    if request.method == 'POST':
        form = GoalTransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            # Update goal and account
            goal.current_amount += amount
            goal.save()
            account.balance -= amount  # Money moves from account to goal
            account.save()
            Transaction.objects.create(
                account=account,
                goal=goal,
                type='expense',  # From account's perspective
                amount=amount,
                description=description
            )
            messages.success(request, f"Deposited {amount} KES to goal '{goal.name}' from account '{account.name}'.")
            return redirect('goal-detail', pk=pk)
    else:
        form = GoalTransactionForm()
    return render(request, 'goal/goal_deposit_form.html', {'form': form, 'goal': goal})

@login_required
def goal_withdraw(request, pk):
    goal = get_object_or_404(Goal, pk=pk, account__user=request.user)
    account = goal.account
    if request.method == 'POST':
        form = GoalTransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            if amount > goal.current_amount:
                messages.error(request, "Insufficient goal funds.")
            else:
                goal.current_amount -= amount
                goal.save()
                account.balance += amount  # Money moves from goal back to account
                account.save()
                Transaction.objects.create(
                    account=account,
                    goal=goal,
                    type='income',  # From account's perspective
                    amount=amount,
                    description=description
                )
                messages.success(request, f"Withdrew {amount} KES from goal '{goal.name}' to account '{account.name}'.")
                return redirect('goal-detail', pk=pk)
    else:
        form = GoalTransactionForm()
    return render(request, 'goal/goal_withdraw_form.html', {'form': form, 'goal': goal})
# Transaction Views

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    return render(request, 'transaction/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, account__user=request.user)
    return render(request, 'transaction/transaction_detail.html', {'transaction': transaction})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        form.fields['account'].queryset = Account.objects.filter(user=request.user)
        form.fields['goal'].queryset = Goal.objects.filter(account__user=request.user)
        if form.is_valid():
            transaction = form.save()
            if transaction.type == 'income':
                transaction.account.balance += transaction.amount
            elif transaction.type == 'expense':
                transaction.account.balance -= transaction.amount
            transaction.account.save()
            update_goal_amount(transaction)
            return redirect('transaction-list')
    else:
        form = TransactionForm()
        form.fields['account'].queryset = Account.objects.filter(user=request.user)
        form.fields['goal'].queryset = Goal.objects.filter(account__user=request.user)
    return render(request, 'transaction/transaction_form.html', {'form': form})

@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, account__user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        form.fields['account'].queryset = Account.objects.filter(user=request.user)
        form.fields['goal'].queryset = Goal.objects.filter(account__user=request.user)
        if form.is_valid():
            transaction = form.save()
            update_goal_amount(transaction)
            return redirect('transaction-list')
    else:
        form = TransactionForm(instance=transaction)
        form.fields['account'].queryset = Account.objects.filter(user=request.user)
        form.fields['goal'].queryset = Goal.objects.filter(account__user=request.user)
    return render(request, 'transaction/transaction_form.html', {'form': form})

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, account__user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction-list')
    return render(request, 'transaction/transaction_confirm_delete.html', {'transaction': transaction})

@login_required
def reports(request):
    accounts = Account.objects.filter(user=request.user)
    goals = Goal.objects.filter(account__user=request.user)
    transactions = Transaction.objects.filter(account__user=request.user)

    # Account summaries
    account_summaries = []
    for account in accounts:
        acc_transactions = transactions.filter(account=account)
        acc_income = acc_transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        acc_expense = acc_transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        acc_goal_count = account.goals.count()
        account_summaries.append({
            'account': account,
            'income': acc_income,
            'expense': acc_expense,
            'goal_count': acc_goal_count,
            'balance': account.balance,
        })
    # Goal summaries
    goal_summaries = []
    for goal in goals:
        goal_transactions = transactions.filter(goal=goal)
        goal_in = goal_transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        goal_out = goal_transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        percent = round(goal.current_amount / goal.target_amount * 100, 2) if goal.target_amount and goal.target_amount > 0 else 0
        goal_summaries.append({
            'goal': goal,
            'account': goal.account,
            'current_amount': goal.current_amount,
            'target_amount': goal.target_amount,
            'deposit': goal_out,
            'withdraw': goal_in,
            'progress_percent': percent,
        })
    total_transactions = transactions.count()
    total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    context = {
        'account_summaries': account_summaries,
        'goal_summaries': goal_summaries,
        'total_transactions': total_transactions,
        'total_income': total_income,
        'total_expense': total_expense,
    }
    return render(request, "reports.html", context)