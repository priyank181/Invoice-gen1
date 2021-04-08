This application allows you to create invoices and send conformation mails to trainers on trainings at various colleges.


## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/priyank181/Invoice-gen1/new/master?readme=1
$ cd sample-django-app
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
And navigate to http://127.0.0.1:8000
