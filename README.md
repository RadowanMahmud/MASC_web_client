# MASC Django Web front end
The project is intended to provide a user interface for the user in order to properly use MASC. The user interface shall give the user the privildge to run Masc lab 
and Masc engine. Through this the user will be able to visualize the mutations of Masc.

# Environments
The project is based on django frame work.
python => 3.10.4
Django => (4, 0, 5, 'final', 0)

# Run Project
Create virtual environment
python3 -m venv venv
source venv/bin/activate

Install dependecies
pip install -r requirements.txt

Make Migration
python manage.py makemigrations
python manage.py migrate

Run server
python manage.py runserver
