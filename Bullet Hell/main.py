import pygame
import sys
from config import GAME_CONFIG, COLORS
from player import Player
from boss import Boss
from bullet_manager import BulletManager
from time_manager import TimeManager
from hud import HUD

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (GAME_CONFIG['screen_width'], GAME_CONFIG['screen_height'])
        )
        pygame.display.set_caption("Temporal Bullet Hell")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.paused = False
        
        # Initialize game systems
        self.bullet_manager = BulletManager()
        self.player = Player()
        self.boss = Boss(self.bullet_manager)
        self.time_manager = TimeManager()
        self.hud = HUD(self.time_manager)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.ACTIVEEVENT:
                if event.gain == 0:  # Window lost focus
                    self.paused = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_h:
                    self.player.show_hitbox = not self.player.show_hitbox

    def update(self):
        if not self.paused:
            self.dt = self.clock.tick(60)
            time_scale = self.time_manager.get_time_scale()
            
            self.player.update(self.dt)
            self.boss.update(self.dt, self.time_manager.current_state)
            self.bullet_manager.update(self.dt * time_scale, time_scale)
            self.time_manager.update(self.dt, {
                'boss': self.boss,
                'bullets': self.bullet_manager
            })

    def draw(self):
        self.screen.fill(COLORS['background'])
        self.bullet_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.boss.draw(self.screen)
        self.hud.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()