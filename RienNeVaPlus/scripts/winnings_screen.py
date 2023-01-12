import pygame
from game_info import Game_info
from settings import Settings


class Winnings_screen():
    def __init__(self, screen, settings: Settings, game_info: Game_info) -> None:
        self.screen = screen
        self.settings = settings
        self.gi = game_info
        self.active = True
        self.gi.winnings_screen = self # type: ignore
        
        size = self.settings.screen_size
        self.image = pygame.Surface(size)
        self.image.fill((0,0,0))
        self.image = pygame.Surface.convert_alpha(self.image)
        self.image.set_alpha(120)
        self.rect = self.image.get_rect()

    def update(self):
        if self.active:
            self.gi.current_stage = 1
            self.gi.winnings_screen = self # type: ignore
        else:
            self.gi.winnings_screen = None

    def blitme(self):
        self.screen.blit(self.image, self.rect)
