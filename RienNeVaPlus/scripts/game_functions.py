import possible_bets as pb
import random
import pygame
import sys


def update_screen(screen, *args, **kwargs):
    settings = kwargs["settings"]
    screen.blit(settings.bg_surf, settings.bg_rect)

    kwargs["board"].blitme()
    if settings.debug:
        kwargs["board"].blit_hitboxes()

    pygame.display.flip()


def check_events(*args, **kwargs):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_down_events(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            check_mouse_up_events(event)


def check_mouse_down_events(event, *args, **kwargs):
    pass


def check_mouse_up_events(event, *args, **kwargs):
    pass


def ask_budget(budget=None):
    while not budget:
        try:
            budget = int(input("Enter your budget: "))
        except ValueError:
            print("Please enter a valid integer.")
    return budget


def ask_bet():
    bet = None
    while not bet:
        print("The possible options to bet on are:")
        print("rouge - noir - pair - impair - manque - passe")
        print("premiere - moyenne - derniere - colonne")
        print("t simple - carre - t pleine - cheval")
        print("Enter 1-36 for a single number")
        text = input("Enter your bet: ")

        if text.isdigit():
            bet = int(text)
        elif text == "rouge":
            bet = pb.rouge
        elif text == "noir":
            bet = pb.noir
        elif text == "pair":
            bet = pb.pair
        elif text == "impair":
            bet = pb.impair
        elif text == "manque":
            bet = pb.manque
        elif text == "passe":
            bet = pb.passe
        elif text == "premiere":
            bet = pb.premiere
        elif text == "moyenne":
            bet = pb.moyenne
        elif text == "derniere":
            bet = pb.derniere
        elif text == "colonne":
            row = int(input("Pick row 1, 2 or 3"))
            if row == 1:
                bet = pb.colonne1
            elif row == 2:
                bet = pb.colonne2
            elif row == 3:
                bet = pb.colonne3
        elif text == "t simple":
            number = int(input("give your starting number"))
            bet = pb.transversale_simple(number)
        elif text == "t pleine":
            number = int(input("give your starting number"))
            bet = pb.transversale_pleine(number)
        elif text == "carre":
            number = int(input("give your starting number"))
            bet = pb.carre(number)
        elif text == "cheval":
            number1 = int(input("give your first number"))
            number2 = int(input("give your second"))
            bet = pb.cheval(number1, number2)
    return bet


def spin_wheel():
    """Generates a random number between 0 and 37"""
    outcome = random.randrange(0, 37)
    print(outcome, end="")
    if outcome in pb.noir:
        print("b")
    elif outcome in pb.rouge:
        print("r")
    return outcome


def wheel_math(spinned_number, bet_list):
    bet_values = []
    for bet in bet_list:
        if spinned_number in bet:
            length = len(bet)
            if length == 1:
                bet_values.append(35)
            elif length == 2:
                bet_values.append(17)
            elif length == 3:
                bet_values.append(11)
            elif length == 4:
                bet_values.append(8)
            elif length == 6:
                bet_values.append(5)
            elif length == 12:
                bet_values.append(2)
            elif length == 18:
                bet_values.append(1)
        else:
            bet_values.append(0)
    return bet_values


def create_hitboxes(obj, center_only=False):
    # Create corner hitboxes
    hitbox_rect_list = []
    if not center_only:
        # Create corner hitboxes
        hitbox_pos_list_corners = [obj.rect.topleft, obj.rect.topright,
                                   obj.rect.bottomleft, obj.rect.bottomright,
                                   obj.rect.midtop, obj.rect.midbottom,
                                   obj.rect.midleft, obj.rect.midright]

        size = obj.rect.size[0] / 2, obj.rect.size[1] / 2
        for pos in hitbox_pos_list_corners:
            if pos == obj.rect.midtop:
                size = obj.rect.size[0] / 3, obj.rect.size[1] / 3
            new_rect = pygame.rect.Rect(pos, size)
            new_rect.center = pos
            hitbox_rect_list.append(new_rect)

    # Create center hitbox
    new_rect = pygame.rect.Rect(obj.rect.center, obj.rect.size)
    new_rect.center = obj.rect.center
    hitbox_rect_list.append(new_rect)
    return hitbox_rect_list


def create_text(obj, msg, font_size, rotate=False):
    """Create text inside the box"""
    font = pygame.font.SysFont("Ariel", font_size)
    msg_image = font.render(msg, True, (255, 255, 255))
    msg_image_rect = msg_image.get_rect()
    if rotate:
        msg_image = pygame.transform.rotate(msg_image, 90)
    msg_image_rect.center = obj.rect.center

    return msg_image, msg_image_rect