from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Goal(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Target: {self.target_amount})"

    @property
    def progress_percent(self):
        if self.target_amount > 0:
            return min(100, (self.current_amount / self.target_amount) * 100)
        return 0

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
        ('goal_deposit', 'Goal Deposit'),
        ('goal_withdrawal', 'Goal Withdrawal'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    goal = models.ForeignKey('Goal', null=True, blank=True, on_delete=models.SET_NULL, related_name='transactions')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()}: {self.amount} on {self.date})"