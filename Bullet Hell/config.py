# Core configuration with proper initializations
TIME_STATES = ['normal', 'stopped', 'slowed', 'sped_up', 'reverting', 'skipping']

COLORS = {
    'background': (15, 15, 25),
    'player': (80, 180, 255),
    'boss': (255, 80, 110),
    'bullet_normal': (255, 255, 180),
    'bullet_time_affected': (180, 220, 255),
    'energy_bar': (40, 210, 140),
    'ui_normal': (200, 200, 200),
    'ui_stopped': (160, 80, 200),
    'ui_slowed': (80, 160, 240),
    'ui_sped_up': (240, 160, 80),
    'ui_reverting': (140, 80, 160),
    'ui_skipping': (80, 200, 160),
    'highlight': (255, 255, 100),
    'hud_background': (30, 30, 45, 200),
    'cooldown_ready': (80, 200, 120),
    'cooldown_active': (200, 80, 80)
}

GAME_CONFIG = {
    'screen_width': 1280,
    'screen_height': 720,
    'max_bullets': 2000,
    'player_speed': 500,
    'boss_phase_duration': 30,
    'player_accel': 1200,
    'player_decel': 800,
    'bullet_speed': 400,
    'bullet_trail_length': 8,
    'screen_shake_intensity': 2.5,
    'hazard_spawn_rate': 2.0
}

UI_CONFIG = {
    'energy_bar_x': 20,
    'energy_bar_y': 20,
    'energy_bar_width': 200,
    'energy_bar_height': 15,
    'state_buttons_y': 50,
    'hud_padding': 10,
    'cooldown_radius': 12,
    'cooldown_spacing': 25,
    'hazard_warning_color': (255, 80, 80),
    'boss_rest_timer_y': 80
}
