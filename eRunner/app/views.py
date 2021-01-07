from app import app
from time import strftime
from flask import Flask, render_template, flash, request, redirect, jsonify, url_for, json
import pandas as pd
import mysql.connector
from mysql.connector import Error
from app.mongo import race_initiate
from app.image import image
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="srs12345",
  database="project"
)
mycursor = mydb.cursor()

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		passcode = request.form['passcode']

		query = "select password from user_info where email ='{}';".format(email)
		mycursor.execute(query)
		myresult = mycursor.fetchall()

		if myresult != []:
			if myresult[0][0]== passcode:
				user_id_sql = "SELECT user_id from user_info where email ='{}';".format(email)
				mycursor.execute(user_id_sql)
				myresult = mycursor.fetchall()
				user_id = myresult[0][0]
				flash('Login Successful', 'Success')
				return redirect(url_for("home", user_id=user_id))

			elif (myresult[0][0] != passcode):
				flash('Password is not correct for given email id, please enter the correct password', 'Error')
		else:
			flash('Your email id is not registered yet, Please sign up with your email id!', 'Error')

	return render_template('login.html')

@app.route("/home", methods=['GET', 'POST'])
def home():

	if request.method == 'POST':
		user_id = request.form['user_id']
		race_category = request.form['race_category']
		
		if race_category == "1":
			flash('Welcome to QuickRace', 'Success')
			return redirect(url_for("quickrace", user_id=user_id))

		elif race_category == "2":
			flash('Welcome to Marathon', 'Success')
			return redirect(url_for("marathon", user_id=user_id))

		elif race_category == "3":
			flash('Welcome to Training Ground', 'Success')
			return redirect(url_for("training", user_id=user_id))
		
		else:
			flash('Please select one of the three categorties', 'Error')

	user_id = request.args.get('user_id')

	#Flash name
	sql = '''SELECT first_name, last_name FROM user_info WHERE user_id = {};'''.format(user_id)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	user_name = '{} {}'.format(myresult[0][0], myresult[0][1])		
	
	# Update Flags:
	sql = "UPDATE user_info SET status = {}, quick_race_status = {}, marathon_status = {}, training_run_status = {} WHERE user_id = {};".format(1,0,0,0,user_id)
	mycursor.execute(sql)
	mydb.commit()	

	return render_template('home.html', user_id=user_id, user_name=user_name)

@app.route("/home/quickrace", methods=['GET', 'POST'])
def quickrace():

	if request.method == 'POST':
		user_id = request.form['user_id']
		date = request.form['date']
		distance = request.form['distance']
		time = request.form['time']

		sql1 =  "DELETE FROM quick_race_user WHERE user_id ={};".format(user_id) 
		sql2 = "INSERT INTO quick_race_user () VALUES ({}, {}, {}, '{}');".format(user_id, distance, time, date)
		mycursor.execute(sql1)
		mycursor.execute(sql2)
		mydb.commit()

		sql = "SELECT * FROM quick_race_user where user_id= {};".format(user_id)
		mycursor.execute(sql)
		myresult = mycursor.fetchall()

		date = myresult[0][3]
		distance = myresult[0][1]
		time = myresult[0][2]

		return redirect(url_for("match", user_id=user_id, date=date, time=time, distance=distance))

	user_id = request.args.get('user_id')

	# Update Flags:
	sql = "UPDATE user_info SET status =1, quick_race_status =1, marathon_status =0, training_run_status =0 WHERE user_id = {};".format(user_id)
	mycursor.execute(sql)
	mydb.commit()

	flash('Let us find your Opponent based on your request', 'Success')
	return render_template('quickrace.html', user_id=user_id)


