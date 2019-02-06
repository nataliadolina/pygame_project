import pygame
import sys
import os

pygame.init()
x, y = 1200, 700
size = width, height = x, y
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
FPS = 50
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


blocks1 = [pygame.transform.scale(load_image("grass.jpg"), (25, 25)),
           pygame.transform.scale(load_image("block1.jpg"), (25, 25))]
golden_block = pygame.transform.scale(load_image("goldenblock.png"), (25, 25))
walls = pygame.sprite.Group()
st_fin = pygame.sprite.Group()


class Blocks(pygame.sprite.Sprite):
    grass, wall = blocks1
    start_finish = golden_block

    def __init__(self, blocks, n1, n2):
        super().__init__(blocks)
        self.check_pic(n1, n2)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(25 * n2, 25 * n1)
        self.i = n1
        self.j = n2

    def get_event(self, event, block_pic, n):
        if self.rect.collidepoint(event.pos):
            self.image = pygame.transform.scale(block_pic, (25, 25))
            if n == 1:
                walls.add(self)
            else:
                walls.remove(self)

    def check_pic(self, k1, k2):
        if k2 == 1 and k1 == y // 25 - 2 or k2 == x // 25 - 2 and k1 == 1:
            self.image = Blocks.start_finish
            st_fin.add(self)
        elif k1 == 0 or k2 == 0 or k1 == y // 25 - 1 or k2 == x // 25 - 1:
            self.image = Blocks.wall
            walls.add(self)
        else:
            self.image = Blocks.grass


k = 0
characters = [load_image('hero3.png', -1), load_image('hero4.png', -1), load_image('hero5.png', -1),
              load_image('hero7.png', -1), load_image('hero8.png', -1)]


class Strelka1(pygame.sprite.Sprite):
    st1 = pygame.transform.scale(load_image("error.png"), (25, 25))

    def __init__(self, group):
        super().__init__(group)
        self.image = Strelka1.st1
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(150, 75)
        self.k = 0

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.k += 1
            pic = pygame.transform.scale(characters[self.k % len(characters)], (100, 75))
            return pic


class Strelka2(Strelka1):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(25, 75)

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.k -= 1
            pic = pygame.transform.scale(characters[self.k % len(characters)], (100, 75))
            return pic


class Strelka3(Strelka1):

    def __init__(self, group):
        super().__init__(group)
        self.image = Strelka1.st1
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 75)
        self.k1 = 0

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.k1 += 1
            n = self.k1 % len(blocks1)
            pic = pygame.transform.scale(blocks1[n], (75, 75))
            return pic, n
        return None, -1


class Strelka4(Strelka3):

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(175, 75)

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.k1 -= 1
            n = self.k1 % len(blocks1)
            pic = pygame.transform.scale(blocks1[n], (75, 75))
            return pic, n
        return None, -1


class LetsGo(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('letsgo.png', -1), (50, 50))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(1125, 625)

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False


blocks = pygame.sprite.Group()
board = [[0] * width for _ in range(height)]


def create_level():
    strelka1 = pygame.sprite.Group()
    strelka2 = pygame.sprite.Group()
    strelka3 = pygame.sprite.Group()
    strelka4 = pygame.sprite.Group()
    lets_go = pygame.sprite.Group()
    player = pygame.transform.scale(characters[0], (100, 75))
    block = pygame.transform.scale(blocks1[0], (75, 75))
    for i in range(y // 25):
        for j in range(x // 25):
            board[i][j] = Blocks(blocks, i, j)
    Strelka1(strelka1)
    Strelka2(strelka2)
    Strelka3(strelka3)
    Strelka4(strelka4)
    LetsGo(lets_go)
    flag1, flag2, flag3, flag4 = False, False, False, False
    space_back = pygame.transform.scale(load_image('spacefon.jpg'), (150, 125))
    while True:
        blocks.draw(screen)
        screen.blit(space_back, (25, 25))
        screen.blit(space_back, (175, 25))
        screen.blit(player, (50, 50))
        screen.blit(block, (215, 50))
        strelka1.draw(screen)
        strelka2.draw(screen)
        strelka3.draw(screen)
        strelka4.draw(screen)
        lets_go.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                for i in strelka1:
                    if not flag2:
                        pic = i.get_event(event)
                        if pic is not None:
                            flag1 = True
                for i in strelka2:
                    if not flag1:
                        pic = i.get_event(event)
                if pic is not None:
                    player = pic
                flag1 = False
                flag2 = False
                for i in strelka3:
                    if not flag4:
                        pic, n = i.get_event(event)
                        if pic is not None:
                            flag3 = True
                for i in strelka4:
                    if not flag3:
                        pic, n = i.get_event(event)
                if pic is not None:
                    block = pic
                flag3, flag4 = False, False
                for i in blocks:
                    i.get_event(event, block, n)
                for i in lets_go:
                    if i.get_event(event):
                        StartGame(player)
        pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, group, surface):
        super().__init__(group)
        self.image = pygame.transform.scale(surface, (50, 50))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(25, 625)
        self.vx = 0
        self.vy = 0

    def get_event(self):
        pass


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


camera = Camera()


def StartGame(player_surf):
    player1 = pygame.sprite.Group()
    screen.fill((0, 0, 0))
    blocks.draw(screen)
    Player(player1, player_surf)
    camera.update(*player1)
    camera.apply(*player1)
    player1.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        pygame.display.flip()


create_level()
StartGame()
