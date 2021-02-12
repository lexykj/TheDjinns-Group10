# Big Blue's Parking Genie

## The Djinns - Group 10

A Djinn in Arabic lore is a shapeshifting spirit that possesses supernatural powers that can be conjured to perform various tasks and services. Djinns that have the ability to grant wishes are more colloquially known as genies. Big Blue's Parking Genie takes the unique form of a website that serves all your parking management needs. We aim to make finding parking as easy as making a wish. 

## Version-control procedures 

We will be using git and GitHub as verson control for this project. Group members will be assigned diffrent sections as of the project as marked in TODO.md. Group members will fork the main branch and work on their section on their own. Once they are done they will mark their section as done in the TODO and merge their branch abck to main. There is also a column in the TODO that indicates that that portion should not be worked on by anyone else if that mark is checked in order to minimise merge problems.

Project milestones will be tagged with the "Milestone_$n" tag where $n is the milestone number. 

## Tool stack description and setup procedure 

This application will use the [Django](https://www.djangoproject.com/) as it's web application framework along with [Apache](https://httpd.apache.org/) with [mod_wsgi](https://modwsgi.readthedocs.io/en/develop/index.html) as it's production web server. Django is a web application framework written in and using the Python programming language. The following will be the minimum essential software for our application:

 - Bash command-line interface
 - Git version control system
 - Python programming language version 3.8 or greater
 - The Django Web Application Framework version 3.1 or greater

For a database we will be using SQLite, but this is subject to change.

While Git, Bash, and Python are already likely to be set up on your system, Django, Apahie, and mod_wsgi probably aren't. To install Django we can simply use the `pip` package manager that comes with python and run the following command:

```
$ pip3 install --user django
```

Any other required softwere will also be listed here as the need develops

## Build instructions

Since Python is an interpreted language, no compilation is needed. Simply run the following command to start the server:

```
$ python3 genie/manage.py runserver
```

## Unit testing instructions

Django has a built in [testing interface](https://docs.djangoproject.com/en/3.1/intro/tutorial05/) which we will use to create unit tests. Simply run `python3 genie/manage.py test` followed by the name of one of our apps. Here is the command to test the event app:

```
$ python3 genie/manage.py test event
```

## System testing instructions

