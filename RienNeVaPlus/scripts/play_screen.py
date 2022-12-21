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
        self.board = None
        self.budget, self.new_budget, self.do_update_budget_text = None, None, None
        self.chip_hovered = None
        self.info_field_list = []

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

        """For loop to update chips"""
        for chip in self.chip_group:
            if pygame.Rect.collidepoint(chip.rect, x, y):
                if not self.chip_hovered:
                    self.chip_hovered = Chip(
                        color=chip.color, resize_multiplier=1.5)
                    self.chip_hovered.rect.center = chip.rect.center
                break
            else:
                self.chip_hovered = None

        if self.chip_hovered:
            if not self.info_field_list:
                key = [k for k, v in self.settings.chip_color_dict.items()
                       if v == self.chip_hovered.color]
                price = self.settings.chip_price_dict[key[0]]
                msg = "€" + "{:,}".format(price)
                fields_list = gf.create_info_field(
                    self.chip_hovered.rect.topleft,  60, msg)
                self.info_field_list.append(fields_list)
            else:
                for fields in self.info_field_list:
                    fields = gf.update_info_field(fields)
        elif self.info_field_list:
            self.info_field_list.pop()

        for chip in self.chip_group_temp:
            chip.reposition(x, y)

        if self.board:
            self.board.update()

        if self.pop_up_list[0:]:
            self.update_budget_pop_up(self.pop_up_list[0])

        if self.new_budget != self.budget:
            self.budget = self.new_budget
            self.do_update_budget_text = True

        if self.do_update_budget_text and self.budget:
            self.update_budget_text(self.budget)
            self.do_update_budget_text = False
        
        gf.check_chip_overlap(self.chip_group_placed)


    def update_budget_text(self, budget: int):
        pos = self.settings.bg_rect.bottomright
        msg = "€" + "{:,.2f}".format(budget)
        msg_image, msg_image_rect = gf.create_text(pos, msg, 40)
        msg_image_rect.bottomright = pos
        self.text_list.append((msg_image, msg_image_rect))

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
                self.new_budget = self.number
                self.do_update_budget_text = True
                self.pop_up_list.pop(0)
                self.board = Play_field(self.screen, self.settings)
                self.create_chips()

        text = "€" + "{:,.2f}".format(self.number)
        pop_up.msg_image_list.pop(1)
        pop_up.prep_msg(text, font_color=(0, 0, 0))

    def create_budget_pop_up(self):
        """Function to create the pop up."""

        new_popup = Pop_up(self.settings, (500, 400), (300, 200))
        new_popup.prep_msg("Enter your budget:",
                           (0, 0, 0), 40, pos=(10, 10))
        self.number = 0
        new_popup.prep_msg("")
        self.pop_up_list.append(new_popup)

    def blitme(self):
        """Function to blit to the screen."""

        for button in self.button_list:
            button.blitme(self.screen)
        for popup in self.pop_up_list:
            popup.blitme(self.screen)
        for msg_image, msg_image_rect in self.text_list:
            self.screen.blit(msg_image, msg_image_rect)

        # Draw the chips underneath the table
        self.chip_group.draw(self.screen)

        # Draw the info fields
        if self.info_field_list:
            for field in self.info_field_list:
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 field[0], border_radius=2)
                self.screen.blit(field[2][0], field[2][1])
        # Draw the bigger chip over the hovered chip
        if self.chip_hovered:
            self.screen.blit(self.chip_hovered.image, self.chip_hovered.rect)

        # Draw the rest of the active chips
        self.chip_group_placed.draw(self.screen)
        self.chip_group_temp.draw(self.screen)
