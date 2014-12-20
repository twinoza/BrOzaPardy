OzaPardy
========
Oza Family Jeopardy Game for Annual Holiday Party

This program simply runs by typing (b/c the file is an executable): 
  ozapardy.py
  

Hardware Instructions:
==========================================================================
The USB cable should be connected between the computer and the Arduino. 

On the arduino board, connect the "Mice" controller to Pin 12 and GND.  
Likewise, connect the "Men" controller to Pin A0 and GND.

Game play instructions:
==========================================================================
When the game begins, it automatically imports the clues and responses
from a spreadsheet stored on Google Drive.  The name of this file is listed
as "OzaPardy", but can be changed by changing the doc_name variable in
ozapardy.py.

This initial process results in the command prompt displaying the following lines:
  Start getJeopardyData
  Start getJeopardyData
  Start getFinalJeopardy

Once this has happened, the GUI appears in single jeopardy mode. At this 
point, the host is able to click on any of the clue buttons (designated by
the dollar amounts). 

When the clue buttons are clicked:
  The teams have XXX seconds to respond by clicking their clicker
  If the clicker is clicked:
    The "Correct" and "Wrong" buttons appear in the top center portion of 
    the window.  The host will then click the button appropriate to the 
    correctness of the response provided.

    If the response is correct:
      The response will appear on the main window
    If the response is wrong:
      The clue is displayed again, and points are automatically deducted
      from the team that responded incorrectly.

      At this point, the other team can do two things:
        If they choose to answer by clicking their clicker:
          The game play is as before
        If they choose to pass:
          The host can click the OzaPardy button to display the response.

    If the host ever clicks the clue button while the clue is displayed:
      The clue button goes blank to prevent giving an advantage to any team.

  If no team chooses to respond, by abstaining from clicking:
    The host can click the OzaPardy button to show the response.

    After this the host must click the response button to return back to the
    main board
