import numpy as np
import matplotlib.pyplot as plt
import sys
import random
import time

def theta(pointA, pointB):
    """The function returns the angle between two given points. Special case when t = 0 for Giftwrap algorithm"""
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        t = 0
    else:
        # 1.0 is there to make sure the numerator is not integer
        t = 1.0 * dy / ((abs(dx)) + abs(dy))
    if dx < 0:      
        t = 2 - t
    elif dy < 0:
        t = 4 + t
    if t == 0:
        return 360.00
    else:
        return t * 90
    
def find_distance(pointA, pointB):
    """The function takes two points with x and y values and return the distance between two points."""
    delta_x = pointB[0] - pointA[0]
    delta_y = pointB[1] - pointA[1]
    distance = ((delta_x**2) + (delta_y**2))**1/2
    return abs(distance)
    
def circular_distribution(x, y):
    """Return True if the point satisfies the condition and False otherwise"""
    x_term = (x-500)**2
    y_term = (y-500)**2
    return  (x_term + y_term) < 250000

def generate_random_array(array_sizes):
    """Generate array with random points for a given sizes"""
    pts_array = {}
    for ii in range(array_sizes):
        random_x = random.randrange(0, 1000)
        random_y = random.randrange(0, 1000)
        
        #Uncomment line below and comment while line when want
        #circular_distribution, otherwise it is rectangular distribution
        #while[random_x,random_y] in pts_array.values() or circular_distribution(random_x, random_y) == False:
        
        #check if the point is unique in the list
        while [random_x, random_y] in pts_array.values():
            random_x = random.randrange(0, 1000)
            random_y = random.randrange(0, 1000)                      
        pts_array[ii] = [random_x , random_y]                         
    return list(pts_array.values())   

def giftwrap_e(pts_array):
    """This function takes an array of points and returns the points which form convex hull."""
    # find point with mininum y value
    min_pt = [float('inf'),float('inf')]
    for point in range(len(pts_array)):
        if pts_array[point][1] < min_pt[1]:
            min_pt = pts_array[point]
            k = point
        # if more than one, select the rightmost point
        elif pts_array[point][1] == min_pt[1]:
            if pts_array[point][0] > min_pt[0]:
                min_pt = pts_array[point]
                k = point

    pts_array_copy = list(pts_array)
    pts_array_copy.append(min_pt)
    n = len(pts_array_copy) - 1
    
    solution = []
    index = 0
    previous_angle = 0    
    
    #giftwrap algorithm
    while k != n:
        pts_array_copy[index], pts_array_copy[k] = pts_array_copy[k], pts_array_copy[index]
        solution.append(pts_array_copy[index])
        minAngle = 361
        for ii in range(index + 1, n + 1):
            current_angle = theta(pts_array_copy[index], pts_array_copy[ii])
            if (current_angle < minAngle) and (current_angle > previous_angle) and (pts_array_copy[ii] != pts_array_copy[index]):
                minAngle = current_angle
                k = ii
            # deal with special case when the points are collinear
            elif current_angle == minAngle:
                if find_distance(pts_array_copy[index], pts_array_copy[ii]) > find_distance(pts_array_copy[index], pts_array_copy[k]):
                    minAngle = current_angle
                    k = ii
        index = index + 1
        previous_angle = minAngle
    
    return solution

def draw_graph(list_to_test, sol):
    """The function takes list of points and points on convex hull to graph the convex hull"""
    testx = []
    testy = []
    solx = []
    soly = []
    for i in range(len(list_to_test)):
        testx.append(list_to_test[i][0])
        testy.append(list_to_test[i][1])
    for j in range(len(sol)):
        solx.append(sol[j][0])
        soly.append(sol[j][1])
    figure = plt.figure()
    plt.axis([-100,1100,-100,1100])
    plt.plot(testx, testy, 'bo', solx, soly, 'r--')     

def analyse_time(size_to_test, no_of_trials):
    """This function takes list of array and number of trials as argument. It prints time taken to perfrom giftwrap algorithm for given lists"""
    
    if sys.version_info < (3, 3):
        get_time = time.clock
    else:
        get_time = time.perf_counter
        REZ = time.get_clock_info('perf_counter').resolution   

    total_time = 0  
    for trial in range(no_of_trials):
        list_to_test = generate_random_array(size_to_test)
        start = get_time()
        sol = giftwrap_e(list_to_test)
        end = get_time()
        total_time += (end - start)
    time_taken_per_locate = (1.0*total_time) / no_of_trials
    print('finish timing for array with {} random points'.format(size_to_test))
    
    #Uncomment if want graph
    #draw_graph(list_to_test, sol)
    
    print(size_to_test)
    #print(time_taken_per_locate)
    return time_taken_per_locate

def main():
    no_of_pts = []
    time_taken = []    
    list_of_sizes = list(range(1000, 20001, 1000))
    no_of_trials = 100
    
    for i in range(len(list_of_sizes)):
        no_of_pts.append(list_of_sizes[i])
        time_taken.append(analyse_time(list_of_sizes[i], no_of_trials))
    print(no_of_pts)
    print(time_taken)

main()