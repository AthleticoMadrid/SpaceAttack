import pygame
import controls
from gun import Gun
from pygame.sprite import Group
from scores import Scores
from stats import Stats

#функция запуска, инициализации и создания экрана
def run():
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Космические защитники") #caption - заголовок
    bg_color = (0, 0, 0)
    gun = Gun(screen)
    bullets = Group()
    inos = Group()
    controls.create_army(screen, inos)
    stats = Stats()
    sc = Scores(screen, stats)


    while True:
        controls.events(screen, gun, bullets)
        if stats.run_game:
            gun.update_gun()
            controls.update(bg_color, screen, stats, sc, gun, inos, bullets)
            controls.update_bullets(screen, stats, sc, inos, bullets)
            controls.update_inos(stats, screen, sc, gun, inos, bullets)
    
run()