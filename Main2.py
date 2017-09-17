import generate_map
#import ShowMap
import numpy as np
import matplotlib.pyplot as plt
import math as mth
import random as rd
import time
import integrated
import Sequential

exitFlag = False
while(exitFlag == False):
    print("Please input your choice:")
    print("1. Create a new map")
    print("2. Execute A* (WA* etc)")
    print("3. Print Map (and Path)")
    print("4. Sequential Search")
    print("5. Integrated Search")
    print("6. Exit\n")

    userInput1 = raw_input("Enter your choice: ")

    if userInput1 == '1':
        #userInput2 = raw_input("How many maps would you like to create?: ")
        #userInput4 = raw_input("How many different starting and goal pairs?: ")
        userInput3 = raw_input("Name of file?: ")
        #for i in range(int(float(userInput2))):
        generate_map.map_parser(userInput3)
    elif userInput1 == '2':
        execfile('AstarWeighted.py')
    elif userInput1 == '4':
        #ShowMap.PrintMap()
        execfile('Sequential.py')
    elif userInput1 == '5':
        #ShowMap.PrintMap()
        execfile('integrated.py')
    elif userInput1 == '3':
        #ShowMap.PrintMap()
        execfile('ShowMap.py')
    elif userInput1 == '6':
        exitFlag = True
    else:
        print("Invalid option , choose again")
