# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

## To Load and start this project
## 1. Start up the backend

### Install Dependencies [navigate to backend]
```bash
cd backend
```


#### Ensure you have Python 3.7 or higher

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
or follow code below:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
### Navigate to src directory and start the backend
```bash

cd src
export FLASK_APP=api.py
flask run
```
For more details: 
[View the README.md within ./backend for more details.](./backend/README.md)

## 2. start the frontend
### Navigate to frontend, Install dependencies, start porject
```bash
cd ./frontend/
npm install
sudo npm install -g @ionic/cli
npm start
```
For more detials:
[View the README.md within ./frontend for more details.](./frontend/README.md)





