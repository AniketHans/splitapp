from sqlalchemy.orm import Session
from app.service.user_activity_association import UserActivityAssociationService
from app.model.splitapp import getDB, ActivityModel,UserActivityAssociationModel
from app.resource.splitapp import Activity,ActivityUser,User
from app.dao.splitapp import SplitAppDAO
import time
from datetime import datetime


class ActivityService(UserActivityAssociationService):
    def __init__(self):
        self.session= getDB()
    
    def GetAllActivities(self):
        appDao=SplitAppDAO(self.session)
        try:
            activities=appDao.getAllActivities()
            allActivities=[]
            for activityData in activities:
                activity = Activity(
                    activity_id=activityData.activity_id,
                    activity_name=appDao.activityInfoByActivityID(activityData.activity_id).activity_name,
                    total_amount=activityData.total_amount,
                    total_contributors=activityData.total_contributors,
                    created_by=User(
                        user_id=activityData.created_by,
                        user_name=appDao.userInfoByUserID(activityData.created_by).user_name
                    ),
                    created_at=datetime.utcfromtimestamp(activityData.created_at).strftime('%Y-%m-%d %H:%M:%S')
                )
                allActivities.append(activity.dict(exclude_none=True))
            return allActivities
        except Exception as err:
            print(err)
            raise Exception(err)
    
    def CreateActivity(self,user_id:int,activity:Activity):
        appDao=SplitAppDAO(self.session)
        
        try:
            userInfo=appDao.userInfoByUserID(user_id)
            if userInfo==None:
                raise ValueError({"message":"User Not present"})
            
            activityModel=ActivityModel()
            activityModel.activity_name=activity.activity_name
            activityModel.created_by=user_id
            activityModel.created_at=int(time.time())
            activityModel.total_amount=activity.total_amount

            totalMembers=1

            if activity.users!=None:
                totalMembers+=len(activity.users)
                amount=activityModel.total_amount/totalMembers
                for user in activity.users:
                    self.addUserToActivityWhileCreation(activity,user,amount)
            activityModel.total_contributors=totalMembers
            appDao.createActivity(activityModel)
        
            #Association
            userActivtyAssociation=UserActivityAssociationModel()
            userActivtyAssociation.user_id=user_id
            userActivtyAssociation.activity_id=activityModel.activity_id
            userActivtyAssociation.paid_amount=activityModel.total_amount

            appDao.userAddToActivity(userActivtyAssociation)
            self.session.commit()
            return {"message":"Activity Created Succesfully","status_code":200}
        except Exception as err:
            print(err)
            raise Exception(err)

    
    def GetActivity(self,activity_id:int):
        appDao=SplitAppDAO(self.session)

        try:
            activityData=appDao.activityInfoByActivityID(activity_id)

            activityUsers=self.getUsersFromActivityByActivityID(activity_id)
            print(activityUsers)
            
            body= Activity(
                activity_id=activityData.activity_id,
                activity_name=appDao.activityInfoByActivityID(activityData.activity_id).activity_name,
                total_amount=activityData.total_amount,
                total_contributors=activityData.total_contributors,
                created_by=User(
                    user_id=activityData.created_by,
                    user_name=appDao.userInfoByUserID(activityData.created_by).user_name
                ),
                created_at=datetime.utcfromtimestamp(activityData.created_at).strftime('%Y-%m-%d %H:%M:%S'),
                users=activityUsers
            )

            return body.dict(exclude_none=True)
        except Exception as err:
            print(err)
            raise Exception(err)



    def AddUserToActivity(self,activity_id:int,userData:ActivityUser):
        appDao=SplitAppDAO(self.session)

        try:
            userdata=appDao.userInfoByUserID(userData.user_id)
            if userdata==None:
                return {"message":"User does not exist.","status_code":400}
            
            self.addUserToActivity(activity_id,userData)
            self.session.commit()
            return {"message":"User Added Succesfully","status_code":200}
        except Exception as err:
            print(err)
            raise Exception(err)



        






    





        
