from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from RestAPI.models import *



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fullName','mobileNo','password','email','deviceToken']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ['expenseType','payer','amount_paid','distributed_user']