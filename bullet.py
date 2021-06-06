import pygame
from pygame.sprite import Sprite


class Bullet(Sprite): # Клас для управления выстрелами
    def __init__(self, ai_game):
        super().__init__() # Создание выстрела в позиции корабля
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        # Задаем  информацию о местеположении для создания снаряда
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y) # Содержится информация о позиции снаряда

    def update(self):  
        self.y -= self.settings.bullet_speed # Обновление информации о позиции снаряда
        self.rect.y = self.y

    def draw_bullet(self): # Выводит снаряд на экран 
        pygame.draw.rect(self.screen, self.color, self.rect)

