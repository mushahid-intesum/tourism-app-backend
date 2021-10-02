# import json
# import time
# from django.contrib.auth.hashers import make_password
# from general import util
# from models.constants import ServerEnum
# import pyrebase
# import os
# from django.core.cache import cache
# from django.http import JsonResponse


# def database_commit(request):
#     # return JsonResponse({
#     #     'status': True,
#     #     'responseMessage': "NO DATABASE COMMIT AVAILABLE"
#     # })
#     drop_table(tableList=getAllTableName(),
#                exceptionList=[
#                    'information',
#                    # 'customer_user_table', 'airports',
#                    # 'discount_user_table', 'trips', 'car_trips',
#                    # 'book_valet', 'valet_user_table', 'payment_transaction',
#                    # 'admin_user_table', 'car_companies', 'discount_table'
#                ])

#     create_customer_table()
#     create_valet_table()
#     create_admin_table()
#     create_bookValet_table()
#     create_airport_table()
#     create_trip_table()
#     create_car_trip_table()
#     create_information_table()
#     create_payment_transaction_table()
#     create_discount_table()
#     create_discount_user_table()
#     add_dummy_admin()
#     create_car_company_table()
#     return JsonResponse({
#         'status': True,
#         'responseMessage': "DATABASE COMMIT SUCCESS"
#     })


# def add_super_admin():
#     superAdminId = util.generateID("SUPER_ADMIN")
#     email = ServerEnum.MASTER_ADMIN_EMAIL
#     password = make_password(ServerEnum.MASTER_ADMIN_PASS)
#     phone = "+880123456789"
#     userType = ServerEnum.APP_SUPER_ADMIN
#     userDetails = {'USER_NAME': 'ezeeDrop'}
#     registrationTime = util.utcTimeStamp()
#     activeStatus = 1
#     emailVerified = 1
#     airportList = ['ALL']

#     util.executesql(query="INSERT INTO admin_user_table "
#                           "(userId, userEmail, userPassword, userPhone, userType, userDetails, "
#                           "createdTime, activeStatus, emailVerified, signInType, airportList)"
#                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                     datatuple=[superAdminId, email, password, phone, userType, userDetails,
#                                registrationTime, activeStatus, emailVerified,
#                                ServerEnum.SIGNIN_EMAIL_PASS, str(airportList)])


# def add_dummy_admin():
#     superAdminId = util.generateID("SUPER_ADMIN")
#     email = 'ezeedropmasteradmin@admin.com'
#     password = make_password('123123')
#     phone = "+880123456789"
#     userType = ServerEnum.APP_SUPER_ADMIN
#     userDetails = {'USER_NAME': 'ezeeDrop'}
#     registrationTime = util.utcTimeStamp()
#     activeStatus = 1
#     emailVerified = 1
#     airportList = ['ALL']

#     util.executesql(query="INSERT INTO admin_user_table "
#                           "(userId, userEmail, userPassword, userPhone, userType, userDetails, "
#                           "createdTime, activeStatus, emailVerified, signInType, airportList)"
#                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                     datatuple=[superAdminId, email, password, phone, userType, userDetails,
#                                registrationTime, activeStatus, emailVerified,
#                                ServerEnum.SIGNIN_EMAIL_PASS, str(airportList)])


# def create_customer_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS customer_user_table (" \
#                    "userId VARCHAR(250) NOT NULL," \
#                    "userEmail VARCHAR(250)," \
#                    "userPassword VARCHAR(250)," \
#                    "userPhone VARCHAR(250)," \
#                    "createdTime BIGINT NOT NULL," \
#                    "deleteStatus INT NOT NULL DEFAULT 0," \
#                    "activeStatus INT NOT NULL DEFAULT 1," \
#                    "emailVerified INT NOT NULL DEFAULT 0," \
#                    "phoneVerified INT NOT NULL DEFAULT 0," \
#                    "userType ENUM('SUPER_ADMIN','ADMIN','CUSTOMER','VALET')," \
#                    "signInType ENUM('EMAIL_PASS','PHONE','GOOGLE','APPLE') NOT NULL," \
#                    "userDetails MEDIUMBLOB," \
#                    "PRIMARY KEY (userId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_customer_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })

