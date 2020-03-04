# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 21:25:54 2019

@author: zuq31
"""

import VBASim
import Basic_Classes as bc
import RNG
import numpy as np
import pandas as pd

TheQueues = []
TheResources = []
TheDTStats = []
TheCTStats = []

# Define objects for this simulator
ParkingLot  = bc.FIFOQueue()
MaxCars = 0 # This is an integer type statistic that keeps track of the maximum number of cars in the garage
TimeSpent = bc.DTStat()
Calendar = bc.EventCalendar()

TheQueues.append(ParkingLot)
TheDTStats.append(TimeSpent)

# These are needed to collect across-replication outputs
AllAverageQueues = []
AllMaxCars = []
AllTimeSpent = []

# File output
f = open('MMInfoutput.txt','w')
f.write("Rep\t Average Number\t Max Number\t Average Time Spent\n")

# Here, we import data from the CSV file
PCrate = [] # for piece-wise constant arrival rates
Data = pd.read_excel('CarCounts.xlsx',usecols = range(0,8,1))
Data.columns = range(0,8,1)
for col in range(0,8,1):
    PCrate.append(np.mean(Data[col]))
    
maxRate = max(PCrate)

# Constants for the input models
MeanTBA = 1/maxRate
MeanPT = 1.0

def NextInterarrival():
    # This is a function creating the time between arrivals according to the piece-wise constant rate function fitted from data
    A = RNG.Expon(MeanTBA,1)
    S = Clock + A
    if S > 8: # This is to avoid the index out of range error
        return A
    
    while RNG.Uniform(0,1,3) > PCrate[int(S)]/maxRate:
        S = S + RNG.Expon(MeanTBA,1)
        if S > 8: 
            break
    return S - Clock

def Arrival():
    NewCar = bc.Entity(Clock)
    ParkingLot.Add(NewCar,Clock)
    VBASim.Schedule(Calendar,"Arrival",NextInterarrival(),Clock)
    VBASim.Schedule(Calendar,"Departure",RNG.Expon(MeanPT,2),Clock)
    global MaxCars
    if ParkingLot.NumQueue()>MaxCars:
        MaxCars = ParkingLot.NumQueue()
    
def Departure():
    DepartingCar = ParkingLot.Remove(Clock)
    TimeSpent.Record(Clock-DepartingCar.CreateTime)


for reps in range(0,2000,1):
    Clock = 0.0
    MaxCars = 0
    VBASim.VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources,Clock)
    VBASim.Schedule(Calendar,"Arrival",NextInterarrival(),Clock)
    VBASim.Schedule(Calendar,"EndSimulation",8,Clock)
    
    NextEvent = Calendar.Remove()
    Clock = NextEvent.EventTime
    if NextEvent.EventType == "Arrival":
        Arrival()
    elif NextEvent.EventType == "Departure":
        Departure()
    
    while NextEvent.EventType != "EndSimulation":
        NextEvent = Calendar.Remove()
        Clock = NextEvent.EventTime
        if NextEvent.EventType == "Arrival":
            Arrival()
        elif NextEvent.EventType == "Departure":
            Departure()
            
    AllAverageQueues.append(ParkingLot.Mean(Clock))
    AllMaxCars.append(MaxCars)
    AllTimeSpent.append(TimeSpent.Mean())
    #print(reps+1,ParkingLot.Mean(Clock),MaxCars,TimeSpent.Mean())
    f.write(str(reps+1)+"\t"+str(ParkingLot.Mean(Clock))+"\t"+str(MaxCars)+"\t"+str(TimeSpent.Mean())+"\n")
    
print(np.mean(AllAverageQueues))
print(np.std(AllAverageQueues))
print(np.mean(AllMaxCars))
print(np.std(AllMaxCars))
print(np.mean(AllTimeSpent))
print(np.std(AllTimeSpent))

#f.write(str(np.mean(AllAverageQueues)))
#f.write(str(np.std(AllAverageQueues)))
#f.write(str(np.mean(AllMaxCars)))
#f.write(str(np.std(AllMaxCars)))
#f.write(str(np.mean(AllTimeSpent)))
#f.write(str(np.std(AllTimeSpent)))

f.close()


