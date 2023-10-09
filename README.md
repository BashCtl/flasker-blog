# Clone of blog application by using Flask
#### Project structure
````
src/
├── blueprints - application routes
├── forms - app forms
├── models - db models
├── services - interation with db
├── static - content for styles, images, js code
│   ├── css
│   ├── images
│   └── js
└── templates - application web pages templates
````
Install project requirements
````
pip install -r requirements.txt
````
Install MySQL database

[Download MySQL](https://dev.mysql.com/downloads/)

Create .env file in the root of the project, with following variables
````
SECRET_KEY=(some random secret value, can be generated hash value) 
DATABASE_URI=mysql+pymysql://{username}:password@localhost/{db name}?charset=utf8mb4
TEST_DATABASE_URI=sqlite:///test.db - for testing using sqlite
````
To start application run following command:
````
python run.py
````
Alternative way to start application on Linux OS using CLI
````
export FLASK_APP=run.py
flask run
````
On Windows CMD:
````
set FLASK_APP=run.py
flask run
````