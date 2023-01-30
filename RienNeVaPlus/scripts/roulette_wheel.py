from math import atan2, cos, degrees, pi, sin
from random import randint

import possible_bets as pb
import pygame


class Roulette():
    def __init__(self, settings, game_info) -> None:
        self.settings, self.gi = settings, game_info
        self.text_list = []
        self.og_text_list = []
        self.coord_list = []
        self.center_points_list = []
        self.angles_list = []
        self.rotation = 0
        self.spinning = False
        self.ball = None

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

            centerpoint = self.find_center(points_list[0], points_list[3], points_list[-2], points_list[-1])
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
        font_size = int(self.settings.font_size / 2.5)
        font = pygame.font.SysFont(font_type, font_size)
        msg_image = font.render(msg, True, text_color)
        self.og_text_list.append(msg_image)
        msg_image = self.rotate_surf(msg_image, angle)
        msg_image_rect = msg_image.get_rect()

        msg_image_rect.center = pos

        self.text_list.append([msg_image, msg_image_rect])

    def rotate_surf(self, surf, angle):
        surf = pygame.transform.rotozoom(surf, -angle, 1)
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

        self.ball = Ball(self.settings, self.gi, self)

    def update_spin(self):

        subt = 200
        speed = self.settings.base_spinning_speed * self.ticks_left / subt
        self.ticks_left = self.end_tick - pygame.time.get_ticks()
        if self.ticks_left <= 0:
            self.spinning = False
            self.gi.current_stage = 1
        self.rotation += speed
        if self.rotation > 360:
            self.rotation -= 360

    def update(self):
        if self.spinning:
            self.update_spin()

            self.coords_list.clear()
            self.center_points_list.clear()
            self.angles_list.clear()
            self.coords_list, self.color_list = self.create_fields(
                self.rotation)

            angle_offset = 360 / len(pb.wheel)
            for i, text in enumerate(zip(self.text_list, self.og_text_list)):
                angle = i*angle_offset + self.rotation + (angle_offset / 2)
                text[0][0] = self.rotate_surf(text[1], angle)
                pos = self.get_msg_pos(self.coords_list[i])
                text[0][1].center = pos

            if self.ball:
                self.ball.update()

    def blitme(self, screen):
        for points, color, text in zip(self.coords_list, self.color_list, self.text_list):
            pygame.draw.polygon(screen, color, points[:-2], 0)
            pygame.draw.polygon(
                screen, self.settings.color_dict["offwhite"], points[:-2], 3)
            pygame.draw.line(
                screen, self.settings.color_dict["offwhite"], points[-2], points[-1], 2)
            screen.blit(*text)

        if self.ball:
            self.ball.blitme(screen)
            
        # for point in self.center_points_list:
        #     pygame.draw.circle(screen, (0,0,0), point, 4)

        # pygame.draw.rect(screen, (0, 0, 0), self.rect, 5)
        # pygame.draw.circle(screen, (0,0,255), self.settings.wheel_center, self.settings.wheel_radius_big)


class Ball():
    def __init__(self, settings, game_info, wheel: Roulette) -> None:
        self.settings, self.gi = settings, game_info
        self.wheel = wheel
        self.radius = settings.wheel_radius_big + 20
        self.center = 300, 100
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
                high=True
            else:
                high=False
                
            if high:
                radius += randint(-4, 4)
                if radius < self.settings.wheel_radius_big:
                    radius = self.settings.wheel_radius_big
            else:
                if radius > self.settings.wheel_radius_big:
                    radius = self.settings.wheel_radius_big
                radius += randint(-8, 8)
        
        return radius

    def rotate(self, angle):
        subt = 190
        self.ticks_left = self.wheel.end_tick - pygame.time.get_ticks()
        if self.ticks_left > 3000:
            subt = 180
        else:
            self.drop = True
            subt = 200
        speed = self.settings.base_spinning_speed * self.ticks_left / subt
        angle += speed

        return angle

    def update(self):

        if self.drop:
            self.angle = min(self.wheel.angles_list,
                             key=lambda x: abs(x-self.angle))
            index = self.wheel.angles_list.index(self.angle)
            self.center = self.wheel.center_points_list[index]
            self.ticks_left = self.wheel.end_tick - pygame.time.get_ticks()
            if self.ticks_left <= 0:
                self.gi.outcome = pb.wheel[index]
                print(self.gi.outcome)
        else:
            self.angle = self.get_angle(self.center)
            self.angle = self.rotate(self.angle)
            self.radius = self.update_radius(self.radius)
            self.center = self.wheel.find_coords(self.angle-180, self.radius)

    def blitme(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.center, 7)
