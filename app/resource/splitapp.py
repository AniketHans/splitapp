from pydantic import BaseModel
from typing import List,Optional


class UserActivity(BaseModel):
    activity_id:int
    activity_name:str
    total_amount:float
    to_be_paid_amount:float
    paid_amount:float
    balance_to_be_paid:Optional[float]
    money_to_be_collected:Optional[float]
    all_setteled:Optional[bool]=False


class User(BaseModel):
    user_id:int
    user_name:str
    user_activities:Optional[List[UserActivity]]

class ActivityUser(BaseModel):
    user_id:int
    user_name:Optional[str]
    to_be_paid_amount:Optional[float]=0
    paid_amount:Optional[float]=0
    lend_amount:Optional[float]=0
    

class Activity(BaseModel):
    activity_id:Optional[int]
    activity_name:str
    total_amount:Optional[float]=0
    total_contributors:Optional[int]=0
    created_by:Optional[User]
    created_at:Optional[str]
    users:Optional[List[ActivityUser]]


class Payment(BaseModel):
    payment_amount:float
    payment_reason:Optional[str]






