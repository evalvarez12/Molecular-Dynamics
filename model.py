import physics

class system:
    def __init__(self,
                 initial_pos,
                 initial_vel,
                 box_size,
                 evolution,
                 interaction):
        self.state_pos = initial_pos
        self.state_vel = initial_vel
        self.N = len(initial_pos)
        self.evolution = evolution
        self.box_size = box_size
        self.interaction = interaction
        self.time = 0

    def step(self, dt):
        self.time += dt
        # find interaction forces
        f = physics.find_force(self.interaction, self.state_pos)

        # update state
        self.state_pos, self.state_vel = self.evolution(self.state_pos, self.state_vel, f, dt)

        # correct position for box_size
        self.state_pos = self.state_pos % self.box_size
