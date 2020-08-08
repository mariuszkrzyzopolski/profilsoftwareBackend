from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

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

    def calculatenextbirthday(self):
        today = date.today()
        if today.month == self.month and today.day >= self.day or today.month > self.month:
            nextbirthdayear = today.year + 1
        else:
            nextbirthdayear = today.year
        if self.day == 29 and self.month == 2:
            nextbirthdayear = 2024
        nextbirthday = date(nextbirthdayear, self.month, self.day)
        return (nextbirthday - today).days

    def calculatebestpassword(password):
        score = 0
        if not password.isupper() and password.isalnum and not password.isdigit():
            score += 1
        if not password.islower() and password.isalnum and not password.isdigit():
            score += 2
        if not password.isalpha():
            score += 1
        if len(password) >= 8:
            score += 5
        if not password.isalnum():
            score += 3
        return {password: score}
