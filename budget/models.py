from django.utils import timezone
from django.db import models
from django.utils.text import slugify

class Budget(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    start_budget = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Budget, self).save(*args, **kwargs)

    def expence_sum(self):
        expense_list = Expense.objects.filter(budget=self)
        total_expence_amount = 0
        for expence in expense_list:
            total_expence_amount += expence.amount
        return total_expence_amount
    
    def income_sum(self):
        income_list = Income.objects.filter(budget=self)
        total_income_amount = 0
        for income in income_list:
            total_income_amount += income.amount
        return total_income_amount
    
    def budget_current(self):
        total_income_amount = self.income_sum()
        total_expence_amount = self.expence_sum()      
        return self.start_budget - total_expence_amount + total_income_amount
    
    def expences_per_category_data(self):
        expense_list = Expense.objects.filter(budget=self)
        category_list = Category.objects.filter(budget=self)
        amount_list = []
        category_names_list = []
        for category in category_list:
            amount_sum = 0
            for expense in expense_list:
                if expense.category.name == category.name:
                    amount_sum += expense.amount
            if amount_sum >0:
                category_names_list.append(category.name)
                amount_list.append(amount_sum)
        return category_names_list, amount_list
    
    def income_per_category_data(self):
        income_list = Income.objects.filter(budget=self)
        category_list = Category.objects.filter(budget=self)
        amount_list = []
        category_names_list = []
        for category in category_list:
            amount_sum = 0
            for income in income_list:
                if income.category.name == category.name:
                    amount_sum += income.amount
            if amount_sum >0:
                category_names_list.append(category.name)
                amount_list.append(amount_sum)
        return category_names_list, amount_list
        
    



class Category(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField(blank=True)

    class Meta:
        ordering = ('-date', '-amount')

    

class Income(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='incomes')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField(blank=True)

    class Meta:
        ordering = ('-date', '-amount')