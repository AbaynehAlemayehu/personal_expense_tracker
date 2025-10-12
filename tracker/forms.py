# tracker/forms.py
from django import forms  # ✅ Corrected

from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'note']  # remove 'date' if auto_now_add=True
        widgets = {
            'note': forms.Textarea(attrs={'rows': 2}),
        }
