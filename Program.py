import pygame
import copy


class Board:
    def __init__(self, width, height, cell=50):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.cell_size = cell

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 [(i * self.cell_size, j * self.cell_size), (self.cell_size, self.cell_size)], 1)


class Persona:
    def __init__(self, inventory=[], speed=1, damage=1, hp=10, mp=10, st=10, armor=0, tileset=None):
        self.inventory = inventory
        self.speed = speed
        self.hp = hp
        self.mp = mp
        self.st = st
        self.damage = damage
        self.armor = armor

    def move(self):
        pass

    def attack(self):
        pass


class Player(Persona):
    pass


class Item:
    def __init__(self, dur=10, damage=1, armor=0, mp=0, st=0, missale=0, active=0, activation=None, tile=None):
        self.dur = dur
        self.damage = damage
        self.armor = armor
        self.mp = mp
        self.st = st
        self.missale = missale
        self.active = active
        self.activation = activation

    def activate(self):
        self.activation()


fps = 50  # ÐºÐ¾Ð»Ð¸Ñ‡ÐµÑÑ‚Ð²Ð¾ ÐºÐ°Ð´Ñ€Ð¾Ð² Ð² ÑÐµÐºÑƒÐ½Ð´Ñƒ
cell = 50
clock = pygame.time.Clock()
pygame.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
X, Y = width // cell, height // cell
board = Board(X, Y, cell)
running = True
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.toggle_fullscreen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False
    screen.fill((0, 0, 0))
    board.render(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
#govnoy vonyaet v0.1