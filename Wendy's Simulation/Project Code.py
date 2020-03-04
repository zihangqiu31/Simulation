# -*- coding: utf-8 -*-
"""
@author: zuq31 Zihang Qiu
"""


import VBASim
import Basic_Classes as bc
import RNG
import csv
import numpy as np

TheQueues = []
TheResources = []
TheDTStats  = []
TheCTStats = []

RunLength = 2200.0
WarmUp = 200.0
Calendar = bc.EventCalendar()

NumAgents = 4# try different value to see how it goes
Agents = bc.Resource()
Agents.SetUnits(NumAgents)
TheResources.append(Agents)

Queue0 = bc.FIFOQueue()
Queue1 = bc.FIFOQueue()
Queue2 = bc.FIFOQueue()
Queue3 = bc.FIFOQueue()
Queue4 = bc.FIFOQueue()
Queue5 = bc.FIFOQueue()
Queue6 = bc.FIFOQueue()
CallQueues = bc.FIFOQueue()
TheQueues.append(Queue0)
TheQueues.append(Queue1)
TheQueues.append(Queue2)
TheQueues.append(Queue3)
TheQueues.append(Queue4)
TheQueues.append(Queue5)
TheQueues.append(Queue6)
TheQueues.append(CallQueues)

f = open('WTdata.csv','w', newline='')
fwriter = csv.writer(f)
WTrecords = []

STMean = 1.4137
STStream = [3,4,5,6,7,8,9]
CMTMean = 0.0904
ATMean = 0.7608
ProbType = [0.148693472,0.213783426,0.392007958,0.502522592,0.650297105,0.800247171,1]


    
def Arrival():
    VBASim.Schedule(Calendar,"Arrival",RNG.Expon(ATMean,1),Clock)
    U = RNG.Uniform(0,1,2)
    
    if U<ProbType[0]:
        Customer = bc.Entity2(Clock,0)#0 means type
        TheQueues[0].Add(Customer,Clock)
        if TheQueues[0].NumQueue() == 1:
            VBASim.SchedulePlus(Calendar,"DrivingIn",RNG.Expon(CMTMean,1),Customer,Clock)


    elif U<ProbType[1]:
        Customer = bc.Entity2(Clock,1)#0 means type
        if TheQueues[1].NumQueue() == 1:
            VBASim.SchedulePlus(Calendar,"DrivingIn",RNG.Expon(CMTMean,1),Customer,Clock)
        else:
            TheQueues[1].Add(Customer,Clock)

    elif U<ProbType[2]:
        Customer = bc.Entity2(Clock,2)#0 means type
        TheQueues[2].Add(Customer,Clock)
        if TheQueues[2].NumQueue() == 1:
            VBASim.SchedulePlus(Calendar,"DrivingIn",RNG.Expon(CMTMean,1),Customer,Clock)
            

    elif U<ProbType[3]:
        Customer = bc.Entity2(Clock,3)#0 means type
        TheQueues[3].Add(Customer,Clock)
        if TheQueues[3].NumQueue() == 1:
            VBASim.SchedulePlus(Calendar,"DrivingIn",RNG.Expon(CMTMean,1),Customer,Clock)
           

    elif U<ProbType[4]:
        Customer = bc.Entity2(Clock,4)#0 means type
        TheQueues[4].Add(Customer,Clock)
        if TheQueues[4].NumQueue() == 1:
            VBASim.SchedulePlus(Calendar,"DrivingIn",RNG.Expon(CMTMean,1),Customer,Clock)
          

    elif U<ProbType[5]:
        Customer = bc.Entity2(Clock,5)#0 means type
        TheQueues[5].Add(Customer,Clock)
        if TheQueues[5].NumQueue() == 1:
            VBASim.SchedulePlus(Calendar,"DrivingIn",RNG.Expon(CMTMean,1),Customer,Clock)
            

    else:
        Customer = bc.Entity2(Clock,6)#0 means type
        TheQueues[6].Add(Customer,Clock)
        if TheQueues[6].NumQueue() == 1:
            VBASim.SchedulePlus(Calendar,"DrivingIn",RNG.Expon(CMTMean,1),Customer,Clock)
            



def DrivingIn(Customer):
    if (Agents.Busy<NumAgents):
        Agents.Seize(1,Clock)
        VBASim.SchedulePlus(Calendar,"EndOfService",RNG.Expon(STMean,1),Customer,Clock)
        if Clock>200:
            WTrecords.append(0)
    else:
        TheQueues[7].Add(Customer,Clock) 



def EndOfService(OldCustomer):
    TheQueues[OldCustomer.Type].Remove(Clock)
    if TheQueues[OldCustomer.Type].NumQueue() != 0:
        CustomerTemp = bc.Entity2(Clock,OldCustomer.Type)
        VBASim.SchedulePlus(Calendar,"DrivingIn",RNG.Expon(CMTMean,1),CustomerTemp,Clock)
        
    if TheQueues[7].NumQueue()>0:
        Customer = TheQueues[7].Remove(Clock)
        if Clock>200:
            WTrecords.append(Clock-TheQueues[7].AddedTime())
        VBASim.SchedulePlus(Calendar,"EndOfService",RNG.Expon(STMean,1),Customer,Clock)
    else:
        Agents.Free(1,Clock)



for reps in range(0,10,1):
    WTrecords = []
    Clock = 0.0
    VBASim.VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources,Clock)
    VBASim.Schedule(Calendar,"Arrival",RNG.Expon(ATMean,1),Clock)
    VBASim.Schedule(Calendar,"EndSimulation",RunLength,Clock)
    VBASim.Schedule(Calendar,"ClearIt",WarmUp,Clock)
    
    NextEvent = Calendar.Remove()
    Clock = NextEvent.EventTime
    if NextEvent.EventType == "Arrival":
        Arrival()
    elif NextEvent.EventType == "DrivingIn":
        DrivingIn(NextEvent.WhichObject)
    elif NextEvent.EventType == "EndOfService":
        EndOfService(NextEvent.WhichObject)
    elif NextEvent.EventType == "ClearIt":
        VBASim.ClearStats(TheCTStats,TheDTStats,Clock)
        
    while NextEvent.EventType != "EndSimulation":
        NextEvent = Calendar.Remove()
        Clock = NextEvent.EventTime
        if NextEvent.EventType == "Arrival":
            Arrival()
        elif NextEvent.EventType == "DrivingIn":
            DrivingIn(NextEvent.WhichObject)
        elif NextEvent.EventType == "EndOfService":
            EndOfService(NextEvent.WhichObject)
        elif NextEvent.EventType == "ClearIt":
            VBASim.ClearStats(TheCTStats,TheDTStats,Clock)
    fwriter.writerow(WTrecords)
f.close()






















