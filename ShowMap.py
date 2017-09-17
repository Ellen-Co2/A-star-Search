import numpy as np
import matplotlib.pyplot as plt
import math as mth
fig = plt.figure()
mr = raw_input("Enter name of map file: ")
mr = mr + ".txt"
Mapplot = np.loadtxt(mr, skiprows=8, delimiter=',', dtype="S4")
ask = raw_input(" Add Path?  hit enter skip,1:yes =>> ")
print("Does the map path file have hval and gval values?")
print("1. Yes")
print("2. No")
valueCheck = raw_input("Enter choice here: ")

def PrintMap(Mapplot=Mapplot, ask = ask,valueCheck=valueCheck):
    if (ask == "1"):
        pf = raw_input("Enter name of map path file: ")
        pf = pf + ".txt"
        path = np.loadtxt(pf, skiprows=1, dtype="float")
        pathArray = []
        if (valueCheck == "1"):
            for i in range(0, len(path)):
                [xPath, yPath, gval, hval] = path[i]
                xPath1 = int(float(xPath))
                yPath1 = int(float(yPath))
                pathArray.append([xPath1, yPath1, hval, gval])
            start = path[0]
            goal = path[-1]
            for i,j,h,g in pathArray:
                #print i,j,h,g
                if  (i == start[0]) and (j == start[1]):
                    Mapplot[int(i)][int(j)] = "4"
                elif (i == goal[0]) and (j== goal[1]):
                    Mapplot[int(i)][int(j)] = "8"
                else:
                    Mapplot[int(i)][int(j)] = "5"
        
        else:    
            start = path[0]
            #print start[0]
            end = path[-1]
            #print end[0]
            for i,j in path:
                if  (i == start[0]) and (j == start[1]):
                    Mapplot[int(i)][int(j)] = "4"
                elif (i == end[0]) and (j== end[1]):
                    Mapplot[int(i)][int(j)] = "8"
                else:
                    Mapplot[int(i)][int(j)] = "5"

    for i in range(Mapplot.shape[0]):
        for j in range(Mapplot.shape[1]):
            if Mapplot[i][j] in set(["1","2","0","5","4","8"]): # 1: normal 2: hard 0: blocked 5: path 4:start 8:goal
                Mapplot[i][j] = int(Mapplot[i][j])# 3: highway 1 6: highway 2
            elif Mapplot[i][j][0] == "a":
                Mapplot[i][j] = 6
            elif Mapplot[i][j][0] == "b":
                Mapplot[i][j] = 3
            else:
                Mapplot[i][j] = 9 # just in case
    mapdata = Mapplot.astype(np.int32)
    #fig = plt.
    plt.imshow(mapdata, interpolation='nearest', cmap='jet')
    plt.colorbar()
    print("Save Map?")
    print("1. Yes")
    print("2. No")
    ans = raw_input("Enter choice=>> ")
    ans = int(float(ans))
    if ans == 1:
        ask = raw_input("Save file as: ")
        plt.savefig(str(ask) + '.png', dpi=300)
    else:
        pass
    plt.show()
    return pathArray
    
pathArray = PrintMap(Mapplot,ask,valueCheck)
coords = []
def onclick(event):
    global x, y
    x, y =event.xdata, event.ydata
    xi = mth.floor(x)
    yi = mth.floor(y)
    xi = int(xi)
    yi = int(yi)
    if valueCheck == 1:
        for xPath, yPath, gval, hval in pathArray:
            if (xi == xPath )and (yi == yPath):
                print("gval: " + str(gval) + " hval: " + str(hval))
    #print (xi, yi)
    global coords
    coords.append((x, y))

    if len(coords) == 1000:
        fig.canvas.mpl_disconnect(cid)

    return coords

cid = fig.canvas.mpl_connect('button_press_event', onclick)
'''
[xPath, yPath] = path[i]
        xPath1 = int(float(xPath))
        yPath1 = int(float(yPath))
        Mapplot[xPath1][yPath1] = '7'

    mapdata = []
    for i in range(120):
        mapdata.append([])
        for j in range(160):
            mapdata[i].append([])

    for i in range(0, 120):
        for j in range(0, 160):
            if map[i][j] == 'a':
                mapdata[i][j] = 3
            elif map[i][j] == 'b':
                mapdata[i][j] = 4
            elif map[i][j] == '1':
                mapdata[i][j] = 1
            elif map[i][j] == '2':
                mapdata[i][j] = 2
            elif map[i][j] == '0':
                mapdata[i][j] = 0
            elif map[i][j] == '3':
                mapdata[i][j] = 3
            elif map[i][j] == '4':
                mapdata[i][j] = 4
            elif map[i][j] == '7':
                mapdata[i][j] = 5
            else:
                mapdata[i][j] = 9
'''
    
