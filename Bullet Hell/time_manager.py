import pygame
import json
from config import TIME_STATES, COLORS, UI_CONFIG

class TimeManager:
    def __init__(self):
        self.current_state = 'normal'
        self.state_history = []
        self.game_snapshots = []
        self.state_transition_cooldown = 0
        self.energy = 100.0
        self.last_state_change = 0
        
        self.time_scales = {
            'normal': 1.0,
            'stopped': 0.0,
            'slowed': 0.3,
            'sped_up': 1.7,
            'reverting': 0.0,
            'skipping': 0.0
        }
        
        self.cooldowns = {
            'normal': 0,
            'stopped': 5,
            'slowed': 3,
            'sped_up': 4,
            'reverting': 10,
            'skipping': 8
        }

        self.energy_costs = {
            'normal': 0,
            'stopped': 15,
            'slowed': 8,
            'sped_up': 12,
            'reverting': 40,
            'skipping': 30
        }

    def create_snapshot(self, game_objects):
        """Capture current game state for reversion"""
        return {
            'boss': game_objects['boss'].get_state(),
            'bullets': game_objects['bullets'].get_state(),
            'time': pygame.time.get_ticks()
        }

    def set_state(self, new_state, game_objects=None):
        if (pygame.time.get_ticks() - self.last_state_change > 
            self.cooldowns[self.current_state] * 1000 and
            self.energy > self.energy_costs[new_state]):
            
            if new_state in ['reverting', 'skipping'] and game_objects:
                self.handle_temporal_shift(new_state, game_objects)
                
            self.current_state = new_state
            self.last_state_change = pygame.time.get_ticks()
            self.state_history.append(new_state)
            self.energy = max(0, self.energy - self.energy_costs[new_state])

    def handle_temporal_shift(self, state_type, game_objects):
        """Handle revert/skip temporal displacement"""
        if state_type == 'reverting' and len(self.game_snapshots) >= 5:
            game_objects['boss'].set_state(self.game_snapshots[-5]['boss'])
            game_objects['bullets'].set_state(self.game_snapshots[-5]['bullets'])
        elif state_type == 'skipping':
            # Fast-forward simulation would go here
            pass

    def get_time_scale(self):
        return self.time_scales[self.current_state]

    def update(self, dt, game_objects=None):
        # Maintain rolling 5 second snapshot buffer
        if self.current_state == 'normal':
            if pygame.time.get_ticks() % 1000 == 0:  # Save snapshot every second
                self.game_snapshots.append(self.create_snapshot(game_objects))
                if len(self.game_snapshots) > 5:
                    self.game_snapshots.pop(0)

        # Update energy based on current state
        self.energy += (-self.energy_costs[self.current_state] * dt / 1000 
                       if self.current_state != 'normal' else 2)  # Regen in normal
        self.energy = max(0, min(100, self.energy))

    def draw_ui(self, surface):
        # Existing UI drawing code with added states
        state_colors = COLORS.copy()
        # ... (previous UI implementation)
        # Add new state buttons
        for i, state in enumerate(TIME_STATES):
            # Adjust button positions for 6 states
            rect = pygame.Rect(
                10 + i*70 if i < 4 else 10 + (i-4)*70,
                UI_CONFIG['state_buttons_y'] if i < 4 else UI_CONFIG['state_buttons_y'] + 40,
                60,
                30
            )
            # ... rest of drawing logic