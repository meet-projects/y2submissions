from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import psycopg2

import datetime

Base = declarative_base()


class Submission(Base):
    __tablename__ = 'submission'
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    github_url = Column(String(255))
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship("Student", back_populates="submissions")

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    student_id = Column(String)
    first_name = Column(String(255))
    last_name = Column(String(255))
    username = Column(String(255), unique=True)
    submissions = relationship("Submission", back_populates="student")
    password_hash = Column(String(255))
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)




engine = create_engine('postgres://cacshzietwzevn:a16e4ed0adfc9751a8377e095d1169422e193bbb80bcc1cbf4f3b0ffb376de68@ec2-54-247-166-129.eu-west-1.compute.amazonaws.com:5432/d4rfh9hk6vkk33')
Base.metadata.create_all(engine)
