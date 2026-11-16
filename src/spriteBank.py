
import pygame


class SpriteBank:
    def __init__(self) -> None:
        self._content: dict[str, pygame.Surface] = {}

    def __len__(self) -> int:
        return len(self._content)

    def __contains__(self, key: str) -> bool:
        return key in self._content

    def get_sprite(self, key: str) -> pygame.Surface:
        return self._content[key]

    def store(self, key: str, content: pygame.Surface) -> None:
        is_new = key not in self._content
        self._content[key] = content
        return is_new

    def delete(self, key: str) -> bool:
        return self._content.pop(key, None) is not None
