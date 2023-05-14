
from fastapi import FastAPI,Body
from app.service.user import UserService
from app.service.activity import ActivityService
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.resource.splitapp import User,Activity,ActivityUser,Payment
import sys



sys.path.append("..")

app= FastAPI()


@app.get("/",summary="Greetings")
def greetings():
    return JSONResponse(content="Hello! Welcome to the SplitApp.")

# User APIs
@app.get("/all-users",summary="Get basic Info about all the users")
def getusers():
    try:
        userService=UserService()
        result=userService.GetAllUsers()
        return JSONResponse(content=result)
    except Exception as err:
        print(err)
        return JSONResponse(content="Server Side Error",status_code=500)


@app.get("/user/{user_id}",summary="Get full info about a user by its user_id")
def getuser(user_id:int):
    try:
        userService=UserService()
        result=userService.GetUser(user_id)
        return JSONResponse(content=result)
    except Exception as err:
        print(err)
        return JSONResponse(content="Server Side Error",status_code=500)

@app.post("/user",summary="Create a user")
def createuser(userData:User = Body(...)):
    try:
        print(userData)
        userService=UserService()
        result=userService.CreateUser(userData)
        return JSONResponse(content=result["message"],status_code=result["status_code"])
    except Exception as err:
        print(err)
        return JSONResponse(content="Server Side Error",status_code=500)


@app.put("/user/{user_id}/activity/{activity_id}/expense",summary="Adding expense to a specific activity by the user")
def usernewpaymemt(user_id:int,activity_id:int,payment:Payment= Body(...)):
    try:
        userService=UserService()
        result=userService.AddNewExpense(user_id,activity_id,payment)
        return JSONResponse(content=result["message"],status_code=result["status_code"])
    except Exception as err:
        print(err)
        return JSONResponse(content="Server Side Error",status_code=500)

@app.put("/user/{user_id}/activity/{activity_id}/settlement",summary="Adding money for settlement in a activity by the user")
def usersettlementpaymemt(user_id:int,activity_id:int,payment_info:Payment= Body(...)):
    try:
        userService=UserService()
        result=userService.AddSettlement(user_id,activity_id,payment_info)
        return JSONResponse(content=result["message"],status_code=result["status_code"])
    except Exception as err:
        print(err)
        return JSONResponse(content="Server Side Error",status_code=500)
    


# Activity APIs
@app.get("/all-activity",summary="Getting all activities basic info")
def getusers():
    try:
        activityService=ActivityService()
        result=activityService.GetAllActivities()
        return JSONResponse(content=result)
    except Exception as err:
        print(err)
        return JSONResponse(content="Server Side Error",status_code=500)

@app.post('/user/{user_id}/activity',summary="Creating an activity by a specific user")
def createactivity(user_id:int,activity:Activity= Body(...,embed=True)):
    try:
        activityService=ActivityService()
        result=activityService.CreateActivity(user_id,activity)
        return JSONResponse(content=result["message"],status_code=result["status_code"])
    except Exception as err:
        print(err)
        return JSONResponse(content="Server Side Error",status_code=500)

@app.get('/activity/{activity_id}',summary="Getting full info about an activity")
def getactivity(activity_id:int):
    try:
        activityService=ActivityService()
        result=activityService.GetActivity(activity_id)
        return JSONResponse(content=result)
    except Exception as err:
        print(err)
        return JSONResponse(content="Server Side Error",status_code=500)


@app.put('/activity/{activity_id}/add-user',summary="Adding a specific user to an activity")
def addusertoactivity(activity_id:int,user:ActivityUser =Body(...)):
    try:
        activityService=ActivityService()
        result=activityService.AddUserToActivity(activity_id,user)
        return JSONResponse(content=result["message"],status_code=result["status_code"])
    except Exception as err:
        print(err)
        return JSONResponse(content="Server Side Error",status_code=500)



