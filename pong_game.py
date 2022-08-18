"""
Dilyana Koleva, August 2022
Pong game with PyGame
"""
import pygame

# Initialise game
pygame.init()

# Adjust width and height
width, height = 700, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

frame_per_second = 60

white = (255, 255, 255)
black = (0, 0, 0)

paddle_width, paddle_height = 20, 100
# Size of the ball
ball_radius = 10

font_score = pygame.font.SysFont("comicsans", 50)
winning_score = 10


class Paddle:
    colour = white
    velocity = 4

    # Initialize paddle
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    # Draw paddle as a rect
    def draw(self, window):
        pygame.draw.rect(
            window, self.colour, (self.x, self.y, self.width, self.height))

    # Move paddle by changing the velocity
    # If up = True : move upwards
    # Else : move downwards
    def move(self, up=True):
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    # Resets
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    max_velocity = 5
    colour = white

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.max_velocity
        self.y_vel = 0

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


# Draws screen and adds elements to it
def draw(window, paddles, ball, left_score, right_score):
    # Fills window with black colour
    window.fill(black)

    # Adds text/labels to window
    left_score_text = font_score.render(f"{left_score}", 1, white)
    right_score_text = font_score.render(f"{right_score}", 1, white)
    window.blit(left_score_text, (width // 4 - left_score_text.get_width() // 2, 20))
    window.blit(right_score_text, (width * (3 / 4) -
                                   right_score_text.get_width() // 2, 20))

    # Draws paddle on screen
    for paddle in paddles:
        paddle.draw(window)

    # Draws the dotted line in the centre
    for i in range(10, height, height // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, white, (width // 2 - 5, i, 10, height // 20))

    # Draws ball on screen
    ball.draw(window)
    pygame.display.update()


def collision(ball, left_paddle, right_paddle):
    # Checks if the ball hits the ceiling of the screen
    if ball.y + ball.radius >= height:
        ball.y_vel *= -1
    # Checks if the ball hits the floor of the screen
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Checks if the ball is colliding with the left paddle
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.max_velocity
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    # Checks if the ball is colliding with the right paddle
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.max_velocity
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


# Handles the movement of both paddles
def paddle_movement(keys, left_paddle, right_paddle):

    # if key W is pressed: move left paddle up
    # Ensure that the paddle doesn't go off screen
    if keys[pygame.K_w] and left_paddle.y - left_paddle.velocity >= 0:
        left_paddle.move(up=True)

    # if key S is pressed: move left paddle down
    # Ensure that the paddle doesn't go off screen
    if keys[pygame.K_s] and left_paddle.y + left_paddle.velocity + left_paddle.height <= height:
        left_paddle.move(up=False)

    # if key UP is pressed: move right paddle up
    # Ensure that the paddle doesn't go off screen
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.velocity >= 0:
        right_paddle.move(up=True)

    # if key DOWN is pressed: move right paddle down
    # Ensure that the paddle doesn't go off screen
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.velocity + right_paddle.height <= height:
        right_paddle.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()

    # Adjusts the left paddle size/position
    left_paddle = Paddle(10, height // 2 - paddle_height //
                         2, paddle_width, paddle_height)
    # Adjust the right paddle size/position
    right_paddle = Paddle(width - 10 - paddle_width, height //
                          2 - paddle_height // 2, paddle_width, paddle_height)
    # Adjusts ball size/position
    ball = Ball(width // 2, height // 2, ball_radius)

    # Sets initial score for both paddles
    left_score = 0
    right_score = 0

    while run:
        clock.tick(frame_per_second)
        # Draws elements to the screen
        draw(window, [left_paddle, right_paddle], ball, left_score, right_score)

        # Safe exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Adds keyboard event
        keys = pygame.key.get_pressed()
        paddle_movement(keys, left_paddle, right_paddle)

        # Moves the ball
        ball.move()
        collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > width:
            left_score += 1
            ball.reset()

        # Ensures the game can be won
        won = False
        if left_score >= winning_score:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= winning_score:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = font_score.render(win_text, 1, white)
            window.blit(text, (width // 2 - text.get_width() //
                               2, height // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

if __name__ == '__main__':
    main()
