
class GameStats(): # Класс для работы с игровой статистикой
    def __init__(self, ai_game): # инициализирует статистику
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False # Состояние игры при запуске

        self.high_score = 0

    def reset_stats(self): # инициализирует статистику, которая имзменяется в ходе игры
        self.ships_left = self.settings.ship_limit
        self.score = 0 # очки
        self.level = 1 # Уровень

