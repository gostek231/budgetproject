
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_list, name='budget_list'),
    path('add', views.BudgetCreateView.as_view(), name='add'),
    path('expence/<slug:budget_slug>', views.expense_detail, name='e_detail'),
    path('income/<slug:budget_slug>', views.income_detail, name='i_detail'),
    path('charts/<slug:budget_slug>', views.chart_view, name='chart_detail'),
]
