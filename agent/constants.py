from enum import Enum

# Tasks
class Task(Enum):
    EXPLORE = 0
    TRAVEL = 1
    
# Orientations
class Orientation(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    def __int__(self):
        if self == Orientation.RIGHT:
            return 0
        elif self == Orientation.UP:
            return 1
        elif self == Orientation.LEFT:
            return 2
        elif self == Orientation.DOWN:
            return 3
        else:
            return None

# Actions
class Action(Enum):
    GOFORWARD = 0
    TURNLEFT = 1
    TURNRIGHT = 2
    GRAB = 3
    SHOOT = 4
    CLIMB = 5
    
    def __int__(self):
        if self == Action.GOFORWARD:
            return 0
        elif self == Action.TURNLEFT:
            return 1
        elif self == Action.TURNRIGHT:
            return 2
        elif self == Action.GRAB:
            return 3
        elif self == Action.SHOOT:
            return 4
        elif self == Action.CLIMB:
            return 5
        else:
            return None

    def cost(self):
        if self == Action.GOFORWARD:
            return 1
        elif self == Action.TURNLEFT:
            return 1
        elif self == Action.TURNRIGHT:
            return 1
        elif self == Action.GRAB:
            return 1
        elif self == Action.SHOOT:
            return 10
        elif self == Action.CLIMB:
            return 1

# Perceptions
class Perception(Enum):
    STENCH = 0
    BREEZE = 1
    GLITTER = 2
    BUMP = 3
    SCREAM = 4

    def __str__(self):
        if self == Perception.STENCH:
            return "STENCH"
        elif self == Perception.BREEZE:
            return "BREEZE"            
        elif self == Perception.GLITTER:
            return "GLITTER"            
        elif self == Perception.SCREAM: 
            return "SCREAM"            
        else:
            return None
# Inferences
class Inference(Enum):
    VISITED = 0
    NOTVISITED = 1
    PWUMPUS = 2
    WUMPUS = 3
    NOTWUMPUS = 4
    PPIT = 5
    PIT = 6
    NOTPIT = 7

    def __str__(self):
        if self == Inference.VISITED:
            return "VISITED"
        elif self == Inference.NOTVISITED:
            return "NOTVISITED"            
        elif self == Inference.PWUMPUS:
            return "PWUMPUS"            
        elif self == Inference.WUMPUS: 
            return "WUMPUS"            
        elif self == Inference.NOTWUMPUS:
            return "NOTWUMPUS"            
        elif self == Inference.PPIT:
            return "PPIT"
        elif self == Inference.PIT:
            return "PIT"
        elif self == Inference.NOTPIT:
            return "NOTPIT"
        else:
            return None
