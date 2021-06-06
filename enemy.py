import pygame
from pygame.sprite import Sprite


class Enemy(Sprite): # Класс противника
    def __init__(self, ai_game): # Создание одного противника
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/enemy.bmp') # Пожгрузка изображения врага
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width # Точка появления врага в левом верхнем углу
        self.rect.y = self.rect.height

        self.x = float(self.rect.x) # Точная горизонтальная позиция

    def check_edges(self): # Проверка достижения края 
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self): # Перемещение врага
        self.x += (self.settings.enemy_speed *
                   self.settings.fleet_direction) # Перемещение в лево или в право
        self.rect.x = self.x

