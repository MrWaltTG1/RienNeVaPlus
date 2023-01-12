import random
import sys
import time

import possible_bets as pb
import pygame
from chips import Chip
from elements import Info_field
from game_info import Game_info
from main_menu import Main_menu
from play_screen import Play_screen
from settings import Settings


def update_screen(screen, settings: Settings, main_menu: Main_menu, play_screen: Play_screen, game_info: Game_info):
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
                info_field.blitme(screen)
        elif type == "chips":
            for group in element_list:
                try:
                    group.draw(screen)
                except AttributeError:
                    pass
        elif type == "winnings_screen":
            if element_list:
                element_list.blitme()

    pygame.display.flip()


def check_events(screen, settings: Settings, main_menu: Main_menu,  play_screen: Play_screen, game_info: Game_info):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_down_events(
                event, screen, settings, main_menu, play_screen, game_info)

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


def check_mouse_down_events(event, screen, settings: Settings, main_menu, play_screen: Play_screen, game_info: Game_info):
    x, y = event.pos
    
    # LMB
    if event.button == 1:
        if game_info.current_stage < 2:
            """If there is a cursor chip"""
            if game_info.cursor_chip:
                reset_chip = True
                do_break = False
                """Place a chip on the right location"""
                for hitbox_dict in game_info.hitboxes_dict.values():
                    for hitbox in hitbox_dict.values():
                        if check_hitbox_mouse_collision(hitbox):
                            new_chip = Chip(game_info.all_chips_group_list[2], settings=settings,
                                            color=game_info.cursor_chip.color,
                                            resize_multiplier=0.5)
                            new_chip.reposition(hitbox.centerx, hitbox.centery)
                            game_info.placed_chips_list.append(new_chip)
                            reset_chip = False
                            do_break = True
                            break
                    if do_break:
                        break
                """If a chip cannot be placed then remove the chip from the cursor"""
                if reset_chip:
                    game_info.cursor_chip = None
                    
            else:
                """If a chip cannot be placed, then check if a placed chip has been clicked to remove it"""
                for placed_chip in game_info.placed_chips_list:
                    if placed_chip.rect.collidepoint(x, y):
                        for chip_check in game_info.placed_chips_list:
                            if placed_chip.rect.collidepoint(chip_check.rect.centerx -2, chip_check.rect.centery + 2):
                                if game_info.placed_chips_list.index(placed_chip) < game_info.placed_chips_list.index(chip_check):
                                    placed_chip = chip_check
                        game_info.placed_chips_list.remove(placed_chip)
                        game_info.placed_chips_undo_list.append([placed_chip])
                        break
            
            """Create a cursor chip"""
            for chip_list in game_info.all_chips_group_list[:1]:
                for chip in chip_list:
                    if chip.rect.collidepoint(x, y) and chip.price <= game_info.personal_budget:
                        new_chip = Chip(settings=settings,
                                        color=chip.color, resize_multiplier=0.5)
                        game_info.cursor_chip = new_chip  # type: ignore
            
            """Set button state to true when clicked"""
            for button in game_info.elements_dict["buttons"]:
                if button.rect.collidepoint(x, y):
                    button.clicked = True

            try:
                if play_screen.roulette_wheel:
                    if play_screen.roulette_wheel.rect.collidepoint(x, y):
                        if game_info.placed_chips_list:
                            # game_info.outcome = spin_wheel()
                            play_screen.roulette_wheel.spin()
                            game_info.current_stage = 2
                        else:
                            print("No chips have been placed on the board yet")
            except Exception:
                pass

            if game_info.winnings_screen:
                if game_info.winnings_screen.rect.collidepoint(x, y):
                    game_info.winnings_screen.active = False


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
    time.sleep(2)
    return outcome


def create_text(pos, msg: str, font_size: int, rotate=False, font_color=(255, 255, 255)):
    """Create text inside the box"""
    font = pygame.font.SysFont("Consolas", int(font_size))
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


def create_info_field(settings, game_info, size=(0, 0), msg=None, color=None, id=None, chip=None):
    """Creates an info field.

    Args:
        settings (Settings object)
         game_info (Game_info object)
        size (list(int, int), optional): Sets the size. Gets overridden when chip is set. Defaults to (0, 0).
        msg (str, optional): Sets the message in the box. Gets overridden when chip is set. Defaults to None.
        color (list(int, int, int), optional): Set the color of the box. Defaults to white.
        id (int, optional): In case you need to set the id. Defaults to None.
        chip (Chip object, optional):Defaults to None.

    Returns:
        Info_field: Returns the created Info_field
    """
    if not color:
        color = (255, 255, 255)
    if chip:
        msg = "€" + "{:,}".format(chip.price)
        size = [len(msg) * 15, chip.rect.h / 2]

    new_info_field = Info_field(settings, size, color, msg, id, chip)
    game_info.info_fields_list.add(new_info_field)

    return new_info_field


def check_chip_overlap(chip_group: pygame.sprite.Group):
    """Checks if chips overlap in the given group and repositions if necessary"""
    chip_list = chip_group.sprites()
    for chip1 in chip_list:
        for chip2 in chip_list:
            if chip1 == chip2:
                continue
            else:
                if chip1.rect.center == chip2.rect.center:
                    chip2.rect.centerx += 2
                    chip2.rect.centery -= 2
                    break


def check_winnings(game_info: Game_info):
    """Calculates the amount of money that was either lost or won for all chips put in."""
    returns = 0
    for chip in game_info.placed_chips_list:
        returns -= chip.price
        expected = chip.expected_return
        for field in chip.field_list:
            if str(game_info.outcome) == field.msg:
                returns += expected
                break

    print(returns)
    return returns


def utility_buttons_action(game_info: Game_info, button_function: str):
    """This function either redos/undos or clear the chips on the table.
    Then it returns the cleared chips and whether it was removed or added back to the table"""
    text_list = ("undo", "cross", "redo")
    remove = True
    chip_list, temp_chip_list = [], []
    if button_function in text_list:
        if button_function == "undo":
            if game_info.placed_chips_list:
                chip = game_info.placed_chips_list[-1]
                game_info.placed_chips_undo_list.append([chip])
                game_info.placed_chips_list.remove(chip)
                chip_list.append(chip)

        elif button_function == "redo":
            if game_info.placed_chips_undo_list:
                temp_chip_list = game_info.placed_chips_undo_list[-1]
                game_info.placed_chips_undo_list.remove(temp_chip_list)
                for chip in temp_chip_list:
                    game_info.placed_chips_list.append(chip)
                    chip_list.append(chip)
                remove = False

        elif button_function == "cross":
            if game_info.placed_chips_list:
                for chip in game_info.placed_chips_list:
                    temp_chip_list.append(chip)
                    chip_list.append(chip)
                game_info.placed_chips_undo_list.append(temp_chip_list)
                game_info.placed_chips_list.clear()

    return chip_list, remove