@app.route("/home/quickrace/match", methods=['GET', 'POST'])
def match():
	user_id = request.args.get('user_id')
	date = request.args.get('date')
	time = request.args.get('time')
	distance = request.args.get('distance')

	print(date, time, distance)

	if request.method == 'POST':
		user_id = request.form['user_id']
		date = request.form['date']
		distance = request.form['distance']
		time = request.form['time']
		opp_user_id = request.form['opp_user_id']
		return redirect(url_for("result", user_id=user_id, date=date, time=time, distance=distance, opp_user_id=opp_user_id))

	## User information
	sql = "select * from user_attributes u1 join user_info u2 on u1.user_id = u2.user_id where u1.user_id ='{}';".format(user_id)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	user_name = '{} {}'.format(myresult[0][9], myresult[0][10])
	user_matches = myresult[0][1]
	user_tot_dist = myresult[0][2]
	user_per_win = myresult[0][3]
	user_stam = myresult[0][4]
	user_level = myresult[0][5]

	sql = '''select q1.user_id from quick_race_user q1
			 join user_info u1 on u1.user_id = q1.user_id
			 where u1.status=1 and u1.quick_race_status=1 and q1.user_id<>{} and q1.race_distance={} and q1.scheduled_time={} and date = '{}';'''.format(user_id, distance, time, date)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	if myresult != []:
		opp_user_id = myresult[0][0]
		
		## Opponent information
		sql = "select * from user_attributes u1 join user_info u2 on u1.user_id = u2.user_id where u1.user_id ='{}';".format(opp_user_id)
		mycursor.execute(sql)
		myresult = mycursor.fetchall()

		opp_name = '{} {}'.format(myresult[0][9], myresult[0][10])
		opp_matches = myresult[0][1]
		opp_tot_dist = myresult[0][2]
		opp_per_win = myresult[0][3]
		opp_stam = myresult[0][4]
		opp_level = myresult[0][5]

		flash("Opponent Found", "Success")

	else:
		opp_user_id = "Bot ID"
		opp_name = "Bot Name"
		opp_matches = "Bot Matches"
		opp_tot_dist = "Bot Distance"
		opp_per_win = "Bot Win Percentage"
		opp_stam = "Bot Stamina"
		opp_level = "Bot Level"

		flash("No Opponent Found, here is a bot based on your level", "Success")


	flash('Gear up, time to race!!', 'Success')
	return render_template('match.html', user_name=user_name, user_matches=user_matches, user_tot_dist=user_tot_dist, user_per_win=user_per_win, user_stam=user_stam, user_level=user_level,
									 opp_name=opp_name, opp_matches=opp_matches, opp_tot_dist=opp_tot_dist, opp_per_win=opp_per_win, opp_stam=opp_stam, opp_level=opp_level, 
									 date=date, time=time, distance=distance, user_id=user_id, opp_user_id=opp_user_id)

@app.route("/home/quickrace/match/result", methods=['GET', 'POST'])
def result():

	user_id = request.args.get('user_id')
	date = request.args.get('date')
	time = request.args.get('time')
	distance = request.args.get('distance')
	opp_user_id = request.args.get('opp_user_id')

	if request.method == 'POST':
		print(user_id)
		user_id = request.form['user_id']
		flash("Match Over", "Success")
		return redirect(url_for("home", user_id=user_id))

	# User info
	sql = '''select * from user_address where user_id={};'''.format(user_id)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	city = myresult[0][2]
	state = myresult[0][3]
	country = myresult[0][4]

	user_location = '{},{},{}'.format(city, state, country)

	# Oppoonent info
	sql = '''select * from user_address where user_id={};'''.format(opp_user_id)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	city = myresult[0][2]
	state = myresult[0][3]
	country = myresult[0][4]

	opp_location = '{},{},{}'.format(city, state, country)

	#update quick match database
	sql = '''INSERT INTO quick_match (user1_id, user2_id, user1_location, user2_location, match_status, race_distance) 
											VALUES ({},{},'{}','{}',1,{});'''.format(user_id, opp_user_id, user_location, opp_location, distance)
	mycursor.execute(sql)
	mydb.commit()

	#mongo db connection:
	sql = '''SELECT * FROM quick_match WHERE user1_id = {} and user2_id = {} and match_status = 1;'''.format(user_id, opp_user_id)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	match_id = myresult[0][0]
	print(match_id)
	user_id = myresult[0][1]
	opp_user_id = myresult[0][2]
	user_location = myresult[0][7]
	opp_location = myresult[0][8]

	sql = '''SELECT first_name, last_name FROM user_info WHERE user_id = {};'''.format(user_id)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	user_name = '{} {}'.format(myresult[0][0], myresult[0][1])

	sql = '''SELECT first_name, last_name FROM user_info WHERE user_id = {};'''.format(opp_user_id)
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	opp_name = '{} {}'.format(myresult[0][0], myresult[0][1])

	start_time_1 = datetime.datetime.now()
	start_time_2 = datetime.datetime.now()


	winner_id, speed1, end_time_1, speed2, end_time_2 = race_initiate(match_id, int(distance), user_id, user_name, user_location, start_time_1, opp_user_id, opp_name, opp_location, start_time_2)

	if winner_id == user_id:
		winner = user_name
		user_win = 0
	else:
		winner = opp_name
		user_win = 1

	sql1= '''UPDATE quick_match SET match_status = 0, user1_speed = {}, user2_speed = {}, user1_end_time = {}, user2_end_time = {} 
					WHERE match_id = {};'''.format(speed1, speed2, end_time_1, end_time_2, match_id)
	sql2= '''INSERT INTO result (match_id, user_id, win , match_type) VALUES ({},{},{}, 'quickrace');'''.format(match_id, user_id, user_win)
	mycursor.execute(sql1)
	mycursor.execute(sql2)
	mydb.commit()

	winner_image = image(winner_id)
	winner_image.save("/Users/shaish/Desktop/projects/eRunner/app/static/winner_image.png")

	print("hello")

	flash(winner, 'Congralutions')

	return render_template('result.html', user_id=user_id, distance=distance, end_time_1=end_time_1, speed1=speed1, winner=winner,
											opp_user_id=opp_user_id, end_time_2=end_time_2, speed2=speed2, user_name=user_name, opp_name=opp_name, winner_image=winner_image)


