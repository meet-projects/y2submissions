from flask import Flask, render_template, request, flash, url_for, redirect
from model import * 
import random
from flask import session as login_session
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
import sys
import logging


app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

app.secret_key = '#$#UJEJOIBVJWOI'




def verify_password(username, password):
    student = session.query(Student).filter_by(username=username).first()
    if not student or not student.verify_password(password):
        return False
    return True


@app.route("/")
def mainPage():
	students = session.query(Student).all()
	latest_submissions = []
	for student in students:
	    submissions = session.query(Submission).filter_by(student_id=student.id).all()
	    if submissions != []:
	        latest_submission = session.query(Submission).filter_by(student_id=student.id).order_by(Submission.id.desc()).first()
	        latest_submissions.append(latest_submission)
	return render_template("main.html", submissions = latest_submissions)


@app.route("/login", methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		username = request.form['username']
		password = request.form['password']
		if username is None or password is None:
			flash("Missing Arguments")
			return redirect(url_for('login'))
		if verify_password(username, password):
			student = session.query(Student).filter_by(username=username).one()
			flash("Login Successful. Welcome, %s!" % student.first_name)
			login_session['first_name'] = student.first_name
			login_session['last_name'] = student.last_name	
			login_session['username'] = username
			login_session['id'] = student.id
			return redirect(url_for('mainPage'))
		else:
			flash("Incorrect username/password combination")
			return redirect(url_for('login'))



@app.route("/loginwithID", methods = ['GET', 'POST'])
def loginwithID():
	if request.method  == 'GET':
		return render_template('loginWithId.html')
	else:
		id_number = request.form['id_number']
		student = session.query(Student).filter_by(student_id = id_number).one()
		flash(" Welcome, %s!" % student.first_name)
		login_session['first_name'] = student.first_name
		login_session['last_name'] = student.last_name
		login_session['id'] = student.id
		login_session['username'] = ""
		return redirect(url_for('viewProfile'))

@app.route('/logout')
def logout():
	if 'id' not in login_session:
		flash("You must be logged in in order to log out")
		return redirect(url_for('mainPage'))
	del login_session['first_name']
	del login_session['last_name']
	del login_session['username']
	del login_session['id']
	flash ("Logged Out Successfully")
	return redirect(url_for('mainPage'))


@app.route("/profile", methods = ['GET', 'POST'])
def viewProfile():
	if 'id' not in login_session:
		flash("You must first sign in to view this page!")
		return redirect(url_for('mainPage'))
	if request.method == 'GET':
		student = session.query(Student).filter_by(id=login_session['id']).one()
		return render_template('profile.html', student = student)
	else:
		username = request.form['username']
		password = request.form['password']
		password_verfiy = request.form['password_verify']
		if password!= password_verfiy:
			flash('Passwords do not match!')
			return redirect(url_for('viewProfile'))
		if username is None:
			flash('Please create a username')
			return redirect('viewProfile')
		if session.query(Student).filter_by(username=username).all() != []:
			flash("A user with this username already exists.")
			return redirect('viewProfile')
		student = session.query(Student).filter_by(id=login_session['id']).one()
		student.username = username
		student.hash_password(password)
		session.add(student)
		session.commit()
		login_session['username'] = username
		flash("Your credentials were saved successfully!")
		return redirect(url_for('submitProject'))



@app.route("/submit", methods = ['GET', 'POST'])
def submitProject():
	if 'id' not in login_session:
		flash("You must first sign in to view this page!")
		return redirect(url_for('mainPage'))
	if request.method == 'GET':
		if 'id' in login_session:
			submissions = session.query(Submission).filter_by(student_id=login_session['id']).all()
		else:
			submissions = []
		return render_template('submissionForm.html', submissions = submissions)
	elif request.method == 'POST':
		url = request.form['url']
		github_url = request.form['github_url']
		description = request.form['description']
		newSubmission=Submission(url = url, github_url = github_url, description=description, student_id = login_session['id'])
		session.add(newSubmission)
		session.commit()
		flash("Thank you for your submission!")
		return redirect(url_for('mainPage'))


if __name__ == '__main__':
	app.run(debug=True)





	###### TODO #######
	# unique email verifcation
	#protect routes that require logins
	# resubmissions