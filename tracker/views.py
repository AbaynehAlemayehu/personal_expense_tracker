from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseListCreate(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Personal Expense Tracker!")
from rest_framework import viewsets
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
from django.shortcuts import render
from .models import Expense
from django.contrib.auth.decorators import login_required

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/expense_list.html', {'expenses': expenses})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Category
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/expense_list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/expense_form.html', {'form': form, 'title': 'Add Expense'})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/expense_form.html', {'form': form, 'title': 'Edit Expense'})
