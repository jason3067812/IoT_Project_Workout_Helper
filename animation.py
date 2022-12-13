from vpython import *
import numpy as np


toRad = 2*np.pi/360
toDeg = 1/toRad
toVirtual = 0.1

scene.range = 15
scene.forward = vector(-1,-1,-1)
scene.width = 100
scene.height = 100

class Bench_press_anims:
    def __init__(self):
        self.excercise_name = text(pos=vector(-9.5,11,0),text='Bench Press', align='center', color=color.yellow)
        self.excercise_name.rotate(angle=90*toRad,axis=vector(0,1,0))
        self.bench_top = box(pos=vector(0,2,-1),width=5,height=.25,length=2,color=color.black)
        self.bench_leg1 = box(pos=vector(-.875,1,1.375),width=.25,height=2,length=.25,color=color.black)
        self.bench_leg2 = box(pos=vector(.875,1,1.375),width=.25,height=2,length=.25,color=color.black)
        self.bench_leg3 = box(pos=vector(-.875,1,-3.375),width=.25,height=2,length=.25,color=color.black)
        self.bench_leg4 = box(pos=vector(.875,1,-3.375),width=.25,height=2,length=.25,color=color.black)
        self.head = ellipsoid(pos=vector(0,2.5,0.75),width=1,height=.75,length=1,color=color.white)
        self.upper_body = ellipsoid(pos=vector(0,2.5,-1),width=2.5,height=.75,length=1.25,color=color.white)
        self.left_leg = ellipsoid(pos=vector(-.4,2.375,-2.875),width=1.25,height=.5,length=.5,color=color.white)
        self.left_leg.rotate(angle=20*toRad,axis=vector(0,1,0))
        self.right_leg = ellipsoid(pos=vector(.4,2.375,-2.875),width=1.25,height=.5,length=.5,color=color.white)
        self.right_leg.rotate(angle=-20*toRad,axis=vector(0,1,0))
        self.bench_press_objects_compound = compound([self.bench_top, self.bench_leg1,self.bench_leg2,
            self.bench_leg3,self.bench_leg4,self.head,self.upper_body,self.left_leg,self.right_leg])
    def invisible(self):
        self.excercise_name.visible = False
        self.bench_press_objects_compound.visible = False
    def visible(self):
        self.excercise_name.visible = True
        self.bench_press_objects_compound.visible = True
        
class Squat_anims:
    def __init__(self):
        self.excercise_name = text(pos=vector(-9.5,11,0),text='Squat', align='center', color=color.yellow)
        self.excercise_name.rotate(angle=90*toRad,axis=vector(0,1,0))
        self.head = ellipsoid(pos=vector(0,3.5,0.375),width=.75,height=1,length=1,color=color.white)
        self.upper_body = ellipsoid(pos=vector(0,2,0.375),width=.75,height=2.5,length=1.25,color=color.white)
        self.left_upperarm = ellipsoid(pos=vector(-0.75,2.625,0.2),width=.25,height=1,length=.25,color=color.white)
        self.left_upperarm.rotate(angle=-45*toRad,axis=vector(0,0,1))
        self.left_upperarm.rotate(angle=35*toRad,axis=vector(1,0,0))
        self.right_upperarm = ellipsoid(pos=vector(0.75,2.625,0.2),width=.25,height=1,length=.25,color=color.white)
        self.right_upperarm.rotate(angle=45*toRad,axis=vector(0,0,1))
        self.right_upperarm.rotate(angle=35*toRad,axis=vector(1,0,0))
        self.squat_objects_compound = compound([self.left_upperarm, self.right_upperarm,
            self.head,self.upper_body])
        self.squat_objects_compound.pos = vector(0,2.375,0.375)
    def update(self,sensor):
        self.squat_objects_compound.pos = vector(0,sensor.distance*toVirtual+3.375,0.375)
    def invisible(self):
        self.excercise_name.visible = False
        self.squat_objects_compound.visible = False
    def visible(self):
        self.excercise_name.visible = True
        self.squat_objects_compound.visible = True
    
# General Animation Objects
ground = box(pos=vector(0,-0.5,0),width=20,height=1,length=20,color=vector(0.72,0.42,0),
            texture={'file':'https://i.imgur.com/vXDWqIH.jpeg'})
