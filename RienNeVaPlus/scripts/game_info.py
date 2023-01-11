import pygame

class Game_info():
    def __init__(self) -> None:
        """Class that saves game info"""
        # Stage 0 == before the table is initialized
        # Stage 1 == active phase of the game
        # Stage 2 == while the roulette wheel is active and after when showing the winnings
        self.current_stage = 0
        self.personal_budget = None
        self.expected_winnings = 0
        self.previous_rolled_numbers_list = []
        
        self.button_list = set()
        self.pop_up_list = set()
        self.chip_group_list = []
        self.placed_chips_list = []
        self.placed_chips_redo_list = []
        self.placed_chips_undo_list = []
        self.info_fields_list = set()
        self.fields_list = list()
        self.hitboxes_dict = dict()
        
        self.elements_dict = {
            "buttons" : self.button_list,
            "pop_ups" : self.pop_up_list,
            "chips" : self.chip_group_list,
            "info_fields" : self.info_fields_list,
            "fields_list" : self.fields_list,
            "hitboxes" : self.hitboxes_dict
        }
        
    def update(self):
        if len(self.previous_rolled_numbers_list) > 5:
            self.previous_rolled_numbers_list.pop(-1)
        
        if self.chip_group_list:
            # Index 2 is placed chips group
            for chip in self.chip_group_list:
                self.placed_chips_list.append(chip)
