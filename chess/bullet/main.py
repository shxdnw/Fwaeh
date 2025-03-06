import pygame
import sys
from pygame.math import Vector2
from boss import Boss
from player import Player
from time_system import TimeState, TimeSystem
from bullet import Bullet

class BulletHellGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        
        # Time system initialization
        self.time_system = TimeSystem()
        self.global_speed = 1.0
        
        # Game entities
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(self)
        self.boss = Boss(self)
        
        # Time distortion surface
        self.distortion_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)

    def run(self):
        while True:
            # Handle time dilation
            dt = self.clock.tick(60) * 0.001
            self.time_system.update(dt)
            self.global_speed = self.time_system.get_speed_factor()
            
            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_time_controls(event)
            
            # Update game state
            self.all_sprites.update(dt)
            self.check_collisions()
            
            # Rendering
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            self.apply_time_distortion()
            pygame.display.flip()

    def handle_time_controls(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.time_system.set_state(TimeState.NORMAL)
            elif event.key == pygame.K_2:
                self.time_system.set_state(TimeState.STOPPED)
            elif event.key == pygame.K_3:
                self.time_system.set_state(TimeState.SLOWED)
            elif event.key == pygame.K_4:
                self.time_system.set_state(TimeState.SPED_UP)
            elif event.key == pygame.K_5:
                self.time_system.set_state(TimeState.SKIPPING)
            elif event.key == pygame.K_6:
                self.time_system.set_state(TimeState.REWINDING)

    def check_collisions(self):
        # Player bullets vs boss
        for bullet in pygame.sprite.spritecollide(self.boss, self.bullets, True):
            if bullet.type == "player":
                self.boss.take_damage(10)
        
        # Enemy bullets vs player
        for bullet in pygame.sprite.spritecollide(self.player, self.bullets, True):
            if bullet.type == "enemy" and not self.player.temporal_dash['invulnerable']:
                self.player.health -= 20

    def spawn_bullet(self, pos, vel, bullet_type="enemy"):
        bullet = Bullet(pos, vel, 600, bullet_type)
        bullet.game = self  # Add game reference
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def apply_time_distortion(self):
        # Basic visual effect placeholder
        if self.time_system.current_state != TimeState.NORMAL:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
            color = {
                TimeState.STOPPED: (100, 100, 255, 50),
                TimeState.SLOWED: (255, 150, 50, 75),
                TimeState.SPED_UP: (50, 255, 50, 25)
            }[self.time_system.current_state]
            overlay.fill(color)
            self.screen.blit(overlay, (0, 0))

if __name__ == "__main__":
    game = BulletHellGame()
    game.run()