@app.route("/profile", methods=['GET', 'POST'])
def profile():

	if request.method == 'POST':
		user_id = request.form['user_id']
		address_line = request.form['address_line']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		zip_code = request.form['zip_code']
		
		# Update profile query
		sql = "UPDATE user_address SET address_line = '{}', city = '{}', state = '{}', country = '{}', zipcode = '{}' WHERE user_id = {};".format(address_line, city, state, country, zip_code, user_id)
		mycursor.execute(sql)
		mydb.commit()


		flash("Profile Updated", "Success")
		return redirect(url_for("home", user_id=user_id))

	flash("Please update your profile", "Profile Update")
	user_id = request.args.get('user_id')

	return render_template('profile.html', user_id = user_id)

@app.route("/logout", methods=['GET', 'POST'])
def logout():

	user_id = request.args.get('user_id')

	if request.method == 'POST':
		user_id = request.form['user_id']
		logout = request.form['logout']

		print(logout)

		if logout =="1":
			sql = "UPDATE user_info SET status = {}, quick_race_status = {}, marathon_status = {}, training_run_status = {} WHERE user_id = {};".format(0,0,0,0,user_id)
			mycursor.execute(sql)
			mydb.commit()

			flash('Logged Out Successfully', 'Success')
			return redirect("http://127.0.0.1:5000/login")

		if logout =="2":
			sql = "UPDATE user_info SET status = {}, quick_race_status = {}, marathon_status = {}, training_run_status = {} WHERE user_id = {};".format(1,0,0,0,user_id)
			mycursor.execute(sql)
			mydb.commit()
			flash('Back to Home Page', 'Success')
			return redirect(url_for("home", user_id=user_id))

	return render_template('logout.html', user_id=user_id)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']
		passcode1 = request.form['passcode1']
		passcode2 = request.form['passcode2']
		first_name = request.form['first_name']
		last_name = request.form['last_name']

		if passcode1 == passcode2:
			sql =  '''INSERT INTO user_info (email, password, first_name, last_name, status, quick_race_status, marathon_status, training_run_status)
							VALUES ('{}', '{}','{}', '{}', 0,0,0,0);'''.format(email, passcode1, first_name, last_name)
			mycursor.execute(sql)
			mydb.commit()

			flash('New account created', 'Success')
			return redirect("login")

		else:
			flash('Password does not match, Please try again', 'Error')

	return render_template('signup.html')

@app.route("/home/marathon", methods=['GET', 'POST'])
def marathon():

	## Needs to be completed later
	user_id = request.args.get('user_id')
	
	# Update Flags:
	sql = "UPDATE user_info SET status =1, quick_race_status =0, marathon_status =1, training_run_status =0 WHERE user_id = {};".format(user_id)
	mycursor.execute(sql)
	mydb.commit()

	return render_template('marathon.html', user_id=user_id)

@app.route("/home/training", methods=['GET', 'POST'])
def training():

	## Needs to be completed later
	user_id = request.args.get('user_id')

	# Update Flags:
	sql = "UPDATE user_info SET status =1, quick_race_status =0, marathon_status =0, training_run_status =1 WHERE user_id = {};".format(user_id)
	mycursor.execute(sql)
	mydb.commit()

	return render_template('training.html', user_id=user_id)


