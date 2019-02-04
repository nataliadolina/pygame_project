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


class Blocks(pygame.sprite.Sprite):
    grass = pygame.transform.scale(load_image("grass.jpg"), (25, 25))
    wall = pygame.transform.scale(load_image("block1.jpg"), (25, 25))

    def __init__(self, blocks, n1, n2):
        super().__init__(blocks)
        self.check_pic(n1, n2)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(25 * n2, 25 * n1)

    def move_rect(self, x, y):
        self.rect = self.rect.move(x, y)

    def check_pic(self, k1, k2):
        if k1 == 0 or k2 == 0 or k1 == y // 25 - 1 or k2 == x // 25 - 1:
            self.image = Blocks.wall
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

    def get_event(self, event):
        global k
        if self.rect.collidepoint(event.pos):
            k += 1
            pic = pygame.transform.scale(characters[k % len(characters)], (100, 75))
            return pic


class Strelka2(pygame.sprite.Sprite):
    st2 = pygame.transform.scale(load_image("error.png"), (25, 25))

    def __init__(self, group):
        super().__init__(group)
        self.image = Strelka2.st2
        self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(25, 75)

    def get_event(self, event):
        global k
        if self.rect.collidepoint(event.pos):
            k -= 1
            pic = pygame.transform.scale(characters[k % len(characters)], (100, 75))
            return pic


def create_level():
    blocks = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    strelka1 = pygame.sprite.Group()
    strelka2 = pygame.sprite.Group()
    player = pygame.transform.scale(characters[0], (100, 75))
    for i in range(y // 25):
        for j in range(x // 25):
            Blocks(blocks, i, j)
    Strelka1(strelka1)
    Strelka2(strelka2)
    flag1 = False
    flag2 = False
    space_back = pygame.transform.scale(load_image('spacefon.jpg'), (150, 125))
    while True:
        blocks.draw(screen)
        screen.blit(space_back, (25, 25))
        screen.blit(player, (50, 50))
        strelka1.draw(screen)
        strelka2.draw(screen)
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
                            flag2 = True
                if pic is not None:
                    player = pic
                flag1 = False
                flag2 = False
        pygame.display.flip()


create_level()
