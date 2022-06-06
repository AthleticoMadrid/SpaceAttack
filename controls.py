import pygame, sys
from bullet import Bullet
from ino import Ino
import time

def events(screen, gun, bullets):
    """обработка событий"""
    for event in pygame.event.get():    #event - событие
        if event.type == pygame.QUIT:
            sys.exit()
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
    screen.fill(bg_color)           #fill - заливка
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    gun.output()
    inos.draw(screen)
    pygame.display.flip()           #flip - щелчок
    
def update_bullets(screen, stats, sc, inos, bullets):
    """обновление позиций пуль"""
    bullets.update()                #отрисовываем и помещаем на экран пули
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:         #когда низ пули переходит границу экрана
            bullets.remove(bullet)          #удаляем пулю из контейнера
    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)      #уничтожение пришельцев
    if collisions:
        for inos in collisions.values():
            stats.score += 10 * len(inos)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_guns()
    if len(inos) == 0:
        bullets.empty()
        create_army(screen, inos)

def gun_kill(stats, screen, sc, gun, inos, bullets):
    """столкновение пушки и армии пришельцев"""
    if stats.guns_left > 0:                     #если количество жизни пушки > 0
        stats.guns_left -= 1
        sc.image_guns()
        inos.empty()
        bullets.empty()
        create_army(screen, inos)
        gun.create_gun()
        time.sleep(1)
    else:
        stats.run_game = False
        sys.exit()

def update_inos(stats, screen, sc, gun, inos, bullets):
    """обновление позиций инопланетян"""
    inos.update()
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(stats, screen, sc, gun, inos, bullets)
    inos_check(stats, screen, sc, gun, inos, bullets)

def inos_check(stats, screen, sc, gun, inos, bullets):
    """проверка соприкосновения армии пришельцев с границей экрана"""
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, sc, gun, inos, bullets)
            break

def create_army(screen, inos):
    """создание армии пришельцев"""
    ino = Ino(screen)
    ino_width = ino.rect.width          #ширина
#сколько помещается пришельцев в одном ряду по горизонтали:    
    number_ino_x = int((600 - 2 * ino_width) / ino_width)
    ino_height = ino.rect.height        #высота
    number_ino_y = int((700 - 100 - 2 * ino_height) / ino_height)

#создание рядов пришельцев:    
    for row_number in range(number_ino_y - 1):    
#создание одного ряда пришельцев:
        for ino_number in range(number_ino_x):
            ino = Ino(screen)           #создание одного пришельца
            ino.x = ino_width + (ino_width * ino_number)
            ino.y = ino_height + (ino_height * row_number)
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + (ino.rect.height * row_number)
            inos.add(ino)               #добавление пришельцев в группу
            
def check_high_score(stats, sc):
    """проверка новых рекордов"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('highscore.txt', 'w') as f:
            f.write(str(stats.high_score))
                