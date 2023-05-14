from sqlalchemy import create_engine,Column, Integer,String,ForeignKey,Float
from sqlalchemy.dialects.mysql import TINYINT,BIGINT

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


# Creating engine and session

def getEngine():
    # engine = create_engine('mysql+pymysql://admin:password@splitapp-db:3306/splitapp')
    engine = create_engine('mysql+pymysql://admin:password@localhost:3306/splitapp')

    if not database_exists(engine.url):
        create_database(engine.url)
    return engine

def getDB():
    # engine = create_engine('mysql+pymysql://admin:password@splitapp-db:3306/splitapp')
    engine = create_engine('mysql+pymysql://admin:password@localhost:3306/splitapp')

    Session= sessionmaker(bind=engine)
    session=Session()
    return session

engine= getEngine()

Base=declarative_base()

class UserModel(Base):
    __tablename__='user'
    user_id=Column(BIGINT,primary_key=True) #phone_number
    user_name=Column(String(50))


class ActivityModel(Base):
    __tablename__='activity'
    activity_id=Column(Integer,primary_key=True)
    activity_name=Column(String(50))
    created_by=Column(BIGINT,ForeignKey(UserModel.user_id))
    created_at=Column(Integer)
    total_amount=Column(Float(6,2),default=0)
    total_contributors=Column(Integer,default=0)

class UserActivityAssociationModel(Base):
    __tablename__='user_activity_association'
    user_activity_association_id=Column(Integer,primary_key=True)
    user_id=Column(BIGINT,ForeignKey(UserModel.user_id))
    activity_id=Column(Integer,ForeignKey(ActivityModel.activity_id))
    to_be_paid_amount=Column(Float(6,2),default=0)
    paid_amount=Column(Float(6,2),default=0)
    is_active=Column(TINYINT(1),default=1)




# Creating table in database with the above 4 columns

Base.metadata.create_all(engine)



