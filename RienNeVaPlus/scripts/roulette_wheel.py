from math import atan2, cos, degrees, pi, sin
from random import randint
import time

import possible_bets as pb
import game_functions as gf
import pygame


class Roulette():
    def __init__(self, settings, game_info, play_screen) -> None:
        self.settings, self.gi = settings, game_info
        self.ps = play_screen
        self.text_list = []
        self.og_text_list = []
        self.coord_list = []
        self.center_points_list = []
        self.angles_list = []
        self.bling_list = []
        self.pole_list = []
        self.rotation = 0
        self.p_rotation = 15
        self.spinning = False
        self.ball = None
        self.inner_compartment_list = []

        self.coords_list, self.color_list = self.create_fields()
        numbers = pb.wheel
        angle_offset = 360 / len(numbers)
        for i, number in enumerate(pb.wheel):
            pos = self.get_msg_pos(self.coords_list[i])
            angle = i*angle_offset + self.rotation + (angle_offset / 2)
            self.prep_msg(str(number), pos, angle)

        self.rect = pygame.Rect(
            (0, 0), (self.settings.wheel_radius_big*2, self.settings.wheel_radius_big*2))
        self.rect.center = self.settings.wheel_center

        self.center_compartments()
        self.center_pole()
        self.gi.wheel = self

    def find_coords(self, angle, radius="medium"):
        center = self.settings.wheel_center
        if radius == "small":
            radius = self.settings.wheel_radius_small
        elif radius == "big":
            radius = self.settings.wheel_radius_big
        elif radius == "medium":
            radius = self.settings.wheel_radius
        if isinstance(radius, int):
            x, y = (radius*sin(angle * (pi/-180))
                    ), (radius*cos(angle * (pi/-180)))

            x += center[0]
            y += center[1]
            return x, y

        assert "Invalid radius"
        return center

    def create_fields(self, start_angle=0):
        numbers = pb.wheel
        angle_offset = 360 / len(numbers)
        color_list, points_list, coords_list = [], [], []

        for i, number in enumerate(numbers):
            angle = i*angle_offset + start_angle
            if angle > 360:
                angle -= 360
            self.angles_list.append(angle)
            points_list = []
            min_x, min_y = self.find_coords(angle-180, radius="small")
            max_x, max_y = self.find_coords(angle-180, radius="big")
            max_x2, max_y2 = self.find_coords(
                angle-180+angle_offset, radius="big")
            min_x2, min_y2 = self.find_coords(
                angle-180+angle_offset, radius="small")

            points_list.append((min_x, min_y))
            points_list.append((max_x, max_y))
            points_list.append((max_x2, max_y2))
            points_list.append((min_x2, min_y2))

            try:
                x1_avg = (min_x2 + max_x2) / 2  # type: ignore
                y1_avg = (min_y2 + max_y2) / 2  # type: ignore
                points_list.append((x1_avg, y1_avg))
                x2_avg = (min_x + max_x) / 2  # type: ignore
                y2_avg = (min_y + max_y) / 2  # type: ignore
                points_list.append((x2_avg, y2_avg))
            except ValueError:
                print("Invalid coordinates")
                assert "Invalid coordinates" in str(number)

            centerpoint = self.find_center(
                points_list[0], points_list[3], points_list[-2], points_list[-1])
            self.center_points_list.append(centerpoint)

            coords_list.append(points_list)
            if number in pb.noir:
                color = self.settings.color_dict["black"]
            elif number in pb.rouge:
                color = self.settings.color_dict["red"]
            else:
                color = self.settings.color_dict["light_green"]
            color_list.append(color)

        return coords_list, color_list

    def find_center(self, a, b, c, d):
        x = (a[0] + b[0] + c[0] + d[0]) / 4
        y = (a[1] + b[1] + c[1] + d[1]) / 4

        return x, y

    def prep_msg(self, msg: str, pos, angle=0.0):
        text_color = self.settings.font_color
        font_type = self.settings.font_type
        font_size = int(self.settings.font_size / 2)
        font = pygame.font.SysFont(font_type, font_size)
        msg_image = font.render(msg, True, text_color)
        self.og_text_list.append(msg_image)
        msg_image = self.rotozoom_surf(msg_image, angle)
        msg_image_rect = msg_image.get_rect()

        msg_image_rect.center = pos

        self.text_list.append([msg_image, msg_image_rect])

    def rotozoom_surf(self, surf, angle, size=1.0):
        surf = pygame.transform.rotozoom(surf, -angle, size)
        return surf

    def get_msg_pos(self, points):
        new_x = (points[-2][0] + points[-1][0] +
                 points[1][0] + points[2][0]) / 4
        new_y = (points[-2][1] + points[-1][1] +
                 points[1][1] + points[2][1]) / 4
        return [new_x, new_y]

    def spin(self):
        self.gi.current_stage = 2
        self.spinning = True
        self.start_tick = pygame.time.get_ticks()
        self.spinning_time = randint(
            self.settings.spinning_time_min, self.settings.spinning_time_max)

        self.end_tick = self.start_tick + self.spinning_time
        self.ticks_left = self.spinning_time
        x, y = pygame.mouse.get_pos()
        self.ball = Ball(self.settings, self.gi, self, (x,y))

    def update_spin(self):

        subt = 200
        speed = self.settings.base_spinning_speed * self.ticks_left / subt
        self.ticks_left = self.end_tick - pygame.time.get_ticks()
        if self.ticks_left <= 0:
            self.spinning = False
        self.rotation += speed
        if self.rotation > 360:
            self.rotation -= 360
            
        # Pole spin
        p_subt = 250
        p_speed = self.settings.base_spinning_speed * self.ticks_left / p_subt
        self.p_rotation += p_speed
        if self.p_rotation > 360:
            self.p_rotation -= 360

    def update(self):
        if self.spinning:
            self.update_spin()
            self.center_pole()

            self.coords_list.clear()
            self.center_points_list.clear()
            self.angles_list.clear()
            self.coords_list, self.color_list = self.create_fields(
                self.rotation)

            angle_offset = 360 / len(pb.wheel)
            for i, text in enumerate(zip(self.text_list, self.og_text_list)):
                angle = i*angle_offset + self.rotation + (angle_offset / 2)
                text[0][0] = self.rotozoom_surf(text[1], angle)
                pos = self.get_msg_pos(self.coords_list[i])
                text[0][1].center = pos

        if self.ball:
            self.ball.update()

    def center_compartments(self):
        outer_circle = self.settings.wheel_radius_big+39
        angle_offset = (360 / 8) / 2
        angle = 0
        rotation = 0
        og_surf = pygame.image.load("RienNeVaPlus/images/bling.png")

        while angle < 360:
            x, y = self.find_coords(angle, radius=outer_circle)
            self.inner_compartment_list.append((x, y))
            angle += angle_offset

            x, y = self.find_coords(angle, radius=outer_circle-20)
            size = 0.06
            surf = self.rotozoom_surf(og_surf, angle+rotation, size)
            rect = surf.get_rect(center=(x, y))
            self.bling_list.append((surf, rect.topleft))
            rotation += 90
            angle += angle_offset
        
        self.wood_circle = pygame.image.load("RienNeVaPlus/images/wood_circle.png")
        self.wood_circle = pygame.transform.smoothscale(self.wood_circle, (outer_circle*2, outer_circle*2))
        self.wood_circle_rect = self.wood_circle.get_rect(center=self.settings.wheel_center)
        
    def center_pole(self):
        self.pole_list.clear()
        radius = int(self.settings.wheel_radius_small / 2)
        angle_offset = 360 / 4
        i=4
        while i>0:
            # line
            x, y = self.find_coords(self.p_rotation, radius) # type: ignore       
            self.pole_list.append((x, y))
            self.p_rotation += angle_offset
            i-=1

    def blitme(self, screen):
        # Center of the roulette wheel
        center = self.settings.wheel_center
        screen.blit(self.wood_circle, self.wood_circle_rect)
        gf.draw_circle(screen, self.settings.color_dict["black"], center, self.settings.wheel_radius_small-8, 3)
        gf.draw_circle(
            screen, self.settings.color_dict["black"], center, self.settings.wheel_radius_big+40, 3)
        gf.draw_circle(
            screen, self.settings.color_dict["dark_brown"], center, self.settings.wheel_radius_big+48, 8)
        for point in self.inner_compartment_list:
            pygame.draw.line(
                screen, self.settings.color_dict["dark_brown"], center, point, 3)
        for bling, pos in self.bling_list:
            screen.blit(bling, pos)

        for points, color, text in zip(self.coords_list, self.color_list, self.text_list):
            pygame.draw.polygon(screen, color, points[:-2], 0)
            pygame.draw.polygon(
                screen, self.settings.color_dict["offwhite"], points[:-2], 3)
            screen.blit(*text)

        # Draw the golden lines in the wheel
        gf.draw_circle(
            screen, self.settings.color_dict["yellow_faint"], center, self.settings.wheel_radius, 3)
        gf.draw_circle(
            screen, self.settings.color_dict["yellow_faint"], center, self.settings.wheel_radius_big+2, 5)
        gf.draw_circle(
            screen, self.settings.color_dict["yellow_faint"], center, self.settings.wheel_radius_small+2, 10)

        if self.ball:
            self.ball.blitme(screen)
            
        # Draw the center pole
        for point in self.pole_list:
            pygame.draw.line(
                screen, self.settings.color_dict["black"], center, point, 7)
            gf.draw_circle(screen, self.settings.color_dict["black"], point, 9)
            pygame.draw.line(
                screen, self.settings.color_dict["yellow"], center, point, 5)
            gf.draw_circle(screen, self.settings.color_dict["yellow"], point, 8)
            
        gf.draw_circle(screen, self.settings.color_dict["black"], center, 15)
        gf.draw_circle(screen, self.settings.color_dict["yellow"], center, 14)
        gf.draw_circle(screen, self.settings.color_dict["yellow_dark"], center, 7, 4)

        # for point in self.center_points_list:
        #     pygame.draw.circle(screen, (0,0,0), point, 4)

        # pygame.draw.rect(screen, (0, 0, 0), self.rect, 5)
        # pygame.draw.circle(screen, (0,0,255), center, self.settings.wheel_radius_big)



