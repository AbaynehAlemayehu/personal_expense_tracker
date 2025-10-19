from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Expense, Category


def home(request):
    return HttpResponse("Welcome to Personal Expense Tracker!")


# -------------------- Expense List --------------------
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    categories = Category.objects.all()

    # Handle AJAX request for adding a new expense directly
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        category_name = request.POST.get('category', '').strip()
        amount = request.POST.get('amount')
        note = request.POST.get('note', '')
        date = request.POST.get('date')

        if not category_name or not amount or not date:
            return JsonResponse({'errors': 'Category, Amount, and Date are required.'}, status=400)

        # Get or create category
        category, _ = Category.objects.get_or_create(name=category_name)

        # Create expense
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
    })


# -------------------- Create Expense --------------------
@login_required
def expense_create(request):
    from .forms import ExpenseForm
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
    from .forms import ExpenseForm
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
