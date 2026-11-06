import pygame


class Timer():
    """
    Every level will have its own timer
    
    """
    def __init__(self, level_max_time: int) -> None:
        self.level_max_time = level_max_time
        self.start_time: int = 0
        # when we started a pause
        self.paused_time: int = 0

    def start_timer(self) -> None:
        self.start_time = pygame.time.get_ticks()

    def time_since_start(self) -> int:
        return int((pygame.time.get_ticks() - self.start_time) / 1000)

    def pause(self) -> None:
        self.paused_time = pygame.time.get_ticks()

    def resume(self) -> None:
        now = pygame.time.get_ticks()
        self.start_time += now - self.paused_time
