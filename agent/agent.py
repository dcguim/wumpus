from .constants import Perception, Action, Orientation, Inference, Task
from .position import Position as P
from itertools import product
from z3 import *
from string import ascii_uppercase
from math import inf

class MentalModel():
    def __init__ (self):
        # Agent`s mental model, dealing with partial knowledge
        # assume that the world is size 2x2 at first
        self.sModel = 2
        self.mentalModel =[[[] for i in range(self.sModel)]
                           for i in range(self.sModel)]
        # A possible mental model
        self.hypMentalModel = None
        self.fixed = False
        # If true then there exist a hypothetical mental model
        self.hypothetical = False
        self.foundWumpus = None
        
    def removeRedundant(self, position, hyp):
        if hyp:             
            if self.existKnowledgeP(position, Inference.PWUMPUS):
                self.hypMentalModel[position.x-1][position.y-1].remove(Inference.PWUMPUS)
            if self.existKnowledgeP(position, Inference.WUMPUS):
                self.hypMentalModel[position.x-1][position.y-1].remove(Inference.WUMPUS)
            if self.existKnowledgeP(position, Inference.NOTWUMPUS):
                self.hypMentalModel[position.x-1][position.y-1].remove(Inference.NOTWUMPUS)
            if self.existKnowledgeP(position, Inference.PPIT):
                self.hypMentalModel[position.x-1][position.y-1].remove(Inference.PPIT)
            if self.existKnowledgeP(position, Inference.PPIT):
                self.hypMentalModel[position.x-1][position.y-1].remove(Inference.PIT)
            if self.existKnowledgeP(position, Inference.PPIT):
                self.hypMentalModel[position.x-1][position.y-1].remove(Inference.NOTPIT)
        else:
            if self.existKnowledgeP(position, Inference.PWUMPUS):
                self.mentalModel[position.x-1][position.y-1].remove(Inference.PWUMPUS)
            if self.existKnowledgeP(position, Inference.WUMPUS):
                self.mentalModel[position.x-1][position.y-1].remove(Inference.WUMPUS)
            if self.existKnowledgeP(position, Inference.NOTWUMPUS):
                self.mentalModel[position.x-1][position.y-1].remove(Inference.NOTWUMPUS)
            if self.existKnowledgeP(position, Inference.PPIT):
                self.mentalModel[position.x-1][position.y-1].remove(Inference.PPIT)
            if self.existKnowledgeP(position, Inference.PPIT):
                self.mentalModel[position.x-1][position.y-1].remove(Inference.PIT)
            if self.existKnowledgeP(position, Inference.PPIT):
                self.mentalModel[position.x-1][position.y-1].remove(Inference.NOTPIT)
                
    def addKnowledge(self, position, knw):
        if position.x > self.sModel or position.y > self.sModel:
            if self.hypothetical:                
                self.hypMentalModel[position.x-1][position.y-1].append(knw)
                if str(knw) == 'VISITED':
                    self.removeRedundant(position, True)
        else:
            if self.hypothetical:                
                self.hypMentalModel[position.x-1][position.y-1].append(knw)
                if str(knw) == 'VISITED':
                    self.removeRedundant(position, True)
            else:
                self.mentalModel[position.x-1][position.y-1].append(knw)
                if str(knw) == 'VISITED':
                    self.removeRedundant(position, False)
                    
    def removeKnowledge(self, position, knw):
        if position.x > self.sModel or position.y > self.sModel:
            if self.hypothetical:
                self.hypMentalModel[position.x-1][position.y-1].remove(knw)
        else:
            if self.hypothetical:                
                self.hypMentalModel[position.x-1][position.y-1].remove(knw)
            else:
                self.mentalModel[position.x-1][position.y-1].remove(knw)
                
    def existKnowledgeP(self, position, knw):
        "return a boolean corresp. to given knowledge in the given position"
        if self.hypothetical:
            if knw in self.hypMentalModel[position.x-1][position.y-1]:
                return True
            return False
        else:
            if knw in self.mentalModel[position.x-1][position.y-1]:
                return True
            return False

    def widenWorld(self):
        "The agent always widen his world simmetrically for rows and columns"
        l = int(self.sModel)+1
        if not self.hypothetical:
            self.sModel += 1
            m = self.mentalModel
        else:
            m = self.hypMentalModel
        # widen rows
        for row in range(len(m)):
            m[row].append([])
        # widen columns
        m.append([[] for i in range(l)])

    def assureHypothesis(self):
        self.sModel += 1 
        self.mentalModel = self.hypMentalModel
        self.hypothetical = False
        self.hypMentalModel = None


    def rejectHypothesis(self):
        sh = int(len(self.hypMentalModel[0]))
        m = self.hypMentalModel
        self.sModel = sh - 1
        for i in range(sh):
            m[i].remove(m[i][self.sModel])
        m.remove(m[self.sModel])
        self.mentalModel = m
        self.hypothetical = False
        self.hypMentalModel = None
        
    def addInferences(self, cells, inf, percept, m, adj=True):
        if adj:
            for a in cells:
                if (is_true(simplify(m.evaluate(inf['pwumpus'](a.x,a.y)))) and
                    not self.existKnowledgeP(a, Inference.PWUMPUS) and
                    not self.existKnowledgeP(a, Inference.VISITED) and
                    not self.foundWumpus and
                    percept['stench']):
                    self.addKnowledge(a, Inference.PWUMPUS)            
                if (not is_true(simplify(m.evaluate(inf['wumpus'](a.x,a.y)))) and
                      not self.existKnowledgeP(a, Inference.NOTWUMPUS) and
                      not self.foundWumpus and
                      not percept['stench']):
                    self.addKnowledge(a, Inference.NOTWUMPUS)
                    if self.existKnowledgeP(a, Inference.PWUMPUS):
                        self.removeKnowledge(a,Inference.PWUMPUS)
                # add inf about pits
        else:
            for a in cells:
                if (is_true(simplify(m.evaluate(inf['wumpus'](a.x,a.y)))) and
                    self.existKnowledgeP(a, Inference.PWUMPUS) and
                    not self.existKnowledgeP(a, Inference.WUMPUS) and
                    not self.existKnowledgeP(a, Inference.VISITED)):
                    self.addKnowledge(a, Inference.WUMPUS)
                    self.foundWumpus = a
                    for x in range(1,self.sModel+1):
                        for y in range(1,self.sModel+1):
                            if self.existKnowledgeP(P(x,y), Inference.PWUMPUS):
                                self.removeKnowledge(P(x,y), Inference.PWUMPUS)
                            
    def getWumpusPos(self,x,y,d):
        if d == Orientation.RIGHT:
            x = x + 1
        elif d == Orientation.UP:
            y = y + 1
        elif d == Orientation.LEFT:
            x = x - 1
        elif d == Orientation.DOWN:
            y = y - 1
        return x,y
                    
    def assimilateInferences(self, inf, percept, pos, m, f):
        "Add inferences from the model around the agent`s pos. accordingly"
        # Consider a hypothetical wider world if not fixed
        if not self.hypothetical and not f:
            if (pos.x == self.sModel or pos.y == self.sModel):
                self.hypMentalModel = list(self.mentalModel)
                self.hypothetical = True
                self.widenWorld()
        if percept['scream']:
            self.removeKnowledge(P(pos.x,pos.y,pos.d), Perception.STENCH)
            x, y = self.getWumpusPos(pos.x,pos.y,pos.d)
            self.foundWumpus = P(x,y)
            print(self.foundWumpus)
            print('found Wumpus!')
        adj = pos.getAdj(self.sModel,f)
        self.addInferences(adj, inf, percept, m)
        diag = pos.getDiag(self.sModel,f)
        self.addInferences(diag, inf, percept, m, adj=False)
        
    def display(self):        
        if self.hypothetical:
            print('Agent Hypothetical Mental Model')
            m = self.hypMentalModel            
            size = self.sModel+1
            print(self.hypMentalModel)
        else:
            print('Agent Mental Model')
            size = self.sModel
            m = self.mentalModel
            print(self.mentalModel)
        
        l = ""
        for j in range(size-1,-1,-1):
            for i in range(size):
                for inf in m[i][j]:
                    if str(inf) == 'VISITED':
                        l = l +'VS '
                    elif str(inf) == 'NOTVISITED':
                        l = l +'NV '
                    elif str(inf) == 'PWUMPUS':
                        l = l +'PW '
                    elif str(inf) == 'WUMPUS':
                        l = l +'WP '
                    elif str(inf) == 'NOTWUMPUS':
                        l = l +'NW '
                    elif str(inf) == 'PPIT':
                        l = l +'PP '
                    elif str(inf) == 'PIT':
                        l = l +'PT '
                    elif str(inf) == 'NOTPIT':
                        l = l +'NP '
                l = l + '}'
            l = l + '{'
        def p(w):
            print(w,end='')
        line = ""
        sCell = 5
        for i in range(size):
            line = line+'+'+'-'*sCell
        prev = '|'
        p(line+'+'+'\n'+prev)
        cInf = 0
        cSpc = 0        
        for w in l:
            if w == '}':
                cInf = 0
                if (sCell-cSpc) >= 0:
                    p(' '*(sCell-cSpc)+'|')
                cSpc = 0
                prev = w
                continue
            elif w == '{':
                p('\n'+line+'+'+'\n|')
                cSpc = 0
                cInf = 0
                prev = w
                continue
            else:
                if cSpc < sCell:
                    p(w)
                if prev in ascii_uppercase:
                    cInf += 1
            if cSpc < sCell:
                cSpc+=1
            
    
