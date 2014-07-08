
from scipy import *
import numpy as np
from math import *
import pdb
import pylab as pl
debug = False

            


#Given three sequential measurements, this function estimates the bearing of
#the robot at the third measurement and the amount (in radians) the robot turned 
# at measurement 2
def calculate_bearing_turning(measurement1, measurement2, measurement3):


    x1 = measurement1[0]
    y1 = measurement1[1]
    x2 = measurement2[0]
    y2 = measurement2[1]
    x3 = measurement3[0]
    y3 = measurement3[1]


    #Calculate the bearing between measurement 1, measurement 2. Domain [0, 2pi]
    if(x2-x1)==0:
        if(y2>y1):
            HA1 = pi/2
        else:
            HA1 = -pi/2
    else:
        HA1 = atan( (y2-y1)/(x2-x1) )

    if (x2<x1):
        HA1 += pi

    #Calculate the bearing between measurement 2, measurement 3. Domain [0, 2pi]
    if (x3-x2)==0:
        if(y3>y2):
            HA2 = pi/2
        else:
            HA2 = -pi/2
    else:
        HA2 = atan( (y3-y2)/(x3-x2) )
    if (x3<x2):
        HA2 += pi

    #The turning angle is equal to the difference in these angles. Domain (-pi, pi]
    turning = (HA2 - HA1)
    
    while turning <= -pi :
        turning += 2*pi
    while turning > pi:
        turning -= 2*pi

    #Calculate the new bearing. Domain [0,2pi]
    bearing = (HA2+turning)%(2*pi)

    return [bearing, turning]

# Returns a boolean. True denotes that the given point is within a tolerance of the box's walls.
def is_near_wall(measurement):
    x_lower_boundary = 180
    y_lower_boundary = 100
    x_upper_boundary = 665
    y_upper_boundary = 410

    if (measurement[0] > x_upper_boundary): 
        return True
    if (measurement[1] > y_upper_boundary): 
        return True
    if (measurement[0] < x_lower_boundary): 
        return True
    if (measurement[1] < y_lower_boundary): 
        return True

    return False

# This code was taken from given code in the Runaway Robot project and computes the distance between points
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


#Misread measurements in the given data files are represented as [-1,-1]. This function takes up to 3 measurements as 
#input. Returns true if no measurements are misread; returns false if any measurement is misread. 
def contains_misread_measurement(measurement1, measurement2 = [0,0], measurement3 = [0,0]):

    if measurement1[0] == -1: 
        return True
    if measurement2[0] == -1: 
        return True
    if measurement3[0] == -1: 
        return True

    return False

# Takes as input: 'testing_video-centroid_data' or 'training_video1-centroid_data'.
# Returns the list of measurements contained in the given file name
def import_file(filename_string):
    f = open(filename_string)
    f.next()
    string_lines = []
    float_lines = []

    for line in f:
        string_lines.append(line.strip().strip(','))
    for item in string_lines :
        float_lines.append(item.split())
    for i in float_lines:
        i[0]=i[0].strip('[')
        i[0]=i[0].strip(',')
        i[1]=i[1].strip(']')
    for i in float_lines:
        i[0] = float(i[0])
        i[1] = float(i[1])

    return float_lines

# Produces graphs corresponding to data in the training data set given
def analyze_data_far_from_wall():
    measurements = import_file('training_video1-centroid_data')
    radians_turned = []
    radians_x = []
    distances_traveled = []
    distance_x = []
    
    # Collects data regarding how much the hexbug turns from frame to frame
    for i in range(len(measurements)):
        if i+2<len(measurements):
            measurement1 = measurements[i] 
            measurement2 = measurements[i+1]
            measurement3 = measurements[i+2]
        if not contains_misread_measurement(measurement1, measurement2, measurement3):
            if not (is_near_wall(measurement1) and is_near_wall(measurement2) and is_near_wall(measurement3)):
                [bearing,turning] = calculate_bearing_turning(measurement1, measurement2, measurement3)
                if debug:
                    if (turning>2.5 or turning<-2.5):
                        print("Turning angle is huge for the ", i, "th point")
                # Ignores erratic turning behavior (turns>2 radians between measurements)
                if(turning<2 and turning>-2):
                    radians_x.append(i)
                    radians_turned.append(turning)

    # Collects data regarding how far the hexbug moves from frame to frame                 
    for i in range(len(measurements)):
        if i+2<len(measurements):
            measurement1 = measurements[i] 
            measurement2 = measurements[i+1]
        if not contains_misread_measurement(measurement1, measurement2, [0,0]):
            if not (is_near_wall(measurement1) and is_near_wall(measurement2)):
                distance = distance_between(measurement1, measurement2)
                
                if debug:
                    if(distance>30):
                        print("Distance is greater than 100 for the ", i, "th point")
                #Ignores erratic velocity behavior (>30 pixels between measurements)
                if (distance<30):
                    distance_x.append(i)
                    distances_traveled.append(distance)  



    pl.subplot(221)
    pl.plot(radians_x, radians_turned)
    pl.xlabel("Frame/Measurement Number")
    pl.ylabel("Radians Turned")

    pl.subplot(222)
    pl.plot(distance_x,distances_traveled)
    pl.xlabel("Frame/Measurement Number")
    pl.ylabel("Velocity / Pixels Traveled")


    pl.subplot(223)
    pl.hist(radians_turned)
    pl.xlabel("Distribution of Radians Turned")

    pl.subplot(224)
    pl.hist(distances_traveled)
    pl.xlabel("Distribution of Velocities")
    pl.show()



def analyze_data_near_wall():
    measurements = import_file('training_video1-centroid_data')
    near_wall = []
    near_wall_grouped = []
    counter = 0

    for i in range(len(measurements)):
        meas1 = measurements[i]
        if not contains_misread_measurement(meas1):
            if is_near_wall(meas1):
                near_wall.append([i,meas1])

    #Further code to be added to 



analyze_data_near_wall()
analyze_data_far_from_wall()