# def create_admin_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS admin_user_table (" \
#                    "userId VARCHAR(250) NOT NULL," \
#                    "userEmail VARCHAR(250)," \
#                    "userPassword VARCHAR(250)," \
#                    "userPhone VARCHAR(250)," \
#                    "createdTime BIGINT NOT NULL," \
#                    "deleteStatus INT NOT NULL DEFAULT 0," \
#                    "activeStatus INT NOT NULL DEFAULT 1," \
#                    "emailVerified INT NOT NULL DEFAULT 0," \
#                    "phoneVerified INT NOT NULL DEFAULT 0," \
#                    "userType ENUM('SUPER_ADMIN','ADMIN')," \
#                    "signInType ENUM('EMAIL_PASS','PHONE') NOT NULL," \
#                    "airportList MEDIUMBLOB," \
#                    "userDetails MEDIUMBLOB," \
#                    "PRIMARY KEY (userId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_admin_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def create_airport_valet_table(airportId):
#     try:
#         tableName = "valet_" + str(airportId).lower()
#         sqlQuery = "CREATE TABLE IF NOT EXISTS " + \
#                    tableName + \
#                    "(" \
#                    "valetId VARCHAR(250) NOT NULL," \
#                    "valetUserId VARCHAR(250) NOT NULL," \
#                    "valetAccountStatus INT NOT NULL DEFAULT 1," \
#                    "adminAuthorityOnValet ENUM('ALLOWED', 'BLOCKED', 'PENALIZED', 'AIRPORT_STATUTS_ACTIVE', 'AIRPORT_STATUTS_INACTIVE') DEFAULT 'BLOCKED', " \
#                    "valetStatus ENUM('INACTIVE', 'ACTIVE') DEFAULT 'INACTIVE', " \
#                    "valetTripStatus ENUM('STARTED_MONITORING_CUSTOMER','RECIEVED_CAR','ON_WAY_TO_DROP_CAR','DROPPED_OFF_CAR','ON_WAY_TO_AIRPORT','CANCEL_TRIP') DEFAULT NULL, " \
#                    "valetRating DOUBLE PRECISION DEFAULT 0," \
#                    "valetTotalRateProviders INT DEFAULT 0," \
#                    "valetTripTimes MEDIUMBLOB," \
#                    "valetDetails MEDIUMBLOB," \
#                    "PRIMARY KEY (valetId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_airport_valet_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def create_bookValet_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS book_valet (" \
#                    "bookingId VARCHAR(250) NOT NULL," \
#                    "customerId VARCHAR(250) NOT NULL, " \
#                    "valetId VARCHAR(250)," \
#                    "airportId VARCHAR(250) NOT NULL," \
#                    "bookingTime BIGINT NOT NULL," \
#                    "journeyTime BIGINT NOT NULL," \
#                    "valetMatched INT NOT NULL DEFAULT 0," \
#                    "bookingPriority ENUM('HIGH','MODERATE','NORMAL') NOT NULL DEFAULT 'NORMAL'," \
#                    "bookingStatus ENUM('COMPLETED','ONGOING_TRIP','CANCELLED','NOT_STARTED') NOT NULL DEFAULT 'NOT_STARTED'," \
#                    "bookingReport MEDIUMBLOB," \
#                    "customerBookingRating MEDIUMBLOB," \
#                    "bookingValetList MEDIUMBLOB," \
#                    "paymentDetails MEDIUMBLOB," \
#                    "paymentStatusToValet ENUM('PAID','UNPAID') NOT NULL DEFAULT 'UNPAID'," \
#                    "carDetails MEDIUMBLOB," \
#                    "carImageDetails LONGBLOB," \
#                    "carImageUploaded ENUM('YES','NO') NOT NULL DEFAULT 'NO'," \
#                    "carReceiptUploaded ENUM('YES','NO') NOT NULL DEFAULT 'NO'," \
#                    "bookingDetails MEDIUMBLOB," \
#                    "PRIMARY KEY (bookingId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         # BOOKING_VALET_LIST will be enabled later whom we send request.
#         # We will have two or three list saved as BLOB.
#         # First List will have the highest rated Valet who are ACTIVE
#         # Second List will have the mid rated Valet who are Active
#         # Third List will have rest of the Valet who are booked

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_bookValet_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def create_airport_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS airports (" \
#                    "airportId VARCHAR(250) NOT NULL," \
#                    "airportName VARCHAR(250) NOT NULL, " \
#                    "airportCountry VARCHAR(250) NOT NULL, " \
#                    "airportActiveStatus INT NOT NULL DEFAULT 0," \
#                    "airportFee DOUBLE PRECISION DEFAULT 0," \
#                    "valetFeePercentage DOUBLE PRECISION DEFAULT 100," \
#                    "consecutiveBookingStopTimeValet INT NOT NULL DEFAULT 30," \
#                    "bookingViewTimeValet INT NOT NULL DEFAULT 360," \
#                    "bookValetTimeCustomer INT NOT NULL DEFAULT 360," \
#                    "autoCancellationTime INT NOT NULL DEFAULT 30," \
#                    "airportTerminalList MEDIUMBLOB," \
#                    "airportRentalCarTerminalList MEDIUMBLOB," \
#                    "airportDetails LONGBLOB," \
#                    "PRIMARY KEY (airportId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_airport_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def create_trip_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS trips (" \
#                    "tripId VARCHAR(250) NOT NULL," \
#                    "bookingId VARCHAR(250) NOT NULL," \
#                    "customerId VARCHAR(250) NOT NULL," \
#                    "valetId VARCHAR(250) NOT NULL," \
#                    "customerLocationDetails MEDIUMBLOB," \
#                    "valetLocationDetails MEDIUMBLOB," \
#                    "tripStatus ENUM('COMPLETED', 'ONGOING', 'CANCELLED') DEFAULT 'ONGOING', " \
#                    "customerJourneyStarted ENUM('YES', 'NO') DEFAULT 'YES', " \
#                    "valetJourneyStarted ENUM('YES', 'NO') DEFAULT 'NO', " \
#                    "customerJourneyEnded ENUM('YES', 'NO') DEFAULT 'NO', " \
#                    "valetJourneyEnded ENUM('YES', 'NO') DEFAULT 'NO', " \
#                    "journeyTime BIGINT NOT NULL," \
#                    "tripReport MEDIUMBLOB," \
#                    "tripDetails MEDIUMBLOB," \
#                    "PRIMARY KEY (tripId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })
#     except Exception as e:
#         print("ERROR IN create_trip_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def create_car_trip_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS car_trips (" \
#                    "carTripId VARCHAR(250) NOT NULL," \
#                    "bookingId VARCHAR(250) NOT NULL, " \
#                    "valetId VARCHAR(250) NOT NULL, " \
#                    "tripId VARCHAR(250) NOT NULL, " \
#                    "customerFirebasePushToken VARCHAR(250) NOT NULL, " \
#                    "carTripStatus ENUM('COMPLETED', 'ONGOING') DEFAULT 'ONGOING', " \
#                    "carJourneyStartTime BIGINT," \
#                    "carJourneyEndTime BIGINT," \
#                    "carDetails MEDIUMBLOB," \
#                    "PRIMARY KEY (carTripId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_car_trip_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def create_discount_table():
#     try:
#         # TODO: add showDiscountToCustomer column
#         sqlQuery = "CREATE TABLE IF NOT EXISTS discount_table (" \
#                    "discountId VARCHAR(250) NOT NULL," \
#                    "discountCode VARCHAR(250)," \
#                    "discountText VARCHAR(250)," \
#                    "discountAmount DOUBLE PRECISION NOT NULL," \
#                    "discountsApplicableOn ENUM('CUSTOMERS','AIRPORTS') DEFAULT 'AIRPORTS', " \
#                    "discountCustomerPhone MEDIUMBLOB, " \
#                    "discountAmountReceiveType ENUM('INSTANT_AMOUNT','PERCENTAGE','CASH_BACK') DEFAULT 'PERCENTAGE'," \
#                    "discountMethodType ENUM('VOUCHER_CODE','VISA_CARD','MASTER_CARD','AMERICAN_EXPRESS') DEFAULT 'VOUCHER_CODE'," \
#                    "discountStartTime BIGINT," \
#                    "discountEndTime BIGINT," \
#                    "maxDiscountAmountApplied DOUBLE PRECISION," \
#                    "maxTimeApplicableDiscount INT DEFAULT 10," \
#                    "discountActive ENUM('YES','NO') DEFAULT 'YES'," \
#                    "applicableDiscountUserList MEDIUMBLOB," \
#                    "applicableDiscountAirportList MEDIUMBLOB," \
#                    "showDiscountToCustomer BOOLEAN, " \
#                    "description VARCHAR(250)," \
#                    "PRIMARY KEY (discountId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_discount_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def create_discount_user_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS discount_user_table (" \
#                    "customerId VARCHAR(250) NOT NULL," \
#                    "discountId VARCHAR(250)," \
#                    "lastDiscountUsedTime BIGINT," \
#                    "totalDiscountUsed INT DEFAULT 0) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_discount_user_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# # This table stores data that are to be Handled via scheduler
# def create_removal_execution_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS REMOVAL_EXECUTION_TABLE (" \
#                    "REMOVAL_ID VARCHAR(250) NOT NULL," \
#                    "EXECUTION_TYPE ENUM('CAR_JOURNEY','PAYMENT_TRANSACTION')," \
#                    "START_TIME BIGINT," \
#                    "REMOVE_AT_TIME BIGINT," \
#                    "INFO MEDIUMBLOB," \
#                    "PRIMARY KEY (REMOVAL_ID)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_discount_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def create_payment_transaction_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS payment_transaction (" \
#                    "transactionId VARCHAR(250) NOT NULL," \
#                    "airportId VARCHAR(250) NOT NULL, " \
#                    "valetId VARCHAR(250) NOT NULL, " \
#                    "paymentAmount DOUBLE PRECISION NOT NULL," \
#                    "paymentTime VARCHAR(250) NOT NULL," \
#                    "bookingDetails MEDIUMBLOB," \
#                    "paymentDetails MEDIUMBLOB," \
#                    "PRIMARY KEY (transactionId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN payment_transaction_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def create_information_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS information (" \
#                    "INFO_NAME VARCHAR(250) NOT NULL, " \
#                    "MAIN_INFO MEDIUMBLOB NOT NULL, " \
#                    "PRIMARY KEY (INFO_NAME)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_car_trip_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# # Written by Mushahid
# def create_car_company_table():
#     try:
#         sqlQuery = "CREATE TABLE IF NOT EXISTS car_companies (" \
#                    "carCompanyId VARCHAR(250) NOT NULL, " \
#                    "carCompanyName VARCHAR(250) NOT NULL, " \
#                    "country VARCHAR(250) NOT NULL, " \
#                    "carCompanyDetails MEDIUMBLOB, " \
#                    "deleteStatus ENUM('YES', 'NO') DEFAULT 'NO', " \
#                    "PRIMARY KEY (carCompanyId)) " \
#                    "Engine = Innodb DEFAULT CHARSET=utf8;"

#         cursor = util.getdbconection()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN create_car_trip_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# # # # --------------------------------------------------------------------- # # #

# def drop_table(tableList, exceptionList):
#     try:
#         for tableName in tableList:
#             if tableName not in exceptionList:
#                 util.executesql(query="DROP TABLE " + tableName, datatuple=[])

#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })
#     except Exception as e:
#         print("ERROR IN drop_table() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def getAllTableName():
#     try:
#         result = util.executesql(query="SHOW TABLES", datatuple=[])
#         table_list = []

#         for i in range(0, len(result)):
#             table_list.append(result[i][0])

#         return table_list

#     except Exception as e:
#         print("ERROR IN getAllTableName() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# def clearFirebaseStorage():
#     firebase_folders = ['car/', 'valet/', 'customer/', 'extra/']
#     try:
#         firebaseConfig = {
#             "apiKey": "AIzaSyC4HC8XvJQ8AIYQqJh7fiqEOKCa8mAmgNk",
#             "authDomain": "ezeedrop-c06cd.firebaseapp.com",
#             "databaseURL": "https://ezeedrop-c06cd.firebaseio.com",
#             "projectId": "ezeedrop-c06cd",
#             "storageBucket": "ezeedrop-c06cd.appspot.com",
#             "messagingSenderId": "793853730658",
#             "appId": "1:793853730658:web:f02a77d148a39f35cf163b",
#             "measurementId": "G-YJJT4S9RDJ",
#             "serviceAccount": os.getcwd() + "/jsonfiles/" + "service-admin-firebase-storage.json"
#         }

#         firebase = pyrebase.initialize_app(firebaseConfig)
#         storage = firebase.storage()
#         all_files = storage.list_files()

#         for file in all_files:
#             if (file.name in firebase_folders):
#                 pass
#             else:
#                 firebase.storage().delete(file.name)
#                 # storage.child(file.name).get_url(None) This gets URL

#         return JsonResponse({
#             'status': True,
#             'responseMessage': ServerEnum.RESPONSE_SUCCESS
#         })

#     except Exception as e:
#         print("ERROR IN clearFirebaseStorage() method in database/views.py")
#         print(e)
#         return JsonResponse({
#             'status': False,
#             'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })
