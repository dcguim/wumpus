from .constants import Orientation, Action

class Position():
    def __init__ (self, x, y, o = None):
        self.x = x
        self.y = y
        self.d = o
        
    def tup(self):
        return str((self.x,self.y))

    def aim(self, pos):
        "Given an adj pos, return true or the next action to aim at it"
        if pos.x > self.x:
            if self.d == Orientation.RIGHT:
                return True
            elif self.d == Orientation.DOWN or self.d == Orientation.LEFT:
                return Action.TURNLEFT
            else:                
                return Action.TURNRIGHT
        elif pos.x < self.x:
            if self.d == Orientation.LEFT:
                return True
            elif self.d == Orientation.DOWN or self.d == Orientation.RIGHT:
                return Action.TURNRIGHT
            else:
                return Action.TURNLEFT
        elif pos.y > self.y:
            if self.d == Orientation.UP:
                return True
            elif self.d == Orientation.DOWN or self.d == Orientation.LEFT:
                return Action.TURNRIGHT
            else:
                return Action.TURNLEFT
        elif pos.y < self.y:
            if self.d == Orientation.DOWN:
                return True
            elif self.d == Orientation.UP or self.d == Orientation.LEFT:
                return Action.TURNLEFT
            else:
                return Action.TURNRIGHT
        else:
            print('Position not adjacent')
            return None
                
    def turn(self, act):
        if act == Action.TURNLEFT and self.d:
            self.d = Orientation((int(self.d)+1)%4)
        elif act == Action.TURNRIGHT and self.d:
            if self.d == Orientation.RIGHT:
                self.d = Orientation.DOWN
            else:
                self.d = Orientation(int(self.d)-1)
                
    def update(self, act):
        if act == Action.GOFORWARD and self.d:
            if self.d == Orientation.RIGHT:
                self.x = self.x + 1
            elif self.d == Orientation.UP:
                self.y = self.y + 1
            elif self.d == Orientation.LEFT:
                self.x = self.x - 1
            elif self.d == Orientation.DOWN:
                self.y = self.y - 1
            print(self.x,self.y)
        elif act != Action.GOFORWARD and self.d:
            self.turn(act)
                
    def getDiag(self, size, fixed):
        'If the world is not fixed, diag. cells may extrapolate the given size'
        if self.x == 1:
            if self.y == 1:
                return [Position(2,2)]
            elif self.y == size:
                return ([Position(2,size-1)] if fixed
                        else [Position(2,size-1),Position(2,size+1)])
            elif self.y > 1 and self.y < size:
                return [Position(2,self.y+1),Position(2,self.y-1)]
        elif self.x == size:
            if self.y == 1:
                return ([ Position(self.x - 1, 2)] if fixed
                        else [Position(self.x-1,2),Position(self.x+1,2)])
            elif self.y == size:
                return ([Position(self.x-1,size-1)] if fixed
                        else [Position(self.x-1,size-1),
                              Position(self.x-1,size+1),
                              Position(self.x+1,size-1),
                              Position(self.x+1,size+1)])
            elif self.y > 1 and self.y < size:
                return ([Position(self.x-1,self.y+1),
                         Position(self.x-1,self.y-1)] if fixed
                        else [Position(self.x-1,self.y-1),
                              Position(self.x-1,self.y+1),
                              Position(self.x+1,self.y+1),
                              Position(self.x+1,self.y-1)])
        elif self.x > 1 and self.x < size:
            if self.y == 1:
                return [Position(self.x-1,2),Position(self.x+1,2)]                        
            elif self.y == size:
                return ([Position(self.x+1,size-1),
                         Position(self.x-1,size-1)] if fixed
                        else [Position(self.x-1,size+1),
                              Position(self.x-1,size-1),
                              Position(self.x+1,size+1),
                              Position(self.x+1,size-1)])
            elif self.y > 1 and self.y < size:
                return [Position(self.x-1,self.y+1),Position(self.x-1,self.y-1),
                        Position(self.x+1,self.y-1),Position(self.x+1,self.y+1)]
            
    def getAdj(self, size, fixed):
        'If the world is not fixed, adj. cells may extrapolate the given size'
        if self.x == 1:
            if self.y == 1:
                return [Position(1,2),Position(2,1)]
            elif self.y == size:
                return ([Position(1,self.y-1),Position(2,self.y)] if fixed
                        else [Position(1,self.y-1),Position(2,self.y),
                              Position(1,self.y+1)])
            elif self.y > 1 and self.y < size:
                return [Position(1,self.y+1),Position(1,self.y-1),
                        Position(2,self.y)]
        elif self.x == size:
            if self.y == 1:
                return ([Position(self.x-1,self.y),Position(self.x,2)] if fixed
                        else [Position(self.x-1,1),Position(self.x,2),
                              Position(self.x+1,1)])
            elif self.y == size:
                return ([Position(self.x-1,size),
                        Position(self.x,size-1)] if fixed
                        else [Position(self.x-1,size),
                              Position(self.x,size-1),
                              Position(self.x,size+1),
                              Position(self.x+1,size)])
            elif self.y > 1 and self.y < size:
                return ([Position(self.x-1,self.y),Position(self.x,self.y-1),
                        Position(self.x,self.y+1)] if fixed
                        else [Position(self.x-1,self.y),
                              Position(self.x,self.y-1),
                              Position(self.x,self.y+1),
                              Position(self.x+1,self.y)])
        elif self.x > 1 and self.x < size:
            if self.y == 1:
                return [Position(self.x,2),Position(self.x+1,1),
                        Position(self.x-1,1)]                
            elif self.y == size:
                return ([Position(self.x,size-1),Position(self.x+1,self.y),
                        Position(self.x-1,self.y)] if fixed
                        else [Position(self.x-1,size),
                              Position(self.x,size-1),
                              Position(self.x,size+1),
                              Position(self.x+1,size)])
            elif self.y > 1 and self.y < size:
                return [Position(self.x-1,self.y),Position(self.x+1,self.y),
                        Position(self.x,self.y-1),Position(self.x,self.y+1)]   
