import os
import pathlib

from dataclasses import dataclass


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

    # Filesystem
    base_dir = pathlib.Path(__file__).parent.parent
    project_root = base_dir.parent
    templates_dir = project_root / 'templates'
    static_files_dir = project_root / 'static'
    emotes_dir = project_root / 'static' / 'emotes'
