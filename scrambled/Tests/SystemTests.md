Testing Manual for Scrambled

Tests on system functionality of Scrambled 
Tester account usable for testing:
    Username: tester
    Password: password

Login Procedure Test:
    Testing Failure for wrong password:
        1. Go to login page on the website
        2. For username type in admin
        3. For password type in password
        4. An alert should appear saying "Invalid Username and Password"
    This indicates the login failed - as expected

    Testing Failure for invalid username:
        1. Go to login page on the website 
        2. For username type in testWrongUsername
        3. Type in any password
        4. An alert should appear saying "Invalid Username and Password"
     This indicates the login failed - as expected

    Testing Sucess:
        1. Go to login page on the website
        2. For username type in admin
        3. For password type in admin
        4. Should direct you to the admin's statistics page 
    This indicates login success - as excepted

Registration Procedure Test:
    Testing Failure for used username:
        1. Go to registration page 
        2. For username type in admin 
        3. Fill the rest of the forms out as you wish
        4. Click submit
        5. Error under username should appear stating "Please choose a different username" 
    This indicates failure - as expected

     Testing Failure for invalid password:
        1. Go to registration page 
        2. For email type in invalid email (without @, etc.) 
        3. Fill the rest of the forms out as you wish
        4. Click submit
        5. Error under email should appear stating "Please use a valid email"
    This indicates failure - as expected

    Testing Sucess:
        1. Go to registration page 
        2. Type in your details (so long as not previously signed up)
        3. Click submit
        4. Will direct you to login page
    This indicates success - as expected

Testing Game Functionality:
    Testing Submission to Database:
        1. Login with your username (OR tester account)
        2. Play a game of Normal/Speed Scrambled
        3. Go to statistic's page
        4. Graph should be updated according to your result
    This is expected procedure

    Testing Non-Repeat Submission:
        1. After played game, note the number of games played within statistics 
        2. Reload a finished game (either Speed or Normal)
        3. Return to statistics and check the number of games played is consistnet
    This is expected procedure 

    Testing Word Checker Wrong Word:
        1. Load a game of Scrambled
        2. Enter into the game a non-word
        3. If the modal appears stating incorrect word, it works correctly 

    Testing Word Checker Correct Word:
        1. Load a game of Scrambled
        2. Enter an English word 
        3. If accepted and put into submitted area, it works correctly

    Testing Maintenance of Game Data (test both modes):
        1. Start playing a game of scrambled
        2. Enter a few words noting the updating score and time 
        3. Reload page 
        4. If game data (time, score, words) are consistent this works

Testing Admin Privileges:
    Changing Letters Functionality (repeat for both modes):
        1. Login as admin (username admin - password admin)
        2. Click the link to change letters on statistics page
        3. Enter desired letters in to Speed mode 
        4. Click Submit
        5. Go to Speed Mode and check the letters are updated accordingly
    If they reflect the updates, the admin overwrite works correctly

    Reset Game after Admin Changes (repeat for both modes):
        1. Enter a word into a game of Scrambled
        2. Login as admin 
        3. Reset letters as you wish 
        4. Return to game 
        5. Success if word entered, score and time have reset back to base conditions
    If this is the case, the admin overwrite works correctly

    Testing Access to Admin only alter page:
        1. Either log on (with an account other than admins) or without login 
        2. Type /alter into the search bar
        3. If not logged in will direct you to login 
        4. If logged in it will direct you to the statistics page
    This means only admin can access the special priveleges to change game

Testing Error Handling:
    1. Go onto the Scrambled website
    2. Enter in the search bar /test or any non-supported link
    3. A special error page will appear and direct you back to the welcome page
If this is the case, the error handling works correctly 

Testing Dark Mode:
    General Test:
        1. Load Scrambled website 
        2. Click settings and click dark mode
        3. Everything should switch colours (except blue buttons)
        4. Reload page
    If everything maintains this theme, the dark mode functionality works correctly 
