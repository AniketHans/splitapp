from sqlalchemy.orm import Session
from app.service.user_activity_association import UserActivityAssociationService
from app.model.splitapp import getDB, UserModel, ActivityModel
from app.resource.splitapp import User,UserActivity,Payment
from app.dao.splitapp import SplitAppDAO

class UserService(UserActivityAssociationService):
    def __init__(self):
        self.session= getDB()
    

    def GetAllUsers(self):
        appDao=SplitAppDAO(self.session)
        try:
            users=appDao.getAllUsers()
            allUsers=[]
            for oneuser in users:
                user= User(
                    user_id=oneuser.user_id,
                    user_name=oneuser.user_name
                )
                allUsers.append(user.dict(exclude_none=True))
            
            return allUsers
        except Exception as err:
            print(err)
            raise Exception(err)
    
    
    def GetUser(self,userId:int):
        appDao=SplitAppDAO(self.session)
        try:
            userData= appDao.userInfoByUserID(userId)
            userActivityDataList=appDao.userActivityAssociationByUserID(userId)

            #dataFormation
            totalActivities=list()
            for userActivityData in userActivityDataList:
                activity=appDao.activityInfoByActivityID(userActivityData.activity_id)
                userActivity=UserActivity(
                    activity_id=userActivityData.activity_id,
                    activity_name=activity.activity_name,
                    total_amount=float(activity.total_amount),
                    to_be_paid_amount=float(userActivityData.to_be_paid_amount),
                    paid_amount=float(userActivityData.paid_amount)
                )
                if userActivityData.to_be_paid_amount>userActivityData.paid_amount:
                    userActivity.balance_to_be_paid=float(userActivityData.to_be_paid_amount-userActivityData.paid_amount)
                elif userActivityData.to_be_paid_amount==userActivityData.paid_amount:
                    userActivity.all_setteled=True
                else:
                    userActivity.money_to_be_collected=-float(userActivityData.to_be_paid_amount-userActivityData.paid_amount)
                totalActivities.append(userActivity)

            body= User(
                user_id=userData.user_id,
                user_name=userData.user_name,
                user_activities=totalActivities
            )

            return body.dict(exclude_none=True)
        except Exception as err:
            print(err)
            raise Exception(err)


    def CreateUser(self,userData:User):
        appDao=SplitAppDAO(self.session)
        try:
            userModel=UserModel(
                user_id=userData.user_id,
                user_name=userData.user_name
            )
            appDao.createUser(userModel)
            self.session.commit()
            return {"message":"User Created Succesfully","status_code":200}
        except Exception as err:
            print(err)
            raise Exception(err)

    
    def AddNewExpense(self,user_id:int,activity_id:int,payment:Payment):
        appDao=SplitAppDAO(self.session)
        try:
            adjustedAmount= self._addExpenseToUsers(activity_id,payment.payment_amount,userAdded=False)
            userAndActivity=appDao.userActivityAssociationByUserIDAndActivityID(user_id,activity_id)
            userAndActivity.paid_amount=float(userAndActivity.paid_amount)+payment.payment_amount

            self.session.commit()
            return {"message":"Expense Added Succefully","status_code":200}
        except Exception as err:
            print(err)
            raise Exception(err)
    
    def AddSettlement(self,user_id:int,activity_id:int,payment:Payment):
        appDao=SplitAppDAO(self.session)
        try: 
            userAndActivityInfo=appDao.userActivityAssociationByUserIDAndActivityID(user_id,activity_id)
            if userAndActivityInfo.to_be_paid_amount<=userAndActivityInfo.paid_amount:
                self.session.rollback()
                return {"message":"You dont have any due for this activity","status_code":400}
            else:
                dueAmount=userAndActivityInfo.to_be_paid_amount-userAndActivityInfo.paid_amount
                if payment.payment_amount>dueAmount:
                    self.session.rollback()
                    return {"message":f"You are paying more money than your dues. Due amount is {dueAmount}","status_code":400}
                else:
                    userAndActivityInfo.paid_amount=float(userAndActivityInfo.paid_amount)+payment.payment_amount
                    self.session.commit()
                    return {"message":"Payment amount added","status_code":200}
        except Exception as err:
            print(err)
            raise Exception(err)




















        

        