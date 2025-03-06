import pygame
from pygame.math import Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, speed, bullet_type):
        super().__init__()
        self.type = bullet_type
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0) if bullet_type == "player" else (255, 0, 0))
        self.rect = self.image.get_rect(center=position)
        self.pos = Vector2(position)
        self.vel = direction * speed
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        # Handle different time states
        time_factor = self.game.time_system.get_speed_factor()
        if self.game.time_system.current_state == TimeState.REWINDING:
            self.pos -= self.vel * dt * abs(time_factor)
        elif self.type == "enemy":
            self.pos += self.vel * dt * time_factor
        else:
            self.pos += self.vel * dt
            
        # Handle skipping state (only projectiles move)
        if self.game.time_system.current_state == TimeState.SKIPPING:
            if self.type == "enemy":
                self.pos += self.vel * dt * 2.0
            else:
                self.pos += self.vel * dt * 0.5
            
        self.rect.center = self.pos
        
        # Auto-remove off-screen bullets
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()

    def apply_temporal_effect(self, current_speed_factor):
        """Handle bullet inheritance during time state changes"""
        if self.type == "enemy":
            self.vel = self.vel.normalize() * (self.vel.length() * current_speed_factor)