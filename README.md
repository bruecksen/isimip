# ISIMIP (Inter-Sectoral Impact Model Intercomparison Project)

This [Django](https://docs.djangoproject.com/en/stable/) and [Wagtail CMS](http://docs.wagtail.io/en/latest/) based repository powers the [ISIMIP](https://www.isimip.org/) website.

> ISIMIP offers a framework for consistently projecting the impacts of climate change across affected sectors and spatial scales. An international network of climate-impact modellers contribute to a comprehensive and consistent picture of the world under different climate-change scenarios.

## Features
- Django 
- Wagtail CMS
- Elasticsearch
- Twitter bootstrap

## Getting started
This project is based on the "Two Scoops of Django" best practices [project template](https://github.com/twoscoops/django-twoscoops-project). The installation assumes a working PostgreSQL (with table creation rights) database and python 3.x environment. To use this project follow these steps:

### Create your working environment
You have several options in setting up your working environment. We recommend using virtualenv to separate the dependencies of your project from your system's python environment. If on Linux or Mac OS X, you can also use virtualenvwrapper to help manage multiple virtualenvs across different projects.

- https://virtualenv.pypa.io/en/stable/
- http://virtualenvwrapper.readthedocs.io/en/latest/

### Populate .env with your environment variables
Some of these services rely on environment variables set by you. There is an env.example file in the root directory of this project as a starting point. Add your own variables to the file and rename it to .env. This file won’t be tracked by git by default so you’ll have to make sure to use some other mechanism to copy your secret if you are relying solely on git.

### Install dependencies
Depending on where you are installing dependencies:

In development:

    $ pip install -r requirements/local.txt

For production:

    $ pip install -r requirements.txt

### Migrate
Run any migrations required:

    python manage.py migrate

## Running the application

In the root project folder, run:

    python manage.py runserver

## Credits
- https://github.com/wagtail/wagtail
- https://github.com/django/django
- https://github.com/twoscoops/django-twoscoops-project

## Contact
Feel free to contact me to discuss any issues, questions, or comments.

My contact info can be found on my [GitHub page](https://github.com/bruecksen).

## License
MIT License, see license [file](https://github.com/bruecksen/isimip/blob/master/LICENSE)