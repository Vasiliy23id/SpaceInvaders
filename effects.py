import pygame

class Effects:
    def __init__ (self):
        pygame.init()
        pygame.mixer.music.load("sounds/ost.mp3")
        self.shoot = pygame.mixer.Sound("sounds/shoot.ogg ")
        self.hit = pygame.mixer.Sound("sounds/hit.ogg ")
        self.death = pygame.mixer.Sound("sounds/death.ogg ")
        self.enemy_run = pygame.mixer.Sound("sounds/smeh.ogg ")

