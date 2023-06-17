from django.contrib import admin
from .models import Budget, Expense, Income, Category


admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(Category)
# Register your models here.
