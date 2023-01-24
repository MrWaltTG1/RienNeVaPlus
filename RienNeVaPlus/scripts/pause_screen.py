import pygame
from settings import Settings
import game_functions as gf


class Pause_screen():
    def __init__(self, screen, settings: Settings, game_info, game_over=False) -> None:
        self.screen = screen
        self.settings = settings
        self.game_over = game_over
        self.gi = game_info
        self.active = True
        self.text_list = []

        self.image, self.rect = gf.get_darkened_screen_list(settings)

        if not game_over:
            self.gi.winnings_screen = self  # type: ignore
            returns = gf.check_winnings(self.gi)
            self.gi.returns = returns
            if returns > 1:
                self.gi.personal_budget += returns

            self.text_creator(str(self.gi.outcome))
            self.text_creator("$" + str(self.gi.returns))
        else:
            self.text_creator(str(self.gi.outcome))
            self.text_creator("You've ran out of money!")
            self.text_creator(
                "Click the left mouse button to reset to main menu")

    def text_creator(self, msg: str):
        pos = (500, 100 * (1 + len(self.text_list)))
        font_size = self.settings.font_size
        surf, rect = gf.create_text(pos, msg, font_size)
        self.text_list.append((surf, rect))

    def update(self):
        if self.active:
            self.gi.current_stage = 1
        elif not self.game_over:
            self.gi.outcome = -1
            self.gi.placed_chips_list.clear()
            self.gi.winnings_screen = None

    def blitme(self, screen):
        screen.blit(self.image, self.rect)

        for text in self.text_list:
            screen.blit(text[0], text[1])
