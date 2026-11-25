
from pathlib import Path
import pygame


class SpriteLoadingError(Exception):
    def __init__(self, msg: str, file: Path):
        self.message = msg
        self.content = file
        super.__init__(self.message)


class SpriteBank:
    _content: dict[str, dict[str, pygame.Surface]] = {}

    def __len__(self) -> int:
        return len(self._content)

    def __contains__(self, key: str) -> bool:
        return key in self._content

    @classmethod
    def get_sprites(self, category: str) -> dict[str, pygame.Surface]:
        return self._content[category]

    @classmethod
    def get_sprite(self, category: str, key: str) -> pygame.Surface:
        return self._content[category][key]

    @classmethod
    def store(self, category: str, key: str, content: pygame.Surface) -> bool:
        self._content.setdefault(category, {})
        is_new: bool = key not in self._content[category]
        self._content[category][key] = content
        return is_new

    @classmethod
    def delete(self, key: str) -> bool:
        return self._content.pop(key, None) is not None
