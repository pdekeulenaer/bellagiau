# import pyglet
# import pyglet.gl as gl
#
# win = pyglet.window.Window(width = 600, height = 400, caption = "Hello world")
# win.set_location(100, 100)
# gl.glClearColor(1, 0, 0, 0.5)
#
# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=36,
#                           x=win.width//2, y=win.height//2,
#                           anchor_x='center', anchor_y='center')
#
# @win.event
# def on_draw():
#     win.clear()
#     label.draw()
#
# pyglet.app.run()

import arcade
import pyglet.gl as gl

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"

class Testgame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        arcade.set_background_color(arcade.color.RED)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_xywh_rectangle_filled(0,0,SCREEN_WIDTH, SCREEN_HEIGHT,arcade.color.RED)
        arcade.draw_circle_filled(200,200,100,arcade.csscolor.TAN)

def main():
    game = Testgame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == '__main__':
    main()