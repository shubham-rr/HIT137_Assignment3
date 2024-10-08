# jump.py

class JumpMechanics:
    def __init__(self):
        self.jump_speed = -15
        self.gravity = 1
        self.velocity_y = 0
        self.jump_hold_time = 0
        self.max_jump_hold_time = 15
        self.coyote_time = 0.1  # Coyote time duration in seconds
        self.coyote_timer = 0
        self.jump_buffer_time = 0.1  # Jump buffer duration in seconds
        self.jump_buffer_timer = 0
        self.terminal_velocity = 20  # Maximum falling speed

    def apply_gravity(self):
        self.velocity_y += self.gravity

    def increase_falling_speed(self):
        if self.velocity_y > 0:
            self.velocity_y += self.gravity  # Increase gravity effect

    def cap_falling_speed(self):
        if self.velocity_y > self.terminal_velocity:
            self.velocity_y = self.terminal_velocity

    def reset_jump_timers(self):
        self.jump_hold_time = 0
        self.coyote_timer = self.coyote_time
        self.jump_buffer_timer = 0

