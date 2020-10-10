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
- TravisCI

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

1. Clone this repo.
2. Create a Firebase account, create a new project, and enable Firebase Authentication. This account will also be used with [productivity-hub](https://github.com/nicholaspung/productivity-hub).
3. Add environment variables to .env file using Firebase settings.
4. `pip install -r requirements.txt`
5. `cd hub_api && python manage.py runserver`

#### Tested with Python 3.8.5
