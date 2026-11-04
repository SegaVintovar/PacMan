import pygame
from .config import GameConfig
from .constants import WINDOW_SIZE, HEADER_HEIGHT, FONT_PATH, FONT_SIZE
from .game import Game
from .menu import Menu
import json
from .scoreboard import ScoreBoard
from .gradient import make_gradient
from typing import Any
from .game_state import GameState


# controls
# rules from the cofig: points per pacgum/supergum/ghost
class Instructions():
    rules = ["The game consists of multiple levels (at least 10).",
             "• Each level has a time limit (e.g., 90 seconds).\n",
             "• If the time limit is reached, you can decide what happens ",
             "(e.g., restart the level, end the game, etc.).\n",
             "• If the player completes a level, they move to the next level.",
             "• The player keeps their score and",
             "remaining lives between levels.\n",
             "• The game ends when all levels are completed or ",
             "when the player loses all lives.\n",
             "• During the game, the player can pause and resume the game.\n",
             "• When the game ends (win or lose),",
             "the final score is displayed, and the player can ",
             "enter their name to save the highscore.\n",
             "• After the game ends, the player is returned to the main menu."
             ]

    def __init__(self, config: GameConfig) -> None:
        self.background: pygame.Surface = make_gradient(
            (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2))
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE - 25)
        # self.text = self.font.render(self.rules, True, "white")
        # self.image_with_txt = pygame.Surface(
        #     self.font.size(self.rules), masks=pygame.SRCALPHA)
        # self.image_with_txt.blit(self.text, dest=(0, 0))
        # self.background.blit(
        #     self.image_with_txt,
        #     dest=(WINDOW_SIZE[0] * 0.3, WINDOW_SIZE[1] * 0.2)
        #     )
        self.config = config
        self._prep_rules()

    def _prep_rules(self) -> None:
        start_pos = (WINDOW_SIZE[0] * 0.2, WINDOW_SIZE[1] * 0.2)
        step = (FONT_SIZE - 15) * 2 
        for i, rule in enumerate(self.rules):
            position = (start_pos[0], start_pos[1] + i * step)
            self.background.blit(
                self.font.render(rule, True, "white"),
                dest=(position)
            )

    def process(self,
                events: list[pygame.event.Event], screen: pygame.Surface
                ) -> tuple[int, Any]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return (2, None)
            if event.type == pygame.QUIT:
                return (0, None)
        self._show_me(screen=screen)
        return (4, None)

    def _show_me(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, dest=(0, 0))


class App():
    """
    Handles final output, by knowing current state
    delegates input.
    Two members Game and Menu.
    also own main screen(WINDOW)

    """
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        pygame.init()
        screen = pygame.display.set_mode(
            (WINDOW_SIZE[0], WINDOW_SIZE[1] + HEADER_HEIGHT * 2))
        self.screen: pygame.Surface = screen  # 1. window first
        clock = pygame.time.Clock()
        self.clock: pygame.time.Clock = clock
        self.game: Game = Game(config=self.config)
        self.menu: Menu = Menu(self.game)
        self.scoreboard: ScoreBoard = ScoreBoard()
        self.intructions: Instructions = Instructions(config=config)
        self.state: Game | Menu | ScoreBoard | Instructions = self.menu
        self.game_state: GameState

    # if  state returns some value we are checking it and making some decisions
    # if 1 then  self.state = self.game
    # if 2 then self.state = self.menu
    # if 3 then game over - save the result
    # if 4 then instructions
    # if 0 then exit()
    def process(self, evns: list[pygame.event.Event]) -> bool:
        state, extra = self.state.process(evns, self.screen)
        match state:
            case 1:
                ...
            case 2:
                ...
            case 3:
                ...
        if state == 1:
            self.state = self.game
            # print("Game")
            return True
        if state == 2:
            if extra:
                self.scoreboard.add_score(extra)
                self.scoreboard.save_scores()
            self.state = self.menu
            return True
        if state == 3:
            self.state = self.scoreboard
            return True
        if state == 4:
            self.state = self.intructions
            return True
        if state == 0:
            self.scoreboard.save_scores()
            return False

    # def _open_scoreboard_file(self) -> dict:
    #     """
    #     Open, read and save it to the self.scoreboard
    #     """
    #     with open(self.scoreboard_file, "r") as file:
    #         self.scores = json.load(file.read())
    #     with open(self.scoreboard_file, "w") as file:
    #         self.scoreboard = json.load(file.read())

    def _save_results(self) -> None:
        with open(self.scoreboard_file, "w+") as file:
            file.write(json.dumps(str(self.scores)))
            print("File scores.json was updated")
