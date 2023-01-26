import pygame
import game_functions as gf
from settings import Settings
from game_info import Game_info


def run():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("Rien Ne Va Plus")
    pygame.display.set_icon(settings.bg_surf)

    clockobject = pygame.time.Clock()
    # Initialize the game objects
    game_info = Game_info(screen, settings)

    # Create the main menu
    game_info.main_menu.create_self()

    # As long as active is true the game will continue
    active = True
    while active:
        if game_info.reset == True:
            game_info = Game_info(screen, settings)
            game_info.main_menu.create_self()
        clockobject.tick(60)
        game_info.update()
        if game_info.current_stage == 0:
            game_info.main_menu.update()
        elif game_info.current_stage > 0:
            if not game_info.play_screen.active:
                game_info.play_screen.create_self()
            game_info.play_screen.update()
            if game_info.tabel:
                game_info.tabel.update()

            if game_info.winnings_screen:
                game_info.winnings_screen.update()
        for button in game_info.elements_dict["buttons"]:
            button.update()

        gf.check_events(screen, settings, game_info.main_menu,
                        game_info.play_screen, game_info)
        gf.update_screen(screen, settings, game_info.main_menu,
                         game_info.play_screen, game_info)


run()
