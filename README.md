# AccuKnox Assignment
**This repository can be used for review of the assignment by AccuKnox team as a part of recruitment process.**

### Problem Statement
Create an API for social networking application using Django Rest Framework with
below functionalities.

### Constraints
- Use any database of your choice
- You are free to design Request/Response fields/formats

### User Login/Signup
- Users should be able to login with their email and password (email should be case-insensitive)
- User should be able to signup with their email only (no otp verification required, valid email format is sufficient)
- Except signup and login every api should be called for authenticated users only

### Develop API for following functionalities
- API to search other users by email and name(paginate up to 10 records per page).
  - If search keyword matches exact email then return user associated with the
  email.
  - If the search keyword contains any part of the name then return a list of all
  users.
  eg:- Amarendra, Amar, aman, Abhirama are three users and if users search with "am"
  then all of these users should be shown in the search result because "am"
  substring is part of all of these names.
  - There will be only one search keyword that will search either by name or email.
- API to send/accept/reject friend request
- API to list friends (list of users who have accepted friend request)
- List pending friend requests(received friend request)
- Users can not send more than 3 friend requests within a minute.

## Installation Steps
### Requirements
- postgres 13.3
- python 3.9
- python packages are available in [requirements.txt](./requirements.txt)
- Docker CLI

### How to use (non-docker way)
- Pull the github code to your system.
- To run without container; make sure you have postgres, python installed on your system. Before running the python
code, check whether postgres service is started.
- Edit environment variable present in [.env](./.env) file, like **DB_NAME**, **DB_USER**, **DB_PASSWORD**, **DB_HOST**
& **DB_PORT** as needed.
- **DB_HOST=db** & **DB_PORT=5433** needs to be commented out during edit.
- Enter to the project root directory.
- Run the migrations; This will create the required tables in database
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- Now, the server is ready to start; the apis can be accessed through localhost with port **8000**.
  ```bash
  python manage.py runserver 0.0.0.0:8000
  ```

### How to use (with docker)
- Pull the github code to your system.
- Enter to the project root directory.
- Make sure your system port **8000** is available.
- Run the docker compose command to start build & start the containers.
  ```bash
  docker-compose up
  ```
- The service port is expose to port **8000** of your system. So the APIs can be used from localhost.

## API documentation
- Import the API documentation & collection in postman from 
https://api.postman.com/collections/14283218-d83175d4-3ef0-4ae6-b033-45d7522accd6?access_key=PMAT-01HFPBZY7D2SFQVEGPPCWPMT6R