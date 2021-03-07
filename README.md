# Productivity Hub

Backend application to house productivity tools:

- A habit tracker
- A post saver

Note: to be used in conjunction with [productivity-hub](https://github.com/nicholaspung/productivity-hub)

## Tech Stack

- Python
- Django
- Django Rest Framework
- Firebase Admin
- Fuzzywuzzy
- Beautiful Soup 4
- APScheduler (development only)
- Dotenv
- PostgreSQL
- Cron

## Environment Variables

```
FIREBASE_PROJECT_ID=
FIREBASE_PRIVATE_KEY_ID=
FIREBASE_PRIVATE_KEY=
FIREBASE_CLIENT_EMAIL=
FIREBASE_CLIENT_ID=
FIREBASE_CLIENT_CERT_URL=
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS_DOMAIN=
ALLOWED_HOSTS_IP_ADDRESS=
CORS_ALLOWED_ORIGINS=
POSTGRES_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
FIRST_TIME=
```

### Future Features + Needs Work

See the project page [here](https://github.com/nicholaspung/productivity-hub-api/projects/1)

## Project Setup

1. Clone this repo
2. Create a Firebase account, create a new project, and enable Firebase Authentication. This account will also be used with [productivity-hub](https://github.com/nicholaspung/productivity-hub)
   - Go to Settings > Service Accounts > Generate new private key for .env
3. Add environment variables to .env file using Firebase settings
4. In `/hub_api/hub_api/wsgi.py`, change up the project directory folder to be able to load .env files in your server configuration
5. In `/hub_api/hub_api/settings.py`, for logs, change up the project directory folder to your designated log directory.
6. `pip install -r requirements.txt`
   - _You may need to install Build Tools for Visual Studio - Microsoft_
7. `cd hub_api`
8. `python manage.py migrate`
   - On first run, set `FIRST_TIME=True` in .env
   - On subsequent runs, set `FIRST_TIME=False` in .env
9. `python manage.py runserver`

## For Development

1. In `/hub-api/hub-api`, run `python manage.py createsuperuser`

#### Tested with Python 3.8.5

## Setup Cron jobs on a server

1. Example script is given in `run_cron_jobs`
2. On your server, modify the scripts to each command
   - i.e. `run_cron_jobs` line 8, `python manage.py sample`
3. Change the permissions of the cron jobs using `chmod +x /path/to/script`
4. `crontab -e` to open up/create the main cron file
5. Example usage for the following commands:

   - `*/30 * * * *` /path/to/script/runevery30minutes
   - `0 */3 * * *` /path/to/script/runevery3hours
   - `0 0 * * 0` /path/to/script/runeveryweek
   - `0 * 1,16 * *` /path/to/script/runevery2weeks (2 times a month, rather than every 2 weeks)

   - You can also set outputs to files by attaching `>> /path/to/log/sample.log 2>&1`. This is good for debugging why your script isn't running

6. You can also set up a `MAILTO=` in `crontab -e` to be sent an email everytime a cron job is finished

## To auto-generate schema

`python manage.py generateschema --format openapi > schema.yml`

## To generate Django Secret Key

- Go into Django shell `python manage.py shell`

`python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

## Example of how to move Django models around in apps

Examples that require database downtime when changing models around in apps

- Use `python manage.py sqlmigrate xxxx` to check the generated SQL statements created by Django. Modify if needed

- See `/open_apps/migrations/0001_initial.py` and `/post_saver/migrations/0006_auto_20201129_2151.py` in combination

For a no downtime migration remapping a model to a different table, in `models.py`, for your Model classes, set a

```
class Meta:
   db_table = 'xxxxx'
```

for your table to be called 'xxxx'. By explicitly calling the db_table name, you bypass Django's auto-generated table names and gain control over your database naming conventions. (Not sure about any other operations you perform in a database)
