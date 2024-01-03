from django.urls import path
from RestAPI.views import *

urlpatterns = [

    path('user/registration',UserRegistration.as_view()),
    path('add/expenses',AddExpenses.as_view()),
    path('get/expense',GetExpensesBasedonId.as_view())
]