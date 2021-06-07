import sys
import pygame
from time import sleep


from ship import Ship
from settings import Settings
from bullet import Bullet
from enemy import Enemy
from game_stats import GameStats
from start_button import Button
from scoreboard import Scoreboard
from effects import Effects
from exit_button import Exit_button


class AlienInvasion: # Основной класс управляющий ресурсами и поведением игры

    def __init__(self): # Функция инициализирующая игру и создающая игровые ресурсы
        pygame.init()
        self.settings = Settings() # инициализирую настройки игры
        self.effects = Effects() # инициализируем звуковые эфекты

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Игра запускается во весь экран
        self.settings.screen_width = self.screen.get_rect().width # Параметры экрана записываются в настройки
        self.settings.screen_height = self.screen.get_rect().height# Параметры экрана записываются в настройки
        pygame.display.set_caption("Alien Invasion") # Как называется окно с игрой

        self.stats = GameStats(self) # Подготовка статистики
        self.sb = Scoreboard(self) # Вывод счетчиков

        self.ship = Ship(self) # Вывод корабля
        self.bullets = pygame.sprite.Group() # подготовка выстрелов
        self.enemis = pygame.sprite.Group() # Вывод врагов

        self._create_fleet() # Выстраиваем флот

        self.play_button = Button(self, "Click to start") # Вывод кнопки на экран
        self.exit_button = Exit_button(self, "Exit")

    def _check_events(self): # Проверяет нажатия клавишь и события мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN: # Проверяет кликнул ли пользователь мышкой
                mouse_pos = pygame.mouse.get_pos() 
                self._check_play_button(mouse_pos)
                self._check_exit_button(mouse_pos) 

    def _check_keydown_events(self, event): 
        if event.key == pygame.K_RIGHT: # Ниже клавиши управления кораблем
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_F1:
            if self.settings.pause:
                pygame.mixer.music.pause()
                self.settings.pause = False
            else:
                pygame.mixer.music.unpause()
                self.settings.pause = True
        elif event.key == pygame.K_F2:
            self.settings.ost -= 0.1
            pygame.mixer.music.set_volume(self.settings.ost)
        elif event.key == pygame.K_F3:
            self.settings.ost += 0.1
            pygame.mixer.music.set_volume(self.settings.ost)
        elif event.key == pygame.K_ESCAPE: # выход из игры 
             self.stats.game_active = False
             pygame.mouse.set_visible(True)
             pygame.mixer.music.stop()
        elif event.key == pygame.K_SPACE: # Стрельба
            self._fire_bullet()

    def _check_keyup_events(self, event): # Проверка на отпускание
        if event.key == pygame.K_RIGHT: # Клавиши управления
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos): # Cрабатывает при нажатии кнопки старт
        Start_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if Start_button_clicked and not self.stats.game_active: # Если в момент нажати кнопки игра не была активна то запускаем новую игру 

            self.settings.initialize_dynamic_settings() # Сбросс изменяющихся настроек 

            self.stats.reset_stats() # Сбрасываем статистику
            self.stats.game_active = True # Меняем состояние игры
            self.sb.prep_score() # Обнуление счетчиков
            self.sb.prep_level()
            self.sb.prep_ships()
            # Очищаем экран от врагов и выстрелов
            self.enemis.empty()
            self.bullets.empty()

            self._create_fleet() # Пересоздаем флот 
            self.ship.center_ship() # спавним корабль в положенном месте
            
            if self.settings.pause:
                pygame.mixer.music.play(-1)

            pygame.mouse.set_visible(False) # Убираем видимость мыши

    def _check_exit_button(self, mouse_pos): # Cрабатывает при нажатии кнопки выход
        Exit_button_clicked = self.exit_button.exit_rect.collidepoint(mouse_pos)
        if Exit_button_clicked and not self.stats.game_active:
            sys.exit()
            

    def _update_screen(self): # Обновляет экран 
        self.screen.fill(self.settings.bg_color)
        
        if not self.stats.game_active: # Rнопку видно если игра не активна
            self.play_button.draw_button()
            self.exit_button.draw_exit_button()
        else: # Содержимое экрана обновляется только во время игры 
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.enemis.draw(self.screen) # Выводим на экран пришельца

            self.sb.show_score() # Вывод счетчика на экран

        pygame.display.flip()

    def _fire_bullet(self): # Создание нового снаряда и включение его в группу
        if len(self.bullets) < self.settings.bullets_allowed: # Проверка количества снарядов на экране
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.effects.shoot.play()

    def _update_bullets(self):
        self.bullets.update() # Одновление позиции снарядов
        for bullet in self.bullets.copy():# Удаление снарядов за экраном
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_enemy_collisions()

    def _ship_hit(self): # Отвечает за столкновение коробля с противником
        if self.stats.ships_left > 0:
            self.effects.death.play() # Воиспроизведение звука смерти корабля
            pygame.mixer.music.rewind() # Перезапуск фоновой музыки

            self.stats.ships_left -= 1 # Вычитание жизни
            self.sb.prep_ships()

            self.enemis.empty() # Очищаем экран
            self.bullets.empty()

            self._create_fleet() # Строим заново флот и выставляем корабль игрока на точку спавна
            self.ship.center_ship()

            sleep(1) # pflth;rf gjckt cvthnb

        else:
            self.stats.game_active = False # Если кончатся жизни, останавливаем игру
            pygame.mixer.music.pause() # Если кончатся жизни, останавливаем фоновую музыку
            pygame.mouse.set_visible(True) # Возвращаем видимость мыши

    def _create_fleet(self):
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        available_space_x = self.settings.screen_width - (2 * enemy_width) # Доступное пространнство для построения ряда
        number_enemis_x = available_space_x // (2 * enemy_width) # Подщет количества врагов в ряду

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (5 * enemy_height) - ship_height) # Определяем доступное пространнство для построения рядов зв вычитом зоны для игрока

        number_rows = available_space_y // (2 * enemy_height) # Вычисляем количество рядов

        for row_number in range(number_rows): # Создание флота
            for enemy_number in range(number_enemis_x):
                self._create_enemy(enemy_number, row_number) # Создание противника

    def _create_enemy(self, enemy_number, row_number): # Создание противника и размещение его в ряду
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        enemy.x = enemy_width + 2 * enemy_width * enemy_number
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
        self.enemis.add(enemy)

    def _check_bullet_enemy_collisions(self): # Проверка попадания по врагу 
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.enemis, True, True) # при попадании убирает врага и выстрел

        if collisions:
            self.effects.hit.play()
            for enemis in collisions.values():
                self.stats.score += self.settings.enemy_points * len(enemis) # Начисление очков за попадание
            self.sb.prep_score()
            self.sb.check_high_score() # Проверка изменений рекорда

        if not self.enemis: # Удаление оставшихся выстрелов и пересоздание флота
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.settings.increase_speed() # Ускоряет следующий флот

            self.stats.level += 1
            self.sb.prep_level()

    def _update_enemis(self):
        self._check_fleet_edges() # Реакция при достижения края экрана
        self.enemis.update() # Обновление позиции всех пришельцев во флоте

        if pygame.sprite.spritecollideany(self.ship, self.enemis):
            self._ship_hit() # Проверка столкновения
        self._check_enemis_bottom() # Дошли ли враги донизу

    def _check_fleet_edges(self): # Реагирует при достижения врагом края
        for enemy in self.enemis.sprites():
            if enemy.check_edges():
                self._change_fleet_direction() # Смена направления
                break

    def center_ship(self): # Выставляем корабл на точке спавна и перезаписываем кординаты
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def _check_enemis_bottom(self): # Проверяет дошел ли враг до края снизу
        screen_rect = self.screen.get_rect()
        for enemy in self.enemis.sprites():
            if enemy.rect.bottom >= screen_rect.bottom: # В случае если враг дошел до края реагируем как при столкновении корабля
                self.effects.enemy_run.play() # Для того чтобы отличить эти две смерти воспроизведем еще один звук
                self._ship_hit()
                break

    def _change_fleet_direction(self): # Смена направления движения противника
        for enemy in self.enemis.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self): # Запуск основного цикла игры 
        while True:
            self._check_events()

            if self.stats.game_active: # Нижеперечисленное выполняется только тогда когда игра активна
                self.ship.update()
                self._update_bullets()
                self._update_enemis()
                

            self._update_screen()


if __name__ == '__main__': # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
