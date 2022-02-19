# Jasper: Automated Crowdsourced News

[See the project](https://jaspernews.herokuapp.com/)

## Description

Jasper is an online news aggregator built on the Python Django framework. It provides crowdsourced news coverage from popular news related Reddit.com subreddits. Create an account to select your interests, add articles to your reading list, and more!

## Getting Started

### Dependencies

* asgiref==3.4.1
* backports.entry-points-selectable==1.1.1
* beautifulsoup4==4.10.0
* certifi==2021.10.8
* charset-normalizer==2.0.9
* distlib==0.3.4
* dj-database-url==0.5.0
* Django==4.0
* filelock==3.4.0
* gunicorn==20.1.0
* idna==3.3
* Pillow==8.4.0
* platformdirs==2.4.0
* psycopg2-binary==2.9.2
* requests==2.26.0
* six==1.16.0
* soupsieve==2.3.1
* sqlparse==0.4.2
* urllib3==1.26.7
* virtualenv==20.10.0
* whitenoise==5.3.0

### Installing

```
git clone https://github.com/Arden-Zeng/Jasper.git
```

### Executing program

See how to [deploy](https://devcenter.heroku.com/articles/deploying-python) Django apps on Heroku.

If you want to test things out locally:

```
python manage.py runserver
```
The webapp will be hosted at: http://127.0.0.1:8000/

Please note that deployment to Heroku requires static files to be stored in a way that does not permit them to be shown on local builds. In particular, CSS, JS files will be missing meaning that a local build won't be feature complete.

Please note that deployment to Heroku requires a PostgreSQL database - you will probably want to use a SQLite database for local development purposes.

## Authors

Arden Zeng

## License

This project is licensed under the MIT License.
