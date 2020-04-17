# -*- coding: utf-8 -*-
import random as r
from Timetable import *
import copy as copy
import openpyxl as xw
from Subject import *
import time as t
from matplotlib import pyplot as plt

from mpi4py import MPI
import sys


def readFromFile(filename):
    book = xw.load_workbook('data.xlsx', data_only=True)
    sht = book.worksheets[0]
    # sht = [list(map(str,row)) for row in sht]
    teachers = []
    subjects = []
    # app = xw.apps.active

    for i in range(2, 15):
	    teachers.append(Teacher(int(float(sht[i][0].value)), list(map(int, sht[i][1].value.split(
	        ';'))), list(map(int, sht[i][2].value.split(';'))), int(float(sht[i][3].value))))

    sht = book.worksheets[1]

    for i in range(2, 15):
    	subjects.append(Subject(
    	    int(float(sht[i][0].value)), sht[i][1].value, int(float(sht[i][2].value))))

    # app.quit()
    return(teachers,subjects)       

class PG():
    def __init__(self,initN,iterNum,mutPr,crossPr,roomN,tup):
        self.roomN = roomN
        self.initN = initN
        self.teachers = []
        self.subjects = []
        self.getFromFile(tup)
        self.pop = self.createPop()
        self.bestTb = []
        self.iterNum = iterNum
        self.mutPr = mutPr
        self.crossPr = crossPr
        
    def getFromFile(self,tup):
        self.teachers,self.subjects = tup

    def createPop(self):
        pop = []
        for i in range(self.initN):
            pop.append(Timetable(self.teachers,self.subjects,self.roomN))
        return pop
        
    def classify(self):
        for item in self.pop:
            item.setConflicts()
        self.bestTb.append(self.getBestTimetable().conflicts)
            
    def sampleTwoObjects(self):
        sampInd = r.sample(range(self.initN),2)              
        return (self.pop[sampInd[0]],self.pop[sampInd[1]])
    
    def takeBest(self):
        pair = self.sampleTwoObjects()
        if (pair[0].conflicts<pair[1].conflicts):
            return pair[0]
        return pair[1]
    
    def selection(self):
        parents = []
        for i in range(self.initN-2):
            parents.append(self.takeBest())
        parents.append(self.getBestTimetable())        
        parents.append(self.getBestTimetable())
        return parents
    
    def makePairs(self,parents):
        helpList = r.sample(parents,len(parents))        
        return list(zip(helpList[::2],helpList[1::2]))
    
    def mutate(self, descendents,k):
        for i in range(len(descendents)):
            pr = r.randint(0,100)
            if pr< self.mutPr:    
                helpDesc = copy.deepcopy(descendents[i])
                randInd = r.randrange(0,len(helpDesc.records))
                
                if (r.randint(1,self.iterNum)<k*r.random()):     
                    worstRec = helpDesc.getWorstRecord()
                    randInd = helpDesc.getRecordId(worstRec)
                    
                helpDesc.records[randInd] = Record(helpDesc.teacherList,helpDesc.roomN)
                helpDesc.setConflicts()
                
                if helpDesc.conflicts < descendents[i].conflicts:
                    descendents[i] = helpDesc
        return descendents
        
                    
    def crossing(self, pairs):
        descendents =[]
        for item in pairs:
            pr = r.randint(0,100)
            if pr < self.crossPr:
                pCopy = copy.deepcopy(item)
                
                fstConflicts = item[0].conflicts
                sndConflicts = item[1].conflicts
                
                fstInd = r.randrange(0,len(item[0].records))
                sndInd = r.randrange(0,len(item[1].records))
                
                pCopy[0].records[fstInd],pCopy[1].records[sndInd] = pCopy[1].records[sndInd],pCopy[0].records[fstInd]
                
                pCopy[0].setConflicts()
                pCopy[1].setConflicts()
                
                if (fstConflicts>pCopy[0].conflicts or sndConflicts>pCopy[1].conflicts):
                    if pCopy[0].conflicts < pCopy[1].conflicts:
                        item = (pCopy[0],pCopy[0])
                    else:
                        item = (pCopy[1],pCopy[1])
            descendents.extend(item)
        return descendents
        
    def run(self):
        self.classify()
        lastconflicts = []
        i = 0
        while ((i < self.iterNum) or (self.getBestTimetable().conflicts!=0)):
            i += 1
            parents = self.selection()
            pairs = self.makePairs(parents)
            descendents = self.crossing(pairs) 
            self.pop = self.mutate(descendents,i)
            self.classify()
            lastconflicts.append(self.getBestTimetable())
 
    def getBestTimetable(self, pop = [] ):
        if len(pop)==0:
            pop=self.pop
        return min(pop, key = lambda x: x.conflicts)    

    def getWorstTimetable(self, pop = [] ):
        if len(pop)==0:
            pop=self.pop
        return max(pop, key = lambda x: x.conflicts) 

    def generateBest(self,path,pop,show):
        self.getBestTimetable(pop).generate(path,show)          
        
    
        
if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.rank
    name = MPI.Get_processor_name()    
	
    path = r'/home/lukasz/nauka/AIIR/program trying/program/timetable.xlsx'

    filename = r'/home/lukasz/AIIR/program trying/program/data.xlsx' #r'/home/lukasz/nauka/aiir/program/Constraint-satisfaction-problem-master/data.xlsx'


    initNumber = int(sys.argv[1])
    iterNum = 2000 		
    mProb = 100
    cProb = 0
    roomN = 4 
    dataTuple = readFromFile(filename)
    

    ########################################################################################################
    if rank == 0:
	start = t.time()  

        amountOfNodes = comm.size - 1
        dataList = []

    	print "name: ", name, rank
    	data = [1,2,3,4]
        
	counter = 1
        for x in range(amountOfNodes):
	    comm.send(data, dest = counter)
	    counter += 1

	counter = 1
        for x in range(amountOfNodes):
	    dataList.append(comm.recv(source = counter))
	    counter += 1
	
	
        finalTimetable = min(dataList, key = lambda x: x.conflicts)
    	finalTimetable.generate(path,True) 
	
        end = t.time()
        print "done master!", end - start;
    else:
        start = t.time()  

    	data = comm.recv(source = 0)
    	data = [x+5 for x in data]	    
    	print "name: ", name, rank
	
        pg = PG(initNumber,iterNum,mProb,cProb,roomN,dataTuple)        
        pg.run()
        datka = pg.getBestTimetable();

    	comm.send(datka, dest = 0)

        end = t.time()
        print "done slave!", rank, " ", end - start;
    ########################################################################################################
  


    
