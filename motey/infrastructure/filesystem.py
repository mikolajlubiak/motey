import os
from io import BufferedReader
from pathlib import Path

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
    def location(self) -> Path:
        return self._build_file_location()

    def save_to_filesystem(self) -> None:
        if not self.extension_valid:
            raise InvalidFileExtension
        file_content = self._reader.read()
        location = self._build_file_location()
        with open(location, 'wb') as output_file:
            output_file.write(file_content)

    def rollback(self) -> None:
        location = self._build_file_location()
        os.remove(location)

    def _build_file_location(self) -> Path:
        extension = self._get_file_extension()
        return self._emotes_dir / self._emote_name + f'.{extension}'

    def _get_file_extension(self) -> str:
        return self._file_name.split('.')[-1]
