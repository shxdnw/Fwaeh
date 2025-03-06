import pygame
import math
from config import COLORS, GAME_CONFIG
from bullet_manager import BulletManager

class Boss:
    def __init__(self, bullet_manager: BulletManager):
        self.phase = 1
        self.health = 1000
        self.max_health = 1000
        self.position = pygame.Vector2(
            GAME_CONFIG['screen_width'] // 2, 
            150
        )
        self.bullet_manager = bullet_manager
        self.attack_patterns = {
            1: self._phase1_attack,
            2: self._phase2_attack,
            3: self._phase3_attack
        }
        self.attack_timer = 0
        self.bullet_spread = 0

    def update(self, dt, time_state):
        self.attack_timer += dt
        if self.attack_timer > 1000:  # Attack every second
            self.attack_patterns[self.phase](time_state)
            self.attack_timer = 0
            
    def _phase1_attack(self, time_state):
        bullet_count = 12 if time_state == 'normal' else 24
        speed = 400 if time_state == 'sped_up' else 300
        for angle in range(0, 360, 360//bullet_count):
            rad = math.radians(angle)
            velocity = pygame.Vector2(math.cos(rad), math.sin(rad)) * speed
            self.bullet_manager.add_bullet(self.position, velocity)

    def _phase2_attack(self, time_state):
        arms = 5 if time_state == 'normal' else 3
        speed = 500 if time_state == 'sped_up' else 400
        current_time = pygame.time.get_ticks()
        for i in range(arms):
            angle = math.radians((current_time/10 % 360) + (i * 360/arms))
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            self.bullet_manager.add_bullet(self.position, velocity)

    def _phase3_attack(self, time_state):
        # Homing bullet pattern
        num_bullets = 8
        speed = 300 if time_state == 'slowed' else 450
        for i in range(num_bullets):
            angle = math.radians(360/num_bullets * i)
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            self.bullet_manager.add_bullet(self.position, velocity, 'homing')

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= self.max_health * 0.66:
            self.phase = 2
        if self.health <= self.max_health * 0.33:
            self.phase = 3

    def draw(self, surface):
        pygame.draw.circle(surface, COLORS['boss'], (int(self.position.x), int(self.position.y)), 40)
        self._draw_health_bar(surface)

    def _draw_health_bar(self, surface):
        bar_width = 200
        bar_height = 15
