import pygame
import math
from pygame.math import Vector2
from config import COLORS, GAME_CONFIG

class Bullet:
    def __init__(self, position, velocity, bullet_type='normal'):
        self.position = Vector2(position)
        self.base_velocity = Vector2(velocity)
        self.velocity = Vector2(velocity)
        self.radius = 4
        self.type = bullet_type
        self.active = True
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt, time_scale):
        if self.type == 'homing':
            # Homing logic would be implemented here
            pass
        else:
            self.position += self.velocity * time_scale * dt / 1000
        
        # Screen bounds check
        if not (0 <= self.position.x <= GAME_CONFIG['screen_width'] and 
                0 <= self.position.y <= GAME_CONFIG['screen_height']):
            self.active = False

    def draw(self, surface):
        color = COLORS['bullet_time_affected' if self.type != 'normal' else 'bullet_normal']
        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), self.radius)

class BulletManager:
    def __init__(self):
        self.bullets = []
        self.time_state = 'normal'

    def add_bullet(self, position, velocity, bullet_type='normal'):
        if len(self.bullets) < GAME_CONFIG['max_bullets']:
            self.bullets.append(Bullet(position, velocity, bullet_type))

    def update(self, dt, time_scale):
        self.bullets = [bullet for bullet in self.bullets if bullet.active]
        for bullet in self.bullets:
            bullet.update(dt, time_scale)

    def create_radial_pattern(self, center, count, speed):
        angle_step = 360 / count
        for i in range(count):
            angle = math.radians(i * angle_step)
            velocity = Vector2(math.cos(angle), math.sin(angle)) * speed
            self.add_bullet(center, velocity)

    def create_spiral_pattern(self, center, arms, rotations, speed):
        current_time = pygame.time.get_ticks()
        for i in range(arms):
            angle = math.radians((current_time/10 % 360) + (i * 360/arms))
            offset = Vector2(math.cos(angle), math.sin(angle)) * rotations
            velocity = Vector2(math.cos(angle), math.sin(angle)) * speed
            self.add_bullet(center + offset, velocity)

    def check_collisions(self, player_rect):
        return any(
            bullet.position.distance_to(player_rect.center) < bullet.radius + player_rect.width/2
            for bullet in self.bullets
            if bullet.active
        )

    def draw(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)

    def get_state(self):
        return [{
            'position': (bullet.position.x, bullet.position.y),
            'velocity': (bullet.base_velocity.x, bullet.base_velocity.y),
            'type': bullet.type,
            'spawn_time': bullet.spawn_time
        } for bullet in self.bullets]

    def set_state(self, state):
        self.bullets = [
            Bullet(
                position=Vector2(b['position']),
                velocity=Vector2(b['velocity']),
                bullet_type=b['type']
            ) for b in state
        ]