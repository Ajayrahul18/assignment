from django.shortcuts import get_object_or_404
from .models import *
from django.shortcuts import render, redirect
from .forms import *
from django.http import JsonResponse



def home_page(request):
    users = User.objects.all()
    return render(request,'home.html',{'users':users})


def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            expense.calculate_equal_amount()
            return redirect('home_page')  # Redirect to the expense list or any other page
    else:
        form = ExpenseForm()

    return render(request, 'create_expense.html', {'form': form})






