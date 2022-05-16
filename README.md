# CITS3403Project

Agile Web Dev Project for CITS3403 

1. the purpose of the web application, explaining the design of the game
    - 

2. the architecture of the web application.
3. describe how to launch the web application.
    1. cd scrambled/
    2. source venv/bin/activate
    3. make sure to run pip install -r requirements.txt make sure that the webiste will run with al of its dependencies otherwise there might be   problems
    4. flask run  
    5. while running the application there are multiple ways to access the webiste one being, 127.0.0.1:5000/index or localhost:5000/index
4. describe some unit tests for the web application, and how to run them.
    1. make sure the directory is located inside Scrambled 
    2. run python3 tests.py

## Short description of some unit tests

    1. Statistics ForeignKey
        - this unit test will open both the user and Statistics table while inputting dummy data into both and will make sure that each table will be referenced together with both the username and id
    2. Avatar test  
        - this simple test will make sure that when referencing the gravtar library for easy an easy to use avatar system, the hashing done, in md5, outputs the correct avatar for the string that is created 
    3. Password Hashing 
        - this simple check will test the provided password like admin and check it against another word to make sure its working fine in the actual environment where it matters 
5. Include commit logs, showing contributions and review from both contributing students


