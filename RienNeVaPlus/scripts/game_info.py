import pygame
from main_menu import Main_menu
from play_screen import Play_screen


class Game_info():
    def __init__(self, screen, settings) -> None:
        """Class that saves game info"""
        # Stage 0 == before the table is initialized
        # Stage 1 == active phase of the game
        # Stage 2 == while the roulette wheel is active and after when showing the winnings
        self.current_stage = 0
        self.personal_budget = 0
        self.returns = 0
        self.total_returns = 0
        self.expected_winnings = 0
        self.previous_rolled_numbers_list = [-1, -1, -1, -1, -1]

        self.button_list = set()
        self.pop_up_list = set()
        self.info_fields_list = set()
        self.fields_list = list()
        self.selected_fields_list = set()
        self.previous_fields_list = list()
        self.hitboxes_dict = dict()
        self.budget_bar = None
        self.winnings_screen = None
        self.wheel = None
        self.game_over = None

        self.all_chips_group_list = []
        self.cursor_chip = None
        self.hover_chip = None
        self.placed_chips_list = []
        self.placed_chips_undo_list = []
        self.tabel = None

        self.outcome = -1

        self.elements_dict = {
            "pop_ups": self.pop_up_list,
            "buttons": self.button_list,
            "chips": self.all_chips_group_list,
            "info_fields": self.info_fields_list,
            "fields_list": self.fields_list,
            "selected_fields": self.selected_fields_list,
            "hitboxes": self.hitboxes_dict,
            "winnings_screen": self.winnings_screen,
            "budget_bar": self.budget_bar,
            "tabel": self.tabel,
            "game_over" : self.game_over,
        }

        self.current_tick = pygame.time.get_ticks()

        self.main_menu = Main_menu(screen, settings, self)
        self.play_screen = Play_screen(
            screen=screen, settings=settings, game_info=self)
        self.reset = False

    def update(self):
        """Updates the game info with the current information"""

        """Elements in the order they are blitted to the screen"""
        self.elements_dict = {
            "pop_ups": self.pop_up_list,
            "buttons": self.button_list,
            "chips": self.all_chips_group_list,
            "fields_list": self.fields_list,
            "previous_fields": self.previous_fields_list,
            "selected_fields": self.selected_fields_list,
            "hitboxes": self.hitboxes_dict,
            "winnings_screen": self.winnings_screen,
            "budget_bar": self.budget_bar,
            "tabel": self.tabel,
            "wheel" : self.wheel,
            "hover_chip" : self.hover_chip,
            "cursor_chip" : self.cursor_chip,
            "info_fields": self.info_fields_list,
        }

        if self.budget_bar:
            self.budget_bar.update()

        self.current_tick = pygame.time.get_ticks()

        if len(self.previous_rolled_numbers_list) > 5:
            self.previous_rolled_numbers_list.pop(-1)
        if len(self.previous_fields_list) > 5:
            self.previous_fields_list.pop(-1)

        if self.all_chips_group_list:
            # Index 0 is the chip group that is clickable
            """This doesnt change"""
            # Index 2 is the chip that is following the cursor
            if self.all_chips_group_list[2] != self.cursor_chip:
                self.all_chips_group_list[2] = self.cursor_chip

            # Index 1 is placed chips group
            for chip in self.all_chips_group_list[1]:
                if not chip in self.placed_chips_list:
                    self.all_chips_group_list[1].remove(chip)

        for field in self.fields_list:
            if field in self.selected_fields_list:
                field.selected = True
            else:
                field.selected = False
