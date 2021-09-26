import sys
import numpy as np
import matplotlib.pyplot as plt
import getopt
from math import sin, cos, sqrt, atan2, radians
import math

#Open Read and Write File
#Read file will contain the coordinates of the Cities in Tennessee
#Write file will output the jgr file needed for jgraph
readCoordinates = open('grid.txt', 'r')
jgr = open('map.jgr', 'w')

#Read the Tennessee Map ppm File
readFile = open('ten.ppm', 'r')

#Read the Tennessee Map ppm File
one = ''
ppmGrid = [] #Store PPM as a matrix
for i, line in enumerate(readFile.readlines()):
    vals = []
    for j, val in enumerate(line.split()):
        if j % 3 == 0:
            if j != 0:
                vals.append(one)
            one = ''
        one = one + str(float(val)/255) + ' '
    ppmGrid.append(vals)

#Read the coordinates and store the longitude and latitude values in xs and ys. The city names will be stored in cities
xs = []
ys = []
cities = []

for line in readCoordinates:
    splitted = line.split(',')
    city = splitted[0]
    latitude = float(splitted[2])
    longitude = float(splitted[1])
    cities.append(splitted[0])
    xs.append(latitude)
    ys.append(longitude)

#initialize Variables, Initial City will be Nashville
city1 = 'Nashville'
city2 = ''
city2Check = False
zoom = .2

#Read the Command Line Arguments
argumentList = sys.argv[1:]
 
options = "a:b:z:"
 
long_options = ["city1 =", "city2 =", "zoom ="]
 
try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-a", "--city1"):
            city1 = currentValue
             
        elif currentArgument in ("-b", "--city2"):
            city2 = currentValue
            city2Check = True
             
        elif currentArgument in ("-z", "--zoom"):
            zoom = float(currentValue)
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))


#Start writing the jgr
jgr.write('newgraph\n')
print('newgraph\n')

#If the user wants to view the TNMap using jgr display it and write the jgr code
#print(len(ppmGrid))
#print(len(ppmGrid[0]))
if city1 == 'TNMap':
    for x, i in enumerate(ppmGrid):
        for y, j in enumerate(i):
            if x % 2 == 0 and y % 2 == 0:
                jgr.write('newcurve marktype box pts '+ str(y) + ' -' + str(x) + ' color ' + j + '\n')
                print('newcurve marktype box pts ' + str(y) + ' -' + str(x) + ' color ' + j)
    exit()


def dist(x1, y1, x2, y2):
    # R = 6373.0
    # x1r = radians(abs(x1))
    # y1r = radians(abs(y1))
    # x2r = radians(abs(x2))
    # y2r = radians(abs(y2))

    # dlong = y2r - y1r
    # dlat = x2r - x1r

    # a = sin(dlat/2)**2 + cos(x1r) * cos(x2r) * sin(dlong/2)**2
    # c = 2 * atan2(sqrt(a), sqrt(1-a))
    # distance = R*c
    # return distance
    lat1, lon1 = x1, y1
    lat2, lon2 = x2, y2
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    conv_fac = 0.621371
    d = d*conv_fac
    return d


#If the user would like to see the distance between two cities
if city2Check and city1 in cities and city2 in cities:
    idx1 = cities.index(city1)
    idx2 = cities.index(city2)
    latval1 = xs[idx1]
    longval1 = ys[idx1]
    latval2 = xs[idx2]
    longval2 = ys[idx2]
    minxval = min([latval1, latval2]) - .2
    maxxval = max([latval1, latval2]) + .2
    minyval = min([longval1, longval2]) - .2
    maxyval = max([longval1, longval2]) + .2
    midxval = min([latval1, latval2]) + abs(latval1-latval2)/2
    midyval = min([longval1, longval2]) + abs(longval1-longval2)/2
    jgr.write('\txaxis min ' + str(minxval) + ' max ' + str(maxxval) + ' size 7\n')
    jgr.write('\tyaxis min ' + str(minyval) + ' max ' + str(maxyval) + ' size 5\n\n')
    print('\txaxis min ' + str(minxval) + ' max ' + str(maxxval) + '\n')
    print('\tyaxis min ' + str(minyval) + ' max ' + str(maxyval) + '\n\n')
    jgr.write('newstring hjl vjc x ' + str(latval1) + ' y ' + str(longval1) + ' : ' + city1 + '\n')
    print('newstring hjl vjc x ' + str(latval1) + ' y ' + str(longval1) + ' : ' + city1 + '\n')
    jgr.write('newstring hjl vjc x ' + str(latval2) + ' y ' + str(longval2) + ' : ' + city2 + '\n')
    print('newstring hjl vjc x ' + str(latval2) + ' y ' + str(longval2) + ' : ' + city2 + '\n')
    d = dist(latval1, longval1, latval2, longval2)
    jgr.write('newstring hjl vjc x ' + str(midxval) + ' y ' + str(midyval) + ' : ' + str(d) + ' miles\n')
    print('newstring hjl vjc x ' + str(midxval) + ' y ' + str(midyval) + ' : ' + str(d) + ' miles\n')
    exit()

#If the user wants to see which cities are around a city they choose. They can specify the zoom
if city1 in cities:
    idx = cities.index(city1)
    latval = xs[idx]
    longval = ys[idx]
    minxval = float(latval - zoom)
    maxxval = float(latval + zoom)
    minyval = float(longval - zoom)
    maxyval = float(longval + zoom)

jgr.write('\txaxis min ' + str(minxval) + ' max ' + str(maxxval) + ' size 7\n')
jgr.write('\tyaxis min ' + str(minyval) + ' max ' + str(maxyval) + ' size 5\n\n')
print('\txaxis min ' + str(minxval) + ' max ' + str(maxxval) + '\n')
print('\tyaxis min ' + str(minyval) + ' max ' + str(maxyval) + '\n\n')

#Display cities based on zoom 
for city in cities:
    idx = cities.index(city)
    latval = xs[idx]
    longval = ys[idx]
    longf = float(latval)
    latf = float(longval)
    if latval > minxval and  latval < maxxval and longval > minyval and longval < maxyval:
        jgr.write('newstring hjl vjc x ' + str(latval) + ' y ' + str(longval) + ' : ' + city + '\n')
        print('newstring hjl vjc x ' + str(latval) + ' y ' + str(longval) + ' : ' + city + '\n')

