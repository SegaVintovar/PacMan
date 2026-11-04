from pydantic import BaseModel, Field, model_validator, ConfigDict
from .constants import WINDOW_SIZE, FONT_PATH, FONT_SIZE, HEADER_HEIGHT
from .constants import PINK, CYAN, MAX_SCORES
import pygame
import json
from typing import Any
from .gradient import make_gradient


class Score(BaseModel):
    # model config is to make pydantic work with pygame object types
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(min_length=3)
    score: int = Field(ge=0)
    font: pygame.font.Font
    image: pygame.Surface | None = None

    @model_validator(mode="after")
    def post_init(self) -> None:
        text = self.font.render(
            f"{self.name}: {self.score}", True, PINK)
        self.image = pygame.Surface(
            (WINDOW_SIZE[0] * 0.5, WINDOW_SIZE[1] * 0.1),
            pygame.SRCALPHA
        )
        self.image.blit(
            text,
            dest=(WINDOW_SIZE[0] * 0.1, WINDOW_SIZE[1] * 0.05)
            )
        print("post validation of the score is done")
        return self


class ScoreBoard():
    def __init__(self) -> None:
        self.scores: list[Score] = []
        self.image = make_gradient(
            (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2))
        self.font: pygame.font.Font = pygame.font.Font(
            FONT_PATH, FONT_SIZE)
        try:
            self._upload_scores()
        except Exception as e:
            print(str(e))
        self._fill_image()

    def _upload_scores(self) -> None:
        with open("scores.json", mode="r") as file:
            scores: list[dict] = json.loads(file.read())
        scores.sort(key=lambda s: s["score"], reverse=True)
        # lets assume that scores is a list of dicts
        for score in scores:
            n = score["name"]
            scr = score["score"]
            self.scores.append(Score(
                    name=n,
                    score=scr,
                    font=self.font
                    ))
        # print(len(self.scores))

    def process(self,
                events: list[pygame.event.Event],
                screen: pygame.Surface
                ) -> tuple[int, Any]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or\
                  event.key == pygame.K_q:
                    return (2, None)
            if event.type == pygame.QUIT:
                return (0, None)
        self.show_me(screen=screen)
        return (3, None)

    def _fill_image(self) -> None:
        if self.scores:
            start_pos = (WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.2)
            for i, score in enumerate(self.scores):
                position = (
                    start_pos[0], start_pos[1] + i * WINDOW_SIZE[1] * 0.1)
                self.image.blit(score.image, position)
        else:
            self.image.blit(
                self.font.render("No scores yet", True, PINK, CYAN),
                dest=(WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.4)
            )

    def show_me(self, screen: pygame.Surface) -> None:
        """
        Blits the image of the Scoreboard on the given Surface
        """
        screen.blit(self.image, dest=(0, 0))

    def _create_score(self, name: str, score: int) -> Score:
        """"
        Creation of the Score object
        name and score are required
        """
        return Score(name=name, score=score)

    def add_score(self, score: Score) -> None:
        self.scores.append(score)
        self.scores.sort(key=lambda s: s.score, reverse=True)
        self.scores = self.scores[:MAX_SCORES]
        self._fill_image()

    # def add_score(self, name: str, time: int, score: int) -> None:
    #     self.scores.append(Score(
    #         name=name, score=score, date=time, font=self.font
    #         ))
    #     self.scores.sort(key=lambda s: s.score, reverse=True)
    #     self.scores = self.scores[:10]
    #     self._fill_image()

    # this one is not working as it should
    def save_scores(self) -> None:
        data = []
        for score in self.scores:
            data.append({"name": score.name, "score": score.score})
        with open("scores.json", mode="w") as file:
            json.dump(data, file, indent=4)
