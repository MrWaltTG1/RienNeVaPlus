import game_functions as gf
import pygame
from chips import Chip
from elements import Button, Pop_up
from play_table import Play_field


class Play_screen():
    """Creates the play screen"""

    def __init__(self, screen, settings) -> None:
        """Init"""

        self.screen, self.settings = screen, settings
        self.button_list, self.pop_up_list, self.text_list = [], [], []
        self.board, self.budget, self.do_update_budget = None, None, None
        self.info_field = []

        self.chip_group = pygame.sprite.Group()
        self.chip_group_temp = pygame.sprite.Group()
        self.chip_group_placed = pygame.sprite.Group()

        self.create_start_screen()

    def create_start_screen(self) -> None:
        """Function to create the start screen"""

        button_pos = self.settings.start_button_pos
        button_size = self.settings.start_button_size

        new_button = Button(self.settings, "START", button_pos, button_size)
        self.button_list.append(new_button)

    def create_chips(self):
        """Function to create chips"""

        if self.board:
            x_start = self.board.play_table_rect.right - 100
            x_step = -45
            x_stop = x_start - abs(x_step) * 6
            x_range = range(x_start, x_stop, x_step)

            y = self.board.play_table_rect.bottom + 30

            color_list = list(self.settings.chip_color_dict.values())

            for color, x in zip(color_list, x_range):
                new_chip = Chip(color=color)
                new_chip.rect.center = (x, y)
                self.chip_group.add(new_chip)

    def update(self):
        """Function to update the board"""

        x, y = pygame.mouse.get_pos()
        for button in self.button_list:
            if button.rect.collidepoint(x, y):
                self.create_pop_up()
                self.button_list.remove(button)

        """For loop to update chips"""
        for chip in self.chip_group:
            if pygame.Rect.collidepoint(chip.rect, x, y):
                chip.image = pygame.transform.scale(
                    chip.original_image, (chip.size[0]*1.5, chip.size[1]*1.5))
                chip.image.fill(chip.color, special_flags=pygame.BLEND_MAX)
                if not self.info_field:
                    fields_list = gf.create_info_field(chip.rect.topleft, (100,40), "TEST BOX")
                    self.info_field.append(fields_list)
                else:
                    gf.update_info_field(self.info_field)
            else:
                chip.image = pygame.transform.scale(
                    chip.original_image, chip.size)
                chip.image.fill(chip.color, special_flags=pygame.BLEND_MAX)
                if self.info_field:
                    self.info_field.pop()

        for chip in self.chip_group_temp:
            chip.rect.center = (x, y)

        if self.board:
            self.board.update()

        if self.pop_up_list[0:]:
            self.update_budget_pop_up(self.pop_up_list[0])

        if self.do_update_budget:
            self.update_budget()

    def update_budget(self):
        pos = self.settings.bg_rect.bottomright
        msg = "€" + "{:,.2f}".format(self.budget)
        msg_image, msg_image_rect = gf.create_text(pos, msg, 40)
        msg_image_rect.bottomright = pos
        self.text_list.append((msg_image, msg_image_rect))
        self.do_update_budget = False

    def update_budget_pop_up(self, pop_up: Pop_up):
        """Function to update the budget pop up."""
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
                self.do_update_budget = True
                self.pop_up_list.pop(0)
                self.board = Play_field(self.screen, self.settings)
                self.create_chips()

        text = "€" + "{:,.2f}".format(self.number)
        pop_up.msg_image_list.pop(1)
        pop_up.prep_msg(text, font_color=(0, 0, 0))

    def create_pop_up(self):
        """Function to create the pop up."""

        new_popup = Pop_up(self.settings, (500, 400), (300, 200))
        new_popup.prep_msg("Enter your budget:",
                           (0, 0, 0), 40, pos=(10, 10))
        self.number = 0
        new_popup.prep_msg("")
        self.pop_up_list.append(new_popup)

    def blitme(self):
        """Function to blit the screen."""

        for button in self.button_list:
            button.blitme(self.screen)
        for popup in self.pop_up_list:
            popup.blitme(self.screen)
        for msg_image, msg_image_rect in self.text_list:
            self.screen.blit(msg_image, msg_image_rect)

        self.chip_group.draw(self.screen)
        self.chip_group_temp.draw(self.screen)
        self.chip_group_placed.draw(self.screen)

        if self.info_field:
            pygame.draw.rect(self.screen, (255, 255, 255),self.info_field[0])
            pygame.draw.rect(self.screen, (255, 255, 255),self.info_field[0])
            self.screen.blit(self.info_field[2][0], self.info_field[2][1])
                