import os
import sys

import pygame
import requests

pygame.init()

COLOR_INACTIVE = (50, 50, 50)
COLOR_ACTIVE = (255, 204, 0)
FONT = pygame.font.Font(None, 32)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.min_w = w
        self.rect = pygame.Rect(x, y, w, h)
        self.rect2 = pygame.Rect(x + 2, y + 2, w - 2, h - 3)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def txt(self):
        txt = self.text
        self.text = ''
        return txt

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode if (
                                                          event.unicode != '\r' and event.unicode != '\x1b') and len(
                        self.text) + 1 <= 35 else ''
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(self.min_w, self.txt_surface.get_width() + 10)
        self.rect.w = width
        self.rect2.w = width

    def draw(self, screen):
        self.update()
        pygame.draw.rect(screen, (150, 150, 150), self.rect2)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))


def get_pic(coords='39 52', spn='0.005 0.005'):
    picserver = 'https://static-maps.yandex.ru/1.x/'
    picparams = {
        'l': 'map',
        'll': ','.join(coords.split()),
        'spn': ','.join(spn.split())
    }
    response = requests.get(picserver, params=picparams).content
    return response


map_file = "map.png"
try:
    with open(map_file, "wb") as file:
        file.write(get_pic())
except IOError as ex:
    print("Ошибка записи временного файла:", ex)
    sys.exit(2)

spm = ['0.005 0.005', '0.01 0.01', '0.05 0.05', '0.1 0.1', '0.25 0.25', '0.5 0.5', '1 1', '2 2',
       '5 5', '10 10', '20 20', '30 30', '50 50']
k = 0
screen = pygame.display.set_mode((600, 450))
pygame.display.flip()
FPS = 40
running = True
clock = pygame.time.Clock()
img = pygame.image.load(map_file)
first_c, sec_c = 39, 52
find = InputBox(10, 400, 300, 40)
while running:
    try:
        with open(map_file, "wb") as file:
            file.write(get_pic(spn=spm[k], coords=' '.join([str(i) for i in [first_c, sec_c]])))
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    screen.blit(pygame.image.load(map_file), (0, 0))

    for event in pygame.event.get():
        find.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == 281:
                if k < len(spm) - 1:
                    k += 1
            elif event.key == 280:
                if k > 0:
                    k -= 1
            elif event.key == pygame.K_UP:
                sec_c += (float(spm[k].split()[0]) * 2)
            elif event.key == pygame.K_DOWN:
                sec_c -= (float(spm[k].split()[0]) * 2)
            elif event.key == pygame.K_RIGHT:
                first_c += (float(spm[k].split()[1]) * 2)
            elif event.key == pygame.K_LEFT:
                first_c -= (float(spm[k].split()[1]) * 2)
            if first_c >= 180:
                first_c -= 359
            elif first_c <= - 180:
                first_c += 359
            if sec_c >= 86:
                sec_c -= 171
            elif sec_c <= -86:
                sec_c += 171
    find.draw(screen)
    find.update()
    pygame.display.flip()
    clock.tick(FPS)

os.remove(map_file)
pygame.quit()
