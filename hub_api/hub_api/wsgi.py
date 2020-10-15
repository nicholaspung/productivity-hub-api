import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

project_folder = os.path.expanduser('')  # project directory
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub_api.settings')

application = get_wsgi_application()
