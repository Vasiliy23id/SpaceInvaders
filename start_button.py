import pygame.font # Позволяет выводить текст на экран

class Button(): # Класс для работы с состоянием игры
    def __init__(self, ai_game, msg): #
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Параметры и свойства кнопки
        self.width = 210 # Высота и ширна определяется по параметрам экрана
        self.height = 50
        self.button_color = (173, 255, 47)
        self.text_color = (105, 105, 105)
        self.font = pygame.font.SysFont(None, 48) # шрифты и их размер
        # выравнивание кнопки относительно центра экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        #
        self._prep_msg(msg) # Выводит текст на кнопку

    def _prep_msg(self, msg): # Выводит текст на центр кнопки

        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self): # Отображает кнопку на экране
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

        