----- SplitApp -----
    This app is created to keep track of all the expenses and contributions to an activity by some people

----- Stack Used -----
    Programming Language:
        Python 3

    Libraries and Frameworks:
        FastAPI, sqlalchemy

    Databse:
        MariaDB

----- Included Files in this Repo -----
    1. Code Repo
    2. Docker File
    3. docker-compose.yaml
    4. requirements.txt
    5. readme.txt
    6. ApisInfo.txt (For Information about the apis present)
    7. Postman Collection (Note: This postman collection also has examples for your reference to use the apis)

    

Steps to run the App:
    1. Go to a Linux/Windows machine
    2. Install Docker on that machine
    3. Either Copy the docker-compose.yaml file and put it there in machine or copy contents of the docker-compse.yaml file
       and create a new file named "docker-compose.yaml"
    4. Now run the following command
        $ docker-compose up
    5. Now open any web browser on search
        http://localhost:5005/docs
        This will give information about all the apis present
    