from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=7, choices=CATEGORY_TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
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

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=100)
    period_start = models.DateField()
    period_end = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} [{self.period_start} - {self.period_end}]"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    budget = models.ForeignKey(Budget, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} on {self.date}"

    class Meta:
        ordering = ['-date', '-created_at']