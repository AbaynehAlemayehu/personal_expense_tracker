from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Expense, Category
from .forms import ExpenseForm
from datetime import datetime
from django.views.decorators.http import require_GET

# -------------------- Home --------------------
def home(request):
    return HttpResponse("Welcome to Personal Expense Tracker!")

# -------------------- Expense List / Dashboard --------------------
@login_required
def expense_list(request):
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    expenses = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).order_by('-date')

    categories = Category.objects.all()
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    monthly_income = 0

    # Handle AJAX request
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        category_name = request.POST.get('category', '').strip()
        amount = request.POST.get('amount')
        note = request.POST.get('note', '')
        date = request.POST.get('date')

        if not category_name or not amount or not date:
            return JsonResponse({'errors': 'Category, Amount, and Date are required.'}, status=400)

        category, _ = Category.objects.get_or_create(name=category_name)
        expense = Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            note=note,
            date=date
        )

        return JsonResponse({
            'id': expense.id,
            'category': expense.category.name,
            'amount': str(expense.amount),
            'note': expense.note,
            'date': expense.date.strftime('%b. %d, %Y'),
        })

    return render(request, 'tracker/expense_list.html', {
        'expenses': expenses,
        'categories': categories,
        'total_expense': total_expense,
        'current_month': today.strftime('%B'),
        'current_year': today.year,
        'monthly_income': monthly_income,
    })

# -------------------- Create Expense --------------------
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
    return render(request, 'tracker/expense_form.html', {'form': form})

# -------------------- Update Expense --------------------
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
    return render(request, 'tracker/expense_form.html', {'form': form})

# -------------------- Delete Expense --------------------
@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/expense_confirm_delete.html', {'expense': expense})

# -------------------- User Signup --------------------
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('expense_list')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

# -------------------- User Login --------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('expense_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

# -------------------- User Logout (GET version) --------------------
@login_required
@require_GET
def logout_view(request):
    logout(request)
    return redirect('login')
