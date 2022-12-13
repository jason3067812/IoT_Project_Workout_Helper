import json
from classes import Sensor,User,Barbell
import json
from flask import Flask, jsonify, request
from pymongo import MongoClient
import csv
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from flask import Flask
import csv
import time
from pymongo import MongoClient
import math



sensor = Sensor()
user = User()
barbell = Barbell()
data = {}
l = [0]
s = [0]
store_data = False


# from animation import *
# squat_anims = Squat_anims()
# bench_press_anims = Bench_press_anims()
# squat_anims.invisible()
# bench_press_anims.invisible()


uri = "mongodb+srv://eric:qwert1234@cluster0.xweafpe.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.iot_final
coll = db.sensor_data
userInput = db.userInput
#coll.delete_many({}) #################################

userInfoQuery = {}
userInfo = userInput.find_one(userInfoQuery)
height = int(userInfo['height'])
lengthofarm  = int(userInfo['lengthofarm'])
lengthofleg = int(userInfo['lengthofleg'])
print(height, lengthofarm, lengthofleg)


# calculate bench distance

#求cos()
#备注：直接用math.cos()出来的结果不完全正确
x = 10
sin_mt = math.sin(math.radians(x))
cos_mt = math.sqrt(1-sin_mt**2)
user.bench_press_distance = float(lengthofarm) * cos_mt
print("you need to hit this height for bench press " + str(user.bench_press_distance))

upper_length = (height-lengthofleg) / 2
user.squat_distance = (upper_length + lengthofleg) / 2
print("you need to go this low for squat " + str(user.squat_distance))


app = Flask(__name__)

@app.route('/test', methods=['GET','POST'])
def test_server():
                
    return "hello world"

@app.route('/init', methods=['GET','POST'])
def initialize():
    if request.method == 'POST':
     
        user.rep_count = 0
        print(user.rep_count)
        print("finish initial")
                
    return "initial"
    

@app.route('/data', methods=['GET','POST'])
def upload_data():
    if request.method == 'POST':
        global data
        data = json.loads(request.data)
            
    return "data"

rest_counter = 0

@app.route('/result', methods=['GET','POST'])
def data_analysis():
    if request.method == 'GET':
        print(" ")
        
        global l,s
      
        user.change_exercise(data['exercise'])
        sensor.update(data)
        sensor.print_data()
        barbell.hit_detect(user,sensor)
        #user.rest_detect(sensor)
        
        print(" ")
        
        # unbalacne check
        if abs(sensor.pitch) > 20 or (sensor.yaw > 20 and sensor.yaw < 180) or (sensor.yaw < 340 and sensor.yaw > 180):
            barbell.unbalanced = True
        else:
            barbell.unbalanced = False   
            
        # hit check
        if len(l)<2:
            l.append(user.rep_count)
            
        else:
            l.pop(0)
            l.append(user.rep_count)
  
        if l[0]<l[1]:
            
            barbell.hit_check = True
            
            # insert code goes here
            insert_time = data['time']
            print(insert_time)
            result = coll.insert_one( { "date": data['time'], 'type': data['exercise'] } )
            print('Inserted data to database',barbell.hit_check)
        else:
            barbell.hit_check = False
            
        # rest check #########################
        global rest_counter
        
        if abs(sensor.distance - sensor.last_distance) < 3:
            rest_counter += 1
        else:
            rest_counter = 0
            user.alarming = False
            
        print("Rest Count: " + str(rest_counter))
            
        if rest_counter ==6:
            user.alarming = True
            if user.rep_count >= 6:
                user.set_count += 1
                user.rep_count = 0
                # insert code goes here
                insert_time = data['time']
                print(insert_time)
                result = coll.insert_one( { "date_s": data['time'], 'type_s': data['exercise'] } )
                print('Inserted set data to database')
                
            
        # send back result

        jsonFile = {"unbalanced":str(barbell.unbalanced),"hit":str(barbell.hit_check),
                "alarming":str(user.alarming),"set_count":str(user.set_count),"rep_count":str(user.rep_count)}
        jsonFile = json.dumps(jsonFile)
        
        if store_data == True:
            
            a,b,c,d,e,f = data['time'], data['yaw'], data['pitch'], data['roll'], data['distance'], str(barbell.hit_check)
        
            with open("/home/ubuntu/iot.csv", 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([a,b,c,d,e,f])
   
    return jsonFile
       

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
    # Close the connection to MongoDB when you're done.
    client.close()