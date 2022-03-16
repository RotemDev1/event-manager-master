# Event Manager
Event manager project for college course

## How to run?
Make sure you are in event_manager directory using command `pwd`

And then run following command to run the server:

`python manage.py runserver`

## Requirements
Python v3+

django v2+

## Installation
To install django, run the following command:
`pip install django`

To install MySQL, use:
`pip install pymysql`

To install crispy-forms, use:
`pip install django-crispy-forms`

To check if django is installed, use:
`python -m django --version`

To check if python is installed, use:
`python --version`

## Migrations
To run migrations run the following commands in order:

`python manage.py makemigrations`

`python manage.py migrate`

## Test
Run the following commands to install requirements for tests:

`pip install django_jenkins`

`pip install 'coverage==4.5.4'`

`pip install pep8`

`pip install pyflakes`

`pip install pylint`


To run tests, use:
`python manage.py jenkins --enable-coverage`

## Start new app
To start a new app use:
`python manage.py startapp <app_name>`

And then add the app to INSTALLED_APPS and PROJECT_APPS in event_manager/setting.py.