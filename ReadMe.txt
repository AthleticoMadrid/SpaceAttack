Создание игры по мотивам Space Invaders на Python(библиотека Pygame)

---------------------------------------------------------------------------------------
Создание виртуального окружения:
python -m venv env
env\Scripts\activate

----------------------------------------------------------------------------------------
Установка Pygame:
pip install pygame

----------------------------------------------------------------------------------------
Создание файла для игры:
space_game.py

----------------------------------------------------------------------------------------
Создание пустого окна для игры в space_game.py:

import pygame   #библиотека для создания игр
import contols
from gun import Gun     #подключаем класс пушки
from pygame.sprite import Group     #для реализации пуль
from scores import Scores           #класс со счётом игры
from stats import Stats             #модуль со статистикой

#функция запуска, инициализации и создания экрана
def run():
    pygame.init()                                           #метод инициализации игры
    screen = pygame.display.set_mode((600, 700))           #создание графической области(размер окна - 600*700)
    pygame.display.set_caption("Космические защитники")     #заголовок игры(caption - заголовок)
    bg_color = (0, 0, 0)                                    #фоновый цвет окна
    gun = Gun(screen)                                       #создаём класс пушки и отрисовываем его
    bullets = Group()                                       #создание контейнера для пуль
    inos = Group()                                           #создание группы пришельцев
    controls.create_army(screen, inos)                      #отрисовка армии пришельцев
    stats = Stats()                                   #сохранение статистики текущего хода игры
    sc = Scores(screen, stats)                              #отрисовка статистики

    #главный цикл игры с обработкой событий пользователя:
    while True:
        contols.events(screen, gun, bullets)             #обработка событий (экран, передвижение пушки и пуль)
        if stats.run_game:                  #если жизни ещё не закончились, то:
            gun.update_gun()                #вызов функции обновляющей позицию пушки    
            controls.update(bg_color, screen, stats, sc, gun, inos, bullets)      #вызов функции обновления экрана
            controls.update_bullets(screen, stats, sc, inos, bullets)
            controls.update_inos(stats, screen, sc, gun, inos, bullets)                

run()

-----------------------------------------------------------------------------------------
Рисование пушки в PIXILART.com (размер файла 100*100)
выбор цвета, рисование объекта
файл(file) -> export/download -> download png

создание папки images с помещением в неё сделанного изображения пушки

Рисование пришельца в PIXILART.com (отражением половины по вертикали с помощью Select Tools(S))
Сохранение объекта в папку images\

-----------------------------------------------------------------------------------------
Создание файла с логикой пушки gun.py:

import pygame
from pygame.sprite import Sprite                        #для создания жизней

class Gun(Sprite):
    
    def __init__(self, screen):
        """инициализация пушки"""
        super(Gun, self).__init__()                                     #подтягиваем данные из родительского класса
        self.screen = screen                                            #получение экрана
        self.image = pygame.image.load('images/pixil-frame-0.png')      #загрузка рисунка
        self.rect = self.image.get_rect()                               #получаем картинку пушки как прямоугольник(rectangle - прямоугольник)
        self.screen_rect = screen.get_rect()                            #получаем объект экрана
#наложение объекта пушки на экран:        
        self.rect.centerx = self.screen_rect.centerx    #координаты центра пушки по центру экрана
        self.center = float(self.rect.centerx)          #для восприятия вещ.чисел
        self.rect.bottom = self.screen_rect.bottom      #координаты низа пушки внизу экрана
#передвижение пушки по экрану(с нажатой клавишей):
        self.mright = False                             #движение вправо
        self.mleft = False                              #движение влево

#функция вывода пушки на экран:        
    def output(self):
        """рисование пушки"""
        self.screen.blit(self.image, self.rect)         #отрисовка пушки

    def update_gun(self):
        """обновление позиции пушки"""
    #если клавиша движения вправо нажата и правый край пушки < правого края экрана:
        if self.mright and self.rect.right < self.screen_rect.right:        
            self.center += 3.5          #пушка перемещается вправо
    #если клавиша движения влево нажата и левый край пушки > левого края экрана (координаты 0):        
        if self.mleft and self.rect.left > 0:        
            self.center -= 3.5          #пушка перемещается влево

        self.rect.centerx = self.center         #подключение аттрибута
    
    def create_gun(self):
        """появление пушки в центре внизу экрана"""
        self.center = self.screen_rect.centerx        

----------------------------------------------------------------------------------------------
Создание файла с обработчиком событий controls.py:

import pygame
import sys                      #обработка события и закрытия окна игры
from bullet import Bullet
from ino import Ino             #импорт класса с пришельцем
import time                     #для задержки в момент столкновения пушки с пришельцем

