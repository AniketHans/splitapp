from sqlalchemy.orm import Session
from app.model.splitapp import getDB, UserActivityAssociationModel
from app.resource.splitapp import User,UserActivity,Activity,ActivityUser
from app.dao.splitapp import SplitAppDAO
import time
from typing import List



class UserActivityAssociationService():
    def __init__(self,session:Session):
        self.session=session()
    
    def addUserToActivityWhileCreation(self,activityData:Activity,activityUser:ActivityUser,amount:int):

        appDao=SplitAppDAO(self.session)
        try:
            userActivityAssociation=UserActivityAssociationModel()
            userActivityAssociation.activity_id=activityData.activity_id
            userActivityAssociation.user_id=activityUser.user_id
            userActivityAssociation.to_be_paid_amount=amount

            appDao.userAddToActivity(userActivityAssociation)
        except Exception as err:
            raise Exception(err)

    
    def getUsersFromActivityByActivityID(self,activityID:int) -> List[ActivityUser]:
        appDao=SplitAppDAO(self.session)
        try:
            usersAndActivities = appDao.userActivityAssociationByActivityID(activityID)

            activityUsers=[]
            for userandactivity in usersAndActivities:
                activityUser=ActivityUser(
                    user_id=userandactivity.user_id,
                    user_name= appDao.userInfoByUserID(userandactivity.user_id).user_name,
                    to_be_paid_amount=float(userandactivity.to_be_paid_amount),
                    paid_amount=float(userandactivity.paid_amount)
                )
                if userandactivity.to_be_paid_amount <=userandactivity.paid_amount:
                    activityUser.lend_amount=float(userandactivity.paid_amount-userandactivity.to_be_paid_amount)
                
                activityUsers.append(activityUser)
            return activityUsers
        except Exception as err:
            raise Exception(err)

    def _addExpenseToUsers(self,activityId:int,paidAmount:float,userAdded:bool) -> float:
        appDao=SplitAppDAO(self.session)
        try:
            activityData=appDao.activityInfoByActivityID(activityId)
            activityData.total_amount=float(activityData.total_amount)+paidAmount
            if userAdded:
                activityData.total_contributors+=1

            newAmountForEachUser=(paidAmount)/(activityData.total_contributors)
            
            #Update Existing amount for exsting users
            usersandactivities =appDao.userActivityAssociationByActivityID(activityId)
            for userandactivity in usersandactivities:
                userandactivity.to_be_paid_amount=float(userandactivity.to_be_paid_amount)+newAmountForEachUser
            return newAmountForEachUser
        except Exception as err:
            raise Exception(err)


    
    def addUserToActivity(self,activityId:int,activityUser:ActivityUser):

        appDao=SplitAppDAO(self.session)
        try:
            activityData=appDao.activityInfoByActivityID(activityId)
            
            newAmountForEachUser=self._addExpenseToUsers(activityId,activityUser.paid_amount,userAdded=True)
            #Adding new menber
            userActivityAssociation=UserActivityAssociationModel()
            userActivityAssociation.activity_id=activityData.activity_id
            userActivityAssociation.user_id=activityUser.user_id
            userActivityAssociation.to_be_paid_amount=newAmountForEachUser
            userActivityAssociation.paid_amount=activityUser.paid_amount
            appDao.userAddToActivity(userActivityAssociation)
        except Exception as err:
            raise Exception(err)


    def updateAmountInActivity(self,activity_id:int,amount:int):
        
        appDao=SplitAppDAO(self.session)
        try:
        
            userActivityAssociations=appDao.userActivityAssociationByActivityID(activity_id)
            for userActivityAssociation in userActivityAssociations:
                userActivityAssociation.to_be_paid_amount=amount
        except Exception as err:
            raise Exception(err)
    


        

    


        