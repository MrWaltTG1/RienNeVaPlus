import random
import sys

import possible_bets as pb
from chips import Chip
from settings import Settings
from main_menu import Main_menu
from play_screen import Play_screen
from game_info import Game_info

import pygame


def update_screen(screen, settings, main_menu, play_screen, game_info):
    screen.blit(settings.bg_surf, settings.bg_rect)
    
    if main_menu.active and game_info.current_stage == 0:
        main_menu.blitme()
    if play_screen.active and not game_info.current_stage == 0:
        play_screen.blitme()
    
    for type, element_list in game_info.elements_dict.items():
        if type == "buttons":
            for button in element_list:
                button.blitme(screen)
        elif type == "pop_ups":
            for pop_up in element_list:
                pop_up.blitme(screen)
        elif type == "info_fields":
            for info_field in element_list:
                info_field.blitme()
        elif type == "chips":
            for group in element_list:
                group.draw(screen)

    pygame.display.flip()


def check_events(screen, settings: Settings, main_menu: Main_menu,  play_screen: Play_screen, game_info: Game_info):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_down_events(event, screen, settings, main_menu, play_screen, game_info)

        elif event.type == pygame.MOUSEBUTTONUP:
            check_mouse_up_events(event)
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, main_menu, game_info)


def check_key_down_events(event, main_menu, game_info):
    if game_info.current_stage == 0:
        if main_menu.budget_pop_up_active == True:
            main_menu.update_budget_pop_up(event)
    elif game_info.current_stage == 1:
        pass


def check_mouse_down_events(event, screen, settings, main_menu, play_screen, game_info):
    x, y = event.pos

    if event.button == 1:
        if play_screen.chip_group_temp:
            reset_chip = True
            do_break = False
            for hitbox_dict in play_screen.board.all_hitbox_rects_dict.values():
                for hitbox in hitbox_dict.values():
                    if check_hitbox_mouse_collision(hitbox):
                        new_chip = Chip(play_screen.chip_group_placed, settings=settings,
                                        color=play_screen.chip_group_temp.sprites(
                                        )[-1].color,
                                        resize_multiplier=0.5)
                        new_chip.reposition(hitbox.centerx, hitbox.centery)
                        play_screen.new_budget -= new_chip.price
                        reset_chip = False
                        do_break = True
                        break
                if do_break:
                    break
            if reset_chip:
                play_screen.chip_group_temp.empty()

        for chip in play_screen.chip_group:
            if chip.rect.collidepoint(x, y):
                new_chip = Chip(settings=settings, color=chip.color)
                play_screen.chip_group_temp.add(new_chip)

        for button in game_info.elements_dict["buttons"]:
            if button.rect.collidepoint(x, y):
                button.clicked = True

        try:
            if play_screen.roulette_wheel:
                if play_screen.roulette_wheel.rect.collidepoint(x, y):
                    play_screen.outcome = spin_wheel()
        except Exception:
            pass


def check_mouse_up_events(event):
    pass


def spin_wheel():
    """Generates a random number between 0 and 37"""
    outcome = random.randrange(0, 37)
    print(outcome, end="")
    if outcome in pb.noir:
        print("b")
    elif outcome in pb.rouge:
        print("r")
    return outcome


def create_text(pos, msg: str, font_size: int, rotate=False, font_color=(255, 255, 255)):
    """Create text inside the box"""
    font = pygame.font.SysFont("Ariel", font_size)
    msg_image = font.render(msg, True, font_color)
    msg_image_rect = msg_image.get_rect()
    if rotate:
        msg_image = pygame.transform.rotate(msg_image, 90)
    msg_image_rect.center = pos  # type: ignore

    if len(msg) == 1:
        msg_image_rect.centery += 7
        msg_image_rect.centerx -= 2

    return msg_image, msg_image_rect


def create_hitboxes(obj, center_only=False):
    """Create hitboxes"""

    # Create corner hitboxes
    hitbox_rect_dict = {}
    if not center_only:
        # Create corner hitboxes
        hitbox_pos_list_corners = [obj.rect.topleft, obj.rect.topright,
                                   obj.rect.bottomleft, obj.rect.bottomright,
                                   obj.rect.midtop, obj.rect.midbottom,
                                   obj.rect.midleft, obj.rect.midright]
        dict_text_list = ["topleft", "topright", "bottomleft", "bottomright",
                          "centertop", "centerbottom",
                          "centerleft", "centerright"]
        size = obj.rect.size[0] / 2, obj.rect.size[1] / 2
        for pos, text in zip(hitbox_pos_list_corners, dict_text_list):
            new_rect = pygame.rect.Rect(pos, size)
            new_rect.center = pos
            hitbox_rect_dict[text] = new_rect

    # Create center hitbox
    new_rect = pygame.rect.Rect(obj.rect.center, obj.rect.size)
    new_rect.center = obj.rect.center
    hitbox_rect_dict[0] = new_rect
    return hitbox_rect_dict


