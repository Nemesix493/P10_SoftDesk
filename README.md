# P10_SoftDesk

## Install with virtual env
### Get a virtual env
In the code directory type this command
```shell
python -m venv env
```
### Active the virtual env
macOS or linux
```shell
source /env/bin/activate
```
Windows
```shell
\env\Scripts\activate.bat
```
### Install dependencies
```shell
python -m pip install -r requirements.txt
```
### Init the database
```shell
python -m manage.py migrate
```
### Set up the test environement
If you want test the app with preloaded data.

This command set up the [test env](#to-test-the-test-environement)
```shell
python -m manage.py init_local_test
```
### Run the test server
```shell
python -m manage.py runserver
```
By default the server run on the 8000 port
To run it on another port like "8080" run
```shell
python -m manage.py runserver 0.0.0.0:8080
```
___
## Test with docker
You just need ro run the docker-compose file in the project directory by
```shell
docker-compose up
```
or if you want test the app with preloaded data, 
this command to run the [test env](#to-test-the-test-environement)
```shell
docker compose -f "test_env_Docker-compose.yml" up --build
```
By default it run server on port 8000 
```yaml
    ports:
      - "8000:8000"
```
to run it on another port like "8080" change to 
```yaml
    ports:
      - "8000:8080"
```
___
## To test the test environement
The test environement comes with three user with some post to test manualy the features 
```json
[
    {
        'email': 'daniel@SoftDesk.com',
        'first_name': 'Daniel',
        'password': 'motdepasse',
        'last_name': 'last-name'
    },
    {
        'email': 'serge@SoftDesk.com',
        'first_name': 'Serge',
        'password': 'motdepasse',
        'last_name': 'last-name'
    },
    {
        'email': 'claude@SoftDesk.com',
        'first_name': 'Claude',
        'password': 'motdepasse',
        'last_name': 'last-name'
    },
]
```
___
## The server is running in DEBUG mod
### **Do not run it in production !!!**
