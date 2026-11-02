from pydantic import BaseModel, Field, model_validator, ConfigDict
from .constants import WINDOW_SIZE, FONT_PATH, FONT_SIZE, HEADER_HEIGHT, PINK
import pygame
import json
from typing import Any


class Score(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(min_length=3)
    score: int = Field(ge=0)
    font: pygame.font.Font
    image: pygame.Surface = Field(
        default_factory=pygame.Surface(
            (WINDOW_SIZE[0] * 0.5, WINDOW_SIZE[1] * 0.1),
            pygame.SRCALPHA
        ))

    @model_validator(mode="after")
    def post_init(self) -> None:
        text = self.font.render(self.name, True, PINK)
        self.image.blit(
            text,
            dest=(WINDOW_SIZE[0] * 0.1, WINDOW_SIZE[1] * 0.05)
            )


class ScoreBoard():
    def __init__(self) -> None:
        self.scores: list[Score] = []
        self.image: pygame.Surface = pygame.Surface(
            (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2),
            pygame.SRCALPHA)
        self.font: pygame.font.Font = pygame.font.Font(
            FONT_PATH, FONT_SIZE)
        try:
            self._upload_scores()
        except Exception as e:
            print(str(e))
        else:
            self._fill_image()

    def _upload_scores(self) -> None:
        with open("scores.json", mode="w") as file:
            scores: list[dict] = json.loads(file.read())
        scores.sort(key=scores["score"], reverse=True)
        # lets assume that scores is a list of dicts
        for score in scores:
            n = score["name"]
            scr = score["score"]
            self.scores.append(Score(
                    name=n,
                    score=scr,
                    font=self.font
                    ))

    def process(self,
                events: list[pygame.event.Event],
                screen: pygame.Surface
                ) -> tuple[int, Any]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event == pygame.K_ESCAPE or event == pygame.K_q:
                    return (2, None)
        screen.blit(self.image, dest=(0, 0))
        return (2, None)

    def _fill_image(self) -> None:
        if self.scores:
            start_pos = (WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.2)
            for i, score in enumerate(self.scores):
                position = (
                    start_pos[0], start_pos[1] + i * WINDOW_SIZE[1] * 0.1)
                self.image.blit(score.image, position)

    def show_me(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, dest=(0, HEADER_HEIGHT))

    def add_score(self, score: Score) -> None:
        self.scores.append(score)
        self.scores.sort(key=lambda s: s.score, reverse=True)
        self.scores = self.scores[:10]
        self._fill_image()

    
    # def add_score(self, name: str, time: int, score: int) -> None:
    #     self.scores.append(Score(
    #         name=name, score=score, date=time, font=self.font
    #         ))
    #     self.scores.sort(key=lambda s: s.score, reverse=True)
    #     self.scores = self.scores[:10]
    #     self._fill_image()

    def save_scores(self) -> None:
        with open("scores.json", mode="w") as file:
            json.dump(self.scores, file, indent=4)
