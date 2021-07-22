# OC_Projet_09
Développez une application web en utilisant Django

## Set up the project
This project runs in python 3

Make a copy of this project on your hard drive <br>
`git clone https://github.com/friquette/OC_Projet_09.git`

Go in the root project and create a virtual environment <br>
`cd OC_Projet_09` <br>
`python -m venv env`

Activate your virtual environment <br>
- On Windows `env\Scripts\activate.bat`
- On Mac OS/Linux `source env/bin/activate`

Install the packages <br>
`pip install -r requirements.txt`

## How to use it
Go to the litreview folder
`cd litreview`

For the first time you are using the applicatin, migrate the tables in the database<br/>
`python manage.py migrate`

Run your server</br>
`python manage.py runserver` </br>

And go to `localhost:8000` on your web browser.

The database will be created in the root application folder and 
is named db.sqlite3 </br>
All the images uploaded by the users will be saved in a media folder in 
the root application folder.

Before sending the application online, open the settings.py file in litreview folder, 
and change the `DEBUG = True` to `DEBUG = False`

## Admin part

To create an admin user, go to the root application folder and enter:
`python manage.py createsuperuser`
and follow the instructions.

To access the admin site page, go to
`localhost:8000/admin` in your web browser.
