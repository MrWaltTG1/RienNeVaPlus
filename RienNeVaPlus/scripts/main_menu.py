import pygame
from elements import Button, Pop_up
import game_functions as gf


class Main_menu():
    def __init__(self, screen, settings, game_info):
        """Class that holds the main menu"""

        self.screen = screen
        self.settings = settings
        self.gi = game_info
        self.button_list, self.pop_up_list, self.image_list = [], [], []
        self.active = False
        self.budget_pop_up_active = False

        # Form the screen
        try:
            self.og_image_bg = pygame.image.load(
                "RienNeVaPlus/images/french_roulette.png")
            size = self.og_image_bg.get_size()
            self.image_bg = pygame.transform.smoothscale(
                self.og_image_bg, (size[0] * 0.9, size[1] * 0.9))
        except FileNotFoundError:
            self.image_bg = pygame.Surface(self.settings.screen_size)
        finally:
            self.rect = self.image_bg.get_rect()
            self.rect.centerx = self.settings.bg_rect.centerx
            self.rect.top += 40

    def create_pop_up_budget(self):
        self.budget_pop_up_active = True
        size = self.settings.screen_size
        pos = size[0] / 2, size[1] / 1.5
        new_popup = Pop_up(self.settings, pos, (size[0] * 0.7, size[1] * 0.4), (0,0,0, 160))
        new_popup.prep_msg("Enter your budget:",
                           (221, 151, 0), 40, pos=(50, 50))
        self.budget_number = 0
        new_popup.prep_msg("")
        self.pop_up_list.append(new_popup)
        self.gi.pop_up_list.update(self.pop_up_list)
        self.update_budget_pop_up(pygame.event.Event(pygame.KEYDOWN, {'unicode': '0', 'key': 1073741922, 'mod': 4096, 'scancode': 98, 'window': None}))


    def update_budget_pop_up(self, event: pygame.event.Event) -> None:
        """Function to update the budget pop up."""
        pop_up = self.pop_up_list[0]
        font_color = (255, 255, 255)
        if event.unicode.isdigit():
            if self.budget_number < 1000000:
                self.budget_number = int(
                    str(self.budget_number) + str(event.unicode))
                if self.budget_number > 1000000:
                    self.budget_number = 1000000
            elif self.budget_number == 1000000:
                pop_up.start_shake()

        elif event.key == pygame.K_BACKSPACE:
            if len(str(self.budget_number)) > 1:
                self.budget_number = int(str(self.budget_number)[:-1])
            else:
                self.budget_number = 0

        elif event.key == pygame.K_RETURN:
            """ When the user presses the ENTER key do:"""
            self.gi.current_stage = 1
            self.pop_up_list.remove(pop_up)
            self.gi.pop_up_list.remove(pop_up)
            self.gi.button_list.clear()
            self.gi.personal_budget = int(self.budget_number)
            self.budget_pop_up_active = False
            self.active = False

        text = "€" + "{:,.2f}".format(self.budget_number)
        del pop_up.msg_image_list[3:]
        pop_up.prep_msg(text, font_color=font_color, center=True)


    def create_start_button(self):
        button_pos = (self.settings.screen_size[0] / 2, self.settings.screen_size[1] /1.5)
        button_size = (400,200)

        new_button = Button(self.settings, button_pos,
                            button_size, msg="START", image="start")
        self.button_list.append(new_button)

    def create_self(self):
        """Function to make itsself."""
        self.create_start_button()
        self.active = True

    def create_preset_budget_buttons(self):
        pop_up = self.pop_up_list[-1]
        size = (int(pop_up.static_rect.w / 5), 80)
        start_x, end_x, step_x = int(
            pop_up.static_rect.left + (size[0]/2) + int(size[0] / 5)), int(pop_up.static_rect.right -10), size[0] + int(size[0] / 5)
        y = pop_up.static_rect.bottom - 100
        text_dict = {
            0: "€10000",
            1: "€1000",
            2: "€500",
            3: "€100"
        }
        for i, x in enumerate(range(start_x, end_x, step_x)):
            new_button = Button(self.settings, (x, y), size, msg=text_dict[i], image="start")
            self.button_list.append(new_button)
            if i == 3:
                break

    def update(self):
        if self.active:
            # Do button updates here
            for button in self.button_list:
                self.gi.button_list.add(button)
                if button.clicked == True:
                    # do button click
                    if len(self.button_list) > 1:
                        budget = button.msg[1:]
                        pygame.event.post(pygame.event.Event(
                            pygame.KEYDOWN, key=pygame.K_RETURN, unicode="/r"))
                        self.budget_number = int(budget)
                        self.button_list.clear()
                        self.gi.button_list.clear()

                    elif button == self.button_list[0]:
                        # The start button should be number one
                        self.create_pop_up_budget()
                        self.create_preset_budget_buttons()
                        self.button_list.remove(button)
                        self.gi.button_list.remove(button)
                        if not self.pop_up_list:
                            raise Exception(
                                "The start button should be number one. But it isnt")
            for pop_up in self.pop_up_list:
                pop_up.update()
                            
        
    def create_box(self):
        dark_surf, dark_rect = gf.get_darkened_screen_list(self.settings)
        self.image_list.append((dark_surf, dark_rect))

    def blitme(self):
        if self.active:
            self.screen.blit(self.image_bg, self.rect)
                
            for image, rect in self.image_list:
                self.screen.blit(image, rect)
