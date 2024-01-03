from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

class CustomAccountManager(BaseUserManager):
    pass


class User(AbstractBaseUser,PermissionsMixin):
    fullName = models.CharField(max_length=255)
    mobileNo = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=now, editable=False)
    deviceToken = models.CharField(max_length=255, null=True, default=None)
    deviceType = models.SmallIntegerField(default=0) #1 for Android #2 for Apple # 3 for web user
    profileImage = models.CharField(max_length=255,null=True,default=None)
    createdAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName','mobileNo']
    objects = CustomAccountManager()

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.fullName
    


class Expenses(models.Model):
    expenseType = models.SmallIntegerField() #1 means Equal 2 means exact 3 means Percentage
    payer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='payer_user_ref')
    amount_paid = models.DecimalField(max_digits=10,decimal_places=2)
    distributed_user = models.ManyToManyField(User)


    class Meta:
        db_table = "Expenses"


class ExpensesDistributedBetweenUser(models.Model):
    expense = models.ForeignKey(Expenses,on_delete=models.CASCADE,related_name='expense_ref')
    distributed_amount = models.DecimalField(max_digits=10,decimal_places=2)
    distributed_user = models.ForeignKey(User,on_delete=models.CASCADE)


    class Meta:
        db_table = "ExpensesDistributed"



