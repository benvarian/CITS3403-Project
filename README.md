# CITS3403Project

Agile Web Dev Project for CITS3403 

1. the purpose of the web application, explaining the design of the game
    The purpose of this web application is to provide a fun daily game, similar to Wordle. Scrambled is a new, fun take on a number of different games. Taking inspiration from Scrabble and Countdown, Scrambled is a word game which requires users to create the highest 6 words possible with the 7 letters generated each day. The game also provides a number of fun, interactive features for the users. It also tracking of statisitcs and viewing of friend's profiles. 

2. the architecture of the web application.
    Scrambled uses many technologies to deliver the game the user sees. 
    
    Underlying everything is the database which stores important information regarding the user and their statistics. The interactions with the database are dictated by the corresponding Python model classes. The database is used to maintain statistics of the users to be displayed on their user profiles. 

    Flask provides the middleware for the application. It provides the interaction with the databases using the models. This includes transmitting game scores to the database and inputting new users.  As an example of server-side rendering, Flask is also responsible for rendering the HTML templates. Consequently, Flask is responsible for controlling the routes of the website. Through Jinja and server-side rendering, the website content is dynamic based upon the user's status. Flask also handles the necessary input and output from the Scrambled game. It is responsible for transmitting the daily letters to the Javascript and allows the admin to overwrite the daily letters. Further, it checks the words inputted by users and responds appropriately. Each game statistic's is transmitted to the Flask server and then appropriatley stored within the database for future use.
    
    Javascript is responsible for the user's interaction with the game. Interacting with the server through AJAX requests, Javascript renders the game and permits the users interaction with it through the document object model (DOM). This allows the user to play the game, providing the functionality for clicking buttons, etc. It is also vital for storing the game's data whilst in progress, using cookies to do so. Javascript also supports the dark mode functionality. 

    HTML and CSS provide the user's view of the web application. Using a mix of custom CSS and Bootstrap, Scrambled provides a responsive view depending on the devices used. Supporting both mobile, desktop and tablet, the CSS and HTML are essential for the user's game experience.

3. describe how to launch the web application.
    1. cd scrambled
    2. source venv/bin/activate
    3. make sure to run pip install -r requirements.txt make sure that the webiste will run with all of its dependencies otherwise there might be problems
    4. flask run  
    5. Scrambled is the accessible at 127.0.0.1:5000/ or 127.0.0.1:5000/welcome

4. Describe some unit tests for the web application, and how to run them.
    1. make sure the directory is located inside Scrambled 
    2. run python3 Test/tests.py

## Short description of some unit tests

Unit Tests for Statistics 
    1.
    2.

Unit Tests for User
    1. Statistics ForeignKey
        - this unit test will open both the user and Statistics table while inputting dummy data into both and will make sure that each table will be referenced together with both the username and id
    2. Password Hashing 
        - this simple check will test the provided password like admin and check it against another word to make sure its working fine in the actual environment where it matters 
    
5. Include commit logs, showing contributions and review from both contributing students


A number of other pieces of information:
Admin Functionality:
    To test the admin functionality please login with the admin account (username:admin, password:admin). This will account will only have access to the admin overwrite functionality. 

A note on the HTML validation:
    Due to our use of the server-side rendering service Jinja, our HTML does not pass the validator. However, these error are due to how the validator sees the templates that get rendered. As they all extend the base.html (which includes doctype, lang, etc.), they should not actually fail the validation due to these factors because, when rendered, the website has these elements. 
 


