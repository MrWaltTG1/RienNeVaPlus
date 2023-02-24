import game_functions as gf
import pygame
import time
from chips import Chip
from elements import Button, Info_field, Pop_up, Budget_bar
from play_table import Play_field
from roulette_wheel import Roulette
from settings import Settings
from number_tabel import Tabel
from pause_screen import Pause_screen


class Play_screen():
    """Creates the play screen"""

    def __init__(self, screen, settings: Settings, game_info) -> None:
        """Init"""

        self.screen, self.settings, self.gi = screen, settings, game_info
        self.button_list, self.pop_up_list, self.image_list = [], [], []
        self.board = None
        self.budget, self.new_budget, self.do_update_budget_text = 0, 0, None
        self.info_field_list, self.info_field_list_expected = [], []
        self.active = False
        self.roulette_wheel = None

        self.chip_group = []
        self.cursor_chip = None
        self.hovered_chip = None
        self.chip_group_placed = pygame.sprite.Group()
        self.chip_all_groups_list = [self.chip_group,
                                     self.cursor_chip, self.chip_group_placed]

    def create_self(self):

        self.board = Play_field(self.screen, self.settings, self.gi)
        self.roulette_wheel = Roulette(self.settings, self.gi, self)
        self.create_chips(True)
        self.create_budget_text(self.budget, self.settings.bg_rect.bottomright)
        self.create_placement_buttons()
        self.create_back_button()
        Budget_bar(self.settings, self.gi)
        Tabel(self.settings, self.gi)
        self.br_surf = self.settings.br_surf
        self.br_rect = self.br_surf.get_rect(
            topright=self.settings.screen_size)
        self.budget = self.gi.personal_budget
        self.active = True

    def create_placement_buttons(self):
        text_list = ["undo", "cross", "redo"]
        size = [70, 70]
        y = self.settings.bg_rect.bottom + 30
        x = range(1000, 1200, int(size[0]*1.1))
        for i, text in enumerate(text_list):
            new_button = Button(self.settings, self.gi,
                                (x[i], y), size, image=text)
            self.button_list.append(new_button)

    def create_back_button(self):
        text = "back"
        pos = 50, 70
        size = [80, 80]
        new_button = Button(self.settings, self.gi, pos, size, image=text)
        self.button_list.append(new_button)

    def create_chips(self, do_anim=False):
        """Function to create chips legend"""

        if self.board:
            self.chip_group.clear()
            size = self.settings.bg_rect.w / 1.8, self.settings.bg_rect.h / 4
            self.legend_rect = pygame.Rect((0, 0), size)
            if do_anim:
                self.legend_rect.topright = self.settings.bg_rect.bottomright
                self.legend_rect.top += 216
                self.do_anim = True
            else:
                self.legend_rect.bottomright = self.settings.bg_rect.bottomright
                self.do_anim = False

            chip_dict = gf.calculate_legend_chips(self.gi.personal_budget)

            name_list = ["thousand", "five hundred",
                         "hundred", "twentyfive", "five", "one"]
            slot_x_offset = self.legend_rect.w / 6.5
            name_x_list = []
            x = self.legend_rect.left
            for name in name_list:
                x += slot_x_offset
                name_x_list.append([name, x])

            color_list = list(self.settings.chip_color_dict.values())

            for name, x in name_x_list:
                i = chip_dict[name]
                y = self.legend_rect.top + 5
                j = -(name_list.index(name)+1)
                while i > 0:
                    new_chip = Chip(
                        color=color_list[j], settings=self.settings)
                    new_chip.rect.center = (x, y)
                    self.chip_group.insert(0, new_chip)
                    y += 50
                    i -= 1

    def opening_anim(self):
        if self.br_rect.bottomright != self.settings.screen_size:
            self.br_rect.bottom -= 14
            if self.br_rect.bottom < self.settings.screen_size[1]:
                self.br_rect.bottom = self.settings.screen_size[1]
            text_list = ["undo", "cross", "redo"]
            for button in self.button_list:
                if button.image in text_list:
                    y = button.rect.centery - 14
                    button.pos = (button.rect.centerx, y)

        if self.legend_rect.top > self.br_rect.top + 140:
            self.legend_rect.top -= 14
            for chip in self.chip_group:
                chip.rect.top -= 14
        else:
            self.legend_rect.top = self.br_rect.top
            self.do_anim = False

    def update(self):
        """Function to update the board"""
        if self.active:
            self.update_chips()
            if self.do_anim:
                self.opening_anim()

            try:
                self.chip_all_groups_list = [self.chip_group,
                                             self.chip_group_placed, self.cursor_chip]
                self.gi.all_chips_group_list = self.chip_all_groups_list
            except:
                print("No groups")

            if self.info_field_list:
                for field in self.info_field_list:
                    field.update_info_field()

            # Do button updates here
            for button in self.button_list:
                self.gi.button_list.add(button)
                if button.clicked == True:
                    if button.image_msg != "back":
                        chip_list, remove = gf.utility_buttons_action(
                            self.gi, button.image_msg)
                        if remove:
                            for chip in chip_list:
                                self.chip_group_placed.remove(chip)
                        elif remove == False:
                            for chip in chip_list:
                                self.chip_group_placed.add(chip)
                    else:
                        self.gi.reset = True
                    button.clicked = False

            if self.board:
                self.board.update()

            if self.roulette_wheel:
                self.roulette_wheel.update()

            if self.budget != self.gi.personal_budget:
                self.budget = self.gi.personal_budget
                self.update_budget_text(self.budget)
                self.create_chips()

            if self.gi.personal_budget <= 0 and not self.gi.placed_chips_list and not self.gi.winnings_screen:
                gf.game_over(self.screen, self.settings, self.gi)

    def update_chips(self):
        """Function that handles updating the chips."""
        gf.check_chip_overlap(self.chip_group_placed)

        x, y = pygame.mouse.get_pos()

        """For loop to update chips"""
        for chip in reversed(self.chip_group):
            if pygame.Rect.collidepoint(chip.rect, x, y):
                if not self.hovered_chip or self.hovered_chip.rect.center != chip.rect.center:
                    self.info_field_list.clear()
                    self.gi.info_fields_list.clear()
                    self.hovered_chip = Chip(
                        settings=self.settings, color=chip.color, resize_multiplier=1.1, shadow=True)
                    self.hovered_chip.rect.center = chip.rect.center
                    self.gi.hover_chip = self.hovered_chip
                break

        """Create an information box showing the hovered chips price"""
        if self.hovered_chip:
            if not self.info_field_list:
                new_info_field = gf.create_info_field(
                    self.settings, self.gi, chip=self.hovered_chip, id=1)
                self.info_field_list.append(new_info_field)

            if not pygame.Rect.collidepoint(self.hovered_chip.rect, x, y):
                self.hovered_chip = None
                self.gi.hover_chip = None

        elif self.info_field_list:
            if self.info_field_list[-1].id == 1:
                self.info_field_list.clear()
                self.gi.info_fields_list.clear()

        # This is the chip that follows the cursor
        c_chip = self.gi.cursor_chip
        if c_chip:
            self.hovered_chip = None
            self.gi.hover_chip = None
            if c_chip.rect.center != (x, y):
                offset_x = c_chip.rect.centerx - x
                if offset_x != 0:
                    new_x = c_chip.rect.centerx - (offset_x / 3)
                else:
                    new_x = x

                offset_y = c_chip.rect.centery - y
                if offset_y != 0:
                    new_y = c_chip.rect.centery - (offset_y / 3)
                else:
                    new_y = y
                c_chip.reposition(new_x, new_y)

            """Create an information box showing the selected chips expected return price"""
            if not self.info_field_list:
                expected_return = c_chip.get_expected_return(
                    self.gi)
                if expected_return != c_chip.price:
                    new_info_field = gf.create_info_field(
                        self.settings, self.gi, chip=c_chip, id=2)
                    self.info_field_list.append(new_info_field)

            else:
                if self.info_field_list:
                    expected_return = c_chip.get_expected_return(
                        self.gi)
                    msg = "€" + "{:,}".format(expected_return)
                    self.info_field_list[-1].prep_msg(msg)
                    if expected_return == c_chip.price:
                        self.info_field_list.clear()
                        self.gi.info_fields_list.clear()

        if not c_chip:
            if self.info_field_list:
                if self.info_field_list[-1].id == 2:
                    self.info_field_list.clear()
                    self.gi.info_fields_list.clear()

        for chip in self.chip_group_placed:
            if not hasattr(chip, "expected_return"):
                chip.get_expected_return(self.gi)

    def update_budget_text(self, budget: int, index=0, font_color=None):
        pos = self.image_list[index][1].bottomright
        if self.image_list:
            self.image_list.pop(index)
        msg = "€" + "{:,.2f}".format(budget)
        if font_color:
            msg_image, msg_image_rect = gf.create_text(
                pos, msg, 40, font_color=font_color)
        else:
            msg_image, msg_image_rect = gf.create_text(pos, msg, 40)
        msg_image_rect.bottomright = pos
        self.image_list.insert(index, (msg_image, msg_image_rect))

    def create_budget_text(self, budget: int, pos, index=0):
        """pos is the position of the text adjusted to the bottom right of the text"""
        msg = "€" + "{:,.2f}".format(budget)
        msg_image, msg_image_rect = gf.create_text(pos, msg, 40)
        msg_image_rect.bottomright = pos
        self.image_list.insert(index, (msg_image, msg_image_rect))

    def create_winnings_screen(self):
        new_screen = Pause_screen(self.screen, self.settings, self.gi)
        self.gi.winnings_screen = new_screen

    def blitme(self):
        """Function to blit to the screen."""

        if self.board:
            self.board.blitme()
        for msg_image, msg_image_rect in self.image_list:
            self.screen.blit(msg_image, msg_image_rect)

        self.screen.blit(self.br_surf, self.br_rect)

        if self.roulette_wheel:
            pass
            # self.roulette_wheel.blitme(self.screen)
