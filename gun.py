import pygame
from pygame.sprite import Sprite

class Gun(Sprite):
    
    def __init__(self, screen):
        """инициализация пушки"""
        super(Gun, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/pixil-frame-0.png')
        self.rect = self.image.get_rect()   #rectangle - прямоугольник
        self.screen_rect = screen.get_rect()
#наложение объекта пушки на экран:        
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)      #для восприятия вещ.чисел
        self.rect.bottom = self.screen_rect.bottom
#передвижение пушки по экрану(с нажатой клавишей):
        self.mright = False     #движение вправо
        self.mleft = False      #движение влево
        
                
    def output(self):
        """рисование пушки"""
        self.screen.blit(self.image, self.rect)
        
    def update_gun(self):
        """обновление позиции пушки"""
        if self.mright and self.rect.right < self.screen_rect.right:
            self.center += 3.5      #пушка перемещается вправо
        if self.mleft and self.rect.left > 0:
            self.center -= 3.5      #пушка перемещается влево
            
        self.rect.centerx = self.center
        
    def create_gun(self):
        """появление пушки в центре внизу экрана"""
        self.center = self.screen_rect.centerx