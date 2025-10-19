from django.urls import path
from . import views

urlpatterns = [
    # Dashboard / Expenses
    path('', views.expense_list, name='expense_list'),
    path('expense/new/', views.expense_create, name='expense_create'),
    path('expense/<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('expense/<int:pk>/delete/', views.expense_delete, name='expense_delete'),

    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

