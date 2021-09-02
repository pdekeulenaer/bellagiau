import arcade
import util
from rider import Rider, BasicRiderAI

# WINDOW SETTINGS
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = arcade.csscolor.LIGHT_BLUE
RIDER_ASSET_SCALING = 0.7
WALL_ASSET_SCALING = 0.5

# TRACK SETTINGS
TRACK_LENGTH_METERS = 400
TRACK_LENGTH_PX = util.get_pixels_from_meters(TRACK_LENGTH_METERS)

# WINDOW VIEWPORT
VP_LEFT_MARGIN = 50
VP_RIGHT_MARGIN = 50
VP_BOTTOM_MARGIN = 100
VP_TOP_MARGIN = 600

# PHYSICS SETTINGS
STARTING_SPEED = util.get_pxspeed_from_kph(50.0)

SPRINT_ACCELERATION_FORCE = 1500
PLAYER_HORIZONTAL_MOVEMENT_SPEED = 200

class RaceLevel(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=False)

        self.player : Rider = None

        self.player_list = None
        self.rider_list = None
        self.wall_list = None

        self.physics = None

        # viewport settings
        self.vp_bottom = 0
        self.vp_left = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.rider_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        self._setup_player()
        self._setup_opponents()
        self._setup_track()

        # self.physics = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.physics = arcade.PymunkPhysicsEngine(damping=1.0, gravity=(0,0))
        self.physics.add_sprite(self.player, damping=1.0, friction=0.0, mass=1, moment=arcade.PymunkPhysicsEngine.MOMENT_INF)
        self.physics.add_sprite_list(self.rider_list, friction=0.1, mass=1, moment=arcade.PymunkPhysicsEngine.MOMENT_INF, body_type=arcade.PymunkPhysicsEngine.DYNAMIC)
        self.physics.add_sprite_list(self.wall_list, friction=0.0, body_type=arcade.PymunkPhysicsEngine.STATIC)

        self._start_movement()

    def _start_movement(self):
        self.physics.apply_impulse(self.player, (0.0, STARTING_SPEED))
        for opp in self.rider_list:
            self.physics.apply_impulse(opp, (0.0, STARTING_SPEED))
        # self.player_sprite.change_y = STARTING_SPEED

    def _setup_player(self):
        self.player = Rider(Rider.PLAYER_IMG, RIDER_ASSET_SCALING)

        # Player positioning on the screen
        self.player.center_x = 150
        self.player.bottom = 128

        self.player_list.append(self.player)

    def _setup_opponents(self):
        for i in range(0,1):
            opp = Rider(Rider.OPPONENT_IMG, RIDER_ASSET_SCALING)
            opp.center_x = ((i+2) * 150)
            opp.bottom = 128
            self.rider_list.append(opp)

            BasicRiderAI(opp)   # automatically registers it on the rider sprite


    def _setup_track(self):
        self._setup_walls()

    def _setup_walls(self):
        wall_size = 64
        img = ":resources:images/tiles/stoneCenter.png"

        for i in range(0, int(TRACK_LENGTH_PX/wall_size) * wall_size, wall_size):
            wall_sprite_l = arcade.Sprite(img, WALL_ASSET_SCALING)
            wall_sprite_l.left = 0
            wall_sprite_l.bottom = i
            self.wall_list.append(wall_sprite_l)

            wall_sprite_r = arcade.Sprite(img, WALL_ASSET_SCALING)
            wall_sprite_r.right = SCREEN_WIDTH
            wall_sprite_r.bottom = i
            self.wall_list.append(wall_sprite_r)

    def _draw_line(self, line_height):
        arcade.draw_line(64, line_height, SCREEN_WIDTH - 64, line_height, arcade.csscolor.LIGHT_GRAY)
        distance_left =  int((1 - (line_height / TRACK_LENGTH_PX)) * TRACK_LENGTH_METERS)
        arcade.draw_text(str(distance_left), 64, line_height, arcade.csscolor.GRAY, 36, font_name="comic" )

    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(self.vp_left, self.vp_bottom, arcade.get_window().width, arcade.get_window().height, BACKGROUND_COLOR)
        arcade.start_render()

        # draw all sprites
        self.player_list.draw()
        self.wall_list.draw()
        self.rider_list.draw()

        # print intermediate lines
        for i in range(0,TRACK_LENGTH_PX,int(TRACK_LENGTH_PX/20)):
            self._draw_line(i)

        # print finish line
        arcade.draw_line(64, TRACK_LENGTH_PX, SCREEN_WIDTH - 64, TRACK_LENGTH_PX, arcade.csscolor.WHITE)
        arcade.draw_line(64, TRACK_LENGTH_PX - 10, SCREEN_WIDTH - 64, TRACK_LENGTH_PX - 10, arcade.csscolor.WHITE)
        arcade.draw_line(64, TRACK_LENGTH_PX - 20, SCREEN_WIDTH - 64, TRACK_LENGTH_PX - 20, arcade.csscolor.WHITE)

    # KEY COMMANDS
    def on_key_press(self, key:int, modifiers:int):
        if (key == arcade.key.LEFT or key == arcade.key.A):
            self.player.move_left()
        if (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player.move_right()
        if (key == arcade.key.SPACE):
            self.player.accelerate()
        if (key == arcade.key.DOWN or key == arcade.key.S):
            self.player.decelerate()

    def on_key_release(self, key: int, modifiers: int):
        velocity = self.physics.get_physics_object(self.player).body.velocity
        self.physics.set_velocity(self.player, (0, velocity.y))
        self.player.clear_forces()

    def on_update(self, delta_time: float):
        self.player.on_update(delta_time)
        self.rider_list.on_update()
        self.physics.step()
        # TODO override physics step() to persist

        print(self.player.get_velocity())
        # viewport update
        changed = False

        top_boundary = self.vp_bottom + SCREEN_HEIGHT - VP_TOP_MARGIN
        if self.player.top > top_boundary:
            self.vp_bottom += self.player.top - top_boundary
            changed = True

        if changed:
            self.vp_bottom = int(self.vp_bottom)
            arcade.set_viewport(self.vp_left, self.vp_left + SCREEN_WIDTH, self.vp_bottom, self.vp_bottom + SCREEN_HEIGHT)

def racelevel():
    game = RaceLevel(SCREEN_WIDTH, SCREEN_HEIGHT, "Test race")
    game.setup()
    arcade.run()


if __name__ == '__main__':
    racelevel()
