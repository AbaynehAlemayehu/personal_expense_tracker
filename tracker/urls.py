from django.urls import path
from .views import expense_list, expense_create, expense_update, expense_delete

urlpatterns = [
    path('', expense_list, name='expense_list'),
    path('expense/new/', expense_create, name='expense_create'),
    path('expense/<int:pk>/edit/', expense_update, name='expense_update'),
    path('expense/<int:pk>/delete/', expense_delete, name='expense_delete'),
]
from tracker.views import home