def events(screen, gun, bullets):
    """обработка событий"""
    for event in pygame.event.get():    #собираем все события игры(event - событие)
        if event.type == pygame.QUIT:   #если пользователь нажал крестик
            sys.exit()                  #закрываем игру
        elif event.type == pygame.KEYDOWN:      #если тип события KEYDOWN(нажатая клавиша)
            
            if event.key == pygame.K_d:         #если нажата клавиша D
                gun.mright = True               #пушка двигается вправо
                
            elif event.key == pygame.K_a:           #если нажата клавиша A
                gun.mleft = True                   #пушка двигается влево

            elif event.key == pygame.K_SPACE:           #если нажат пробел
                new_bullet = Bullet(screen, gun)        #создание новой пули
                bullets.add(new_bullet)                 #добавление новой пули в контейнер                            
                
        elif event.type == pygame.KEYUP:        
            if event.key == pygame.K_d:         #если клавиша D не нажата
                gun.mright = False
                
            elif event.key == pygame.K_a:         #если клавиша A не нажата
                gun.mleft = False

def update(bg_color, screen, stats, sc, gun, inos, bullets):
    """обновление экрана"""
    screen.fill(bg_color)                   #фоновый цвет(fill - заливка)
    sc.show_score()                         #отрисовка счёта
    for bullet in bullets.sprites():        #прорисовка пули при вылете из пушки
        bullet.draw_bullet()    
    gun.output()                            #отрисовка пушки на экране
    inos.draw(screen)                       #отрисовывает пришельцев на экране
    pygame.display.flip()                   #прорисовка последнего экрана(flip - щелчок)

def update_bullets(screen, stats, sc, inos, bullets):
    """обновление позиций пуль"""
    bullets.update()                #отрисовываем и помещаем на экран пули
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:         #когда низ пули переходит границу экрана
            bullets.remove(bullet)          #удаляем пулю из контейнера
#создание колизии(списка с элементами перекрытия между пулями и пришельцами)
    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)      #уничтожение пришельцев
    if collisions:                          #если пуля коснулась пришельца
        for inos in collisions.values():
            stats.score += 10 * len(inos)           #счёт увеличивается на 10 за убийство каждого пришельца                
        sc.image_score()                    #показываем счёт
        check_high_score(stats, sc)         #проверка счёта на рекорд
        sc.image_guns()                     #вывод жизней
    if len(inos) == 0:                      #если вся армия уничтожена
        bullets.empty()
        create_army(screen, inos)           #создаётся новая армия

def gun_kill(stats, screen, sc, gun, inos, bullets):
    """столкновение пушки и армии пришельцев"""
    if stats.guns_left > 0:                     #если количество жизни пушки > 0
        stats.guns_left -= 1                    #отнимаем 1 жизнь
        sc.image_guns()                         #отрисовываем жизни заново
        inos.empty()                            #очищаем группу пришельцев
        bullets.empty()                         #очищаем группу пуль
        create_army(screen, inos)               #заново создаём группу с пришельцами
        gun.create_gun()                        #заново создаём пушку   
        time.sleep(1)                           #длительность перезагрузки
    else:
        stats.run_game = False
        sys.exit()                              #иначе конец игры    

def update_inos(stats, screen, sc, gun, inos, bullets):
    """обновление позиций инопланетян"""
    inos.update()
# если происходит перекрытие пушки пришельцами:
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(stats, screen, sc, gun, inos, bullets)
    inos_check(stats, screen, sc, gun, inos, bullets)       #проверяем пришельцев

def inos_check(stats, screen, sc, gun, inos, bullets):
    """проверка соприкосновения армии пришельцев с границей экрана"""
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
#если нижняя позиция пришельца >= нижней части экрана:    
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, sc, gun, inos, bullets)     #вызов функции перезагрузки экрана
            break                   #выход из цикла        

def create_army(screen, inos):
    """создание армии пришельцев"""
    ino = Ino(screen)                       #создание одного пришельца
    ino_width = ino.rect.width              #ширина пришельца = ширина прямоугольника
#сколько помещается пришельцев в одном ряду(преобразованное в целое число):    
    number_ino_x = int((600 - 2 * ino_width) / ino_width)
    ino_height = ino.rect.height            #высота пришельца
    number_ino_y = int((700 - 100 - 2 * ino_height) / ino_height)

#создание рядов пришельцев:    
    for row_number in range(number_ino_y - 1): 
#создание одного ряда пришельцев:
        for ino_number in range(number_ino_x):
            ino = Ino(screen)                   #создание одного пришельца
            ino.x = ino_width + (ino_width * ino_number)            #создание x
            ino.y = ino_height + (ino_height * row_number)          #создание y           
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + (ino.rect.height * row_number)            
            inos.add(ino)               #добавление пришельцев в группу

def check_high_score(stats, sc):
    """проверка новых рекордов"""
    if stats.score > stats.high_score:              #если текущий счёт больше чем рекорд
        stats.high_score = stats.score
        sc.image_high_score()                       #отрисовываем новый рекорд
        with open('highscore.txt', 'w') as f:             #открываем txt-файл с рекордом в режиме записи
            f.write(str(stats.high_score))                #записываем в него строку с рекордом

--------------------------------------------------------------------------------------------
Создание файла для хранения пуль bullet.py:

import pygame

