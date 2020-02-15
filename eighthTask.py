import os
import sys

import pygame
import requests

pygame.init()

COLOR_INACTIVE = (50, 50, 50)
COLOR_ACTIVE = (255, 204, 0)
FONT = pygame.font.Font(None, 32)
SFONT = pygame.font.Font(None, 15)
buttonBar = pygame.image.load('data/ButtonBar.png')


def after_get():
    try:
        with open(map_file, "wb") as file:
            try:
                file.write(get_pic(spn=spm[k], l=l[Buttons.index(True)],
                                   coords=' '.join([str(i) for i in [first_c, sec_c]]), pt=pt))
            except ValueError:
                file.write(get_pic(spn=spm[k],
                                   coords=' '.join([str(i) for i in [first_c, sec_c]])))
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)


class InputBox:
    def __init__(self, x, y, w, h, text='', search_flag=True, crossy_flag=True):
        self.text_li = []
        self.min_w = w
        self.search_flag = search_flag
        self.crossy_flag = crossy_flag
        self.rect = pygame.Rect(x, y, w, h)
        self.rect2 = pygame.Rect(x + 2, y + 2, w - 2, h - 3)
        self.searchImg = pygame.image.load('data/searchButton.png')
        self.hoveredsearchImg = pygame.image.load('data/hoveredsearchButton.png')
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.deleteButton = pygame.image.load('data/deleteButton.png')
        self.hoveredDeleteButton = pygame.image.load('data/hoverdeleteButton.png')
        self.hovercross = False

    def txt(self):
        txt = self.text

        self.text = ''
        return txt

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if self.text == 'error':
                    self.text = ''
                    self.txt_surface = FONT.render(self.text, True, self.color)
                    self.draw(screen)
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
                        self.text) + 1 <= 30 else ''
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(self.min_w, self.txt_surface.get_width() + 10)
        self.rect.w = width
        self.rect2.w = width - 2

    def draw(self, screen):
        self.update()
        pygame.draw.rect(screen, (150, 150, 150), self.rect2)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))
        if self.hover_on_search(eventy_pos):
            screen.blit(self.hoveredsearchImg, (self.rect.x + self.rect.w + 5, self.rect.y - 4))
        else:
            screen.blit(self.searchImg, (self.rect.x + self.rect.w + 5, self.rect.y - 4))
        if self.hovercross:
            screen.blit(pygame.transform.scale(self.hoveredDeleteButton, (45, 45)),
                        (self.rect.x + self.rect.w + 55, self.rect.y - 4))
        else:
            screen.blit(pygame.transform.scale(self.deleteButton, (45, 45)),
                        (self.rect.x + self.rect.w + 55, self.rect.y - 4))

    def hover_on_search(self, m_pos):
        if self.searchImg.get_rect(x=self.rect.x + self.rect.w + 5, y=self.rect.y).collidepoint(
                m_pos):
            return True

    def hover_on_square(self, m_pos):
        if self.searchImg.get_rect(x=self.rect.x + self.rect.w + 55,
                                   y=self.rect.y - 4).collidepoint(
            m_pos):
            return True


class InputBoxforadress(InputBox):
    def __init__(self, x, y, w, h, text='', search_flag=True, crossy_flag=True):
        super().__init__(x, y, w, h, text, search_flag, crossy_flag)

    def update(self):
        print(self.text_li)
        if self.text_li != []:
            width = max(self.min_w, max([i[0].get_width() for i in self.text_li]) + 10)
        else:
            width = self.min_w
        self.rect.w = width
        self.rect2.w = width - 2

    def draw(self, screen):
        self.update()
        pygame.draw.rect(screen, (150, 150, 150), self.rect2)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if self.text_li != []:
            for i in range(len(self.text_li)):
                screen.blit(self.text_li[i][0], self.text_li[i][1])
        if self.search_flag:
            if self.hover_on_search(eventy_pos):
                screen.blit(self.hoveredsearchImg, (self.rect.x + self.rect.w + 5, self.rect.y - 4))
            else:
                screen.blit(self.searchImg, (self.rect.x + self.rect.w + 5, self.rect.y - 4))
        if self.crossy_flag:
            if self.hovercross:
                screen.blit(pygame.transform.scale(self.hoveredDeleteButton, (45, 45)),
                            (self.rect.x + self.rect.w + 55, self.rect.y - 4))
            else:
                screen.blit(pygame.transform.scale(self.deleteButton, (45, 45)),
                            (self.rect.x + self.rect.w + 55, self.rect.y - 4))


def get_pic(coords='39 52', spn='0.005 0.005', l='map', pt=''):
    picserver = 'https://static-maps.yandex.ru/1.x/'
    picparams = {
        'l': l,
        'll': ','.join(coords.split()),
        'spn': ','.join(spn.split()),
    }
    if pt != '':
        picparams['pt'] = pt
    response = requests.get(picserver, params=picparams).content
    return response


