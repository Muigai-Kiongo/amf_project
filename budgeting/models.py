from django.db import models

class Budget(models.Model):
    budget_name = models.CharField(max_length=100)
    budget_amount = models.IntegerField()
    budget_date = models.DateField()
    
    def __str__(self):
        return self.budget_name
    
    class Meta:
        ordering = ['budget_date']
        
class BudgetItem(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_amount = models.IntegerField()
    
    def __str__(self):
        return self.item_name
