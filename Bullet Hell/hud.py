import pygame
from pygame.math import Vector2
from config import COLORS, UI_CONFIG, TIME_STATES

class HUD:
    def __init__(self, time_manager):
        self.time_manager = time_manager
        self.font = pygame.font.Font(None, 24)
        self.energy_bar_rect = pygame.Rect(
            UI_CONFIG['energy_bar_x'],
            UI_CONFIG['energy_bar_y'],
            UI_CONFIG['energy_bar_width'],
            UI_CONFIG['energy_bar_height']
        )
        self.state_buttons = []
        
        # Initialize state buttons
        button_size = 60
        start_x = 20
        for i, state in enumerate(TIME_STATES):
            self.state_buttons.append({
                'rect': pygame.Rect(
                    start_x + i*(button_size + 10),
                    UI_CONFIG['state_buttons_y'],
                    button_size,
                    30
                ),
                'state': state
            })

    def draw(self, surface):
        self._draw_energy_bar(surface)
        self._draw_state_buttons(surface)
        self._draw_cooldowns(surface)

    def _draw_energy_bar(self, surface):
        # Background
        pygame.draw.rect(surface, COLORS['hud_background'], self.energy_bar_rect)
        
        # Animated fill
        fill_width = UI_CONFIG['energy_bar_width'] * (self.time_manager.energy/100)
        fill_rect = pygame.Rect(
            self.energy_bar_rect.left,
            self.energy_bar_rect.top,
            fill_width,
            self.energy_bar_rect.height
        )
        pygame.draw.rect(surface, COLORS['energy_bar'], fill_rect)
        
        # Border
        pygame.draw.rect(surface, COLORS['highlight'], self.energy_bar_rect, 2)

    def _draw_state_buttons(self, surface):
        current_time = pygame.time.get_ticks()
        for btn in self.state_buttons:
            # Button base
            color = COLORS[f'ui_{btn["state"]}']
            if btn['state'] == self.time_manager.current_state:
                color = pygame.Color(color).lerp(COLORS['highlight'], 0.3)
            
            pygame.draw.rect(surface, color, btn['rect'])
            
            # Cooldown overlay
            cooldown_left = self.time_manager.cooldowns[btn['state']] - \
                           (current_time - self.time_manager.last_state_change)/1000
            if cooldown_left > 0:
                overlay_height = btn['rect'].height * (cooldown_left/self.time_manager.cooldowns[btn['state']])
                overlay_rect = pygame.Rect(
                    btn['rect'].left,
                    btn['rect'].top,
                    btn['rect'].width,
                    overlay_height
                )
                pygame.draw.rect(surface, COLORS['cooldown_active'], overlay_rect)

    def _draw_cooldowns(self, surface):
        # Draw numeric timers
        for i, btn in enumerate(self.state_buttons):
            cooldown_left = self.time_manager.cooldowns[btn['state']] - \
                           (pygame.time.get_ticks() - self.time_manager.last_state_change)/1000
            if cooldown_left > 0:
                text = self.font.render(f"{cooldown_left:.1f}", True, COLORS['highlight'])
                surface.blit(text, (btn['rect'].centerx - 15, btn['rect'].bottom + 5))
