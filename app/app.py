import os
from app.create_app import create_app

app = create_app(os.environ['APP_SETTINGS'])
