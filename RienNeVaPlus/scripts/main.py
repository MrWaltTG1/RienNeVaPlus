import pygame
import game_functions as gf
from settings import Settings
from play_screen import Play_screen
from main_menu import Main_menu
from game_info import Game_info


def run():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Rien Ne Va Plus")
    
    clockobject = pygame.time.Clock()
    # Initialize the game objects
    game_info = Game_info()
    main_menu = Main_menu(screen, settings, game_info)
    play_screen = Play_screen(screen=screen, settings=settings, game_info=game_info)
    
    # Create the main menu
    main_menu.create_self()
    
    # As long as active is true the game will continue
    active = True
    while active:
        clockobject.tick(60)
        
        if game_info.current_stage == 0:
            main_menu.update()
        elif game_info.current_stage > 0:
            if not play_screen.active:
                play_screen.create_self()
            play_screen.update()
        
        gf.check_events(screen, settings, main_menu, play_screen, game_info)
        gf.update_screen(screen, settings, main_menu, play_screen, game_info)


run()
