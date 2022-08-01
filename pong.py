"""
Dilyana Koleva, August 2022
Pong Game with turtle
"""

# Turtle module is great with graphics and especially for starting with game development
import os
import turtle
import winsound

window = turtle.Screen()
window.title("Pong")
window.bgpic("bg.gif")
window.setup(width=800, height=600)

# Stops the window from updating / Speeds up the game
window.tracer(0)

# Score
score_a = 0
score_b = 0

# Left Paddle
left = turtle.Turtle()
left.speed(0)
left.shape("square")
left.color("black")
left.shapesize(stretch_wid=5, stretch_len=1)
left.penup()
left.goto(-350, 0)

# Right Paddle
right = turtle.Turtle()
right.speed(0)
right.shape("square")
right.color("black")
right.shapesize(stretch_wid=5, stretch_len=1)
right.penup()
right.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("black")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.2
ball.dy = -0.2


# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0    Player B: 0", align="center", font=("Courier", 24, "bold"))


# Function to move left paddle
def left_paddle_up():
    y = left.ycor()
    y += 20
    left.sety(y)


def left_paddle_down():
    y = left.ycor()
    y -= 20
    left.sety(y)


# Functions to move right paddle
def right_paddle_up():
    y = right.ycor()
    y += 20
    right.sety(y)


def right_paddle_down():
    y = right.ycor()
    y -= 20
    right.sety(y)


# Keyboard bindings
window.listen()
window.onkeypress(left_paddle_up, "w")
window.onkeypress(left_paddle_down, "s")
window.onkeypress(right_paddle_up, "Up")
window.onkeypress(right_paddle_down, "Down")

# Main Game Loop
while True:
    window.update()

    # Move ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Top and Bottom Border
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    elif ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    # Left and Right Border
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player A: {}    Player B: {}".format(score_a, score_b), align="center",
                  font=("Courier", 24, "bold"))

    elif ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player A: {}    Player B: {}".format(score_a, score_b), align="center",
                  font=("Courier", 24, "bold"))

    if (340 < ball.xcor() < 350) and right.ycor() + 50 > ball.ycor() > right.ycor() - 50:
        ball.setx(340)
        ball.dx *= -1

    # Left Paddle and ball collisions
    if (-350 < ball.xcor() < -340) and left.ycor() + 50 > ball.ycor() > left.ycor() - 50:
        ball.setx(-340)
        ball.dx *= -1

    # Right Paddle and ball collisions
    elif (340 < ball.xcor() < 350) and right.ycor() + 50 > ball.ycor() > right.ycor() - 50:
        ball.setx(340)
        ball.dx *= -1
