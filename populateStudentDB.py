import pandas as pd
import numpy as np
from model import * 

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()


students = pd.read_csv('students.csv')

first_names = students['Student first name']
last_names = students['Student last name']
student_ids = students['ID number']

for i in range(len(first_names)):
	student = Student(first_name = first_names[i], last_name = last_names[i], student_id = str(student_ids[i])[0:9])
	session.add(student)
	session.commit()
