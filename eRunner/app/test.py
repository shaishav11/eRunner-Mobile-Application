from mongo import race_initiate
import datetime


match_id =100
distance = 5
user_id =23
opp_user_id = 3
user_location = 'Boston'
opp_location='Seattle'
start_time_1 = datetime.datetime.now()
start_time_2 = datetime.datetime.now()
user_name = 'Shaishav Shah'
opp_name = 'Parth Rana'



winner, speed1, end_time_1, speed2, end_time_2 = race_initiate(match_id, distance, user_id, user_name, user_location, start_time_1, opp_user_id, opp_name, opp_location, start_time_2)

print(winner, speed1, end_time_1, speed2, end_time_2)