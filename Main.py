import pygame
import copy
import Scene
import Persona
import os
import Interface


def save_record(name, score):
    f = open("Score", "w")
    f.write(name + " " + score)
    f.close()


def get_record():
    f = open("Score")
    return f.readlines()


def load_image(name, colorkey=None):
    fullname = os.path.join("images", name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image.set_colorkey(colorkey)
    return image


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    l = 200
    h = 50
    fill = pct * l
    outline_rect = pygame.Rect(x, y, l, h)
    fill_rect = pygame.Rect(x, y, fill, h)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect)
    pygame.draw.rect(surf, (0, 128, 0), fill_rect)


def set_level(lvl, plr):
    global board, LEVEL, all
    dmg = int(lvl)
    all = pygame.sprite.Group()
    board = Scene.Board(offset, "Levels/tileset_named", load_image("board.png", (255, 255, 255, 255)), "Levels/" + lvl,
                        "Levels/obj_" + lvl, ["1", "2"], "5", "3", "6", 64)
    for coord in board.enemyes:
        x, y = coord
        vraszina = Persona.Enemy(player, 200, offset, load_image("enemy.png", (0, 0, 0, 255)), x, y, 64, 64, 3, 4, 6,
                                 ["move", "attack", "stay"], board, damage=dmg)
        all.add(vraszina)
    for coord in board.obj:
        x, y, t = coord
        if t:
            Scene.Exit(offset, all, load_image("ext.png"), player, x, y)
        else:
            Scene.Chest(offset, all, load_image("cht.png", (255, 255, 255, 255)), player, x, y, 2)
    x, y = plr
    player.set_coords(x, y)
    all.add(player)
    LEVEL = lvl
    player.board = board
    player.hp = player.mx_hp


#############
fps = 20  # количество кадров в секунду
offset = (100, 100)
LEVEL = "1"
#############
scene = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
running = True
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.toggle_fullscreen()
#############
all = pygame.sprite.Group()
obj = Interface.Menu()
obj.menu()
board = Scene.Board(offset, "Levels/tileset_named", load_image("board.png", (255, 255, 255, 255)), "Levels/" + LEVEL,
                    "Levels/obj_1", ["1", "2"], "5", "3", "6", 64)
player = Persona.Player(offset, load_image("player.png", -1), 64, 64, 64, 64, 3, 4, 6,
                        ["stay", "move", "attack"], board, speed=8, damage=5)
set_level("1", (200, 200))
#############
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            obj.menu("pause")
    if player.hp <= 0:
        obj.menu("death")
    screen.fill((0, 0, 0))
    board.draw(screen)
    all.draw(screen)
    all.update(pygame.key.get_pressed())
    draw_shield_bar(screen, 25, 25, player.hp / player.mx_hp)
    clock.tick(fps)
    pygame.display.flip()
    obj.show_poison(player.inventory)
pygame.quit()
