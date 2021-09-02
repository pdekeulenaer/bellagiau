import arcade
import util
from pymunk.vec2d import Vec2d

class RiderAttributes():
    SPRINT_ACCELERATION = util.get_pixels_from_meters(2)
    BREAK_ACCELERATION = -util.get_pixels_from_meters(2.5)

    AERO_EFFICIENCY = 100.0

    MAX_SPEED = util.get_pxspeed_from_kph(75.0)

    STRAFE_SPEED = 200.0

class Rider(arcade.Sprite):

    PLAYER_IMG = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
    OPPONENT_IMG = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"

    def __init__(self, sprite_image_source, sprite_scaling):
        super().__init__(sprite_image_source, sprite_scaling)
        self.attributes = RiderAttributes()
        self.physics : arcade.PymunkPhysicsEngine = None

        self.active_forces = []

        self.ai: BasicRiderAI = None

    def get_velocity(self):
        return self.physics.get_physics_object(self).body.velocity

    def register_ai(self, ai):
        self.ai = ai

    # Physics engine properties
    def accelerate(self, sticky=True):
        force = (0, self.attributes.SPRINT_ACCELERATION)
        self.apply_force(force, sticky)

    def decelerate(self, sticky=True):
        force = (0, self.attributes.BREAK_ACCELERATION)
        self.apply_force(force, sticky)

    def move_left(self):
        self._move_force_speed_x(-self.attributes.STRAFE_SPEED)

    def move_right(self):
        self._move_force_speed_x(self.attributes.STRAFE_SPEED)

    def move_steady(self):
        self._move_force_speed_x(0)

    def apply_force(self, force, sticky):
        self.physics.apply_force(self, force)
        if sticky:
            self.active_forces.append(force)

    def clear_forces(self):
        self.active_forces.clear()

    def _move_force_speed_x(self, velocity_x):
        current_velocity = self.physics.get_physics_object(self).body.velocity
        self.physics.set_velocity(self, (velocity_x, current_velocity.y))

    def persist_forces(self):
        """
        Temp workaround to keep forces alive during a key press
        """
        for f in self.active_forces:
            self.apply_force(f, sticky=False)
            #Using false as sticky param to avoid continuously adding the force

    def register_physics_engine(self, physics_engine):
        super().register_physics_engine(physics_engine)
        self.physics = physics_engine

    # FOLLOW
    def draft(self, other_rider: arcade.Sprite):
        """
        Stay close behind another rider; make small steering adjustments to stay drafting
        1. check if you are in drafting territory, if not, fail and set state to "not drafting"
        2. Check distance vector to center of other guy
        3. Accelerate / decelerate / steer to move yourself right behind other guy
        4. Set player state to "drafting"

        :param other_rider arcade.Sprite: The other rider this rider wants to follow
        """
        pass

    def on_update(self, delta_time: float = 1/60):
        super().on_update(delta_time)
        self.persist_forces()

        if self.ai:
            self.ai.update()


class BasicRiderAI():
    def __init__(self, rider):
        self.rider = rider
        rider.register_ai(self)
        self.sprinting = False

    def update(self):
        # hardcoded AI - moves to the right on 500m, and starts sprinting on 200m
        print("AI UPDATE CALLED")
        print(self.rider.get_velocity().y)
        y_turn = util.get_pixels_from_meters(100)
        x_turn= 550.0
        tolerance = 50.0

        y_sprint = util.get_pixels_from_meters(250)

        if (self.rider.center_y >= y_turn):
            x_dist = self.rider.center_x - x_turn
            if abs(x_dist) <= tolerance:
                self.rider.move_steady()
            elif x_dist > 0:
                self.rider.move_left()
            elif x_dist < 0:
                self.rider.move_right()

        if (self.rider.center_y >= y_sprint):
            # we are now in sprinting range
            if self.rider.get_velocity().y < self.rider.attributes.MAX_SPEED:
                self.rider.accelerate(sticky=False)
