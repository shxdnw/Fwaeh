import pygame
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 120, 255))
        self.rect = self.image.get_rect(center=(640, 600))
        self.pos = Vector2(self.rect.center)
        self.vel = Vector2()
        self.speed = 450
        self.max_health = 100
        self.health = self.max_health
        self.shoot_cooldown = 0
        self.dash_cooldown = 0
        self.dash_duration = 0
        
        # Temporal abilities
        self.temporal_dash = {
            'active': False,
            'duration': 0.2,
            'cooldown': 3.0,
            'speed_mult': 3.5,
            'invulnerable': True
        }

    def update(self, dt):
        self.handle_input(dt)
        self.apply_movement(dt)
        self.update_cooldowns(dt)
        self.handle_dash_state(dt)
        self.handle_shooting(dt)

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        move_vec = Vector2()
        
        if keys[pygame.K_a]:
            move_vec.x -= 1
        if keys[pygame.K_d]:
            move_vec.x += 1
        if keys[pygame.K_w]:
            move_vec.y -= 1
        if keys[pygame.K_s]:
            move_vec.y += 1
            
        if move_vec.length() > 0:
            move_vec.scale_to_length(self.speed * dt * self.game.time_system.get_speed_factor())
            self.vel.update(move_vec)
        else:
            self.vel.update((0, 0))
            
        if keys[pygame.K_LSHIFT]:
            self.activate_temporal_dash()

    def apply_movement(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.rect.clamp_ip(self.game.screen.get_rect())

    def update_cooldowns(self, dt):
        self.shoot_cooldown = max(self.shoot_cooldown - dt, 0)
        self.dash_cooldown = max(self.dash_cooldown - dt, 0)

    def handle_dash_state(self, dt):
        if self.temporal_dash['active']:
            self.dash_duration -= dt
            if self.dash_duration <= 0:
                self.temporal_dash['active'] = False
                self.dash_cooldown = self.temporal_dash['cooldown']

    def handle_shooting(self, dt):
        if pygame.mouse.get_pressed()[0] and self.shoot_cooldown <= 0:
            self.shoot_cooldown = 0.15
            mouse_pos = Vector2(pygame.mouse.get_pos())
            direction = (mouse_pos - self.pos).normalize()
            self.game.spawn_bullet(self.pos, direction * 800, "player")

    def activate_temporal_dash(self):
        if not self.temporal_dash['active'] and self.dash_cooldown <= 0:
            self.temporal_dash['active'] = True
            self.dash_duration = self.temporal_dash['duration']
            self.vel *= self.temporal_dash['speed_mult']
