import os
from io import BufferedReader
from pathlib import Path
import os

from motey.infrastructure.config import Config


class InvalidFileExtension(Exception):
    pass


class EmoteFileWriter:
    VALID_EXTENSIONS = ('jpg', 'png', 'webp', 'gif')

    def __init__(self, emote_name: str, file_name: str, reader: BufferedReader, config: Config = Config()):
        self._emote_name = emote_name
        self._file_name = file_name
        self._reader = reader
        self._emotes_dir = config.emotes_dir

    @property
    def extension_valid(self) -> bool:
        extension = self._get_file_extension()
        return extension in self.VALID_EXTENSIONS

    @property
    def path(self) -> Path:
        return self._build_file_path()

    def save_to_filesystem(self) -> None:
        if not self.extension_valid:
            raise InvalidFileExtension
        file_content = self._reader.read()
        path = self._build_file_path()
        with open(path, 'wb') as output_file:
            output_file.write(file_content)

    def rollback(self) -> None:
        path = self._build_file_location()
        os.remove(path)

    def _build_file_path(self) -> Path:
        extension = self._get_file_extension()
        return self._emotes_dir / f'{self._emote_name}.{extension}'

    def _get_file_extension(self) -> str:
        return self._file_name.split('.')[-1]
