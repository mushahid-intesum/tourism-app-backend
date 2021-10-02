import json
import random
from datetime import datetime, timezone, timedelta
import time
from django.db import connection
from django.http import JsonResponse

from django.conf import settings
from pyfcm import FCMNotification
import uuid
import ast

from models.constants import ServerEnum

fcm_push_service = FCMNotification(
    api_key="AAAAzrb5XPc:APA91bG1D8ZXdtBs2Z37s-SHTU33mudnXnw34bXGYmXwU8oeFqPZxEZTgsA7r3FLEMrkeV7UBGh3PTXX3yG4cW90jS54fgbRBQr12UohehJDTQKi_4YXrpqmxk4kRAFrmnhSWb_OYlhh")


def getClientIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return str(ip)


def sendConnectionErrorResponse():
    return JsonResponse({
            'status': False,
            'responseMessage': ServerEnum.RESPONSE_CONNECTION_ERROR
        })


def sendDatabaseConnectionErrorResponse():
    return JsonResponse({
        'status': False,
        'responseMessage': ServerEnum.RESPONSE_DATABASE_CONNECTION_ERROR
    })

def decodeJson(requestBody):
    bodyUnicode = requestBody.decode('utf-8')
    body = json.loads(bodyUnicode)
    return body


def naValue(data):
    if data:
        return data
    return "N/A"

def checkKey(key, jsonData):
    if key in jsonData:
        return jsonData[key]
    return None


def getObjectFromBinaryDecode(VALUE):
    if VALUE is not None:
        return ast.literal_eval(VALUE.decode())
    else:
        return None


def generateID(prefix):
    uuID = prefix + "_" + str(uuid.uuid4())
    randomUUID = uuID.replace('-', '_')
    return randomUUID


def generateSecurityPin():
    number = random.randint(100000, 999999)
    return number


def convertCurrentLocalTimeToUTCTimestamp(timeDelta):
    timeDeltaHour = int(timeDelta.split(":")[0])
    timeDeltaMinute = int(timeDelta.split(":")[1])
    current_time = datetime.now(timezone.utc)
    current_local_time_in_utc = current_time + timedelta(hours=timeDeltaHour) + timedelta(hours=timeDeltaMinute)
    current_local_time_in_utc_timestamp = int(current_local_time_in_utc.timestamp())

    return current_local_time_in_utc_timestamp


def convertTo12HourFormatTime(time):
    return datetime.fromtimestamp(time, tz=timezone.utc).strftime('%Y-%m-%d %I:%M %p')


def utcTimeStamp():
    from datetime import timezone
    import datetime

    dt = datetime.datetime.now()

    utc_time = dt.replace(tzinfo = timezone.utc)
    utc_timestamp = utc_time.timestamp()

    return int(utc_timestamp)



def executesql(query, datatuple):
    cursor = getdbconection()
    cursor.execute(query, datatuple)
    databaseResult = cursor.fetchall()
    cursor.close()
    return databaseResult


def getdbconection():
    return connection.cursor()


def getshortId(bigId):
    if bigId == None:
        return "N/A"
    return bigId.split("_")[1].upper()