class Bullet(pygame.sprite.Sprite):
    """класс на основе класса Sprite из pygame"""

    def __init__(self, screen, gun):
        """создаём пулю в текущей позиции пушки"""
        super(Bullet, self).__init__()
        self.screen = screen        #экран где будут отрисовываться пули
        self.rect = pygame.Rect(0, 0, 9, 12)    #координаты появление пуль(0, 0) и их высота(2) и ширина(12)
        self.color = 204, 220, 57       #цвет пуль
        self.speed = 7.0                #скорость пули
        self.rect.centerx = gun.rect.centerx        #появление пули в координатах: x
        self.rect.top = gun.rect.top    #появление пули в верхней части пушки
        self.y = float(self.rect.y)     #появление пули в координатах: y

    def update(self):
        """перемещение пули вверх"""
        self.y -= self.speed            #перемещение по координате y
        self.rect.y = self.y            #обновление позиции прямоугольника

    def draw_bullet(self):
        """рисуем пулю на экране"""
        pygame.draw.rect(self.screen, self.color, self.rect)

--------------------------------------------------------------------------------------------
Создание модуля с физикой движения пришельцев ino.py:

import pygame

class Ino(pygame.sprite.Sprite):
    """класс одного пришельца"""

    def __init__(self, screen):
        """инициализируем и задаём начальную позицию"""
        super(Ino, self).__init__()
        self.screen = screen                                    #где происходит действие игры
        self.image = pygame.image.load('images/Ino.png')        #загрузка изображения
        self.rect = self.image.get_rect()                       #преобразование инопланетянина в прямоугольник
        self.rect.x = self.rect.width           #помещаем в левый верхний угол и отслеживаем ширину изображения по оси x
        self.rect.y = self.rect.height          #отслеживаем высоту изображения по оси y
        self.x = float(self.rect.x)             #плавная скорость движения по x
        self.y = float(self.rect.y)             #плавная скорость движения по y

    def draw(self):
        """вывод пришельца на экран"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """перемещение пришельцев по экрану"""
        self.y += 0.1
        self.rect.y = self.y

--------------------------------------------------------------------------------------------
Создание файла с игровой статистикой stats.py:

class Stats():
    """отслеживание статистики"""
    
    def __init__(self):
        """инициализация статистики"""
        self.reset_stats()
        self.run_game = True                #проверка наличия жизней
#открытие файла highscore.txt с сохранённым рекордом (в режиме чтения):        
        with open('highscore.txt', 'r') as f:
            self.high_score = int(f.readline())             #считываем рекорд уничтоженных пришельцев                 
    
    def reset_stats(self):
        """статистика изменяющаяся во время игры"""
        self.guns_left = 2              #жизни пушки
        self.score = 0                  #текущий счёт

---------------------------------------------------------------------------------------------
Создание файла со счётом и текстом внутри игры scores.py:

import pygame.font
from gun import Gun
from pygame.sprite import Group

class Scores():
    """вывод игровой информации"""
    def __init__(self, screen, stats):
        """инициализация подсчёта очков"""
        self.screen = screen                                #подключаем экран
        self.screen_rect = screen.get_rect()                #получение объекта
        self.stats = stats
        self.text_color = (204, 220, 57)                     #цвет шрифта
        self.font = pygame.font.SysFont(None, 36)           #вид и размер шрифта
        self.image_score()                                  #превращение шрифта в изображение с текущим счётом
        self.image_high_score()                             #функция ответственная за рекорд
        self.image_guns()                                   #вывод количества жизней

    def image_score(self):
        """преобразование текста счёта в графическое изображение"""
        self.score_img = self.font.render(str(self.stats.score), True, self.text_color, (0, 0, 0))
        self.score_rect = self.score_img.get_rect()                 #объект прямоугольник для изображения счёта
        self.score_rect.right = self.screen_rect.right - 40         #размещение счёта справа вверху экрана (- 40 пикселей отступ от правого края экрана)
        self.score_rect.top = 20                                    #отступ сверху(20 пикселей)

    def image_high_score(self):
        """преобразование рекорда в графическое изображение"""
        self.high_score_image = self.font.render(str(self.stats.high_score), True, self.text_color, (0, 0, 0))
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx         #выравнивание объекта по координате x (центру экрана)
        self.high_score_rect.top = self.screen_rect.top + 20            #выравнивание объекта верху экрана

    def image_guns(self):
        """количество жизней"""
        self.guns = Group()                                         #группа с жизнями
        for gun_number in range(self.stats.guns_left):              #перебираем по одной
            gun = Gun(self.screen)                                  #отрисовываем на экране
            gun.rect.x = 15 + gun_number * gun.rect.width           #отображение жизней в левом крае 
            gun.rect.y = 20                         #отступ y = 20
            self.guns.add(gun)

    def show_score(self):
        """отображение счёта на экране"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)               #отображение рекорда на экране
        self.guns.draw(self.screen)                     #отображение жизней

----------------------------------------------------------------------------------------------
Создание файла для хранения рекорда highscore.txt: