import json
from general import util


class AdminUser:
    def __init__(self, userId, userEmail, userPassword, userPhone, createdTime,
                 deleteStatus, activeStatus, emailVerified,
                 phoneVerified, userType, signInType, airportList, userDetails):
        # These variables will act as Json Name entities
        self.userId = userId
        self.userEmail = userEmail
        self.userPassword = userPassword
        self.userPhone = userPhone
        self.createdTime = createdTime
        self.deleteStatus = deleteStatus
        self.activeStatus = activeStatus
        self.emailVerified = emailVerified
        self.phoneVerified = phoneVerified
        self.userType = userType
        self.signInType = signInType
        self.airportList = airportList
        self.userDetails = userDetails


    @staticmethod
    def toJsonMapListFromDatabase(databaseResult):
        adminList = []
        for i in range(0, len(databaseResult)):
            userId = databaseResult[i][0]
            userEmail = databaseResult[i][1]
            userPassword = None
            userPhone = databaseResult[i][3]
            createdTime = databaseResult[i][4]
            deleteStatus = databaseResult[i][5]
            activeStatus = databaseResult[i][6]
            emailVerified = databaseResult[i][7]
            phoneVerified = databaseResult[i][8]
            userType = databaseResult[i][9]
            signInType = databaseResult[i][10]
            airportList = util.getObjectFromBinaryDecode(databaseResult[i][11])
            userDetails = util.getObjectFromBinaryDecode(databaseResult[i][12])
            adminList.append(AdminUser(userId, userEmail, userPassword, userPhone, createdTime,
                                       deleteStatus, activeStatus, emailVerified,
                                       phoneVerified, userType, signInType, airportList, userDetails).__dict__)

        return adminList
