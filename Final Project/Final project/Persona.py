import pygame
from math import sqrt


def sound(str):
    if str == "background":
        pygame.mixer.music.load(str + '.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)
    else:
        # sound = pygame.mixer.Sound(str + '.wav')
        # sound.play()
        pass


class Persona(pygame.sprite.Sprite):
    def __init__(self, offset, sheet, x, y, size_x, size_y, st_count, directions, frame_count, states, board,
                 speed=5, damage=1, hp=100):
        super().__init__()
        self.frames = {}
        self.win = 0
        self.direction = 0
        self.cur_frame = 0
        self.st_count = st_count
        self.states = states
        self.directions = directions
        self.cut_sheet(sheet, size_x, size_y)
        self.state = "stay"
        self.image = self.frames[self.state][self.direction][self.cur_frame]
        self.fr_count = frame_count
        self.inventory = 0
        self.speed = [0, 0]
        self.sp = speed
        self.hp = hp
        self.mx_hp = hp
        self.damage = damage
        self.armor = 0
        off_x, off_y = offset
        self.rect.x = x + off_x
        self.rect.y = y + off_y
        self.board = board
        self.surf = sheet

    def cut_sheet(self, sheet, size_x, size_y):
        self.rect = pygame.Rect(0, 0, size_x, size_y)
        for st in range(len(self.states)):
            self.frames[self.states[st]] = []
            for dr in range(self.directions):
                self.frames[self.states[st]].append([])
                for fr in range(sheet.get_width() // size_x):
                    frame_location = (self.rect.w * fr, self.rect.h * (st * self.directions + dr))
                    self.frames[self.states[st]][dr].append(
                        sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def set_direction(self, directions):
        self.direction = directions[-1]
        self.image = self.frames[self.state][self.direction][self.cur_frame]
        if self.state == "move":
            self.set_speed(directions)
        else:
            self.speed = [0, 0]

    def set_state(self, state):
        self.state = state
        if state == "move":
            self.set_speed([self.direction])
        else:
            self.speed = [0, 0]

    def set_speed(self, directions):
        self.speed = [0, 0]
        for direction in directions:
            if direction == 0:
                self.speed[1] -= 1
            elif direction == 1:
                self.speed[0] -= 1
            elif direction == 2:
                self.speed[1] += 1
            else:
                self.speed[0] += 1

    def damaged(self, x):
        x -= self.armor
        if x < 0:
            x = 0
        self.hp -= x

    def block(self):
        self.speed = [0, 0]

    def update(self, events):
        self.cur_frame = (self.cur_frame + 1) % self.fr_count
        if self.state == "stay":
            self.cur_frame = 0
        self.image = self.frames[self.state][self.direction][self.cur_frame]
        if pygame.sprite.spritecollideany(self, self.board.block, pygame.sprite.collide_mask):
            self.rect = self.rect.move(10, 0)
        if pygame.sprite.spritecollideany(self, self.board.block, pygame.sprite.collide_mask):
            self.rect = self.rect.move(-20, 0)
        if pygame.sprite.spritecollideany(self, self.board.block, pygame.sprite.collide_mask):
            self.rect = self.rect.move(10, 10)
        if pygame.sprite.spritecollideany(self, self.board.block, pygame.sprite.collide_mask):
            self.rect = self.rect.move(0, -20)
        move_x, move_y = self.speed
        self.rect = self.rect.move(move_x * self.sp, move_y * self.sp)
        if pygame.sprite.spritecollideany(self, self.board.block, pygame.sprite.collide_mask):
            self.rect = self.rect.move(-move_x * self.sp, -move_y * self.sp)


class Player(Persona):
    def update(self, events):
        directions = []
        if events[pygame.K_w]:
            directions.append(0)
        if events[pygame.K_s]:
            directions.append(2)
        if events[pygame.K_a]:
            directions.append(1)
        if events[pygame.K_d]:
            directions.append(3)
        if events[pygame.K_SPACE]:
            sound("sword")
            if self.state != "attack":
                self.cur_frame = 0
            self.state = "attack"
            if directions:
                self.set_direction(directions)
        elif directions:
            if self.state != "move":
                self.cur_frame = 0
            self.state = "move"
            self.set_direction(directions)
        else:
            self.speed = [0, 0]
            self.state = "stay"
        super().update(events)

    def set_coords(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Enemy(Persona):
    def __init__(self, player, agro, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player
        self.agro = agro
        self.trigger = False

    def update(self, events):
        x, y = self.rect.x, self.rect.y
        p_x, p_y = self.player.rect.x, self.player.rect.y
        distant = sqrt((abs(x - p_x) ** 2) + (abs(y - p_y) ** 2))
        if distant <= self.agro:
            self.trigger = True
        if self.trigger:
            # sound("monster_walk")
            self.set_state("move")
            q_x, q_y = p_x - x, p_y - y
            if q_x > 0:
                if q_y > 0:
                    potential_dirs = [2, 3]
                else:
                    potential_dirs = [0, 3]
            else:
                if q_y > 0:
                    potential_dirs = [2, 1]
                else:
                    potential_dirs = [0, 1]
            q_x, q_y = abs(q_x), abs(q_y)
            if q_x == 0:
                q_x = 1
            if q_y == 0:
                q_y = 1
            if (q_x / q_y) > 2:
                directions = [potential_dirs[1]]
            elif (q_y / q_x) > 2:
                directions = [potential_dirs[0]]
            else:
                directions = potential_dirs
            if directions:
                self.set_direction(directions)
        if pygame.sprite.collide_mask(self, self.player):
            sound("monster")
            self.set_state("attack")
            if self.player.state == "attack":
                self.damaged(self.player.damage)
            self.player.damaged(self.damage)
        super().update(events)
        if self.hp == 0:
            self.kill()
