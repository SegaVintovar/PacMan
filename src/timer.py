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
        self.working: bool = False

    def start_timer(self) -> None:
        if not self.working:
            self.working = True
            self.start_time = pygame.time.get_ticks()

    def time_since_start(self) -> int:
        return int((pygame.time.get_ticks() - self.start_time) / 1000)

    def pause(self) -> None:
        self.working = False
        self.paused_time = pygame.time.get_ticks()

    def resume(self) -> None:
        self.working = True
        now = pygame.time.get_ticks()
        self.start_time += now - self.paused_time

    def isBurned(self) -> bool:
        end = self.start_time + self.level_max_time * 1000
        return end < pygame.time.get_ticks()
