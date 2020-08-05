import json
from sqlalchemy import *
from sqlalchemy_utils import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
from datetime import datetime, timedelta,date


engine = create_engine('sqlite:///RandomUsers.db')
if database_exists(engine.url): drop_database(engine.url) 
create_database(engine.url)
Base = declarative_base()

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

def calculateNextBirthday(birth):
	today = date.today()
	if(today.month == birth.month and today.day >= birth.day or today.month > birth.month):
		nextBirthdayYear=today.year+1
	else:
		nextBirthdayYear=today.year
	if(birth.day == 29 and birth.month == 2):
		nextBirthdayYear=2024
	nextBirthday=date(nextBirthdayYear, birth.month, birth.day)
	return (nextBirthday-today).days


data = open("persons.json","r",encoding="utf8")
f = json.loads(data.read())


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
	dob = datetime.strptime(result['dob']['date'],'%Y-%m-%dT%H:%M:%S.%fZ')
	row['DOB'] = dob.date()
	row['Age'] = result['dob']['age']
	row['RDTB'] = calculateNextBirthday(dob)
	row['Cell'] = ''.join([i for i in result['cell'] if i.isdigit()])
	row['Phone'] = ''.join([i for i in result['phone'] if i.isdigit()])
	row['Password'] = result['login']['password']
	users.append(row)


print(users[0])
Session = sessionmaker(bind=engine)
session = Session()
for user in users:
	row = Users(**user)
	session.add(row)
session.commit()
session.close()
# gender, name, location, email, login,dob,register,phone,cell,id,picture,nat