from .module import Module
import pygame
from .game_state import GameState
from .button import Button
from .constants import FONT_PATH, FONT_SIZE, WINDOW_SIZE, HEADER_HEIGHT, PINK
import json
from .config import GameConfig


def process_txt_input():
    ...


# enter your name to add the score with a name to the scoreslist
# how to pass score from here to the 
class WinLoose(Module):
    def __init__(self, bg: pygame.Surface, config: GameConfig) -> None:
        self.background = bg
        self.config = config
        self.image: pygame.Surface = self.background.copy()
        self.name: str = ""
        self.font: pygame.font.Font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.hfont: pygame.font.Font = pygame.font.Font(
            FONT_PATH, FONT_SIZE * 2)
        # self.background.blit(
        #     self.font.render(
        #         f"Enter your name: {self.player_name}", True, PINK),
        #     dest=(WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.4)
        # )
        self.score: int = 0
        self.buttons: Button = []
        # self.image: pygame.Surface = pygame.Surface(
        #     (WINDOW_SIZE[0],
        #      WINDOW_SIZE[1] + HEADER_HEIGHT * 2)
        # )

    # here we need to handle keyboard input
    # start with "" or player name
    # then track all the stuff that came it
    def process(self,
                events: list[pygame.event.Event],
                gs: GameState,
                screen: pygame.Surface) -> GameState:
        score = gs.extra
        win = gs.win
        if win:
            header = "Congratulations, you won!"
        else:
            if gs.previous == 1:
                header = "You lost."
            else:
                header = "Save your current result here"
        for event in events:
            if event.type == pygame.KEYDOWN:
                # chars, enter, backspace, delete
                if event.key == pygame.K_ESCAPE:
                    gs.gs_update(2)
                    return gs
                ch: str = event.unicode
                if (ch.isalnum() or ch == " ") and len(self.name) < 10:
                    self.name += ch
                if event.key == pygame.K_RETURN:
                    self._save_score(gs.extra, self.name)
                    gs.gs_update(2)
                    return gs
                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
            if event.type == pygame.QUIT:
                gs.quit()
                return gs
        # name = name if not char else char
        self._update_image(header, score)
        screen.blit(self.image, dest=(0, 0))
        return gs

    def _update_image(self, header: str, score: int):
        img_cpy = self.background.copy()
        self.image = img_cpy
        # header
        h = (self.hfont.render(header, True, PINK),
             (WINDOW_SIZE[0] * 0.45, HEADER_HEIGHT))
        # message
        msg = (self.font.render("Now you can save your score", True, PINK),
               (WINDOW_SIZE[0] * 0.35, HEADER_HEIGHT * 3))
        # "Your name: "
        ur_name = (self.font.render("Name: ", True, PINK),
                   (WINDOW_SIZE[0] * 0.1, WINDOW_SIZE[1] // 2))
        # entered text
        ch = (self.hfont.render(self.name, True, PINK),
              (WINDOW_SIZE[0] * 0.4, WINDOW_SIZE[1] // 2))
        # score
        s = (self.font.render(("Your score: " + str(score)), True, "white"),
             (WINDOW_SIZE[0] * 0.4, WINDOW_SIZE[1] * 0.75))
        self.image.blit(h[0], dest=h[1])
        self.image.blit(msg[0], msg[1])
        self.image.blit(ur_name[0], ur_name[1])
        self.image.blit(ch[0], ch[1])
        self.image.blit(s[0], s[1])

    def _upload_scores(self) -> list[dict]:
        try:
            with open(self.config.highscore_filename, mode="r") as file:
                scores: list[dict] = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []
        scores.sort(key=lambda s: s["score"], reverse=True)
        print("Scores: ", scores)
        return scores
        # lets assume that scores is a list of dicts
        # for score in scores:
        #     n = score["name"]
        #     scr = score["score"]
        #     self.scores.append(Score(
        #             name=n,
        #             score=scr,
        #             font=self.font
        #             ))

    def _save_score(self, score: int, name: str) -> None:
        scores = self._upload_scores()
        scores = [] if not scores else scores
        name = "Player" if not name else name
        scores.append({"score": score, "name": name})
        scores.sort(key=lambda s: s["score"], reverse=True)
        with open(self.config.highscore_filename, "w") as file:
            json.dump(scores, file, indent=4)
        
