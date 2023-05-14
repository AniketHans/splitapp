from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List
from app.model.splitapp import UserModel,UserActivityAssociationModel,ActivityModel

class SplitAppDAO:
    def __init__(self,session:Session):
        self.session=session

    #User

    def createUser(self,userData:UserModel):
        try:
            self.session.add(userData)
        except Exception as e:
            raise Exception(e)
    
    def userInfoByUserID(self,userID:int) -> UserModel:
        try:
            user= self.session.query(UserModel).filter(UserModel.user_id==userID).first()
            return user
        except Exception as e:
            raise Exception(e)
    
    def getAllUsers(self) -> List[UserModel]:
        try:
            user= self.session.query(UserModel).all()
            return user
        except Exception as e:
            raise Exception(e)
    
    
    

    #Activity
    def activityInfoByActivityID(self,activityID:int) -> ActivityModel:
        try:
            activity= self.session.query(ActivityModel).filter(ActivityModel.activity_id==activityID).first()
            return activity
        except Exception as e:
            raise Exception(e)
    
    def createActivity(self,activity:ActivityModel):
        try:
            self.session.add(activity)
            self.session.flush()
        except Exception as e:
            raise Exception(e)
    

    def getAllActivities(self) -> List[ActivityModel]:
        try:
            activities= self.session.query(ActivityModel).all()
            return activities
        except Exception as e:
            raise Exception(e)

    


    #UserAndActivityUser
    def userActivityAssociationByUserID(self,userID:int) -> List[UserActivityAssociationModel]:
        try:
            useractivity= self.session.query(UserActivityAssociationModel).filter(UserActivityAssociationModel.user_id==userID)
            return useractivity
        except Exception as e:
            raise Exception(e)
        
    def userAddToActivity(self,userActivity:UserActivityAssociationModel):
        try:
            self.session.add(userActivity)
        except Exception as e:
            raise Exception(e)
    
    def userActivityAssociationByActivityID(self, activityId:int) -> List[UserActivityAssociationModel]:
        try:
            useractivity= self.session.query(UserActivityAssociationModel).filter(UserActivityAssociationModel.activity_id==activityId)
            return useractivity
        except Exception as e:
            raise Exception(e)
    

    def userActivityAssociationByUserIDAndActivityID(self,userID:int,activity_id:int) -> UserActivityAssociationModel:
        try:
            useractivity= self.session.query(UserActivityAssociationModel).filter(and_(UserActivityAssociationModel.user_id==userID,UserActivityAssociationModel.activity_id==activity_id)).first()
            return useractivity
        except Exception as e:
            raise Exception(e)
    
    
    


