import pygame
from enum import Enum

class TimeState(Enum):
    NORMAL = 1
    STOPPED = 2
    SLOWED = 3
    SPED_UP = 4
    SKIPPING = 5
    REWINDING = 6

class TimeSystem:
    def __init__(self):
        self.current_state = TimeState.NORMAL
        self.state_transitions = {
            TimeState.NORMAL: {
                'switched': pygame.time.get_ticks(),
                'cooldown': 0
            }
        }
        self.energy = 100.0
        self._last_update = pygame.time.get_ticks()
        
        # Time modulation parameters
        self.speed_factors = {
            TimeState.NORMAL: 1.0,
            TimeState.STOPPED: 0.0,
            TimeState.SLOWED: 0.3,
            TimeState.SPED_UP: 2.5,
            TimeState.SKIPPING: 1.0,  # Only affects projectiles
            TimeState.REWINDING: -0.5  # Negative for reverse time
        }
        
        # Cooldown constraints
        self.cooldowns = {
            TimeState.STOPPED: 8.0,
            TimeState.SLOWED: 3.0,
            TimeState.SPED_UP: 5.0,
            TimeState.SKIPPING: 4.0,
            TimeState.REWINDING: 10.0
        }

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        delta = (current_time - self._last_update) * 0.001
        self._last_update = current_time
        
        # Energy regeneration/drain logic
        if self.current_state == TimeState.NORMAL:
            self.energy = min(self.energy + 15.0 * delta, 100.0)
        else:
            energy_cost = {
                TimeState.STOPPED: 25.0,
                TimeState.SLOWED: 12.0,
                TimeState.SPED_UP: 18.0
            }[self.current_state]
            self.energy = max(self.energy - energy_cost * delta, 0.0)
            
            if self.energy <= 0:
                self.set_state(TimeState.NORMAL)

        # Update cooldowns
        for state in self.state_transitions.values():
            if state['cooldown'] > 0:
                state['cooldown'] = max(state['cooldown'] - delta, 0)

    def set_state(self, new_state):
        if new_state == self.current_state:
            return

        current_time = pygame.time.get_ticks()
        if new_state != TimeState.NORMAL:
            cooldown = self.state_transitions.get(new_state, {}).get('cooldown', 0)
            if cooldown > 0:
                return

        self.current_state = new_state
        self.state_transitions[new_state] = {
            'switched': current_time,
            'cooldown': self.cooldowns.get(new_state, 0)
        }

    def get_speed_factor(self):
        return self.speed_factors[self.current_state]

    def get_energy_ratio(self):
        return self.energy / 100.0

    def can_activate(self, state):
        if state == TimeState.NORMAL:
            return True
        transition = self.state_transitions.get(state, {})
        return transition.get('cooldown', 0) <= 0
