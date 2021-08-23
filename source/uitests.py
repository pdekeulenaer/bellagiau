import arcade
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "It's go time"

SCALING = 2.0


class SpaceShooter(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__( width, height, title)

        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)

        self.player = arcade.Sprite('images/jet.png', SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)

        arcade.schedule(self.add_enemy, 0.25)
        #arcade.schedule(self.add_cloud, 1.0)

    def add_enemy(self, delta_time: float):
        enemy = arcade.Sprite('images/missile.png', SCALING)

        enemy.left = random.randint(self.width, self.height + 80)
        enemy.top = random.randint(10, self.height-10)

        enemy.velocity = (random.randint(-20, -5), 0)

        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

if __name__ == '__main__':
    app = SpaceShooter(800,600,"Testing")
    arcade.run()
