import json
from sqlalchemy import func
from User import Users
from Database import DataConn
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--start", help="start the program,import data to the database")
parser.add_argument("-percentage-sex", help="percentage of man and women in database")
args = parser.parse_args()
Session = sessionmaker()
conn = DataConn(Session)
if args.start:
    conn.createnewdatabase()
    print(conn.createnewdatabase())
    data = open("persons.json", "r", encoding="utf8")
    f = json.loads(data.read())
    Users.__table__.create(bind=conn.engine, checkfirst=True)
    users = []

    for i, result in enumerate(f['results']):
        dob = datetime.strptime(result['dob']['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        row = {'UserId': i, 'Gender': result['gender'], 'Title': result['name']['title'],
               'FirstName': result['name']['first'], 'LastName': result['name']['last'],
               'City': result['location']['city'], 'Username': result['login']['username'], 'Email': result['email'],
               'DOB': dob.date(), 'Age': result['dob']['age'], 'RDTB': Users.calculatenextbirthday(dob),
               'Cell': ''.join([i for i in result['cell'] if i.isdigit()]),
               'Phone': ''.join([i for i in result['phone'] if i.isdigit()]), 'Password': result['login']['password']}
        users.append(row)

    for user in users:
        row = Users(**user)
        conn.session.add(row)
    conn.session.commit()
elif args.percentage_sex:
    all = conn.session.query(func.count('*')).select_from(Users).scalar()
    male = conn.session.query(Users).filter(Users.Gender.like('male')).count() / all * 100
    female = conn.session.query(Users).filter(Users.Gender.like('female')).count() / all * 100
    print(f'There is {male} % male and {female} % in database')
conn.session.close()
