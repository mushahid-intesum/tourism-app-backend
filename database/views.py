import json
import time
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from general import util
from models.constants import ServerEnum
import pyrebase
import os
from django.core.cache import cache
from django.http import JsonResponse



def database_commit(request):
    # return JsonResponse({
    #     'status': True,
    #     'responseMessage': "NO DATABASE COMMIT AVAILABLE"
    # })
    # tableList = ['admin_user_table', 'customer_user_table', 'reviews_table', 'hotels_table']
    # drop_table(tableList)

    # create_customer_table()
    # create_admin_table()
    # add_dummy_admin()
    # create_hotels_table()
    # create_reviews_table()
    return JsonResponse({
        'status': True,
        'responseMessage': "DATABASE COMMIT SUCCESS"
    })

def add_super_admin():
    superAdminId = util.generateID("SUPER_ADMIN")
    email = ServerEnum.MASTER_ADMIN_EMAIL
    password = make_password(ServerEnum.MASTER_ADMIN_PASS)
    firstName = "ooga"
    secondName = "booga"
    registrationTime = util.utcTimeStamp()

    util.executesql(query="INSERT INTO admin_user_table "
        "(userId, userEmail, userPassword,"
        "createdTime, firstName, secondName)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        datatuple=[superAdminId, email, password,
                               registrationTime, firstName, secondName])
                    
def add_dummy_admin():
    superAdminId = util.generateID("SUPER_ADMIN")
    email = 'ezeedropmasteradmin@admin.com'
    password = make_password('123123')
    registrationTime = util.utcTimeStamp()
    firstName = "ooga"
    secondName = "booga"

    util.executesql(query="INSERT INTO admin_user_table "
        "(userId, userEmail, userPassword,"
        "createdTime, firstName, secondName)"
        "VALUES (%s, %s, %s, %s, %s, %s)",
        datatuple=[superAdminId, email, password,
                               registrationTime, firstName, secondName])


def create_customer_table():
    try:
        sqlQuery = "CREATE TABLE IF NOT EXISTS customer_user_table (" \
                   "userId VARCHAR(250) NOT NULL," \
                   "userEmail VARCHAR(250)," \
                   "userPassword VARCHAR(250)," \
                   "createdTime BIGINT NOT NULL," \
                    "firstName VARCHAR(250), " \
                    "secondName VARCHAR(250), " \
                   "PRIMARY KEY (userId)) " 

        cursor = util.getdbconection()
        cursor.execute(sqlQuery)
        cursor.close()
        return JsonResponse({
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN create_customer_table() method in database/views.py")
        print(e)
        return JsonResponse({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })

def create_admin_table():
    try:
        sqlQuery = "CREATE TABLE IF NOT EXISTS admin_user_table (" \
                   "userId VARCHAR(250) NOT NULL," \
                   "userEmail VARCHAR(250)," \
                   "userPassword VARCHAR(250)," \
                   "createdTime BIGINT NOT NULL," \
                    "firstName VARCHAR(250), " \
                    "secondName VARCHAR(250), " \
                   "PRIMARY KEY (userId)) " 

        cursor = util.getdbconection()
        cursor.execute(sqlQuery)
        cursor.close()
        return JsonResponse({
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN create_admin_table() method in database/views.py")
        print(e)
        return JsonResponse({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


def create_hotels_table():
    try:
        sqlQuery = "CREATE TABLE IF NOT EXISTS hotels_table (" \
                   "hotelId VARCHAR(250) NOT NULL," \
                   "hotelName VARCHAR(250)," \
                   "isRecommended INT, " \
                   "hotelDetails MEDIUMBLOB," \
                   "PRIMARY KEY (hotelId)) " 

        cursor = util.getdbconection()
        cursor.execute(sqlQuery)
        cursor.close()
        return JsonResponse({
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN create_customer_table() method in database/views.py")
        print(e)
        return JsonResponse({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })

def create_reviews_table():
    try:
        sqlQuery = "CREATE TABLE IF NOT EXISTS reviews_table (" \
                   "reviewId VARCHAR(250) NOT NULL," \
                   "hotelId VARCHAR(250)," \
                   "reviewBody VARCHAR(250)," \
                   "sentiment BIGINT NOT NULL," \
                    "reviewerName VARCHAR(250),"\
                   "PRIMARY KEY (reviewId)) " 

        cursor = util.getdbconection()
        cursor.execute(sqlQuery)
        cursor.close()
        return JsonResponse({
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN create_customer_table() method in database/views.py")
        print(e)
        return JsonResponse({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })


def getAllTableName():
    try:
        result = util.executesql(query="SHOW TABLES", datatuple=[])
        table_list = []

        print(result)

        for i in range(0, len(result)):
            table_list.append(result[i][0])

        return table_list

    except Exception as e:
        print("ERROR IN getAllTableName() method in database/views.py")
        print(e)
        return JsonResponse({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })

    
def drop_table(tableList):
    try:
        for tableName in tableList:
            util.executesql(query="DROP TABLE " + tableName, datatuple=[])

        return JsonResponse({
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })
    except Exception as e:
        print("ERROR IN drop_table() method in database/views.py")
        print(e)
        return JsonResponse({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
        })
