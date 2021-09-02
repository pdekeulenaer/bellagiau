import arcade.physics_engines
import numpy as np


class CyclePhysicsEngine(arcade.PymunkPhysicsEngine):
    def __init__(self, gravity=0.0, damping=0.0):
        super().__init__(self, gravity, damping)

    def add_sprite(self, sprite, mass=1.0, friction=0.0, body_type=arcade.PymunkPhysicsEngine.DYNAMIC, moment=arcade.PymunkPhysicsEngine.MOMENT_INF):
        super().add_sprite(sprite, mass=mass, friction=friction, body_type=body_type, moment=moment)

    def add_sprite_list(self, sprite_list, mass=1.0, friction=0.0, body_type=arcade.PymunkPhysicsEngine.DYNAMIC):
        super().add_sprite_list(sprite_list, mass=mass, friction=friction, body_type=body_type)

    def step(self):
        super().step()

    def get_velocity(self, sprite):
        self.get_physics_object(sprite).body.velocity

    ### DEFAULT DRAG MECHANICS

class PhysicsForces():


    @staticmethod
    def get_net_wind_velocity(direction, wind):
        """
        Computes the net wind velocity in the direction of travel.
        :param tuple direction: A tuple (x,y) representing the vector along which we want to normalize wind speed
        :param tuple wind: A tuple (x,y) representing the wind speed
        """
        v = np.array(direction)
        u = np.array(wind)

        v_norm = (np.sqrt(sum(v**2)))
        projection = (np.dot(u,v)/v_norm**2)*v

        return projection

    @staticmethod
    def net_force(drag_coeff, rider_velocity, wind_velocity, density=1.0):
        """
        Computes the net drag force applied on a cyclist, returns a float representing the force in the direction of travel
        All parameters assume the net speeds in the direction of travel
        """
        net_velocity = (rider_velocity - wind_velocity)
        return PhysicsForces.drag_force(drag_coeff, net_velocity, density)


    @staticmethod
    def drag_force(drag_coeff, velocity, density=1.0):
        """
        Computes a drag force taking into account velocity, a drag coefficient and medium density
        F = (drag coeff * medium_density * velocity^2) / 2

        :param float drag_coeff: A float representing the drag coefficient, combining the surface area A and coefficient Cd
        :param float velocity: Current net velocity
        :param float density: Density of medium through which we are moving
        """
        return (drag_coeff * density * velocity **2)/2

