import game_functions as gf
import pygame
from chips import Chip
from elements import Button, Pop_up, Info_field
from play_table import Play_field
from roulette_wheel import Roulette_wheel


class Play_screen():
    """Creates the play screen"""

    def __init__(self, screen, settings, game_info) -> None:
        """Init"""

        self.screen, self.settings, self.game_info = screen, settings, game_info
        self.button_list, self.pop_up_list, self.text_list = [], [], []
        self.board = None
        self.budget, self.new_budget, self.do_update_budget_text = 0, 0, None
        self.info_field_list, self.info_field_list_expected = [], []
        self.outcome = None
        self.active = False

        self.chip_group = pygame.sprite.Group()
        self.chip_group_temp = pygame.sprite.Group()
        self.chip_group_placed = pygame.sprite.Group()
        self.chip_hovered = None
        self.chip_all_groups_list = [self.chip_group,
                                     self.chip_group_temp, self.chip_group_placed]

    def create_self(self):
        self.board = Play_field(self.screen, self.settings, self.game_info)
        self.roulette_wheel = Roulette_wheel(
            self.screen, self.settings, self.game_info)
        self.create_chips()
        self.create_budget_text(self.budget, self.settings.bg_rect.bottomright)

        self.active = True

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

    def update(self):
        """Function to update the board"""

        x, y = pygame.mouse.get_pos()

        self.game_info.chip_group_list = self.chip_all_groups_list
        self.game_info.elements_dict["chips"] = self.chip_all_groups_list

        """For loop to update chips"""
        for chip in self.chip_group:
            if pygame.Rect.collidepoint(chip.rect, x, y):
                self.chip_hovered = chip
                break
            else:
                self.chip_hovered = None

        """Create an information box showing the chips price"""
        if self.chip_hovered:
            if not self.info_field_list:
                price = self.chip_hovered.price
                msg = "€" + "{:,}".format(price)
                size = [5 + len(msg) * 5, self.chip_hovered.rect.h / 2]
                pos = self.chip_hovered.rect.midtop

                new_info_field = Info_field(
                    self.screen, self.settings, pos, size, msg=msg, id=1)
                self.info_field_list.append(new_info_field)
                self.game_info.info_fields_list.add(new_info_field)
        elif self.info_field_list:
            if self.info_field_list[-1].id == 1:
                self.info_field_list.clear()
                self.game_info.info_fields_list.clear()

        # This is the chip that follows the cursor
        for chip in self.chip_group_temp:
            chip.reposition(x, y)

            if isinstance(self.budget, int):
                if self.budget < 1000:
                    if chip.price > self.budget:
                        self.chip_group_temp.remove(chip)

            if not self.info_field_list:
                expected_return = chip.get_expected_return(self.game_info)
                if expected_return != chip.price:
                    msg = "€" + "{:,}".format(chip.price)
                    size = [10 + len(msg) * 5, chip.rect.h / 2]
                    new_info_field = Info_field(
                        self.screen, self.settings, (x, y), size, msg=msg, id=2, chip=chip)
                    self.info_field_list.append(new_info_field)
                    self.game_info.info_fields_list.add(new_info_field)
            else:
                if self.info_field_list:
                    expected_return = chip.get_expected_return(self.game_info)
                    msg = "€" + "{:,}".format(expected_return)
                    self.info_field_list[-1].prep_msg(msg)
                    if expected_return == chip.price:
                        self.info_field_list.clear()
                        self.game_info.info_fields_list.clear()

        if not self.chip_group_temp:
            if self.info_field_list:
                if self.info_field_list[-1].id == 2:
                    self.info_field_list.clear()
                    self.game_info.info_fields_list.clear()
                    
        for chip in self.chip_group_placed:
            if not hasattr(chip, "expected_return"):
                chip.get_expected_return(self.game_info)

        if self.info_field_list:
            for field in self.info_field_list:
                field.update_info_field()

        if self.board:
            self.board.update()
            
        if self.budget != self.game_info.personal_budget:
            self.budget = self.game_info.personal_budget
            self.update_budget_text(self.budget)

        gf.check_chip_overlap(self.chip_group_placed)
        
        if self.outcome or self.outcome == 0:
            returns = gf.check_winnings(self.outcome, self.chip_group_placed)
            self.game_info.personal_budget += returns
            self.outcome = None
            self.chip_group_placed.empty()

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
        self.board.blitme()

        for msg_image, msg_image_rect in self.text_list:
            self.screen.blit(msg_image, msg_image_rect)

        try:
            self.roulette_wheel.blitme()
        except Exception:
            pass
