from django.urls import path
from .views import CategoryListCreate, ExpenseListCreate

urlpatterns = [
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('expenses/', ExpenseListCreate.as_view(), name='expense-list-create'),
]
from django.urls import path
from .views import home, CategoryListCreate, ExpenseListCreate

urlpatterns = [
    path('', home, name='home'),  # ✅ Root URL
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('expenses/', ExpenseListCreate.as_view(), name='expense-list-create'),
]
