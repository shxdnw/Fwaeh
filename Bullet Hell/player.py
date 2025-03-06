import pygame
from pygame.math import Vector2
from config import GAME_CONFIG, COLORS

class Player:
    def __init__(self):
        self.position = Vector2(
            GAME_CONFIG['screen_width']//2,
            GAME_CONFIG['screen_height'] - 100
        )
        self.velocity = Vector2(0, 0)
        self.speed = GAME_CONFIG['player_speed']
        self.acceleration = 1200
        self.deceleration = 800
        self.hitbox_radius = 12
        self.show_hitbox = False
        self.dash_cooldown = 2000
        self.last_dash = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        input_vector = Vector2(0, 0)
        
        if keys[pygame.K_w]: input_vector.y -= 1
        if keys[pygame.K_s]: input_vector.y += 1
        if keys[pygame.K_a]: input_vector.x -= 1
        if keys[pygame.K_d]: input_vector.x += 1

        if input_vector.length() > 0:
            input_vector.scale_to_length(1)
            self.velocity += input_vector * self.acceleration * dt/1000
        else:
            if self.velocity.length() > 0:
                brake = self.velocity.normalize() * self.deceleration * dt/1000
                if brake.length() >= self.velocity.length():
                    self.velocity = Vector2(0,0)
                else:
                    self.velocity -= brake

        self.velocity.x = clamp(self.velocity.x, -self.speed, self.speed)
        self.velocity.y = clamp(self.velocity.y, -self.speed, self.speed)
        
        self.position += self.velocity * dt/1000
        self.position.x = clamp(self.position.x, 0, GAME_CONFIG['screen_width'])
        self.position.y = clamp(self.position.y, 0, GAME_CONFIG['screen_height'])

    def draw(self, surface):
        # Main player body
        pygame.draw.circle(surface, COLORS['player'], self.position, 15)
        
        # Hitbox visualization
        if self.show_hitbox:
            pygame.draw.circle(surface, COLORS['highlight'], self.position, 
                             self.hitbox_radius, 2)

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))