class Ball():
    def __init__(self, settings, game_info, wheel: Roulette, pos=(0,0)) -> None:
        self.settings, self.gi = settings, game_info
        self.wheel = wheel
        self.radius = settings.wheel_radius_big + 20
        self.center = pos
        self.image = pygame.image.load("RienNeVaPlus/images/ball.png")
        self.image = pygame.transform.smoothscale(self.image, (17,17))
        self.rect = self.image.get_rect(center=self.center)
        self.drop = False
        self.get_angle(self.center)

    def get_angle(self, pos) -> float:
        a = self.settings.wheel_center
        b = pos
        y, x = (b[1] - a[1]), (b[0] - a[0])
        angle = atan2(y, x)
        angle = degrees(angle)
        angle += 90

        return angle

    def update_radius(self, radius):
        if not self.drop:
            if self.ticks_left > 5000:
                high = True
            else:
                high = False

            if high:
                radius += randint(-4, 4)
                if radius < self.settings.wheel_radius_big:
                    radius += 4
            else:
                if radius > self.settings.wheel_radius_big:
                    radius -= 8
                elif radius > self.settings.wheel_radius:
                    radius -= 2
                else:
                    radius += randint(-8, 8)

        return radius

    def rotate(self, angle):
        subt = 170
        self.ticks_left = self.wheel.end_tick - pygame.time.get_ticks()
        if self.ticks_left > randint(2500, 3500):
            subt = 170
        else:
            self.drop = True
            subt = 200
        speed = self.settings.base_spinning_speed * self.ticks_left / subt
        angle += speed

        return angle

    def update(self):
        if self.wheel.spinning:
            if self.drop:
                self.angle = min(self.wheel.angles_list,
                                key=lambda x: abs(x-self.angle))
                index = self.wheel.angles_list.index(self.angle)
                if self.center != self.wheel.center_points_list[index]:
                    x = (self.center[0] + self.wheel.center_points_list[index][0]) / 2
                    y = (self.center[1] + self.wheel.center_points_list[index][1]) / 2
                    if abs(x - self.center[0]) < 1:
                        x = self.wheel.center_points_list[index][0]
                    if abs(y - self.center[1]) < 1:
                        y = self.wheel.center_points_list[index][1]
                    self.center = x,y
                self.ticks_left = self.wheel.end_tick - pygame.time.get_ticks()
                if self.ticks_left <= 100:
                    self.gi.outcome = pb.wheel[index]
                    
            else:
                self.angle = self.get_angle(self.center)
                self.angle = self.rotate(self.angle)
                self.radius = self.update_radius(self.radius)
                self.center = self.wheel.find_coords(self.angle-180, self.radius)
            self.rect = self.image.get_rect(center=self.center)
        elif self.drop:
            self.ticks_left = self.wheel.end_tick - pygame.time.get_ticks()
            if self.ticks_left <= -500:
                if not self.gi.winnings_screen:
                    self.wheel.ps.create_winnings_screen()
                    self.drop = False

    def blitme(self, screen):
        screen.blit(self.image, self.rect)
        gf.draw_circle(screen, self.settings.color_dict["offwhite"], self.center, 6)
