class GameState():
    def __init__(self,
                 next_module: int,
                 running: bool,
                 extra: int = 0,
                 win: bool = False) -> None:
        # for now extra is a string, but it maybe changed
        self.next_module = next_module
        self.previous: int = 0
        self.running = running
        # now extra are points, but there should be a mark if it was win or loss
        self.extra = extra
        self.win = win
        self.reload = False
        self.player_name: str = ""

    def gs_update(self,
                  next_module: int,
                  extra: int = 0,
                  win: bool = False,
                  player_name: str = "") -> None:
        if next_module == 0:
            self.running = False
        if next_module == 2 and player_name:
            # save result into the file
            ...
        self.previous = self.next_module
        self.next_module = next_module
        if extra:
            self.extra = extra
            if win:
                self.win = True

    def quit(self) -> None:
        self.running = False
        self.next_module = 0

    def go_to_game(self) -> None:
        self.previous = self.next_module
        self.next_module = 1
        if not self.running:
            self.running = True
    # def __repr__(self) -> tuple[int, bool, str]:
    #     return (self.next_module, self.running, self.extra)
