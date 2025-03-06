import pygame
import math
from pygame.math import Vector2
from time_system import TimeState

class Boss(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((80, 80))
        self.image.fill((255, 40, 40))
        self.rect = self.image.get_rect(center=(640, 360))
        self.pos = Vector2(self.rect.center)
        self.health = 1000
        self.max_health = 1000
        self.attack_phase = 1
        self.attack_patterns = []
        self.current_attack = None
        self.attack_timer = 0
        self.te_adaptation = {
            TimeState.NORMAL: self.normal_attack,
            TimeState.STOPPED: self.stopped_attack,
            TimeState.SLOWED: self.slow_attack,
            TimeState.SPED_UP: self.fast_attack
        }

    def update(self, dt):
        self.attack_timer += dt
        self.adapt_to_time_state()
        self.execute_attack_pattern(dt)
        
        if self.health <= 0:
            self.game.end_game("victory")

    def adapt_to_time_state(self):
        current_state = self.game.time_system.current_state
        attack_method = self.time_state_adaptation.get(current_state, self.normal_attack)
        if attack_method != self.current_attack:
            self.current_attack = attack_method
            self.attack_timer = 0

    def execute_attack_pattern(self, dt):
        if self.current_attack:
            self.current_attack(dt)

    def normal_attack(self, dt):
        if self.attack_timer >= 1.0:
            self.attack_timer = 0
            self.create_bullet_circle(8, 400)

    def stopped_attack(self, dt):
        if self.attack_timer >= 0.5:
            self.attack_timer = 0
            self.create_aimed_barrage(16)

    def slow_attack(self, dt):
        if self.attack_timer >= 2.0:
            self.attack_timer = 0
            self.create_spiral_pattern(3, 200)

    def fast_attack(self, dt):
        if self.attack_timer >= 0.3:
            self.attack_timer = 0
            self.create_wave_pattern(5, 500)

    def create_bullet_circle(self, count, speed):
        for angle in range(0, 360, 360//count):
            rad = math.radians(angle)
            direction = Vector2(math.cos(rad), math.sin(rad))
            self.game.spawn_bullet(self.pos, direction * speed)

    def create_aimed_barrage(self, count):
        player_pos = self.game.player.pos
        direction = (player_pos - self.pos).normalize()
        spread = 30  # degrees
        
        for i in range(count):
            angle = math.radians(-spread/2 + (spread/(count-1))*i)
            rotated = direction.rotate(math.degrees(angle))
            self.game.spawn_bullet(self.pos, rotated * 600)

    def take_damage(self, amount):
        self.health = max(self.health - amount, 0)

    def draw_health_bar(self, surface):
        bar_width = 400
        bar_height = 25
        pos = (self.game.screen.get_width()//2 - bar_width//2, 50)
        
        # Background
        pygame.draw.rect(surface, (50,50,50), (pos[0], pos[1], bar_width, bar_height))
        # Health
        health_width = bar_width * (self.health / self.max_health)
        pygame.draw.rect(surface, (200,40,40), (pos[0], pos[1], health_width, bar_height))