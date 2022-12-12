import pygame
from play_table import Play_field
from elements import Button, Pop_up


class Play_screen():
    def __init__(self, screen, settings) -> None:
        self.screen, self.settings = screen, settings
        self.button_list, self.pop_up_list = [], []
        new_button = Button(settings, "START", (500, 400), (500, 400))
        self.button_list.append(new_button)
        self.board = None

    def update(self):
        x, y = pygame.mouse.get_pos()
        for button in self.button_list:
            if button.rect.collidepoint(x, y):
                self.board = Play_field(self.screen, self.settings)
                new_popup = Pop_up(
                    self.settings, "", (500, 400), (200, 100))
                new_popup.prep_msg("Enter your budget", (0, 0, 0))
                self.pop_up_list.append(new_popup)
                self.button_list.remove(button)
        if self.board:
            self.board.update()

    def blitme(self):
        for button in self.button_list:
            button.blitme(self.screen)
        for popup in self.pop_up_list:
            popup.blitme(self.screen)
