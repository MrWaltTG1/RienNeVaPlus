import random
import sys

import possible_bets as pb
from chips import Chip
from settings import Settings

import pygame


def update_screen(screen, *args, **kwargs):
    settings = kwargs["settings"]
    screen.blit(settings.bg_surf, settings.bg_rect)
    if kwargs["board"]:
        kwargs["board"].blitme()

        if settings.debug:
            kwargs["board"].blit_hitboxes()
    if kwargs["play_screen"]:
        kwargs["play_screen"].blitme()

    pygame.display.flip()


def check_events(screen, settings, play_screen):
    for event in pygame.event.get(exclude=pygame.KEYDOWN):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_down_events(event, screen, settings, play_screen)

        elif event.type == pygame.MOUSEBUTTONUP:
            check_mouse_up_events(event)
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event)


def check_key_down_events(event):
    pass


def check_mouse_down_events(event, screen, settings, play_screen):
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

        for button in play_screen.button_list:
            if button.rect.collidepoint(x, y):
                play_screen.create_budget_pop_up()
                play_screen.button_list.remove(button)
        
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


def update_info_field(field_list, chip=None, resize_speed = 1):
    """Function to update the info field"""

    x, y = 0, 0
    if not field_list[0].bottom > field_list[1].bottom:
        y = 4 * resize_speed
    if not field_list[0].right > field_list[1].right:
        x = 4 * resize_speed

    # Resize the info field
    field_list[0] = field_list[0].inflate(x, y)
    # Align the field top left
    field_list[0].topleft = field_list[1].topleft

    # Align the text on the right side
    field_list[2][1].right = field_list[0].right
    # Increase the text transparency
    alpha = field_list[2][0].get_alpha()
    field_list[2][0].set_alpha(alpha + 10)
    
    if chip:
        field_list[0].topleft = chip.rect.midtop
        field_list[1].topleft = chip.rect.midtop
        field_list[2][1].top = chip.rect.top

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
        expected = chip.expected_return
        for field in chip.field_list:
            if str(outcome) == field.msg:
                returns += expected
                break
            
    print(returns)
    return returns