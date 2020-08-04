import json
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
from datetime import datetime, timedelta,date

engine = create_engine('sqlite:///users.db')
Base = declarative_base()

data = open("persons.json","r",encoding="utf8")
f = json.loads(data.read())

class Users(Base):
	__tablename__ = "users"
	UserId = Column(Integer, primary_key=True)
	Gender = Column(String)
	Title = Column(String)
	FirstName = Column(String)
	LastName = Column(String)
	City = Column(String)
	Username = Column(String)
	Email = Column(String)
	DOB = Column(DateTime)
	Age = Column(Integer)
	RDTB = Column(Integer)
	Phone = Column(Integer)
	Cell = Column(Integer)
	Password = Column(String)


Users.__table__.create(bind=engine, checkfirst=True)
users = []

for i, result in enumerate(f['results']):
	row = {}
	row['UserId'] = i
	row['Gender'] = result['gender']
	row['Title'] = result['name']['title']
	row['FirstName'] = result['name']['first']
	row['LastName'] = result['name']['last']
	row['City'] = result['location']['city']
	row['Username'] = result['login']['username']
	row['Email'] = result['email']
	row['Username'] = result['login']['username']
	dob = datetime.strptime(result['dob']['date'],'%Y-%m-%dT%H:%M:%S.%fZ')#"%Y-%m-%dT%H:%M:%S%z")	
	row['DOB'] = dob.date()
	row['Age'] = result['dob']['age']
	row['RDTB'] = dob.date()
	row['Cell'] = result['cell']
	row['Phone'] = result['phone']
	row['Password'] = result['login']['password']
	
	users.append(row)

Session = sessionmaker(bind=engine)
session = Session()

for user in users:
    row = Users(**user)
    session.add(row)
session.commit()
# gender, name, location, email, login,dob,register,phone,cell,id,picture,nat