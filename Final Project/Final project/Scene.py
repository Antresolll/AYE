import pygame
from Persona import Enemy


def sound(str):
    if str == "background":
        pygame.mixer.music.load(str + '.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)
    else:
        # sound = pygame.mixer.Sound(str + '.wav')
        # sound.play()
        pass


class Board:
    def __init__(self, offset, tiles, tileset, map, map_objects, block, enemy, chest, ext, cell=50):
        off_x, off_y = offset
        f = open(tiles)
        tiles = list(f.read().split())
        f.close()
        self.tiles = {}
        self.block = pygame.sprite.Group()
        for t in range(len(tiles)):
            self.tiles[tiles[t]] = tileset.subsurface(pygame.Rect((t * (cell + 2), 0), (cell, cell)))
        f = open(map)
        self.map = []
        self.enemyes = []
        for y in f.readlines():
            s = []
            ts = list(y.split())
            for x in range(len(ts)):
                temp = [self.tiles[ts[x]], 0]
                if ts[x] in block:
                    temp[1] = 1
                s.append(temp)
            self.map.append(s)
        f.close()
        f = open(map_objects)
        self.enemyes = []
        self.obj = []
        file = f.readlines()
        for y in range(len(list(file))):
            ts = list(file[y].split())
            for x in range(len(ts)):
                if ts[x] == enemy:
                    self.enemyes.append([x * cell, y * cell])
                if ts[x] == chest:
                    self.obj.append([x * cell, y * cell, 0])
                if ts[x] == ext:
                    self.obj.append([x * cell, y * cell, 1])
        f.close()
        self.cell_size = cell
        self.board = pygame.sprite.Group()
        self.render(off_x, off_y)

    def render(self, off_x, off_y):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                tile = self.map[y][x][0]
                sprite = pygame.sprite.Sprite(self.board)
                sprite.image = tile
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = x * self.cell_size + off_x
                sprite.rect.y = y * self.cell_size + off_y
                sprite.mask = pygame.mask.from_surface(sprite.image, 255)
                if self.map[y][x][1]:
                    self.block.add(sprite)

    def draw(self, surf):
        self.board.draw(surf)


class Chest(pygame.sprite.Sprite):
    def __init__(self, offset, group, image, player, x, y, inventory=0):
        super().__init__(group)
        self.inventory = inventory
        self.player = player
        self.image = image
        self.rect = self.image.get_rect()
        off_x, off_y = offset
        self.rect.x = x + off_x
        self.rect.y = y + off_y

    def update(self, *args):
        if pygame.sprite.collide_mask(self, self.player):
            sound("bottle")
            self.player.inventory += self.inventory
            self.inventory = 0


class Exit(pygame.sprite.Sprite):
    def __init__(self, offset, group, image, player, x, y):
        super().__init__(group)
        self.image = image
        self.player = player
        self.rect = self.image.get_rect()
        off_x, off_y = offset
        self.rect.x = x + off_x
        self.rect.y = y + off_y

    def update(self, *args):
        if pygame.sprite.collide_mask(self, self.player):
            self.player.win = 1
