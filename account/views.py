import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from account.models import Account, SELLER, CUSTOMER
from customer.models import Customer, Cart
from seller.models.seller import Seller


def get_register_template(error_str):
    return JsonResponse({"message": error_str}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    password = data['password']
    confirm_password = data['confirm_password']
    email = data['email']
    phone_number = data['phone_number']
    first_name = data['first_name']
    last_name = data['last_name']
    user_type = data['user_type']

    if password != confirm_password:
        return get_register_template('password and confirm_password are different')

    if user_type not in [SELLER, CUSTOMER]:
        return get_register_template('Invalid user_type')

    if User.objects.filter(username=username).exists():
        return get_register_template('username taken')
    elif Account.objects.filter(email=email).exists():
        return get_register_template('email taken')
    elif Account.objects.filter(phone_number=phone_number).exists():
        return get_register_template('phone_number taken')
    else:
        user = User.objects.create_user(
            username=username, password=password
        )

        account_model = Customer

        if user_type == SELLER:
            account_model = Seller

        account = account_model.objects.create(
            user=user, user_type=user_type,
            first_name=first_name, last_name=last_name, email=email,
            phone_number=phone_number, balance=0
        )
        account.save()

        if user_type == CUSTOMER:
            Cart.objects.create(customer=account, products=list())

        return JsonResponse({"message": "registered successfully"}, status=status.HTTP_201_CREATED)


def index(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username,
    }

    return render(request, 'index.html', context=context)
