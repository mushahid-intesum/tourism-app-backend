import json
from general import util


class User:
    def __init__(self, userId, userEmail, userPassword, createdTime, firstName, secondName):
        # These variables will act as Json Name entities
        self.userId = userId
        self.userEmail = userEmail
        self.userPassword = userPassword
        self.createdTime = createdTime
        self.firstName = firstName
        self.secondName = secondName

    @staticmethod
    def toJsonMapFromDatabase(databaseResult):
        userId = databaseResult[0][0]
        userEmail = databaseResult[0][1]
        userPassword = databaseResult[0][2]
        createdTime = databaseResult[0][3]
        firstName = databaseResult[0][4]
        secondName = databaseResult[0][5]
        return User(userId, userEmail, userPassword, createdTime, firstName, secondName).__dict__

