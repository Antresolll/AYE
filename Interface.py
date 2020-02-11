import pygame
import copy
import Scene
import Persona
import os
import sys


def save_record(name, score):
    info = open("Score")
    record = info.readlines()
    f = open("Score", "w")
    record.append(str(name) + " " + str(score))
    print(record)
    f.write("\n".join(record))
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


# исправить:
# handle_event

# вызывается меню подобным образом:
# obj = Menu()
# obj.menu() - атрибутами могут выступать:
#               pause - меню паузы
#               menu - начальное меню игры
#               win - меню сохранения результата
#               death - меню смерти
#               rec - меню отображения рекордов
# больше по сути тебе не надо, но есть еще
#               rules_in_pause - правила в паузе
#               rules - правила в меню
#               lvl_pause - выбор уровня в меню паузы игры
#               lvl_menu - выбор уровня в меню
# obj.show_poison() - атрибут int - кол-во зелий в инвентаре
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# pygame.init()
# screen = pygame.display.set_mode((300, 550))
# COLOR_INACTIVE = pygame.Color('lightskyblue3')
# COLOR_ACTIVE = pygame.Color('dodgerblue2')
# FONT = pygame.font.Font(None, 32)
# ------------------Эта херня нужна для того чтобы вводить имя, обязательно инициализируй-------------------
pygame.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
running = True
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.toggle_fullscreen()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
fps = 100  # количество кадров в секунду
offset = (100, 100)
LEVEL = "1"
#############
scene = pygame.sprite.Group()
clock = pygame.time.Clock()
#############
all = pygame.sprite.Group()
board = Scene.Board(offset, "Levels/tileset_named", load_image("board.png", (255, 255, 255, 255)), "Levels/" + LEVEL,
                    "Levels/obj_1", ["1", "2"], "5", "3", "6", 64)
player = Persona.Player(offset, load_image("player.png", -1), 64, 64, 64, 64, 3, 4, 6,
                        ["stay", "move", "attack"], board, speed=8, damage=5)
set_level("1", (200, 200))


