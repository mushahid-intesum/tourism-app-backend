#
# def drop_shard_table():
#     try:
#         for shard_number in range(0, ShardInfo.BOOK_VALET_ARCHIVE_SHARD):
#             table_name = "BOOK_VALET_ARCHIVE_" + \
#                          str(ShardInfo.BOOK_VALET_ARCHIVE_START_ID + shard_number)
#             sqlQuery = "DROP TABLE " + table_name
#             cursor = connection.cursor()
#             cursor.execute(sqlQuery)
#
#         cursor.close()
#         return JsonResponse({
#             'STATUS': True,
#             'RESPONSE_MESSAGE': ServerEnum.RESPONSE_SUCCESS
#         })
#     except Exception as e:
#         return JsonResponse({
#             'STATUS': False,
#             'RESPONSE_MESSAGE': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })
#
#
# def alter_table():
#     try:
#         sqlQuery = "ALTER TABLE USER_TABLE ADD CONTACT_NUMBER varchar(255) NOT NULL";
#
#         cursor = connection.cursor()
#         cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'STATUS': True,
#             'RESPONSE_MESSAGE': ServerEnum.RESPONSE_SUCCESS
#         })
#     except:
#         print("Something went wrong")
#         return JsonResponse({
#             'STATUS': False,
#             'RESPONSE_MESSAGE': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })
#

# @staticmethod
# def fromJson(stringData):
#     jsonData = json.loads(stringData)
#     return AuthCredential(
#         userId=jsonData['USER_ID'],
#         jwtToken=jsonData['JWT_TOKEN'],
#         createdTime=jsonData['CREATED_TIME']
#     )


# @staticmethod
# def toJsonBlob(bookingId, customerId, airportId, journeyTime, bookingDetails):
#     return json.dumps(BookingData(
#         bookingId, customerId, airportId, journeyTime, bookingDetails).__dict__).encode('utf-8')
#
#
# @staticmethod
# def fromJson(stringData):
#     jsonData = json.loads(stringData)
#     return BookingData(
#         bookingId=jsonData['BOOKING_ID'],
#         customerId=jsonData['CUSTOMER_ID'],
#         airportId=jsonData['AIRPORT_ID'],
#         journeyTime=jsonData['JOURNEY_TIME'],
#         bookingDetails=jsonData['BOOKING_DETAILS']
#     )

#
# @staticmethod
# def fromJson(stringData):
#     jsonData = json.loads(stringData)
#     return BookingDetails(
#         airportInfo=jsonData['AIRPORT_INFO'],
#         customerName=jsonData['CUSTOMER_NAME'],
#         customerPhone=jsonData['CUSTOMER_PHONE'],
#         valetName=jsonData['VALET_NAME'],
#         valetPhone=jsonData['VALET_PHONE']
#     )

#
# @staticmethod
# def fromJson(stringData):
#     jsonData = json.loads(stringData)
#     return User(
#         userId=jsonData['USER_ID'],
#         userName=jsonData['USER_NAME'],
#         userType=jsonData['USER_TYPE'],
#         signInType=jsonData['SIGNIN_TYPE']
#     )
#
# def create_bookValetArchive_table():
#     try:
#         for shard_number in range(0, ShardInfo.BOOK_VALET_ARCHIVE_SHARD):
#             table_name = "BOOK_VALET_ARCHIVE_" + str(ShardInfo.BOOK_VALET_ARCHIVE_START_ID + shard_number)
#             sqlQuery = "CREATE TABLE IF NOT EXISTS " \
#                        + table_name + "(" \
#                                       "BOOKING_ID BIGINT NOT NULL," \
#                                       "CUSTOMER_ID BIGINT NOT NULL, " \
#                                       "VALET_ID BIGINT," \
#                                       "AIRPORT_ID BIGINT NOT NULL," \
#                                       "BOOKING_TIME BIGINT NOT NULL," \
#                                       "JOURNEY_TIME BIGINT NOT NULL," \
#                                       "VALET_MATCHED INT NOT NULL DEFAULT 0," \
#                                       "BOOKING_CANCELLED INT NOT NULL DEFAULT 0," \
#                                       "BOOKING_CHARGE INT," \
#                                       "FINAL_CHARGE INT," \
#                                       "DISCOUNT_ID VARCHAR(250)," \
#                                       "BOOKING_DETAILS MEDIUMBLOB," \
#                                       "PRIMARY KEY (BOOKING_ID)) " \
#                                       "Engine = Innodb DEFAULT CHARSET=utf8;"
#
#             cursor = connection.cursor()
#             cursor.execute(sqlQuery)
#         cursor.close()
#         return JsonResponse({
#             'STATUS': True,
#             'RESPONSE_MESSAGE': ServerEnum.RESPONSE_SUCCESS
#         })
#     except Exception as e:
#         print(e)
#         return JsonResponse({
#             'STATUS': False,
#             'RESPONSE_MESSAGE': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })


