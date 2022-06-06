import pygame

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, screen, gun):
        """создаём пулю в текущей позиции пушки"""
        super(Bullet, self).__init__()
        self.screen = screen        #экран где будут отрисовываться пули
        self.rect = pygame.Rect(0, 0, 9, 12)    #координаты появление пуль(0, 0) и их высота(2) и ширина(12)
        self.color = 204, 220, 57       #цвет пуль
        self.speed = 7.0                  #скорость пули
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
    