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

#MeanTBA = 0.021 #for stationary Poisson arrival
MeanTBA = 0.03312 #for nonstationary Poisson arrival
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
          #add those ifs for nonstationary, erase them for stationary            
          if Clock > 1 and Clock <=2:
              MeanTBA = 0.0257903
          elif Clock > 2 and Clock <=3:
              
              MeanTBA = 0.01701427
          elif Clock > 3 and Clock <=4:
              MeanTBA = 0.012581169
          elif Clock > 4 and Clock <=5:
              MeanTBA = 0.0137553
          elif Clock > 5 and Clock <=6:
              MeanTBA = 0.025368
          elif Clock > 6 and Clock <=7:
              MeanTBA = 0.024257
          elif Clock > 7 and Clock <=8:
              MeanTBA = 0.049919
        
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
    
    
    
    