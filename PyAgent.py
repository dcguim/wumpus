# PyAgent.py
from agent.constants import Action
from agent.agent import Hunter
from sys import exit
hunter = Hunter()
i = 0

def PyAgent_Constructor ():    
    print("MyPyAgent_Constructor")
    
def PyAgent_Destructor ():    
    print("MyPyAgent_Destructor")

def PyAgent_Initialize ():
    i=0
    print("MyPyAgent_Initialize")

def PyAgent_Process (stench,breeze,glitter,bump,scream):
    global i
    percept = {'stench':stench ,
               'breeze':breeze,
               'glitter':glitter,
               'bump':bump,
               'scream':scream}    
    act = hunter.reckon(percept)
    i = i+1
    print(i)
    #if i > 2:
    #    exit()    
    return int(act)

def PyAgent_GameOver (score):
    print("MyPyAgent_GameOver: score = " + str(score))
