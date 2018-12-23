# Wumpus World
The object of this project is to develop an agent that reasons with the use of Satisfiability Modulo Theories, and at each point in time the agent runs a SAT solver assuming what he already knows from the world and obtaining a new action to be performed. It was used as a project for a class called Integrated Logic Systems.
## Usage
1. Clone the directory and including the submodule wumpus-world-simulator dependency available at https://github.com/holderlb/wumpus-world-simulator
git clone --recursive git@github.com:dcguim/wumpus.git

Or clone normally then download submodule`s content of wumpus-world-simulator:
git submodule update --init --recursive

2. Check Makefile and adapt to your OS accordingly.

3. Set the PYTHONPATH to wumpusproj root directory and run ./pywumpsim considering the agent which is in the root folder (not in the submodule):
   PYTHONPATH=./ ./wws/pywumpsim
   To run a test in the suite
   PYTHONPATH=./ ./wws/pywumpsim -world suite/wX.txt
