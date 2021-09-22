# Useful links:
# https://kivy.org/doc/stable/tutorials/pong.html

from kivy.app import App
from random import randint
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty


class PongBall(Widget):

    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referenceList property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):

        # The Vector represents a 2D vector (x, y).
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):

    # Add an ObjectProperty to the PongGame class, and hook it up to the widget created in the kv rule
    ball = ObjectProperty(None)

    def serveBall(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def updatePosition(self, dt):
        self.ball.move()

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1


class MyApp(App):
    def build(self):
        game = PongGame()
        game.serveBall()

        # https://kivy.org/doc/stable/tutorials/pong.html#scheduling-functions-on-the-clock
        Clock.schedule_interval(game.updatePosition, 1.0/60.0)

        return game


if __name__ == '__main__':
    MyApp().run()
