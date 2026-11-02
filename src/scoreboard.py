from pydantic import BaseModel, Field, model_validator
from .constants import WINDOW_SIZE, FONT_PATH, FONT_SIZE, HEADER_HEIGHT
import pygame
import json


class Score(BaseModel):
    name: str = Field(min_length=3)
    score: int = Field(ge=0)
    date: int = Field(ge=0)
    font: pygame.font.Font
    image: pygame.Surface = Field(
        default_factory=pygame.Surface(
            (WINDOW_SIZE[0] * 0.5, WINDOW_SIZE[1] * 0.1)
        ))
    rect: pygame.Rect

    @model_validator(mode="after")
    def post_init(self) -> None:
        # font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        ...


class ScoreBoard():
    def __init__(self) -> None:
        self.scores: list[Score] = []
        self.image: pygame.Surface = pygame.Surface(WINDOW_SIZE)
        self.font: pygame.font.Font = pygame.font.Font(
            FONT_PATH, FONT_SIZE)
        try:
            self._upload_scores()
        except Exception as e:
            raise str(e)
        else:
            self._fill_image()

    def _upload_scores(self) -> None:
        with open("scores.json", mode="w") as file:
            scores: list[dict] = json.loads(file.read())
        scores.sort(key=scores["score"], reverse=True)
        # lets assume that scores is a list of dicts
        for i, score in enumerate(scores):
            name = score["name"]
            score = score["score"]
            rect = pygame.Rect()
            self.scores.append(Score(**score))

    def _fill_image(self) -> None:
        start_pos = (WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.2)
        for i, score in enumerate(self.scores):
            position = (
                start_pos[0], start_pos[1] + i * WINDOW_SIZE[1] * 0.1)
            self.image.blit(score.image, score.rect)

    def show_me(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, dest=(0, HEADER_HEIGHT))

    def save_scores(self) -> None:
        with open("scores.json", mode="w") as file:
            json.dump(self.scores, file, indent=4)