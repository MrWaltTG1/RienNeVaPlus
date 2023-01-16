import pygame
from elements import Button, Pop_up


class Main_menu():
    def __init__(self, screen, settings, game_info):
        """Class that holds the main menu"""

        self.screen = screen
        self.settings = settings
        self.gi = game_info
        self.button_list, self.pop_up_list = [], []
        self.active = False
        self.budget_pop_up_active = False

        # Form the screen
        try:
            self.og_image_bg = pygame.image.load(
                "RienNeVaPlus/images/main_menu_bg.bmp")
            self.image_bg = pygame.transform.scale(
                self.og_image_bg, self.settings.screen_size)
        except FileNotFoundError:
            self.image_bg = pygame.Surface(self.settings.screen_size)
        finally:
            self.rect = self.image_bg.get_rect()
            self.rect.topleft = (0, 0)

    def create_pop_up_budget(self):
        new_popup = Pop_up(self.settings, (500, 400), (300, 200))
        new_popup.prep_msg("Enter your budget:",
                           (0, 0, 0), 40, pos=(10, 10))
        self.budget_number = 0
        new_popup.prep_msg("")
        self.pop_up_list.append(new_popup)
        self.gi.pop_up_list.update(self.pop_up_list)
        self.budget_pop_up_active = True

    def update_budget_pop_up(self, event: pygame.event.Event) -> None:
        """Function to update the budget pop up."""
        pop_up = self.pop_up_list[0]

        if event.unicode.isdigit():
            self.budget_number = int(
                str(self.budget_number) + str(event.unicode))

        elif event.key == pygame.K_BACKSPACE:
            if len(str(self.budget_number)) > 1:
                self.budget_number = int(str(self.budget_number)[:-1])
            else:
                self.budget_number = 0

        elif event.key == pygame.K_RETURN:
            self.gi.current_stage = 1
            self.pop_up_list.remove(pop_up)
            self.gi.pop_up_list.remove(pop_up)
            self.gi.button_list.clear()
            self.gi.personal_budget = int(self.budget_number)
            self.budget_pop_up_active = False
            self.active = False

        text = "€" + "{:,.2f}".format(self.budget_number)
        pop_up.msg_image_list.pop(1)
        pop_up.prep_msg(text, font_color=(0, 0, 0))

    def create_start_button(self):
        button_pos = self.settings.start_button_pos
        button_size = self.settings.start_button_size

        new_button = Button(self.settings, button_pos,
                            button_size, msg="START")
        self.button_list.append(new_button)

    def create_self(self):
        """Function to make itsself."""
        self.create_start_button()
        self.active = True

    def create_preset_budget_buttons(self):
        size = (int(self.settings.screen_size[0] / 6), 80)
        start_x, end_x, step_x = int(
            self.settings.screen_size[0] * 1/5), int(self.settings.screen_size[0] * 4/5), size[0] + 20
        y = self.pop_up_list[-1].rect.bottom + 100
        text_dict = {
            0: "€10000",
            1: "€1000",
            2: "€500",
            3: "€100"
        }
        for i, x in enumerate(range(start_x, end_x, step_x)):
            new_button = Button(self.settings, (x, y), size, msg=text_dict[i])
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

    def blitme(self):
        if self.active:
            # self.screen.blit(self.image_bg, self.rect)
            pass