class Hunter():
    def __init__(self):        
        print('New Hunter')
        self.pos = P(1,1,Orientation.RIGHT)
        self.startPos = None
        self.model = MentalModel()
        self.prevAction = None        
        self.task = Task.EXPLORE
        self.move = None
        self.leave = False
        self.currPath = []
        self.safeCells = []
        self.visited = []
        self.travel = []
        self.hasGold = False
        
    def percept(self, p):
        if (p['stench'] == 1):
            self.model.addKnowledge(self.pos, Perception.STENCH)
        if (p['breeze'] == 1):
            self.model.addKnowledge(self.pos, Perception.BREEZE)
        if (p['glitter'] == 1):
            self.model.addKnowledge(self.pos, Perception.GLITTER)        
        if (p['scream'] == 1):
            self.model.addKnowledge(self.pos, Perception.SCREAM)
                    
    def nextStep(self, p):
        if self.prevAction and p['bump'] ==0 and self.task == Task.EXPLORE:
            self.currPath.append(P(self.pos.x,self.pos.y,self.pos.d))
        if not (p['bump'] == 1 and self.prevAction == Action.GOFORWARD):
            self.pos.update(self.prevAction)
        if (p['bump'] == 0):            
            if self.prevAction == Action.GOFORWARD and not self.model.fixed:
                if (self.pos.x > self.model.sModel or
                    self.pos.y > self.model.sModel):
                    if self.model.hypothetical:
                        self.model.assureHypothesis()                    
                    else:
                        self.model.widenWorld()        
        else:
            print('--- Fixed Model ---')
            if self.model.hypothetical:
                self.model.rejectHypothesis()
            self.model.fixed = True
        if not  self.model.existKnowledgeP(self.pos, Inference.VISITED):
            self.visited.append((self.pos.x,self.pos.y))
            self.model.addKnowledge(self.pos,Inference.VISITED)
            
    def emptyCells(self):
        "Return all cells which without from the agent is currently standing"
        prod = product(range(1,self.model.sModel+1),
                       range(1,self.model.sModel+1))
        cells = list(prod)
        cells.remove((self.pos.x,self.pos.y))
        return cells

    def removePath(self, paths, node):
        noEmptyKey = False
        for key in paths.keys():
            if node in paths[key]:
                paths[key].remove(node)        
        # Fix point to back track removing all the empty paths
        while not noEmptyKey:
            rem = 0
            for key in paths.keys():
                if paths[key] == []:
                    rem += 1
                    del paths[key]
                    for k in paths.keys():
                        if key in paths[k]:
                            paths[k].remove(key)
            if rem == 0:
                noEmptyKey = True
                break
        
    def reach(self, dest):
        "Safe path by iteratively minimizing the distance between pos and dest"
        paths = {}
        currs = [P(self.pos.x, self.pos.y)]
        prevs = []
        found = False
        rems = []
        i = 0
        while not found:
            rems = []
            for c in currs:
                adjs = c.getAdj(self.model.sModel, self.model.fixed)
                safes = []
                for a in adjs:
                    if (a.x,a.y) in self.safeCells:
                        safes.append(a)
                if len(safes) == 1 and prevs and safes[0].tup() in prevs:
                    self.removePath(paths, c)
                    rems.append(c)
                    continue
                else:
                    paths[c] = []
                    for a in safes:
                        if a.tup() not in prevs:
                            paths[c].append(a)
            print('tree')
            for k,v in paths.items():                
                text = k.tup()+':'
                for i in v:
                    text = text +' '+ i.tup()+','
                text = text[:-1]
                print(text)
            
            prevs = list(currs)
            for r in rems:
                prevs.remove(r)
            currs = []
            for c in prevs:
                for n in paths[c]:
                    currs.append(n)
                    if n.tup() == dest.tup():
                        found = c
            prevs = [c.tup() for c in prevs]
            
        path = [c,dest]
        while path[0].tup() != self.pos.tup():
            for k, adj in paths.items():
                if path[0] in adj:
                    path = [k]+path        
        path = path[1:]
        return path
                
    def getSafeCells(self):
        safe = []
        for i in range(1,self.model.sModel+1):
            for j in range(1,self.model.sModel+1):
                p = P(i,j)
                if self.model.existKnowledgeP(p, Inference.VISITED):
                    if (p.x,p.y) not in safe:
                        safe.append((p.x,p.y)) 

                    adjs = p.getAdj(self.model.sModel, self.model.fixed)
                    for a in adjs:
                        if a.x <= self.model.sModel and a.y <= self.model.sModel:
                            if not self.model.existKnowledgeP(a, Inference.PWUMPUS):
                                if not self.model.existKnowledgeP(a, Inference.WUMPUS):
                                    if (a.x,a.y) not in safe:
                                        safe.append((a.x,a.y)) 
        return safe

    def evaluatePaths(self,paths):
        'Return the cost and the actions req. for every considered safe path'
        cost = []
        actions = []
        # for every path
        for i in range(len(paths)):
            # it`s cost start with 0
            cost.append(0)
            actions.append([])
            curr = P(self.pos.x,self.pos.y,self.pos.d)
            # for positions in paths
            for c in paths[i]:
                act = curr.aim(c)
                while type(act).__name__ == 'Action':

                    curr.turn(act)
                    cost[i] += act.cost()
                    actions[i].append(act)

                    act = curr.aim(c)                    
                act = Action.GOFORWARD
                actions[i].append(act)
                curr.update(Action.GOFORWARD)
                cost[i] += act.cost()
        print('costs and actions to be analyzed')
        print(cost, actions)
        return cost, actions
                
    def scheduleTravel(self,costs, actions):
        print('Schedule a travel')
        self.task = Task.TRAVEL
        self.travel = []
        cost = inf
        index = 0
        for i in range(len(costs)):
            if costs[i] < cost:
                cost = costs[i]
                index = i
        self.travel = actions[index]
        print('set travel!')
        print(self.travel)
            
    def reason(self,p):
        act = None
        x, y = Ints('x y')        
        In = Function('In', IntSort(), IntSort(), BoolSort())
        Stench = Function('Stench', IntSort(), IntSort(), BoolSort())
        PWumpus = Function('PWumpus', IntSort(), IntSort(), BoolSort())
        Wumpus = Function('Wumpus', IntSort(), IntSort(), BoolSort())
        PPit = Function('Wumpus', IntSort(), IntSort(), BoolSort())
        Pit = Function('Wumpus', IntSort(), IntSort(), BoolSort())
        Visited = Function('Visited', IntSort(), IntSort(), BoolSort())
        Safe = Function('Safe', IntSort(), IntSort(), BoolSort())
        
        s = Solver()
        s.push()
        ### add assumptions ###
        for xpos in range(self.model.sModel):
            for ypos in range(self.model.sModel):
                for assump in self.model.mentalModel[xpos][ypos]:
                    if str(assump) == 'VISITED':
                        s.add(Visited(xpos+1,ypos+1))
                    elif str(assump) == 'NOTVISITED':
                        s.add(Not(Visited(xpos+1,ypos+1)))
                    elif str(assump) == 'PWUMPUS':
                        s.add(PWumpus(xpos+1,ypos+1))
                    elif str(assump) == 'NOTPWUMPUS':
                        s.add(Not(PWumpus(xpos+1,ypos+1)))
                    elif str(assump) == 'WUMPUS':
                        s.add(Wumpus(xpos+1,ypos+1))
                    elif str(assump) == 'NOTWUMPUS':
                        s.add(Not(Wumpus(xpos+1,ypos+1)))
                    elif str(assump) == 'PPIT':
                        s.add(PPit(xpos+1,ypos+1))
                    elif str(assump) == 'NOTPPIT':
                        s.add(Not(PPit(xpos+1,ypos+1)))
                    elif str(assump) == 'PIT':
                        s.add(Pit(xpos+1,ypos+1))
                    elif str(assump) == 'NOTPIT':
                        s.add(Not(Pit(xpos+1,ypos+1)))
                    elif str(assump) == 'STENCH':
                        s.add(Stench(xpos+1,ypos+1))
                    # elif str(assump) == 'BREEZE':
                    #     s.add(Breeze(xpos+1,ypos+1))


        for sf in self.safeCells:
            s.add(Safe(sf[0],sf[1]))
                        
        ### Strategy ###
        # Localize the agent in the map
        cells = self.emptyCells()
        for c in cells:
            s.add(Not(In(c[0],c[1])))
            if (c[0],c[1]) not in self.visited:
                s.add(Not(Visited(c[0],c[1])))
        s.add(In(self.pos.x,self.pos.y))
        # Specify the visited Cells
        for c in self.visited:
            s.add(Visited(c[0],c[1]))        
        
        s.add(And(x >= 1, y >= 1,
                  x <= self.model.sModel, y <= self.model.sModel))
        # Infering on Stenches
        # with an unfixed/uncomplete world
        if self.model.existKnowledgeP(self.pos, Perception.STENCH):
            s.add(Stench(self.pos.x,self.pos.y))
            if self.pos.y == 1 and self.pos.x > 1 and self.pos.x <= self.model.sModel:
                s.add(And(In(x,y),                      
                        # Agent is on the first line but not in the left corner
                        And(y == 1, x > 1, x <= self.model.sModel,
                            Stench(x,y)) == And(PWumpus(x-1,y), PWumpus(x+1,y),
                                                PWumpus(x,y+1))))
            elif self.pos.y == 1 and self.pos.x == 1:
                s.add(And(In(x,y),
                        # Agent is on the first line but not in the left corner
                        And(y == 1, x == 1, Stench(x,y)) == And(PWumpus(x+1,y),
                                                                PWumpus(x,y+1))))
            elif self.pos.y > 1 and self.pos.x > 1 and self.pos.x <= self.model.sModel:
                 s.add(And(In(x,y),
                        # Agent is on the first column but not in the bottom corner
                        And(y > 1, x == 1, y <= self.model.sModel,
                               Stench(x,y)) == And(PWumpus(x+1,y),
                                                   PWumpus(x,y+1),
                                                   PWumpus(x,y-1))))
            elif self.pos.y > 1 and self.pos.x > 1 and self.pos.x <= self.model.sModel and self.pos.y <= self.model.sModel:
                 s.add(And(In(x,y),
                        # Agent is on the middle of the grid
                        And(y > 1, x > 1, x <= self.model.sModel, y <= self.model.sModel,
                               Stench(x,y)) == And(PWumpus(x+1,y),
                                                   PWumpus(x-1,y),
                                                   PWumpus(x,y+1),
                                                   PWumpus(x,y-1))))       
        else:
            # Not Wumpus in the adjacent cells
            s.add(Not(Stench(self.pos.x,self.pos.y)))
            s.add(And(In(x,y),
                      Not(Stench(x,y)),
                      Or(
                        # Agent is on the first line
                        And(y == 1, x > 1,
                            x <= self.model.sModel) == And(Not(Wumpus(x-1,y)),
                                                           Not(Wumpus(x+1,y)),
                                                           Not(Wumpus(x,y+1))),
                        And(y == 1, x == 1) == And(Not(Wumpus(x+1,y)),
                                                   Not(Wumpus(x,y+1))),
                       # Agent is on a middle line
                        And(y > 1, x > 1,
                            x <= self.model.sModel) == And(Not(Wumpus(x+1,y)),
                                                           Not(Wumpus(x-1,y)),
                                                           Not(Wumpus(x,y+1)),
                                                           Not(Wumpus(x,y-1))),
                        And(y > 1, x == 1,
                            x <= self.model.sModel) == And(Not(Wumpus(x+1,y)),
                                                           Not(Wumpus(x,y+1)),
                                                           Not(Wumpus(x,y-1))))))
        # Infering on Wumpuses iff there is a stench and
        # one diagonal cell is visited
        diags = self.pos.getDiag(self.model.sModel, self.model.fixed)
        visitedDiag = False
        for d in diags:
            if (d.x <= self.model.sModel and d.y <= self.model.sModel and
                  self.model.existKnowledgeP(d, Inference.VISITED)):
                visitedDiag = True
        if (not self.model.foundWumpus and
            self.model.existKnowledgeP(self.pos, Perception.STENCH) and
            visitedDiag):
            # upper left square
            if self.pos.y > 1 and self.pos.x >= 1 and  self.pos.x < self.model.sModel:
                s.add(And(In(x,y),
                          Or(
                              And(y > 1, x>=1, x < self.model.sModel,
                                  Stench(x,y), Stench(x+1,y-1),Visited(x+1,y-1),
                                  Visited(x,y-1),PWumpus(x+1,y)) == Wumpus(x+1,y),
                              And(y > 1, x>=1, x < self.model.sModel,
                                  Stench(x,y), Not(Stench(x+1,y-1)),Visited(x+1,y-1),
                                  PWumpus(x+1,y)) == Not(Wumpus(x+1,y))),            
                          Or(
                              And(y > 1, x>=1, x < self.model.sModel,
                                  Stench(x,y), Stench(x+1,y-1), Visited(x+1,y-1),
                                  Visited(x+1,y),PWumpus(x,y-1)) == Wumpus(x,y-1),
                              And(y > 1, x>=1, x < self.model.sModel,
                                  Stench(x,y), Not(Stench(x+1,y-1)), Visited(x+1,y-1),
                                  PWumpus(x,y-1)) == Not(Wumpus(x,y-1)))))
            if self.pos.y > 1 and self.pos.x > 1 and  self.pos.x <= self.model.sModel and self.pos.y <= self.model.sModel:
                s.add(And(In(x,y),
                          # upper right square
                          Or(
                              And(y > 1, x > 1, x <= self.model.sModel,
                                  y <= self.model.sModel,
                                  Stench(x,y), Stench(x-1,y-1), Visited(x-1,y-1),
                                  Visited(x,y-1),PWumpus(x-1,y)) == Wumpus(x-1,y),
                              And(y > 1, x > 1, x <= self.model.sModel,
                                  y <= self.model.sModel,
                                  Stench(x,y), Not(Stench(x-1,y-1)), Visited(x-1,y-1),
                                  PWumpus(x-1,y)) == Not(Wumpus(x-1,y))),                          
                          Or(
                              And(y > 1, x > 1, x <= self.model.sModel,
                                  y <= self.model.sModel,
                                  Stench(x,y), Stench(x-1,y-1), Visited(x-1,y-1),
                                  Visited(x-1,y),PWumpus(x,y-1)) == Wumpus(x,y-1),  
                              And(y > 1, x > 1, x <= self.model.sModel,
                                  y <= self.model.sModel,
                                  Stench(x,y), Not(Stench(x-1,y-1)), Visited(x-1,y-1),
                                  PWumpus(x,y-1)) == Not(Wumpus(x,y-1)))))
                if self.pos.y >= 1 and self.pos.x >= 1 and self.pos.x < self.model.sModel and self.pos.y < self.model.sModel:
                    s.add(And(In(x,y),
                          # lower left square
                          Or(
                              And(y >= 1, x >= 1, x < self.model.sModel,
                                  y < self.model.sModel,
                                  Stench(x,y), Stench(x+1,y+1), Visited(x+1,y+1),
                                  Visited(x,y+1),PWumpus(x+1,y)) == Wumpus(x+1,y),
                              And(y >= 1, x >= 1, x < self.model.sModel,
                                  y < self.model.sModel,
                                  Stench(x,y), Not(Stench(x+1,y+1)), Visited(x+1,y+1),
                                  PWumpus(x+1,y)) == Not(Wumpus(x+1,y))),
                          Or(
                              And(y >= 1, x >= 1, x < self.model.sModel,
                                  y < self.model.sModel,
                                  Stench(x,y), Stench(x+1,y+1), Visited(x+1,y+1),
                                  Visited(x+1,y),PWumpus(x,y+1)) == Wumpus(x,y+1),
                              And(y >= 1, x >= 1, x < self.model.sModel,
                                  y < self.model.sModel,
                                  Stench(x,y), Not(Stench(x+1,y+1)), Visited(x+1,y+1),
                                  PWumpus(x,y+1)) == Not(Wumpus(x,y+1)))))
                    if self.pos.x > 1 and self.pos.y > 1 and self.pos.y < self.model.sModel:
                        s.add(And(In(x,y),
                            # lower right square
                            Or(
                                And(x > 1, y>= 1, y < self.model.sModel,
                                    Stench(x,y), Stench(x-1,y+1), Visited(x-1,y+1),
                                    Visited(x-1,y), PWumpus(x,y+1)) == Wumpus(x,y+1),
                                And(x > 1, y>= 1, y < self.model.sModel,
                                    Stench(x,y), Not(Stench(x-1,y+1)), Visited(x-1,y+1),
                                    PWumpus(x,y+1)) == Not(Wumpus(x,y+1))),
                            Or(
                                And(x > 1, y>= 1, y < self.model.sModel,
                                    Stench(x,y), Stench(x-1,y+1), Visited(x-1,y+1),
                                    Visited(x,y+1), PWumpus(x-1,y)) == Wumpus(x-1,y),
                                And(x > 1, y>= 1, y < self.model.sModel,
                                    Stench(x,y), Not(Stench(x-1,y+1)), Visited(x-1,y+1),
                                    PWumpus(x-1,y)) == Not(Wumpus(x-1,y)))))
            
                                                            
        s.check()
        print(s.check())       
        m = s.model()        
        s.pop()
        ### End of Strategy ###
        
        ### Update the model ###        
        print(m)
        inf = {'visited':Visited,
               'pwumpus':PWumpus,
               'wumpus':Wumpus,
               'ppit':PPit,
               'pit':Pit}
        self.model.assimilateInferences(inf, p, self.pos, m, self.model.fixed)
        print(self.model.display())
        if self.model.foundWumpus:
            print(self.model.foundWumpus.x,self.model.foundWumpus.y)
        else:
            print('No')
        ### Update the action ###
        print('Update action')
        self.safeCells = self.getSafeCells()       
            
        if p['glitter']:
            act = Action.GRAB
            self.hasGold = True
            self.task = Task.TRAVEL
            path = self.reach(self.startPos)
            if path:
                costs,actions = self.evaluatePaths([path])
                print(costs, actions)
                self.scheduleTravel(costs,actions)
            
        elif len(self.safeCells) == 1 and not self.model.foundWumpus:
            act = Action.SHOOT
        else:
            unexSafes = list(self.safeCells)
            for vc in self.visited:
                unexSafes.remove(vc)
            paths = []
            # if self.pos.d == Orientation.RIGHT
            # in self.pos.getAdj(self.model.sModel, self.model.fixed):
            if len(unexSafes) > 1:
                for un in unexSafes:
                    path = self.reach(P(un[0],un[1]))
                    if len(path) > 1:
                        paths.append(path)
                    else:
                        # If the path is of length 1 and we are pointing at it.
                        if self.pos.aim(path[0]) == True:
                            return Action.GOFORWARD
                        else:
                            paths.append(path)
            elif unexSafes and len(unexSafes) == 1:
                path = self.reach(P(unexSafes[0][0],unexSafes[0][1]))
                print('!foundpath:')
                for p in path: print(p.x,p.y)
                if len(path) > 1:
                    paths.append(path)
                else:
                    if self.pos.aim(path[0]) == True:
                        return Action.GOFORWARD
                    else:
                        paths.append(path)
            if paths:
                costs,actions = self.evaluatePaths(paths)
                self.scheduleTravel(costs,actions)
                act = self.travel[0]
                self.travel = self.travel[1:]
        if not act:
            act = Action.GOFORWARD
        return act
        
    def reckon(self, p):
        if not self.startPos:
            self.startPos = P(self.pos.x,self.pos.y)
        if self.hasGold and self.pos.x == self.startPos.x and self.pos.y == self.startPos.y:
            return Action.CLIMB
            
        self.nextStep(p)       
        if self.task == Task.TRAVEL:
            print('travelling...')
            if self.travel:
                print(self.travel)
                act = self.travel[0]
                self.prevAction = act
                self.travel = self.travel[1:]
                return act
            else:
                print('explore...')
                self.task = Task.EXPLORE
                if self.leave == True:
                    return Action.CLIMB
        self.model.display()
        self.percept(p)
        act = self.reason(p)
        self.prevAction = act
        return act
