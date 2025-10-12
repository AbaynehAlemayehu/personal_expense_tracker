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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
]
