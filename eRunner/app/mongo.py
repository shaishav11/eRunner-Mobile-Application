import pymongo
import datetime
import random


client = pymongo.MongoClient("mongodb+srv://shaishavshah:srs12345@cluster1.jksay.mongodb.net/eRunner?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs='CERT_NONE')
db = client.get_database('eRunner')
records = db.match_info

def race_initiate(match_id, match_distance, user_id_1, user_name_1, user_location_1, start_time_1, user_id_2, user_name_2, user_location_2, start_time_2):
    
    new = {'match_id': match_id, 'match_distance': match_distance, 'match_end': 0, 'match_winner': '', 
       'player_1': {'user_id': user_id_1, 
                    'user_name': user_name_1, 
                    'user_location': user_location_1, 
                    'start_time': start_time_1, 
                    'end_time': 0, 
                    'live_distance': {'dst1': 0}, 
                    'live_speed': {'spd1': 0}}, 
        'player_2': {'user_id': user_id_2, 
                     'user_name': user_name_2, 
                     'user_location': user_location_2, 
                     'start_time': start_time_2, 
                     'end_time': 0, 
                     'live_distance': {'dst1': 0}, 
                     'live_speed': {'spd1': 0}}}
       
    records.insert_one(new)

    player1_distance = 0
    player2_distance = 0
    i = 1
    
    for i in range(1,100000000):
        if (player1_distance < match_distance):
        
            player1_distance = round(player1_distance + float(random.randrange(0,match_distance))/10,3)
            key1 = 'player_1.live_distance.dst'+str(i)
            records.update_one({ 'match_id':match_id},{ '$set' : { key1:player1_distance} }) 
            end_time_1 = datetime.datetime.now()
            
        if (player2_distance < match_distance):
            
            player2_distance = round(player2_distance + float(random.randrange(0,match_distance))/10,3)            
            key2 = 'player_2.live_distance.dst'+str(i)
            records.update_one({ 'match_id':match_id},{ '$set' : { key2:player2_distance} })
            end_time_2 = datetime.datetime.now()
        
        print(player1_distance, player2_distance)
            
        if ((player1_distance >= match_distance) and (player2_distance >= match_distance)):
            break


    records.update_one({ 'match_id': match_id }, { "$set": { "match_end": 1 } })
    
    myquery = { 'match_id': match_id }
    newvalues = { "$set": { "player_1.end_time": end_time_1 } }
    records.update_one(myquery, newvalues)
    newvalues = { "$set": { "player_2.end_time": end_time_2 } }
    records.update_one(myquery, newvalues)
    
    print(player1_distance, player2_distance)

    if end_time_1 < end_time_2:
        records.update_one({ 'match_id': match_id }, { "$set": { "match_winner": user_id_1 } })
        winner =  user_id_1
    else:
        records.update_one({ 'match_id': match_id }, { "$set": { "match_winner": user_id_2 } })
        winner = user_id_2
    
    speed1 = player1_distance / ((end_time_1 - start_time_1).total_seconds())
    speed2 = player2_distance / ((end_time_2 - start_time_2).total_seconds())

    time1 = (end_time_1 - start_time_1).total_seconds()
    time2 = (end_time_2 - start_time_2).total_seconds()
    
    return winner, round(speed1,2), round(time1,2), round(speed2,2), round(time2,2)







