import json
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Budget, Category, Expense, Income
from django.views.generic import CreateView
from django.utils.text import slugify
from .forms import ExpenseForm
import matplotlib.pyplot as plt

def budget_list(request):
    budgeg_list = Budget.objects.all()
    return render(request, 'budget/budget-list.html',{'budgeg_list' : budgeg_list})


def chart_view(request, budget_slug):
    budget = get_object_or_404(Budget, slug=budget_slug)
    category_list = budget.expences_per_category_data()[0]
    expences_amount_list = budget.expences_per_category_data()[1]
    incomes_amount_list = budget.income_per_category_data()[1]
    return render(request, 'budget/chart-detail.html', {'budget': budget,'category_list' : category_list, 'incomes_amount_list' : incomes_amount_list,'expences_amount_list' : expences_amount_list, 'budget_slug' : budget_slug})


def income_detail(request, budget_slug):
    budget = get_object_or_404(Budget, slug=budget_slug)
    if request.method == 'GET':
        category_list = Category.objects.filter(budget=budget)
        return render(request, 'budget/income-detail.html',{'budget': budget, 'income_list' : budget.incomes.all(), 'category_list' : category_list, 'budget_slug' : budget_slug})
    elif request.method == 'POST':
        #process the form
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']
            date = form.cleaned_data['date']

            category = get_object_or_404(Category, budget=budget, name=category_name)

            Income.objects.create(
                budget=budget,
                title=title,
                amount=amount,
                category=category,
                date=date
            ).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = Income.objects.get(id=id)
        expense.delete()

        return HttpResponse('')

    return HttpResponseRedirect(budget_slug)



def expense_detail(request, budget_slug):
    budget = get_object_or_404(Budget, slug=budget_slug)

    if request.method == 'GET':
        category_list = Category.objects.filter(budget=budget)
        return render(request, 'budget/expense-detail.html',{'budget': budget, 'expense_list' : budget.expenses.all(), 'category_list' : category_list, 'budget_slug' : budget_slug})
    elif request.method == 'POST':
        #process the form
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']
            date = form.cleaned_data['date']

            category = get_object_or_404(Category, budget=budget, name=category_name)

            Expense.objects.create(
                budget=budget,
                title=title,
                amount=amount,
                category=category,
                date=date
            ).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = Expense.objects.get(id=id)
        expense.delete()

        return HttpResponse('')

    return HttpResponseRedirect(budget_slug)


    

class BudgetCreateView(CreateView):
    model = Budget
    template_name = 'budget/add-budget.html'
    fields = ('name', 'start_budget')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                budget=Budget.objects.get(id=self.object.id),
                name=category
            ).save()

        return HttpResponseRedirect('expence/' + self.get_success_url())
    
    def get_success_url(self):
        return slugify(self.request.POST['name']) 
    
    
    