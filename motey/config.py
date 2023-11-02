import os
import pathlib
import base64
import secrets

from dataclasses import dataclass
from cryptography.fernet import Fernet


def get_cookie_encryption_key():
    cookie_encryption_key_file_path = pathlib.Path(__file__).parent / "cookie_encryption_key.dat"
    if not cookie_encryption_key_file_path.is_file():
        cookie_encryption_key_file_path.write_bytes(base64.urlsafe_b64decode(Fernet.generate_key()))
    return cookie_encryption_key_file_path.read_bytes()

def get_secret_phrase():
    secret_phrase_path = pathlib.Path(__file__).parent / "secret_phrase.dat"
    if not secret_phrase_path.is_file():
        secret_phrase_path.write_text(secrets.token_hex(16))
    return secret_phrase_path.read_text()


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
    cookie_encryption_key = get_cookie_encryption_key()
    secret_phrase = get_secret_phrase()
    form_field_name = '_csrf_token'
    cookie_name = 'csrf_token'

    # Filesystem
    base_dir = pathlib.Path(__file__).parent
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
