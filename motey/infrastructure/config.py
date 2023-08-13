import os
import pathlib
import base64

from dataclasses import dataclass
from cryptography.fernet import Fernet


@dataclass(frozen=True)
class Config:
    # Database
    database = os.getenv('MYSQL_DATABASE')
    database_user = os.getenv('MYSQL_USER')
    database_password = os.getenv('MYSQL_PASSWORD')
    database_host = os.getenv('MYSQL_HOST')
    database_port = int(os.getenv('MYSQL_PORT'))

    # HTTP
    http_host = os.getenv('HTTP_HOST')
    http_port = int(os.getenv('HTTP_PORT'))
    cookie_encryption_key = base64.urlsafe_b64decode(Fernet.generate_key())

    # Filesystem
    base_dir = pathlib.Path(__file__).parent.parent
    project_root = base_dir.parent
    templates_dir = project_root / 'templates'
    static_files_dir = project_root / 'static'
    emotes_dir = project_root / 'static' / 'emotes'

    # OAUTH
    client_secret = os.getenv('CLIENT_SECRET')
    client_id = os.getenv('CLIENT_ID')
    redirect_url = os.getenv('REDIRECT_URL')
    auth_start_url = os.getenv('AUTH_START_URL')

    # BOT
    token = os.getenv('BOT_TOKEN')
