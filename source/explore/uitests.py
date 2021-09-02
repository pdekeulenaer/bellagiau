import arcade
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Race test"

BACKGROUND_COLOR = arcade.csscolor.LIGHT_BLUE

SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20
GRAVITY = 1

# Viewport settings
LEFT_VP_MARGIN = 250
RIGHT_VP_MARGIN = 250
BOTTOM_VP_MARGIN = 50
TOP_VP_MARGIN = 100


class BellaGiau(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__( width, height, title, resizable=True)
        self.player_list = None
        self.wall_list = None
        self.coin_list = None

        self.player_sprite = None

        self.physics = None

        self.view_bottom = 0
        self.view_left = 0


    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self._setup_player()
        self._setup_walls()

        self.physics = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)


    def _setup_player(self):
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, SCALING)
        self.player_sprite.center_x = 32
        self.player_sprite.bottom = 64
        self.player_list.append(self.player_sprite)
        return self.player_sprite

    def _setup_walls(self):
        wall_size = 64
        image_source = ":resources:images/tiles/grassMid.png"
        # wall_sprite.bottom = 0
        for i in range(0, 20*wall_size, wall_size):
            wall_sprite = arcade.Sprite(image_source, SCALING)
            wall_sprite.left = i
            wall_sprite.bottom = 0
            self.wall_list.append(wall_sprite)

    def on_draw(self):
        arcade.draw_xywh_rectangle_filled(self.view_left, self.view_bottom, arcade.get_window().width, arcade.get_window().height, BACKGROUND_COLOR)
        #TODO - small hack to manually clear screen every time, fix this in final version

        arcade.start_render()
        # draw all sprites
        self.player_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key: int, modifiers: int):
        if (key == arcade.key.LEFT or key == arcade.key.A):
            # move left
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        if (key == arcade.key.RIGHT or key == arcade.key.D):
            # move right
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        if (key == arcade.key.SPACE or key == arcade.key.UP):
            self.player_sprite.change_y = PLAYER_JUMP_SPEED




    def on_update(self, delta_time: float):
        self.physics.update()

        # check to move the viewport
        changed = False
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VP_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            arcade.set_viewport(self.view_left, SCREEN_WIDTH+self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)




if __name__ == '__main__':
    app = BellaGiau(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()
    arcade.run()
