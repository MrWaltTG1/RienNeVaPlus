import pygame
import random
from play_table import Play_field
from elements import Button, Pop_up
import game_functions as gf
from chips import Chip


class Play_screen():
    def __init__(self, screen, settings) -> None:
        self.screen, self.settings = screen, settings
        self.button_list, self.pop_up_list, self.text_list = [], [], []
        new_button = Button(settings, "START", (500, 400), (500, 400))
        self.button_list.append(new_button)
        self.board, self.budget, self.update_budget = None, None, None

        self.chip_group = pygame.sprite.Group()

    def create_chips(self):
        x_start = self.board.play_table_rect.left + 100
        x_stop = x_start + 40 * 10
        i = 0
        color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for x in range(x_start, x_stop, 40):
            y = self.board.play_table_rect.bottom
            if i >= len(color_list):
                i = 0
            color = color_list[i]
            new_chip = Chip(color=color)
            new_chip.rect.topleft = (x, y)
            self.chip_group.add(new_chip)
            i += 1

    def update(self):
        x, y = pygame.mouse.get_pos()
        for button in self.button_list:
            if button.rect.collidepoint(x, y):
                self.create_pop_up()
                self.button_list.remove(button)
        for chip in self.chip_group:
            if pygame.Rect.collidepoint(chip.rect, x,y):
                chip.image = pygame.transform.scale(chip.original_image, (80,80))
                chip.image.fill(chip.color, special_flags=pygame.BLEND_MAX)
            else:
                chip.image = pygame.transform.scale(chip.original_image, (40,40))
                chip.image.fill(chip.color, special_flags=pygame.BLEND_MAX)

        if self.board:
            self.board.update()

        if self.pop_up_list[0:]:
            self.update_pop_up(self.pop_up_list[0])

        if self.update_budget:
            pos = self.settings.bg_rect.bottomright
            msg = "€" + "{:,.2f}".format(self.budget)
            msg_image, msg_image_rect = gf.create_text(pos, msg, 40)
            msg_image_rect.bottomright = pos
            self.text_list.append((msg_image, msg_image_rect))
            self.update_budget = False

    def update_pop_up(self, pop_up: Pop_up):
        for event in pygame.event.get(pygame.KEYDOWN):

            if event.unicode.isdigit():
                self.number = int(str(self.number) + str(event.unicode))

            elif event.key == pygame.K_BACKSPACE:
                if len(str(self.number)) > 1:
                    self.number = int(str(self.number)[:-1])
                else:
                    self.number = 0

            elif event.key == pygame.K_RETURN:
                self.budget = self.number
                self.update_budget = True
                self.pop_up_list.pop(0)
                self.board = Play_field(self.screen, self.settings)
                self.create_chips()

        text = "€" + "{:,.2f}".format(self.number)
        pop_up.msg_image_list.pop(1)
        pop_up.prep_msg(text, font_color=(0, 0, 0))

    def create_pop_up(self):
        new_popup = Pop_up(self.settings, (500, 400), (300, 200))
        new_popup.prep_msg("Enter your budget:",
                           (0, 0, 0), 40, pos=(10, 10))
        self.number = 0
        new_popup.prep_msg("")
        self.pop_up_list.append(new_popup)

    def blitme(self):
        for button in self.button_list:
            button.blitme(self.screen)
        for popup in self.pop_up_list:
            popup.blitme(self.screen)
        for msg_image, msg_image_rect in self.text_list:
            self.screen.blit(msg_image, msg_image_rect)

        self.chip_group.draw(self.screen)
