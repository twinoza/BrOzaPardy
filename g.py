""" Define global variables to be accessible and used by all modules
    All .py modules for ozaPardy should include the following line
        import g
"""

import ozaPardyClasses as opc

# Create the teams
Team1 = opc.team(0, 'Team 1', 0)
Team2 = opc.team(1, 'Team 2', 0)
Team3 = opc.team(2, 'Team 3', 0)
Team4 = opc.team(3, 'Team 4', 0)
Teams = [Team1, Team2, Team3, Team4]

# Create the gameplay boxes
sBoard = [""] * 6 + [opc.ozaPardyBox((ii+1)*10+(jj+1)) 
         for ii in range(6) for jj in range(5)]
dBoard = [""] * 6 + [opc.ozaPardyBox((ii+1)*10+(jj+1)) 
         for ii in range(6) for jj in range(5)]
boards = [sBoard, dBoard]
fBoard = ["", opc.ozaPardyBox(11)]