def draw_buttons():
    screen.blit(buttonBar, (495, 18))
    for i in range(3):
        if Buttons[i]:
            screen.blit(clickedButton, (500 + 25 * i, 20))
        else:
            screen.blit(normalButton, (500 + 25 * i, 20))


map_file = "map.png"

try:
    with open(map_file, "wb") as file:
        file.write(get_pic())
except IOError as ex:
    print("Ошибка записи временного файла:", ex)
    sys.exit(2)

spm = ['0.001 0.001', '0.003 0.003', '0.005 0.005', '0.01 0.01', '0.05 0.05', '0.1 0.1',
       '0.25 0.25', '0.5 0.5', '1 1', '2 2',
       '5 5', '10 10', '20 20', '30 30', '50 50']
k = 0
screen = pygame.display.set_mode((600, 450))
pygame.display.flip()
FPS = 30
running = True
clock = pygame.time.Clock()
img = pygame.image.load(map_file)
first_c, sec_c = 39, 52
find = InputBox(10, 400, 300, 40)
adress = InputBoxforadress(10, 350, 300, 35, search_flag=False, crossy_flag=False)
adress.txt_surface = SFONT.render('no adress', True, adress.color)
Buttons = [True, False, False]
normalButton = pygame.transform.scale(pygame.image.load('data/normalButton.png'), (25, 25))
clickedButton = pygame.transform.scale(pygame.image.load('data/clickedButton.png'), (25, 25))

l = ['map', 'sat', 'sat,skl']
eventy_pos = []
pt = ''
while running:

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
                    after_get()
            elif event.key == 280:
                if k > 0:
                    k -= 1
                    after_get()
            elif event.key == pygame.K_UP:
                sec_c += (float(spm[k].split()[1]))
                after_get()
            elif event.key == pygame.K_DOWN:
                sec_c -= (float(spm[k].split()[1]))
                after_get()
            elif event.key == pygame.K_RIGHT:
                first_c += (float(spm[k].split()[0]))
                after_get()
            elif event.key == pygame.K_LEFT:
                first_c -= (float(spm[k].split()[0]))
                after_get()
            if first_c >= 180:
                first_c -= 359
                after_get()
            elif first_c <= - 180:
                first_c += 359
                after_get()
            if sec_c >= 86:
                sec_c -= 171
                after_get()
            elif sec_c <= -86:
                after_get()
                sec_c += 171

        if event.type == pygame.MOUSEBUTTONDOWN:
            if clickedButton.get_rect(x=500, y=20).collidepoint(event.pos):
                Buttons = [True, False, False]
            elif clickedButton.get_rect(x=525, y=20).collidepoint(event.pos):
                Buttons = [False, True, False]
            elif clickedButton.get_rect(x=550, y=20).collidepoint(event.pos):
                Buttons = [False, False, True]
            elif find.hover_on_search(event.pos):
                if find.text == 'error':
                    find.text = ''
                    find.txt_surface = FONT.render(find.text, True, find.color)
                    continue
                server = 'https://geocode-maps.yandex.ru/1.x'
                params = {
                    'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                    'geocode': find.text,
                    'format': 'json'
                }
                response = requests.get(server, params=params)

                try:
                    first_c, sec_c = response.json()["response"]["GeoObjectCollectio"
                                                                 "n"]["featureMember"][0][
                        "GeoObject"][
                        'Point']['po'
                                 's'].split()
                    first_c, sec_c = float(first_c), float(sec_c)
                    pt = ','.join([str(i) for i in [first_c, sec_c]])
                    txt_adr = response.json()["response"]["GeoObjectCollection"]["featureMemb"
                                                                                 "er"][0][
                        "GeoObject"]['metaDa'
                                     'taProperty'][
                        'GeocoderMetaData']['text']

                    n = len(txt_adr) // 80 + 1 if len(txt_adr) % 80 != 0 else len(txt_adr) // 80
                    print(n)
                    for i in range(n):
                        line = txt_adr[80 * i: 80 * (i + 1)]
                        sur = SFONT.render(line, True, adress.color)
                        adress.text_li.append(
                            [sur, (adress.rect.x + 5, adress.rect.y + 2 + 7 * i)])

                except Exception:
                    find.text = 'error'
                    find.txt_surface = FONT.render(find.text, True, (220, 20, 32))
            elif find.hover_on_square(event.pos):
                find.text = ''
                pt = ''
                adress.text_li = []
                find.txt_surface = FONT.render(find.text, True, find.color)

            after_get()
        if event.type == pygame.MOUSEMOTION:
            eventy_pos = list(event.pos)

    if find.hover_on_square(eventy_pos):
        find.hovercross = True

    adress.draw(screen)
    find.draw(screen)
    draw_buttons()

    find.update()
    find.hovercross = False
    pygame.display.flip()
    clock.tick(FPS)

os.remove(map_file)
pygame.quit()