# URL SYSTEM
# path('track_order_details/<trackID>', user.views.track_order_details, name="track_order_details"),


#
#
# def sendUserAndValetData(airportId, userId):
#     authCredential = util.encodeToJWT(userId)
#
#     userDatabaseResult = checkUserIdAndGetData(userId)
#     user = User.toJsonStringFromDatabase(userDatabaseResult)
#
#     valetDatabaseResult = checkValetIdAndGetValetAirportData(airportId, userId)
#     valet = Valet.toJsonStringFromDatabase(valetDatabaseResult)
#
#     return JsonResponse({
#         'AUTH_CREDENTIAL': authCredential,
#         'USER': user,
#         'VALET': valet,
#         'STATUS': True,
#         'RESPONSE_MESSAGE': ServerEnum.RESPONSE_SUCCESS
#     })



#
#
# def checkUserIdAndGetData(userId):
#     try:
#         cursor = connection.cursor()
#         cursor.execute("SELECT USER_ID, USER_EMAIL, USER_NAME, USER_PHONE,"
#                        "USER_TYPE, SIGNIN_TYPE, USER_DETAILS"
#                        " FROM USER_TABLE WHERE USER_ID = %s LIMIT 1", [userId])
#         databaseResult = cursor.fetchall()
#         cursor.close()
#         return databaseResult
#
#     except Exception as e:
#         print(e)
#         return JsonResponse({
#             'STATUS': False,
#             'RESPONSE_MESSAGE': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })
#

#
# # UserValetDetails is for USER_DETAILS blob in VALET_USER_TABLE
# class UserValetDetails:
#     def __init__(self, valetAirportId=None, ):
#         # These variables will act as Json 'key'
#         self.VALET_AIRPORT_ID = valetAirportId
#
#
#     @staticmethod
#     def fromJson(stringData):
#         # For the first time login, Valet details will be empty.
#         if(stringData is None):
#             return None
#         else:
#             jsonData = json.loads(stringData)
#             return UserValetDetails(
#                 valetAirportId=jsonData['VALET_AIRPORT_ID']
#             )
#
#




#
# @csrf_exempt
# def getAdminBasedAirportData(request):
#     try:
#
#         requestBody = util.decodeJson(request.body)
#
#         adminAirportAllowedIDList = requestBody['AIRPORT_LIST']
#         adminAirportAllowedIDListJson = json.loads(adminAirportAllowedIDList)
#
#         adminAirportDataList = []
#
#         for i in range(0, len(adminAirportAllowedIDListJson)):
#             airportId = adminAirportAllowedIDListJson[i].split(";")[1]
#
#             cursor = connection.cursor()
#             cursor.execute(
#                 "SELECT AIRPORT_ID, AIRPORT_NAME, AIRPORT_COUNTRY, "
#                 "AIRPORT_ACTIVE_STATUS, AIRPORT_FEE, VALET_FEE_PERCENTAGE, AIRPORT_DETAILS "
#                 "FROM AIRPORTS WHERE AIRPORT_ID = %s", [airportId])
#             databaseResult = cursor.fetchall()
#             connection.close()
#
#             airportData = Airport.toJsonStringFromDatabase(databaseResult)
#             adminAirportDataList.append(airportData)
#
#         return JsonResponse({
#             'AIRPORT_DATA_LIST': adminAirportDataList,
#             'STATUS': True,
#             'RESPONSE_MESSAGE': ServerEnum.RESPONSE_SUCCESS
#         })
#
#
#     except Exception as e:
#         print("ERROR IN getAdminBasedAirportData() method in admin/views.py")
#         print(e)
#         return JsonResponse({
#             'STATUS': False,
#             'RESPONSE_MESSAGE': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
#         })
#
#
#
#
#

































