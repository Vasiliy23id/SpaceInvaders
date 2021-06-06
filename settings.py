class Settings(): # Класс с настройками игры настройки игры
    def __init__(self):
        # Параметры выстрелов
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 69, 60)
        self.bullets_allowed = 5 # Только 5 снарядов на экране
        # Параметры экрана
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (25, 25, 112)

        self.ship_limit = 3 # Количество жизней

        self.fleet_drop_speed = 10 # Снижение флота при достижении края

        self.speedup_scale = 1.1
        self.score_scale = 1.5 # Увеличение стоимости противника как и скорость игры

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self): # Настройки которые меняются в ходе игры
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.enemy_speed = 1.0

        self.enemy_points = 50 # За одного врага

        self.fleet_direction = 1 # Движение противника в стороны

    def increase_speed(self): # Изменяет скорость(повышат сложность)

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)

