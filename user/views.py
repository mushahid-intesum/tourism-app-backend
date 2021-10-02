import json
from threading import Thread
from typing import Any
from django.db import connection
from django.db.backends.utils import CursorWrapper
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from models.constants import ServerEnum
from google.oauth2 import id_token
from google.auth.transport import requests
from django.core.cache import cache
from general import util
from customer import views as customer_views
import django

# 
@csrf_exempt
def login(request):
    requestBody = util.decodeJson(request.body)

    if (requestBody['signInType'] == ServerEnum.SIGNIN_PHONE):
        return loginPhone(requestBody)


def loginPhone(requestBody):
    phoneToken = requestBody['authToken']
    phoneNumber = requestBody['phoneNumber']
    appType = requestBody['appType']

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        phoneIdInformation = id_token.verify_firebase_token(
            phoneToken, requests.Request())

        # ID token is valid.
        if (phoneIdInformation['aud'] == 'polar-caldron-291903'
                and phoneIdInformation['phone_number'] == phoneNumber):
            userPhone = phoneIdInformation['phone_number']

            if (appType == ServerEnum.APP_CUSTOMER):
                return customer_views.loginAsCustomer(appType=appType, phone=userPhone,
                                                      email=None, phoneVerified=1, emailVerified=0,
                                                      signInType=ServerEnum.SIGNIN_PHONE)

        return util.sendConnectionErrorResponse()

    except Exception as e:
        print("ERROR IN loginPhone() method in user/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()


@csrf_exempt
def updateProfile(request):
    try:
        requestBody = util.decodeJson(request.body)

        # This is when customer first logs in and sets his account
        if (requestBody['updateType'] == ServerEnum.PROFILE_CUSTOMER_REGISTRATION_UPDATE and
                requestBody['appType'] == ServerEnum.APP_CUSTOMER):
            return customer_views.updateCustomerRegsitrationProfile(requestBody)

        # Changing profile from his Account Tab.
        if (requestBody['updateType'] == ServerEnum.PROFILE_USER_DETAILS_UPDATE):
            userId = requestBody['userId']
            appType = requestBody['appType']
            userDetails = requestBody['userDetails']

            userTableName = appType.lower() + "_user_table"

            util.executesql(query="UPDATE " + userTableName + " SET "
                                                              "userDetails = %s "
                                                              "WHERE userId = %s",
                            datatuple=[userDetails, userId])

            return JsonResponse({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })

    except Exception as e:
        print("ERROR IN updateProfile() method in user/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()



def getSuperAdminEmailList():
    emailList = []
    superAdminsDatabaseResult = util.executesql(query="SELECT userEmail FROM admin_user_table "
                                                      "WHERE userType = %s",
                                                datatuple=[ServerEnum.USER_SUPER_ADMIN])
    
    for emailResult in superAdminsDatabaseResult:
        emailList.append(emailResult[0])

    return emailList




@csrf_exempt
def getDatabaseTableList(request):
    try:
        result = util.executesql(query="SHOW TABLES", datatuple=[])
        table_list = []

        for i in range(0, len(result)):
            table_list.append(result[i][0])

        return JsonResponse({
            'tables': json.dumps(table_list),
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN getDatabaseTableList() method in user/views.py")
        print(e)
        return JsonResponse({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


@csrf_exempt
def server(request):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT count(*)  FROM airports")
        result = cursor.fetchall()
        connection.close()

        redisCheck = cache.keys('*')

        if result and len(redisCheck) >= 0:
            return JsonResponse({
                'databaseMessage': "DATABASE RUNNING",
                'redisMessage': redisCheck,
                'message': "SERVER RUNNING",
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })

        return JsonResponse({
            'databaseMessage': "DATABASE STOPPED",
            'redisMessage': "REDIS STOPPED",
            'message': "SERVER RUNNING",
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        return JsonResponse({
            'databaseMessage': "DATABASE STOPPED",
            'redisMessage': "REDIS STOPPED",
            'message': "SERVER STOPPED",
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_CONNECTION_ERROR
        })

@csrf_exempt
def loadTestServer(request):
    try:
        key = "load_test_server" 
        data = json.dumps({"Latiude": "59.99", "Longitude": "61.88"})

        cache.set(key, data, timeout=302400)
        fetchedData = cache.get(key)

        return JsonResponse({
            'data': json.loads(fetchedData),
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN loadTestServer() method in user/views.py")
        print(e)
        return JsonResponse({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_CONNECTION_ERROR
        })

@csrf_exempt
def testCall(request):
    value = cache.keys('*')
    return JsonResponse({
        'data': len(value),
        'data': value,
        'status': True,
        'responseMessage': ServerEnum.RESPONSE_SUCCESS
    })
