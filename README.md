# Big Blue's Parking Genie

## The Djinns - Group 10

A Djinn in Arabic lore is a shapeshifting spirit that possesses supernatural powers that can be conjured to perform various tasks and services. Djinns that have the ability to grant wishes are more colloquially known as genies. Big Blue's Parking Genie takes the unique form of a website that serves all your parking management needs. We aim to make finding parking as easy as making a wish. 

## Version-control procedures 

We will be using git and GitHub as verson control for this project. Group members will be assigned diffrent sections as of the project as marked in TODO.md. Group members will fork the main branch and work on their section on their own. Once they are done they will mark their section as done in the TODO and merge their branch abck to main. There is also a column in the TODO that indicates that that portion should not be worked on by anyone else if that mark is checked in order to minimise merge problems.

Project milestones will be tagged with the `Milestone_$n` tag where `$n` is the milestone number. 

## Tool stack description

This application will use the [Django](https://www.djangoproject.com/) as it's web application framework. Django is a web application framework written in and using the Python programming language. The following will be the minimum essential software for our application:

 - Bash command-line interface
 - Git version control system
 - Python programming language version 3.8 or greater
 - Django web application framework version 3.1 or greater

For a database we will be using SQLite which is the default for Django, but this is subject to change.

## Setup procedure

While Git and Bash are already likely to be set up on your system, Django and Python probably aren't. Follow [this link](https://www.python.org/downloads/) to download and install Python. To install Django we can simply use the `pip` package manager that comes with Python and run the following command:

```
$ pip install --user django
```

You will also need to install a font package:

```
$ pip install --user django-static-fontawesome
```

## Build instructions

Since Python is an interpreted language, no compilation is needed. Simply run the following command to start the server:

```
$ python genie/manage.py runserver
```

## Unit testing instructions

Django has a built in [testing interface](https://docs.djangoproject.com/en/3.1/intro/tutorial05/) which we will use to create unit tests. Simply run `python3 genie/manage.py test` followed by the name of one of our apps. Here is the command to test the event app:

```
$ python genie/manage.py test event
```

## System testing instructions

Testing your system is as easy as seeing if you have the correct versions of Python and Django installed. First run the command to check python version:

```
$ python --version
```

If the version is 3.8 or higher you can run the command to check Django's version:

```
$ python -m django --version
```

If you see 3.1 or higher your system can run the server!

## Using the website for the first time

If you are the first user to run the website on your device then a few additional steps are necessary.  First create a superuser in order to access `localhost:8000/admin` by running:

```
python manage.py createsuperuser
```

And then entering a username and password. This will create the first system user and allow you admin privileges. Because this first user is created by Django and not by the website itself, an additional step is necessary. Navigate to the Profile tab in `localhost:8000/admin` and press the 'Add Profile' button in the top right of the screen. Fill in the necessary information, including permissions, and then select your existing superuser account as the user tied to the profile. Press 'Save' and you will be done. Navigate to `localhost:8000` and you will be ready to use the website.