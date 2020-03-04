# -*- coding: utf-8 -*-
"""
Created on Thu March 1 21:45:23 2019

@author: zuq31
"""
#import libraries
import VBASim
import Basic_Classes as bc
import RNG
import numpy as np

#initialize variables
TheQueues = []
TheResources = []
TheDTStats = []
TheCTStats = []

#create instances of objects
ParkingLot = bc.FIFOQueue()
MaxCars = 0
TimeSpent = bc.DTStat()
Calendar = bc.EventCalendar()

TheQueues.append(ParkingLot)
TheDTStats.append(TimeSpent)

AllAverageQueues = []
AllMaxCars = []
AllTimeSpent = []

print("Rep","Average Number","Max Number","Average Time Spent")

MeanTBA = 0.021 #for stationary Poisson arrival
#MeanTBA = 0.03312 #for nonstationary Poisson arrival
MeanPT = 1.0

def Arrival():
    NewCar = bc.Entity(Clock)
    ParkingLot.Add(NewCar,Clock)
    VBASim.Schedule(Calendar,"Arrival",RNG.Expon(MeanTBA,1),Clock)
    VBASim.Schedule(Calendar,"Departure",RNG.Expon(MeanPT,2),Clock)
    global MaxCars
    if ParkingLot.NumQueue() > MaxCars:
            MaxCars = ParkingLot.NumQueue()
    
def Departure():
    DepartingCar = ParkingLot.Remove(Clock)
    TimeSpent.Record(Clock-DepartingCar.CreateTime)
    
for reps in range(0,2000,1):
    Clock = 0.0
    MaxCars = 0
    VBASim.VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources,Clock)
    VBASim.Schedule(Calendar,"Arrival",RNG.Expon(MeanTBA,1),Clock)
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
    print(reps+1,ParkingLot.Mean(Clock),MaxCars,TimeSpent.Mean())

print(np.mean(AllAverageQueues))
print(np.std(AllAverageQueues))
print(np.mean(AllMaxCars))
print(np.std(AllMaxCars))
print(np.quantile(AllMaxCars,.9))
    
    
    
    