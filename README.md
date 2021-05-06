# Student Career Portal (Database Project)

![Django CI](https://github.com/Gr8ayu/SPCPortal/workflows/Django%20CI/badge.svg)

This project was developed as project work for college database course.
It is developed in Django and PogreSQL database with following objective.

The portal is being designed for the department, faculties and students, to keep them updated about the internship/placement statistics as well as the upcoming opportunities. The portal will help students to efficiently manage their time and will provide them with an all-in-one hub for internship/placement activities. This portal will help the students and placement department to efficiently manage applications for companies and keep track of offers made to the students.

------------

More detailed information is shared in [report](https://raw.githubusercontent.com/Gr8ayu/SPCPortal/master/Final%20report%20SPC%20Portal.pdf "report") .

A demo website is hosted [here](https://rvians.online/ "here").

[video demonstration](https://youtu.be/I8NV3oDUxRY "video demonstration")


------------


### Steps to run (using docker):
- install docker 
- move to root directory of project and run command 
`docker-compose up  --build`

### Steps to run (Alternate):
- install python 3.6+
- create virtualenv 
`python3 -m venv env`
- activate virtualenv
`source env/bin/activate`
- install dependencies
`pip3 install -r requirements.txt`
- start django server 
```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 0.0.0.0:8000
```
------------

You can access the website on http://127.0.0.1:8000/ and login with superuser account at http://127.0.0.1:8000/admin .

Setup the server to signin with google as explained [here](https://whizzoe.medium.com/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5 "here").



