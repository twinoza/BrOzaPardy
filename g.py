""" Define global variables to be accessible and used by all modules
    All .py modules for ozaPardy should include the following line
        import g
"""

import ozaPardyClasses as opc

# Create the teams
Team1 = opc.team(0, 'Team 1', ['2', '3', '4'], 0)
Team2 = opc.team(1, 'Team 2', ['5', '6', '7'], 0)
Team3 = opc.team(2, 'Team 3', ['8', '9', '10'], 0)
Team4 = opc.team(3, 'Team 4', ['11', '12', '14'], 0)
Teams = [Team1, Team2, Team3, Team4]

# Create the gameplay boxes
sBoard = [""] * 6 + [opc.ozaPardyBox((ii+1)*10+(jj+1)) 
         for jj in range(5) for ii in range(6)]
dBoard = [""] * 6 + [opc.ozaPardyBox((ii+1)*10+(jj+1)) 
         for jj in range(5) for ii in range(6)]
boards = [sBoard, dBoard]
fBoard = ["", opc.ozaPardyBox(11)]

# Global variables to track the gameMode and currMode
gameMode = 'Single'
currMode = 'Single'

# Global variables to track which team is active and which controls the board
currTeam = 0
lastCorrectTeam = 0
