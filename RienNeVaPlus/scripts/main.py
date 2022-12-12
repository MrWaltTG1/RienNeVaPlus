import pygame
import game_functions as gf
from settings import Settings
from play_screen import Play_screen


def run():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Rien Ne Va Plus")

    active = True
    clockobject = pygame.time.Clock()
    play_screen = Play_screen(screen=screen, settings=settings)

    while active:
        board = play_screen.board
        clockobject.tick(60)
        play_screen.update()
        gf.check_events(screen, settings)
        gf.update_screen(screen, settings=settings,
                         board=board, play_screen=play_screen)

    """# Runs the program
    budget = gf.ask_budget()
    spin = False
    bet_list = []
    while not spin:
        bet = gf.ask_bet()
        bet_list.append((bet))
        bet_value = int(input("Enter how much you would like to bet: "))
        budget -= bet_value
        if input("Bet some more? y/n: ") == "n":
            spin = True

    spinned_number = gf.spin_wheel()
    bet_multiplier_list = gf.wheel_math(spinned_number, bet_list)
    if bet_multiplier_list:
        for bet_multiplier in bet_multiplier_list:
            budget += bet_value * bet_multiplier
    print(budget)
    spin = False"""


run()
