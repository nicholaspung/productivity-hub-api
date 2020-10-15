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
- APScheduler
- Dotenv

## Environment Variables

```
FIREBASE_PROJECT_ID=
FIREBASE_PRIVATE_KEY_ID=
FIREBASE_PRIVATE_KEY=
FIREBASE_CLIENT_EMAIL=
FIREBASE_CLIENT_ID=
FIREBASE_CLIENT_CERT_URL=
```

### Future Features + Needs Work

See the project page [here](https://github.com/nicholaspung/productivity-hub-api/projects/1)

## Project Setup

1. Clone this repo
2. Create a Firebase account, create a new project, and enable Firebase Authentication. This account will also be used with [productivity-hub](https://github.com/nicholaspung/productivity-hub)
3. Add environment variables to .env file using Firebase settings
4. In `/hub_api/hub_api/wsgi.py`, change up the project directory folder to be able to load .env files in your server configuration
5. `pip install -r requirements.txt`
6. `cd hub_api && python manage.py runserver`

#### Tested with Python 3.8.5

## Troubleshooting

- On initial `python manage.py migrate`, you'll have to disable `scheduler.start()` lines in `urls.py`
  - Current files needing changes
    - `firebase_auth/urls.py` line 17
    - `post_saver/urls.py` line 18
- After a successful migration, remember to enable `scheduler.start()` again to run background scripts running on the server
