from django.shortcuts import render


def index(request):
    return render(request, 'base.html')

def budget_list(request):
    return render(request, 'budgeting/budget_list.html')

def budget_create(request):
    return render(request, 'budgeting/budget_create.html')

def budget_edit(request, pk):
    return render(request, 'budgeting/budget_edit.html')

def budget_delete(request, pk):
    return render(request, 'budgeting/budget_delete.html')

def budget_detail(request, pk):
    return render(request, 'budgeting/budget_detail.html')
