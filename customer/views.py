import json
import time
from threading import Thread
import requests
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from general import util
from models.constants import ServerEnum
from user import views as user_views
from models.user import User
from django.contrib.auth.hashers import make_password


@csrf_exempt
def customerSignin(request):
    try:
        requestBody = util.decodeJson(request.body)
        email = requestBody['email']
        password = requestBody['password']

        adminDetailsUserDatabaseResult = util.executesql(
            query="SELECT * FROM customer_user_table WHERE userEmail = %s AND password = %s",
            datatuple=[email, password])

        if (adminDetailsUserDatabaseResult):
            return sendCustomerData(adminDetailsUserDatabaseResult)
        else:
            return JsonResponse({
                'status': False,
                'responseMessage': ServerEnum.RESPONSE_PASSWORD_MISMATCH
            })

    except Exception as e:
        print("ERROR IN loginAsAdmin() method in admin/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()

@csrf_exempt
def customerSignup(request):
    try:
        requestBody = util.decodeJson(request.body)
        email = requestBody['email']
        password = requestBody['password']
        firstName = requestBody['firstName']
        secondName = requestBody['secondName']

        userId = util.generateID("CUSTOMER")


        util.executesql(
            query = "INSERT INTO customer_user_table" \
                "(userId, userEmail, password, firstName, secondName, createdTime)" \
                "VALUES (%s, %s, %s, %s, %s, %s)",
            datatuple=[userId, email, make_password(password), firstName, secondName, util.utcTimeStamp()] 
        )

        adminDetailsUserDatabaseResult = util.executesql(
            query="SELECT * FROM admin_user_table WHERE userEmail = %s AND password = %s",
            datatuple=[email, password])

        if (adminDetailsUserDatabaseResult):
            return sendCustomerData(adminDetailsUserDatabaseResult)
        else:
            return JsonResponse({
                'status': False,
                'responseMessage': ServerEnum.RESPONSE_PASSWORD_MISMATCH
            })

    except Exception as e:
        print("ERROR IN loginAsAdmin() method in admin/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()

# ------------------------------------------------------------------------------- #

def sendCustomerData(databaseResult):
    user = User.toJsonMapFromDatabase(databaseResult)

    return JsonResponse({
        'user': user,
        'status': True,
        'responseMessage': ServerEnum.RESPONSE_SUCCESS
    })
