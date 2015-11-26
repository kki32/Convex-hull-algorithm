import numpy as np
import matplotlib.pyplot as plt
import sys

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
    ans = lineFn(ptA, ptB, ptC) > 0
    return ans

def grahamscan_t(pts_array):
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
    sorted_array = sorted(sorted_array, key=lambda angle: angle[2])
    
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
    for j in range(len(sol)):
        solx.append(sol[j][0])
        soly.append(sol[j][1])
    figure = plt.figure()
    plt.axis([-100,1100,-100,1100])
    plt.plot(testx, testy, 'bo', solx, soly, 'r--')
    
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
#file = open('T1.dat')
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
sol = grahamscan_t(list_to_test)

#find position for the point in convex hull
convex_vertices = []
for j in range(len(sol)):
    convex_vertices.append(list_to_test.index(sol[j]))
print("Vertices for convex hull")
print(convex_vertices)

#uncomment if want to see graph
#draw_graph(list_to_test, sol)