class Menu:
    def __init__(self):
        # punkts = [100, 140, u'Punkts', (250, 250, 30), (250, 30, 250)]
        self.punkts = []
        self.best = []

    def render(self, powerhost, font, num_punkts):
        for n in self.punkts:
            if num_punkts == n[5]:
                powerhost.blit(font.render(n[2], 1, n[4]), (n[0], n[1]))
            else:
                powerhost.blit(font.render(n[2], 1, n[3]), (n[0], n[1]))

    def menu(self, mm='menu'):

        if mm == 'death':
            self.punkts = [(78, 70, u'you are dead', pygame.Color('White'), pygame.Color('White'), 100),
                           (120, 140, u'retry', (250, 250, 30), (250, 30, 250), 0),
                           (130, 210, u'levels', (250, 250, 30), (250, 30, 250), 6),
                           (140, 280, u'Rules', (250, 250, 30), (250, 30, 250), 1),
                           (150, 350, u'quit', (250, 250, 30), (250, 30, 250), 2)]
        elif mm == 'menu':
            self.punkts = [(110, 140, u'Game', (250, 250, 30), (250, 30, 250), 0),
                           (120, 210, u'Rules', (250, 250, 30), (250, 30, 250), 1),
                           (130, 280, u'levels', (250, 250, 30), (250, 30, 250), 6),
                           (140, 350, u'highscores', (250, 250, 30), (250, 30, 250), 10),
                           (150, 420, u'Quit', (250, 250, 30), (250, 30, 250), 2)]
        elif mm == 'pause':
            self.punkts = [(110, 140, u'Resume', (250, 250, 30), (250, 30, 250), 0),
                           (120, 210, u'Rules', (250, 250, 30), (250, 30, 250), 1),
                           (130, 280, u'levels', (250, 250, 30), (250, 30, 250), 6),
                           (140, 350, u'Quit', (250, 250, 30), (250, 30, 250), 2)]
        elif mm == 'rules_in_pause':
            self.punkts = [(10, 10, u'keys you have to use', pygame.Color('White'), pygame.Color('White'), 100),
                           (10, 90, u'WASD            MOVE', pygame.Color('White'), pygame.Color('White'), 100),
                           (10, 160, u'T              POISON', pygame.Color('White'), pygame.Color('White'), 100),
                           (10, 230, u'ESC            PAUSE', pygame.Color('White'), pygame.Color('White'), 100),
                           (10, 300, u'SPACE           HIT', pygame.Color('White'), pygame.Color('White'), 100),
                           (60, 450, u'Back to Game', (250, 250, 30), (250, 30, 250), 4)]
        elif mm == 'rules':
            self.punkts = [(10, 10, u'keys you have to use', pygame.Color('White'), pygame.Color('White'), 100),
                           (10, 90, u'WASD          MOVE', pygame.Color('White'), pygame.Color('White'), 100),
                           (10, 160, u'T             POISON', pygame.Color('White'), pygame.Color('White'), 100),
                           (10, 230, u'ESC           PAUSE', pygame.Color('White'), pygame.Color('White'), 100),
                           (10, 300, u'SPACE          HIT', pygame.Color('White'), pygame.Color('White'), 100),
                           (35, 450, u'Back to Main menu', (250, 250, 30), (250, 30, 250), 5)]
        elif mm == 'lvl_pause':
            self.punkts = [(120, 140, u'lvl 1', (250, 250, 30), (250, 30, 250), 7),
                           (130, 210, u'lvl 2', (250, 250, 30), (250, 30, 250), 8),
                           (140, 280, u'back', (250, 250, 30), (250, 30, 250), 4)]
        elif mm == 'lvl_menu':
            self.punkts = [(120, 140, u'lvl 1', (250, 250, 30), (250, 30, 250), 7),
                           (130, 210, u'lvl 2', (250, 250, 30), (250, 30, 250), 8),
                           (140, 280, u'back', (250, 250, 30), (250, 30, 250), 5)]
        elif mm == 'win':
            self.punkts = [(110, 140, u'YOU WIN111', pygame.Color('White'), pygame.Color('White'), 100),
                           (70, 210, u'Save my result', (250, 250, 30), (250, 30, 250), 9),
                           (140, 280, u'game', (250, 250, 30), (250, 30, 250), 0),
                           (140, 350, u'back', (250, 250, 30), (250, 30, 250), 5)]
        elif mm == 'rec':
            self.punkts = [(10, 10, u'highscores', pygame.Color('White'), pygame.Color('White'), 100),
                           (
                               10, 90, self.get_best(get_record())[0], pygame.Color('White'),
                               pygame.Color('White'), 100),
                           (10, 160, self.get_best(get_record())[1], pygame.Color('White'), pygame.Color('White'),
                            100),
                           (10, 230, self.get_best(get_record())[2], pygame.Color('White'), pygame.Color('White'),
                            100),
                           (35, 450, u'Back to Main menu', (250, 250, 30), (250, 30, 250), 5)]
        # 'Calcio-Demo.otf'
        done = True
        font_menu = pygame.font.Font('Calcio-Demo.otf', 50)
        punkt = 0
        while done:
            screen.fill((0, 100, 200))

            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if i[0] < mp[0] < i[0] + 155 and i[1] < mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)

            for n in pygame.event.get():
                if n.type == pygame.QUIT:
                    sys.exit()
                if n.type == pygame.KEYDOWN:
                    if n.key == pygame.K_ESCAPE:
                        done = False
                    if n.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if n.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if n.type == pygame.MOUSEBUTTONDOWN and n.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1 and mm == 'pause':
                        self.menu('rules_in_pause')
                    elif punkt == 1 and mm == 'menu':
                        self.menu('rules')
                    elif punkt == 2:
                        sys.exit()
                    elif punkt == 4:
                        self.menu('pause')
                    elif punkt == 5:
                        self.menu('menu')
                    elif punkt == 6 and mm == 'pause':
                        self.menu('lvl_pause')
                    elif punkt == 6 and mm == 'menu':
                        self.menu('lvl_menu')
                    elif punkt == 7:
                        set_level("1", (200, 200))
                    elif punkt == 8:
                        pass
                    elif punkt == 9:
                        ass()
                    elif punkt == 10:
                        # self.best = self.get_best()
                        self.menu('rec')
            screen.blit(screen, (0, 0))
            pygame.display.flip()

    def get_best(self, lst):
        lst1 = []
        for n in range(len(lst)):
            lst1.append(int(lst[n].split()[1]))
        lst1.sort()
        lst1.reverse()
        lst2 = []
        for n in range(3):
            for y in range(len(lst)):
                if str(lst1[n]) in lst[y]:
                    lst2.append(lst[y])
        return lst2

    def show_poison(self, num):
        poition_surf = pygame.image.load('poition3.png')
        poition_surf.set_colorkey((255, 255, 255))
        screen.blit(poition_surf, (0, 0))
        pygame.font.Font('Calcio-Demo.otf', 50)
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(str(num), 0, (255, 255, 255))
        screen.blit(text1, (45, 0))
    #
    # def wr_in_db(self, name, score):
    #     self.con = sqlite3.connect("REC_BAZA.db")
    #     cur = self.con.cursor()
    #     name, okBtnPressed = QInputDialog.getText(self, "SONG NAME", "Input song name")
    #     if okBtnPressed:
    #         print(song)
    #         print(name)
    #         if len(name) > 0:
    #             cur.execute("insert into RECORD_BASE(NOTE_REC, SONG_NAME) values(?, ?)", (str(song), str(name)))
    #         else:
    #             self.console.setText('  song hasn`t been writed into database' + str(name))


# эта херня инициализируется для вызова окна ввода имени


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    save_record(self.text, player.hp + player.inventory * 40)  # Вот тут сделаешь нормальный вызов
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def ass():
    clock = pygame.time.Clock()
    input_box1 = InputBox(55, 100, 140, 32)
    # input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1]
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)


#############
obj = Menu()
obj.menu()
pygame.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
running = True
size = width, height
screen = pygame.display.set_mode(size)
screen.fill((255, 213, 128))

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            obj.menu("pause")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            if player.inventory > 0:
                player.inventory -= 1
                player.hp += 20
    if player.hp <= 0:
        obj.menu("death")
    screen.fill((0, 0, 0))
    board.draw(screen)
    all.draw(screen)
    all.update(pygame.key.get_pressed())
    draw_shield_bar(screen, 125, 25, player.hp / player.mx_hp)
    clock.tick(fps)
    pygame.display.flip()
    obj.show_poison(player.inventory)
    if player.win:
        obj.menu("win")
pygame.quit()

#
# fk = Menu()
# fk.menu('pause')
# fk.show_poison(2)
