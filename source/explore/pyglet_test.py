import pyglet

window = pyglet.window.Window()


label = pyglet.text.Label("Hello World")

pyglet.gl.glClearColor(0,0,1,0)

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()