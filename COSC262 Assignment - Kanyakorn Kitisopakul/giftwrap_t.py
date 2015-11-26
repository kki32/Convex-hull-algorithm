import numpy as np
import matplotlib.pyplot as plt
import sys

def theta(pointA, pointB):
    """The function returns the angle between two given points. Special case when t = 0 for Giftwrap algorithm"""
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        t = 0
    else:
        # 1.0 is there to make sure the numerator is not integer
        t = 1.0 * dy/((abs(dx)) + abs(dy))
    if dx < 0:
        t = 2 - t
    elif dy < 0:
        t = 4 + t
    if t == 0:
        return 360.00
    else:
        return t*90


def giftwrap_t(pts_array):
    """This function takes an array of points and returns the points which form convex hull from using the Giftwrap algorithm"""

    # find point with mininum y value     
    min_pt = [float('inf'), float('inf')]
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

#open list
file = open(sys.argv[1])
#Uncomment if want to open directly from Wing ide
#file = open('T6.dat')
n = int(file.readline())

#process from file to list that can be used to test the algorithm
list_to_test = []
for i in range(n):
    point = (file.readline().strip().split(" "))
    point[0] = int(point[0])
    point[1] = int(point[1])
    list_to_test.append(point)
    
#print list to test
print("The lists to be tested")
print(list_to_test)
sol = giftwrap_t(list_to_test)
#find position for the point in convex hull
convex_vertices = []
for j in range(len(sol)):
    convex_vertices.append(list_to_test.index(sol[j]))
print("Vertices for convex hull")
print(convex_vertices)

#uncomment if want graph
#draw_graph(list_to_test, sol)