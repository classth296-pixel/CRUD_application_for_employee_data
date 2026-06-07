from sqlalchemy import Column, Integer, String, column
from database import base

class Employee(base):
    __tablename__="employees"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,index=True)
    email=Column(String,index=True,unique=True) 