def check_hitbox_mouse_collision(hitbox: pygame.Rect) -> bool:
    """Maybe reverse the way this works?"""
    x, y = pygame.mouse.get_pos()
    if pygame.Rect.collidepoint(hitbox, x, y):
        return True
    else:
        return False


def give_hovered_fields(all_fields: list, all_hitboxes: dict):
    """Should definitely be a better way to do this"""

    hitbox_list, field_list, field_number_list = [], [], []
    for hitbox_dict in all_hitboxes.values():
        for hitbox in hitbox_dict.values():
            if check_hitbox_mouse_collision(hitbox):
                hitbox_list.append(hitbox)

    field_dict = {}
    for hitbox in hitbox_list:
        for field in all_fields:
            if pygame.Rect.colliderect(hitbox, field.rect):
                field_dict[field.msg] = field
    dict = {
        "column1": pb.colonne1,
        "column2": pb.colonne2,
        "column3": pb.colonne3,
        "MANQUE 1-18": pb.manque,
        "IMPAIR": pb.impair,
        "ROUGE": pb.rouge,
        "PASSE 19-36": pb.passe,
        "PAIR": pb.pair,
        "NOIR": pb.noir,
        "P12": pb.premiere,
        "M12": pb.moyenne,
        "D12": pb.derniere
    }

    if len(field_dict) == 1:
        msg = list(field_dict.keys())[0]
        if msg.isdigit():
            for value in field_dict.values():
                field_list.append(value)
        else:
            field_number_list = dict[msg]

    elif len(field_dict) > 1:
        if list(field_dict.keys())[-1].isdigit():
            for value in field_dict.values():
                field_list.append(value)
        else:
            msg = list(field_dict.keys())[-1]
            msg_list = ["MANQUE 1-18", "IMPAIR",
                        "ROUGE", "PASSE 19-36", "PAIR", "NOIR"]
            if msg in msg_list:
                # TOP ROW
                if msg in msg_list[0:3]:
                    if len(field_dict) == 2:
                        field_number_list = pb.transversale_pleine(
                            int(list(field_dict.keys())[0])-2)
                    else:
                        field_number_list = pb.transversale_simple(
                            int(list(field_dict.keys())[0])-2)
                # BOTTOM ROW
                else:
                    if len(field_dict) == 2:
                        field_number_list = pb.transversale_pleine(
                            int(list(field_dict.keys())[0]))
                    else:
                        field_number_list = pb.transversale_simple(
                            int(list(field_dict.keys())[0]))

    if field_number_list:
        for field in all_fields:
            if field.msg.isdigit():
                if int(field.msg) in field_number_list:
                    field_list.append(field)

    return field_list


def make_field_glow(screen: pygame.Surface, field):
    """Draws a 'glow' around a field."""
    if hasattr(field, "points"):
        pygame.draw.polygon(
            screen, (219, 207, 37), field.points, width=5)
    else:
        pygame.draw.rect(
            screen, (219, 207, 37), field.rect, width=5)


def create_info_field(pos, size: list, msg):
    """Returns a list of textbox info.

    Used to create the chip info box."""
    start_rect = pygame.Rect(pos, (size))
    end_rect = pygame.Rect(pos, (size[0]*2, size[1]))
    msg_surf, msg_rect = create_text(
        end_rect.center, msg, 30, font_color=(0, 0, 0))
    msg_surf.set_alpha(10)
    field_list = [start_rect, end_rect, [msg_surf, msg_rect]]

    return field_list





def check_chip_overlap(chip_group: pygame.sprite.Group):
    """Checks if chips overlap in the given group and repositions if necessary"""

    chip_list = chip_group.sprites()
    for chip1 in chip_list:
        for chip2 in chip_list:
            if chip1 == chip2:
                continue
            else:
                if chip1.color == chip2.color:
                    if chip1.rect.center == chip2.rect.center:
                        chip2.rect.centerx += 2
                        chip2.rect.centery -= 2
                        break
                else:
                    if chip1.rect.center == chip2.rect.center:
                        i = random.randint(1, 2)
                        if i == 1:
                            chip2.rect.centerx += chip2.rect.width
                        else:
                            chip2.rect.centerx -= chip2.rect.width
                        break


def check_winnings(outcome: int, placed_chips: pygame.sprite.Group):
    returns = 0
    for chip in placed_chips:
        returns -= chip.price
        expected = chip.expected_return
        for field in chip.field_list:
            if str(outcome) == field.msg:
                returns += expected
                break

    print(returns)
    return returns
