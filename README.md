# Hangar49_Task
This repo contains the application for the hangar49 Tech Task. The front end was built with React and The backend was built with Flask and SQL ALchemy.The DB used is Postgres 

# Dev Requirements Backend
Required to install postgresql server on local machine and create DB, replace the connection string on line 15 in app.py
Create the Database tables using the model defined in app.py by the following in the Python console

```bash
form app import db
db.create_all()

```


# Install Requirements 
To install and setup local dev environment setup virtualenv using python 3.7
```bash
virtualenv venv -p python3.7
```

Now activate venv:
```bash 
 ## Mac OS or Linux
source venv/bin/activate

## Windows 
venv\Scripts\activate
```

Finally install pip packages:
```bash
pip install -r requirements.txt .
```

# Run application
To run the application locally you can simply run `flask run` inside virtualenv after requirements were installed

# Dev Requirements Frontend

# Install Requirements 
To install and setup local dev environment setup Node and run
```bash
 npm install
```

# Run application
To run the application locally you can simply run `npm start` inside virtualenv after requirements were installed


 
 
