from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from RestAPI.serializers import *
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from RestAPI.models import *
# Create your views here.


class UserRegistration(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):

        try:
            pythonData = request.data

            # pythonData["password"] = make_password(pythonData.get("password"))

            
            serializer = UserRegistrationSerializer(data=pythonData)

            if serializer.is_valid():
                print("valid serializer")


                serializer.save(password = make_password(pythonData.get("password")))

                return Response({"message":"successfullycreated"},status.HTTP_201_CREATED)
            

            else:
                print("Serializer errors:", serializer.errors)  # Printing serializer errors

                return Response({"message": "Validation Error", "errors": serializer.errors},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)



        except Exception as e:
            print(e)

            return Response({"message":f"{e}"},status.HTTP_422_UNPROCESSABLE_ENTITY)
        


class AddExpenses(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):

        try:
            pythonData = request.data

            # pythonData["password"] = make_password(pythonData.get("password"))

            expenseType = pythonData.get('expenseType')
            distributedAmount = pythonData.get('distributedAmount',False)

            if expenseType == 2:
                if not distributedAmount:
                    return Response({"message": "Validation Error", "errors": "distributedAmount is required"},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                
                if type(distributedAmount) != dict:
                    return Response({"message": "Type Error", "errors": "please give valid type"},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)


            
            serializer = ExpenseSerializer(data=pythonData)

            if serializer.is_valid():
                print("valid serializer")


                t = serializer.save()

                if t.expenseType == 1:
                    user_count = t.distributed_user.all().count()
                    distributed_amount = t.amount_paid/user_count

                    for distributeduser in t.distributed_user.all():

                        ExpensesDistributedBetweenUser.objects.create(distributed_amount=distributed_amount,distributed_user=distributeduser,expense=t)


                if t.expenseType == 2:
                    print("type2222")

                    for distributeduser in t.distributed_user.all():
                        distributed_amount = distributedAmount.get(str(distributeduser.id))

                        ExpensesDistributedBetweenUser.objects.create(distributed_amount=distributed_amount,distributed_user=distributeduser,expense=t)


                if t.expenseType == 3:
                    print("type3")

                    for distributeduser in t.distributed_user.all():
                        distributed_percentage = distributedAmount.get(str(distributeduser.id))

                        distributed_amount = t.amount_paid * int(distributed_percentage)/100

                        ExpensesDistributedBetweenUser.objects.create(distributed_amount=distributed_amount,distributed_user=distributeduser,expense=t)





                return Response({"message":"ExpensecreatedSuccessfully"},status.HTTP_201_CREATED)
            

            else:
                print("Serializer errors:", serializer.errors)  # Printing serializer errors

                return Response({"message": "Validation Error", "errors": serializer.errors},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)



        except Exception as e:
            print(e)

            return Response({"message":f"{e}"},status.HTTP_422_UNPROCESSABLE_ENTITY)

       

        
class GetExpensesBasedonId(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):

        id = self.request.query_params.get('id',False)

        if not id:
            return Response({"message": "Validation Error", "errors": "id is required"},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        user = User.objects.filter(id=id).first()

        if not user:
            return Response({"message": "Error", "errors": "user not found with this id"},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        

        if user:
            user_paid_amount = Expenses.objects.filter(payer=user).aggregate(Sum("amount_paid",default=0))

            print(user_paid_amount["amount_paid__sum"],"amountt")

            expenses = Expenses.objects.all()
            mydictoweamount = {}


            for expenses in expenses:
                expensedistribute = expenses.expense_ref.exclude(distributed_user=expenses.payer)
                
                for data in expensedistribute:
                    if data.expense.payer == user:

                        mydictoweamount[data.distributed_user.id] = mydictoweamount.get(data.distributed_user.id,0) + data.distributed_amount


                    elif  data.expense.payer != user and data.distributed_user == user:
                        mydictoweamount[data.expense.payer.id] = mydictoweamount.get(data.expense.payer.id,0) - data.distributed_amount




                        


            




        


        return Response({"values":mydictoweamount,"message":"ExpenseRetrievesuccessfully"},status.HTTP_200_OK)
        

        