import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from account.models import Account, BUSINESS, CUSTOMER


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
        return get_register_template('رمز عبور و تکرار رمز عبور باید یکسان باشند.')

    if user_type not in [BUSINESS, CUSTOMER]:
        return get_register_template('Invalid user_type')

    if User.objects.filter(username=username).exists():
        return get_register_template('نام کاربری تکراری است.')
    elif Account.objects.filter(email=email).exists():
        return get_register_template('آدرس ایمیل تکراری است.')
    elif Account.objects.filter(phone_number=phone_number).exists():
        return get_register_template('شماره تماس تکراری است.')
    else:
        user = User.objects.create_user(
            username=username, password=password
        )

        account = Account.objects.create(
            user=user, user_type=user_type,
            first_name=first_name, last_name=last_name, email=email,
            phone_number=phone_number
        )
        account.save()

        return JsonResponse({"message": "ثبت نام با موفقیت انجام شد."}, status=status.HTTP_201_CREATED)


def index(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username,
    }

    return render(request, 'index.html', context=context)
