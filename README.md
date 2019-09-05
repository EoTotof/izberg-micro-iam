Micro IAM
=========
 
Setup
-----
	$ git clone https://github.com/EoTotof/izberg-micro-iam.git
	$ cd izberg-micro-iam
	$ python -m venv
	$ .\Scripts\activate # on Windows
	(env) pip install -r requirements.txt
	
Launch
------
	(env) cd micro_iam
	(env) python manage.py runserver
	
The API can then be called at localhost:8000.

A Postman collection is available at the root of the repository (micro_iam.postman_collection.json).

To reset the database and repopulate it with data requested in the exercise, delete the DB file db.sqlite3 from the micro_iam folder and run the following commands from the micro_iam folder:

	(env) python manage.py migrate
	(env) python manage.py populate
	
I've written a test suite as an answer to the questions in the exercice which can be run with the following command:

	(env) python manage.py test
	
The source for this test is in micro_iam/apps/iam/tests.py
