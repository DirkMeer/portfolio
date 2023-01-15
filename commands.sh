python -m venv .env
ls -al
#activate the virtual environment
source .env/Scripts/activate
pip install django

#show what is installed in the virtual environment
pip freeze

#start a new django project
django-admin startproject portfolio

#run the dev server
python manage.py runserver

#create an app within the project (we named it projects)
python manage.py startapp projects

#fast html boilerplate
! <Enter>

#make the migrations file
python manage.py makemigrations
#apply the migrations file to the database
python manage.py migrate

#python shell
python manage.py shell
#import the model from our projects app
>>> from projects.models import Project
>>> p1 = Project(title="test project", description="this is a test, 1234!", technology="Django", image="")