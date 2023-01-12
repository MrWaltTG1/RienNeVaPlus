import game_functions as gf
import pygame
from chips import Chip
from elements import Button, Info_field, Pop_up
from game_info import Game_info
from play_table import Play_field
from roulette_wheel import Roulette_wheel
from settings import Settings
from winnings_screen import Winnings_screen


class Play_screen():
    """Creates the play screen"""

    def __init__(self, screen, settings: Settings, game_info: Game_info) -> None:
        """Init"""

        self.screen, self.settings, self.gi = screen, settings, game_info
        self.button_list, self.pop_up_list, self.text_list = [], [], []
        self.board = None
        self.budget, self.new_budget, self.do_update_budget_text = 0, 0, None
        self.info_field_list, self.info_field_list_expected = [], []
        self.active = False
        self.roulette_wheel = None

        self.chip_group = pygame.sprite.Group()
        self.cursor_chip = None
        self.chip_group_placed = pygame.sprite.Group()
        self.chip_all_groups_list = [self.chip_group,
                                     self.cursor_chip, self.chip_group_placed]

    def create_self(self):
        self.board = Play_field(self.screen, self.settings, self.gi)
        self.roulette_wheel = Roulette_wheel(
            self.screen, self.settings, self.gi)
        self.create_chips()
        self.create_budget_text(self.budget, self.settings.bg_rect.bottomright)
        self.create_placement_buttons()

        self.active = True

    def create_placement_buttons(self):
        text_list = ["undo", "cross", "redo"]
        pos = [700, 200]
        size = [35, 35]
        for text in text_list:
            pos[0] += int(size[0]*1.3)
            new_button = Button(self.settings, pos, size, image=text)
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
                new_chip = Chip(color=color, settings=self.settings)
                new_chip.rect.center = (x, y)
                self.chip_group.add(new_chip)
            self.gi.all_chips_group_list = self.chip_all_groups_list

    def update(self):
        """Function to update the board"""
        if self.active:
            self.update_chips()

            if self.info_field_list:
                for field in self.info_field_list:
                    field.update_info_field()

            # Do button updates here
            for button in self.button_list:
                self.gi.button_list.add(button)
                if button.clicked == True:
                    chip_list, remove = gf.utility_buttons_action(
                        self.gi, button.msg)
                    if remove:
                        for chip in chip_list:
                            self.chip_group_placed.remove(chip)
                    elif remove == False:
                        for chip in chip_list:
                            self.chip_group_placed.add(chip)
                    button.clicked = False

            if self.board:
                self.board.update()
                
            if self.roulette_wheel:
                self.roulette_wheel.update()

            if self.budget != self.gi.personal_budget:
                self.budget = self.gi.personal_budget
                self.update_budget_text(self.budget)

            # When the wheel has spun do:
            if not self.gi.outcome == -1:
                returns = gf.check_winnings(self.gi)
                self.gi.personal_budget += returns
                self.gi.outcome = -1
                self.gi.placed_chips_list.clear()
                Winnings_screen(self.screen, self.settings, self.gi)

    def update_chips(self):
        """Function that handles updating the chips."""
        gf.check_chip_overlap(self.chip_group_placed)

        x, y = pygame.mouse.get_pos()

        """For loop to update chips"""
        for chip in self.chip_group:
            if pygame.Rect.collidepoint(chip.rect, x, y):
                self.hovered_chip = chip
                break
            else:
                self.hovered_chip = None

        """Create an information box showing the hovered chips price"""
        if self.hovered_chip:
            if not self.info_field_list:
                new_info_field = gf.create_info_field(
                    self.settings, self.gi, chip=self.hovered_chip, id=1)
                self.info_field_list.append(new_info_field)

        elif self.info_field_list:
            if self.info_field_list[-1].id == 1:
                self.info_field_list.clear()
                self.gi.info_fields_list.clear()

        # This is the chip that follows the cursor
        if self.gi.cursor_chip:
            self.gi.cursor_chip.reposition(x, y)

            """Create an information box showing the selected chips expected return price"""
            if not self.info_field_list:
                expected_return = self.gi.cursor_chip.get_expected_return(
                    self.gi)
                if expected_return != self.gi.cursor_chip.price:
                    new_info_field = gf.create_info_field(
                        self.settings, self.gi, chip=self.gi.cursor_chip, id=2)
                    self.info_field_list.append(new_info_field)

            else:
                if self.info_field_list:
                    expected_return = self.gi.cursor_chip.get_expected_return(
                        self.gi)
                    msg = "€" + "{:,}".format(expected_return)
                    self.info_field_list[-1].prep_msg(msg)
                    if expected_return == self.gi.cursor_chip.price:
                        self.info_field_list.clear()
                        self.gi.info_fields_list.clear()

        if not self.cursor_chip:
            if self.info_field_list:
                if self.info_field_list[-1].id == 2:
                    self.info_field_list.clear()
                    self.gi.info_fields_list.clear()

        for chip in self.chip_group_placed:
            if not hasattr(chip, "expected_return"):
                chip.get_expected_return(self.gi)

    def update_budget_text(self, budget: int, index=0, font_color=None):
        pos = self.text_list[index][1].bottomright
        if self.text_list:
            self.text_list.pop(index)
        msg = "€" + "{:,.2f}".format(budget)
        if font_color:
            msg_image, msg_image_rect = gf.create_text(
                pos, msg, 40, font_color=font_color)
        else:
            msg_image, msg_image_rect = gf.create_text(pos, msg, 40)
        msg_image_rect.bottomright = pos
        self.text_list.insert(index, (msg_image, msg_image_rect))

    def create_budget_text(self, budget: int, pos, index=0):
        """pos is the position of the text adjusted to the bottom right of the text"""
        msg = "€" + "{:,.2f}".format(budget)
        msg_image, msg_image_rect = gf.create_text(pos, msg, 40)
        msg_image_rect.bottomright = pos
        self.text_list.insert(index, (msg_image, msg_image_rect))

    def blitme(self):
        """Function to blit to the screen."""
        if self.board:
            self.board.blitme()

        for msg_image, msg_image_rect in self.text_list:
            self.screen.blit(msg_image, msg_image_rect)

        try:
            self.roulette_wheel.blitme()
        except Exception:
            pass
