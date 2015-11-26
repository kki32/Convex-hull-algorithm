import numpy as np
import matplotlib.pyplot as plt
import sys
import random
import time 

def theta(pointA, pointB):
    """The function returns the angle between two given points"""
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        t = 0
    else:
        t = 1.0*dy/((abs(dx)) + abs(dy))
    if dx < 0:
        t = 2 - t
    elif dy < 0:
        t = 4 + t
    return t*90
    
def lineFn(ptA, ptB, ptC):
    """Given three points, the function finds the value which could be used to determine which sides the third point lies"""
    val1 = (ptB[0]-ptA[0])*(ptC[1]-ptA[1])
    val2 = (ptB[1]-ptA[1])*(ptC[0]-ptA[0])
    ans = val1 - val2
    return ans 

def isCCW(ptA, ptB, ptC):
    """Return True if the third point is on the left side of the line from ptA to ptB and False otherwise"""
    ans = lineFn(ptA, ptB, ptC)
    return ans > 0

def find_distance(pointA, pointB):
    """The function takes two points with x and y values and return the distance between two points."""
    delta_x = pointB[0] - pointA[0]
    delta_y = pointB[1] - pointA[1]
    distance = ((delta_x**2) + (delta_y**2))**1/2
    if distance < 0:
        print('neg')
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

def modified_merge_sort(alist, p0):
    """Merge sort from interactivepython website. The function is modified to sort the points according to their angle"""

    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        modified_merge_sort(lefthalf, p0)
        modified_merge_sort(righthalf, p0)

        i=0
        j=0
        k=0
        while i<len(lefthalf) and j<len(righthalf):
            if lefthalf[i][2]<righthalf[j][2]:
                alist[k]=lefthalf[i]
                i=i+1    
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i<len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j<len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

def grahamscan_e(pts_array):
    """This function takes an array of points and returns the points which form convex hull from using Graham-scan algorithm"""
    
    #find p0
    p0 = [float('inf'), float('inf')]
    for i in range(len(pts_array)):
        if pts_array[i][1] < p0[1]:
            p0 = pts_array[i]
        elif pts_array[i][1] == p0[1]:
            if pts_array[i][0] >  p0[0]:
                p0 = pts_array[i]
                
    #find angle between p0 and other points
    sorted_array = []    
    for j in range(0, len(pts_array)):
        sorted_array.append([pts_array[j][0], pts_array[j][1], theta(p0, pts_array[j])])
        
    #sorting step
    modified_merge_sort(sorted_array, p0)
    
    #special case - when first three points are collinear
    #sorted_array = []
    #unique_angle = []
    #for k in range(0, len(array)):
        #if array[k][2] not in unique_angle:
            #sorted_array.append(array[k])
            #unique_angle.append(array[k][2])
        #else:
            #if find_distance(p0, array[k]) > find_distance(p0, sorted_array[-1]):
                #sorted_array.pop()
                #sorted_array.append(array[k]) 
                
    #construct convex hull
    stack = sorted_array[0:3]
    for ii in range(3, len(sorted_array)):
        while not (isCCW(stack[-2], stack[-1], sorted_array[ii])):
            stack.pop()
        stack.append(sorted_array[ii])    
    
    #remove angle from arrays
    sol = []
    for jj in range(len(stack)):
        sol.append([stack[jj][0], stack[jj][1]])    
        
    return sol

def draw_graph(list_to_test, sol):
    """The function takes list of points and points on convex hull to graph the convex hull"""
    testx = []
    testy = []
    solx = []
    soly = []
    for i in range(len(list_to_test)):
        testx.append(list_to_test[i][0])
        testy.append(list_to_test[i][1])
    #for j in range(len(sol)):
        #solx.append(sol[j][0])
        #soly.append(sol[j][1])
    figure = plt.figure()
    plt.axis([-100,1100,-100,1100])
    #plt.plot(testx, testy, 'bo', solx, soly, 'r--') 
    plt.plot(testx, testy, 'bo')

def analyse_time(size_to_test, no_of_trials):
    """This function takes list of array and number of trials as argument. It prints time taken to perfrom giftwrap algorithm for given lists"""
    
    if sys.version_info < (3, 3):
        get_time = time.clock
    else:
        get_time = time.perf_counter
        REZ = time.get_clock_info('perf_counter').resolution   

    list_to_test = generate_random_array(size_to_test)
    start = get_time()
    sol = grahamscan_e(list_to_test)
    end = get_time()

        
    time_taken_per_locate = end-start
    print('finish timing for array with {} random points'.format(size_to_test))
    
    #Uncomment if want graph
    #draw_graph(list_to_test, sol)
    
    print(size_to_test)
    print(time_taken_per_locate)
    return time_taken_per_locate

def main():
    no_of_pts = []
    time_taken = []    
    list_of_sizes = list(range(1000, 20001, 1000))
    no_of_trials = 1
    
    for i in range(len(list_of_sizes)):
        no_of_pts.append(list_of_sizes[i])
        time_taken.append(analyse_time(list_of_sizes[i], no_of_trials))
    print(no_of_pts)
    print(time_taken)

#main()
list_to_test = [[4,4],[3,3],[2,2],[0,0],[2, 4]]
a = [[0,0]]
#a = grahamscan_e(list_to_test)
draw_graph(list_to_test, a)