wall_left = box(pos=vector(-10,10,0),width=20,length=1,height=20,color=vector(0.72,0.42,0),
                texture={'file':'https://i.imgur.com/vXDWqIH.jpeg'})
wall_right = box(pos=vector(0,10,-10),width=1,height=20,length=20,color=vector(0.72,0.42,0),
                texture={'file':'https://i.imgur.com/vXDWqIH.jpeg'})

unbalanced_text = text(pos=vector(0,10,-9.5),text='!UNBALANCED!', align='center', color=color.red)
unbalanced_text.visible = False
rest_text = text(pos=vector(0,5,-9.5),text='RESTING', align='center', color=color.green)
rest_text.visible = False
time_up_text = text(pos=vector(0,5,-9.5),text='TIME UP', align='center', color=color.red)
time_up_text.visible = False
rest_time_bar = box(pos=vector(0,4,-9.5),width=.25,height=1,length=0,color=color.green)
rest_time_bar.visible = False
L = label(pos=vector(-9.5,10,0),text='',box=False,height=30,opacity=0)

bar = cylinder(pos=vector(.5,0,0),length=6,color=color.gray(.6),radius=.1)
weight_left = cylinder(length=.5,color=color.gray(.6),radius=1)
weight_right = cylinder(pos=vector(6.5,0,0),length=.5,color=color.gray(.6),radius=1)
left_hand = sphere(pos=vector(2,0,0),radius=.25,color=color.white)
right_hand = sphere(pos=vector(5,0,0),radius=.25,color=color.white)
left_forearm = ellipsoid(pos=vector(2.1875,-0.375,0),width=.25,height=.75,length=.25,color=color.white)
left_forearm.rotate(angle=45*toRad,axis=vector(0,0,1))
right_forearm = ellipsoid(pos=vector(4.8125,-0.375,0),width=.25,height=.75,length=.25,color=color.white)
right_forearm.rotate(angle=-45*toRad,axis=vector(0,0,1))
barbell_anim = compound([bar, weight_left,weight_right,left_hand,right_hand,left_forearm,right_forearm])
barbell_anim.axis = vector(1,0,0)
barbell_anim.pos = vector(0,3,0)
barbell_anim.visible = False


def bench_press_anims_update(sensor,user):
    # update animation according to tilt and distance
    k = vector(cos(sensor.yaw*toRad)*cos(sensor.pitch*toRad),sin(sensor.pitch*toRad),
    sin(sensor.yaw*toRad)*cos(sensor.pitch*toRad))
    barbell_anim.axis=k
    if sensor.distance < user.bench_press_distance:
        barbell_anim.pos = vector(0,3+sensor.distance*toVirtual,0)
    else:
        barbell_anim.pos = vector(0,3+user.bench_press_distance*toVirtual,0)
    L.text = 'Set:{}\nRep:{}'.format(user.set_count,user.rep_count)
    


def squat_anims_update(sensor,user):
    # update animation according to tilt and distance
    k = vector(cos(sensor.yaw*toRad)*cos(sensor.pitch*toRad),sin(sensor.pitch*toRad),
    sin(sensor.yaw*toRad)*cos(sensor.pitch*toRad))
    barbell_anim.axis=k
    barbell_anim.pos = vector(0,sensor.distance*toVirtual+4,0)
    L.text = 'Set:{}\nRep:{}'.format(user.set_count,user.rep_count)
    

def unbalance_detect(sensor,barbell):
    # if barbell is unbalanced
    if abs(sensor.pitch) > 5 or (sensor.yaw > 5 and sensor.yaw < 180) \
    or (sensor.yaw < 355 and sensor.yaw > 180):
        unbalanced_text.visible = True
        barbell.unbalanced = True
    else:
        unbalanced_text.visible = False
        barbell.unbalanced = False    

def rest_anims(user):
    if user.resting:
        rest_text.visible = True
        rest_time_bar.visible = True
        rest_time_bar.length = 0.05*user.rest_counter
        if user.rest_counter > user.rest_time - 20 and \
            user.rest_counter < user.rest_time - 10:
            rest_time_bar.color = color.yellow
        elif user.rest_counter >= user.rest_time - 10:
            rest_time_bar.color = color.red
        else:
            rest_time_bar.color = color.green
    else:
        rest_text.visible = False
        rest_time_bar.visible = False
    if user.alarming: 
        time_up_text.visible = True
    else:
        time_up_text.visible = False