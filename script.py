import json
from sqlalchemy import func, sql
from User import Users
from Database import DataConn
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--start", help="start the program,import data to the database")
parser.add_argument("-percentage-sex", help="percentage of men and women in database")
parser.add_argument("-average-age", help="average age of people")
parser.add_argument("-popular-city", help="most popular cities from database")
parser.add_argument("-popular-password", help="most popular passwords from database")
parser.add_argument("-start-birth", help="start date for range of birth user.Format YYYY-MM-DD")
parser.add_argument("-end-birth", help="end date for range of birth user. Format YYYY-MM-DD")
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
elif args.average_age:
    if args.average_age == 'all':
        result = conn.session.query(func.sum(Users.Age)).select_from(Users).scalar() / \
                 conn.session.query(func.count(Users.Age)).select_from(Users).scalar()
    elif args.average_age == 'men':
        result = conn.session.query(func.sum(Users.Age)).filter(Users.Gender.like('male')).scalar() / \
                 conn.session.query(func.count(Users.Age)).filter(Users.Gender.like('male')).scalar()
    else:
        result = conn.session.query(func.sum(Users.Age)).filter(Users.Gender.like('female')).scalar() / \
                 conn.session.query(func.count(Users.Age)).filter(Users.Gender.like('female')).scalar()
    print(f'Average age from database is {result}')
elif args.popular_city:
    result = conn.session.query(Users.City, func.count(Users.City)).group_by(Users.City) \
        .order_by(func.count(Users.City).desc()).limit(args.popular_city).all()
    for city in result:
        print(city)
elif args.popular_password:
    result = conn.session.query(Users.Password, func.count(Users.Password)).group_by(Users.Password) \
        .order_by(func.count(Users.Password).desc()).limit(args.popular_password).all()
    for password in result:
        print(password)
elif args.start_birth:
    if args.end_birth:
        result = conn.session.query(Users.FirstName, Users.LastName, Users.DOB).filter(
            sql.and_(Users.DOB > args.start_birth, Users.DOB < args.end_birth)).all()
        for user in result:
            print(user)
    else:
        print('Need start and end date')
conn.session.close()
