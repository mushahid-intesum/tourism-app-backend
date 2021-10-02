import json
from datetime import datetime, timezone
from threading import Thread
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tourism_app import settings
from general import util
from models.admin_user import AdminUser
from models.constants import ServerEnum
from django.db import connection, transaction
from django.contrib.auth.hashers import make_password, check_password
import time
from models.user import User
import csv
from django.core.mail import EmailMessage
from django.core.cache import cache
import os
import requests
from user import views as user_views

@csrf_exempt
def adminSignin(request):
    print(request.headers)
    try:
        requestBody = util.decodeJson(request.body)

        print(requestBody)
        email = requestBody['email']
        password = requestBody['password']

        adminDetailsUserDatabaseResult = util.executesql(
            query="SELECT * FROM admin_user_table WHERE userEmail = %s AND password = %s",
            datatuple=[email, password])

        if (adminDetailsUserDatabaseResult):
            return sendAdminData(adminDetailsUserDatabaseResult)
        else:
            return JsonResponse({
                'status': False,
                'responseMessage': ServerEnum.RESPONSE_PASSWORD_MISMATCH
            })

    except Exception as e:
        print("ERROR IN adminSignin() method in admin/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()

# ------------------------------------------------------------------------------- #

def sendAdminData(databaseResult):
    user = User.toJsonMapFromDatabase(databaseResult)

    return JsonResponse({
        'user': user,
        'status': True,
        'responseMessage': ServerEnum.RESPONSE_SUCCESS
    })