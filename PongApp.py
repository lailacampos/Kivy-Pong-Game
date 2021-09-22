# Useful links:
# https://kivy.org/doc/stable/tutorials/pong.html

from kivy.app import App
from random import randint
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounceBall(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            ballVelocity = bounced * 1.1
            ball.velocity = ballVelocity.x, ballVelocity.y + offset


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
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def serveBall(self, vel=(4, 0)):
        self.ball.center = self.center
        # self.ball.velocity = vel
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounceBall(self.ball)
        self.player2.bounceBall(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        # TODO Fix bug where player 2's score doesn't update
        # Scoring points
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serveBall(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serveBall(vel=(-4, 0))


class MyApp(App):
    def build(self):
        game = PongGame()
        game.serveBall()

        # https://kivy.org/doc/stable/tutorials/pong.html#scheduling-functions-on-the-clock
        Clock.schedule_interval(game.update, 1.0 / 60.0)

        return game


if __name__ == '__main__':
    MyApp().run()
