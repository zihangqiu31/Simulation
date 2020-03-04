# -*- coding: utf-8 -*-
"""
@author: zuq31
"""

#import libraries
import VBASim
import Basic_Classes as bc
import RNG
import numpy as np
import csv

Clock = 0.0
ZRNG = RNG.InitializeRNSeed()

#initialize variables
TheQueues = []
TheResources = []
TheDTStats = []
TheCTStats = []

WaitingList = bc.FIFOQueue()
WaitingTime = bc.DTStat()
Difference = bc.DTStat()
Calendar = bc.EventCalendar()
Server = bc.Resource()
TimeSpent = bc.DTStat()

TheQueues.append(WaitingList)
TheDTStats.append(WaitingTime)
TheDTStats.append(Difference)
TheResources.append(Server)

Server.SetUnits(3)
MeanTBA = 1.0
MeanST = 2.7
Phases = 2
RunLength = 10000
WarmUp = 250

#File output handler
f = open('MG3data.csv','w', newline='')
fwriter = csv.writer(f)
WTrecords = []

def Arrival():
    VBASim.Schedule(Calendar,"Arrival",RNG.Expon(MeanTBA,1),Clock)
    Customer = bc.Entity(Clock)
    
    if Server.Busy < Server.NumberOfUnits:
        Server.Seize(1,Clock)
        VBASim.SchedulePlus(Calendar,"EndOfService",RNG.Erlang(Phases,MeanST,2),Customer,Clock)
        WaitingTime.Record(0)
        WTrecords.append(0)
    else: 
        WaitingList.Add(Customer,Clock)
        
    
def EndOfService(DepartingCustomer):
    TimeSpent.Record(Clock-DepartingCustomer.CreateTime)

    if WaitingList.NumQueue() > 0:
        NextCustomer = WaitingList.Remove(Clock)
        VBASim.SchedulePlus(Calendar,"EndOfService",RNG.Erlang(Phases,MeanST,2),NextCustomer,Clock)
        WaitingTime.Record(Clock-NextCustomer.CreateTime)
        WTrecords.append(Clock-NextCustomer.CreateTime)
    else:
        Server.Free(1,Clock)


for reps in range(0,1,1):
    WTrecords = []
    Clock = 0.0
    VBASim.VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources,Clock)
    VBASim.Schedule(Calendar,"Arrival",RNG.Expon(MeanTBA,1),Clock)
    
    NextEvent = Calendar.Remove()
    Clock = NextEvent.EventTime
    if NextEvent.EventType == "Arrival":
        Arrival()
    elif NextEvent.EventType == "EndOfService":
        EndOfService(NextEvent.WhichObject)
    
    if WaitingTime.N() == WarmUp:
        VBASim.ClearStats(TheCTStats,TheDTStats,Clock)
        
    while WaitingTime.N() != RunLength-WarmUp:
        NextEvent = Calendar.Remove()
        Clock = NextEvent.EventTime
        if NextEvent.EventType == "Arrival":
            Arrival()
        elif NextEvent.EventType == "EndOfService":
            EndOfService(NextEvent.WhichObject)         
        
        if len(WTrecords) == WarmUp:
            VBASim.ClearStats(TheCTStats,TheDTStats,Clock)
            
        
    fwriter.writerow(WTrecords)
f.close()

BatchMeans = []

for i in range(0,40,1):
    Batch = []
    for j in range(250*i,250*i+250,1):
        Batch.append(WTrecords[j])
    BatchMeans.append(np.mean(Batch))

print(np.mean(BatchMeans),np.var(BatchMeans))



