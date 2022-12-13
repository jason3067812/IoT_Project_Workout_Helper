import math
# from pymongo import MongoClient

# uri = "mongodb+srv://eric:qwert1234@cluster0.xweafpe.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri)
# db = client.iot_final
# sensor_data = db["sensor_data"]
# userInput = db["userInput"]

# userInfoQuery = {}
# userInfo = userInput.find_one(userInfoQuery)
# height = int(userInfo['height'])
# lengthofarm  = int(userInfo['lengthofarm'])
# lengthofleg = int(userInfo['lengthofleg'])

class Sensor:
    def __init__(self):
        self.yaw, self.pitch, self.roll = 0,0,0 # ORIENTATION
        self.last_distance = 0
        self.distance = 0
        self.date = ''
    def update(self,data):
        self.yaw = float(data['yaw']) if abs(float(data['yaw'])) > 1 else 0
        self.pitch = float(data['pitch']) if abs(float(data['pitch'])) > 1 else 0
        self.roll = float(data['roll']) if abs(float(data['roll'])) > 1 else 0
        self.last_distance = self.distance
        self.distance = int(data['distance'])
        # self.date = data['date']

    def print_data(self):
        print('yaw:{:.1f}, pitch:{:.1f}, roll:{:.1f}, distance{:.1f}'
        .format(self.yaw,self.pitch,self.roll,self.distance))     


class Barbell:
    def __init__(self):
        self.unbalanced = False
        self.hitting = False
        self.same_distance_counter = 0
        self.hit_check = False
    def hit_detect(self,user,sensor):
        if user.exercise == 'bench press':
            if not self.hitting and sensor.distance > user.bench_press_distance:
                self.hitting = True
                user.rep_count += 1
                # insert to database 
                # result = sensor_data.insert_one( { "date": sensor.date, 'type': user.exercise } )
                self.hit_check = True
                self.hitting = True
            elif self.hitting and sensor.distance < user.bench_press_distance:
                self.hitting = False
            elif self.hitting and sensor.distance > user.bench_press_distance: 
                self.hit_check = False
        elif user.exercise == 'squat':
            if not self.hitting and sensor.distance < user.squat_distance:
                self.hitting = True
                user.rep_count += 1
                self.hit_check = True
                self.hitting = True
            elif self.hitting and sensor.distance > user.squat_distance:
                self.hitting = False
            elif self.hitting and sensor.distance < user.squat_distance: 
                self.hit_check = False       


class User:
    def __init__(self):
        self.resting = False
        self.exercise = ''
        self.set_count = 0
        self.rep_count = 0
        self.height = 0
        self.arm_length = 0
        self.rest_counter = 0
        self.bench_press_distance = 15
        self.squat_distance = 5
        self.alarming = False
        self.rest_time = 5
    
    def rest_detect(self, sensor):
        print("Rest Count: " + str(self.rest_counter))
        if abs(sensor.distance - sensor.last_distance) < 3:
            sensor.distance = sensor.last_distance
        if sensor.distance == sensor.last_distance:
            self.rest_counter += 1
        else:
            self.rest_counter = 0
            self.resting = False
            self.alarming = False
        if self.rest_counter >= 5 and self.alarming == False:
            if self.rep_count >= 6 and self.resting == False:
                print("start resting")
                # insert to database 
                self.set_count += 1
                # print(result)
                self.rep_count = 0
            self.resting = True

        if self.rest_counter >= self.rest_time:
            print("Time to go back to workout")
            #self.rest_counter = 0
            self.resting = False
            self.alarming = True

    def change_exercise(self, input_exercise):
        if self.exercise != input_exercise:
            self.set_count = 0
            self.rep_count = 0
            self.exercise = input_exercise
            self.resting = False
            self.alarming = False
            self.rest_counter = 0
           
            

    def set_distance(self):
        upper_length = (height-lengthofleg) / 2
        self.squat_distance = (upper_length + lengthofleg) / 2

        sin_mt = math.sin(math.radians(10))
        cos_mt = math.sqrt(1-sin_mt**2)
        self.bench_press_distance = float(lengthofarm) * cos_mt
