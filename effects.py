import pygame

class Effects: #  Класс для работы со звуками
    def __init__ (self):
        pygame.init()
        pygame.mixer.music.load("sounds/ost.mp3") # Загружаем музыкальные файлы
        self.shoot = pygame.mixer.Sound("sounds/shoot.ogg ") # Идут поверх фоновой музыки(выстрел)
        self.hit = pygame.mixer.Sound("sounds/hit.ogg ")# Идут поверх фоновой музыки(попадание)
        self.death = pygame.mixer.Sound("sounds/death.ogg ")# Идут поверх фоновой музыки(столкновение)
        self.enemy_run = pygame.mixer.Sound("sounds/smeh.ogg ")# Идут поверх фоновой музыки(противник прошел мимо)
          
