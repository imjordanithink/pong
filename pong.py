import pygame
pygame.init()
pygame.font.init()

# creation of the window
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# creation of window caption
pygame.display.set_caption("Pong")
FPS = 60
MAIN_FONT = pygame.font.SysFont("arial", 70)
# creation of MAIN LOOP or EVENT LOOP of the program wich displays the window and then draws something on it.

# creation of draw() fuction. this is responsible for putting everything on the screen. note that it is being defined on the global scope
# rgb values are being defined as constants for simplicity and readability.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

class Paddle:
    COLOR = WHITE

    def __init__(self, x, y, width, height):
        # self.original_x and self.original_y are going to be assigned the value of the original x and y values and store them in their variable names: self.original_x and _y
        # self.original_x and _y do not change when we change the value of self.x and self.y.
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    # draw function of the Paddle class. When we draw a rectangle (.rect) the input needed is the window we are drawing on, a color and then the coordinates for the rectangle.
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    COLOR = WHITE
    MAX_VEL = 5
    # the x or horizontal movement of the ball will always be the same that is why it is at a speed of MAX_VEL. The y velocity will change based on how the paddle
    # hits the ball.

    # self.original_x and self.original_y are going to be assigned the value of the original x and y values and store them in their variable names: self.original_x and _y
    # self.original_x and _y do not change when we change the value of self.x and self.y.
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def handle_collision(ball, right_paddle, left_paddle):
    # collision of the roof and ball
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height /2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height /2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

POINT_FONT = pygame.font.SysFont("arial", 30)




def draw(win, paddles, ball, left_score, right_score):
    # filling in the screen with black
    win.fill(BLACK)

    
    left_score_count = POINT_FONT.render("{score}".format(score = left_score), 1, WHITE)
    right_score_count = POINT_FONT.render("{score}".format(score = right_score), 1, WHITE)

    WIN.blit(left_score_count, (WIDTH//4 - left_score_count.get_width()//2, 20))
    WIN.blit(right_score_count, (WIDTH*(3/4) - right_score_count.get_width()//2, 20))

    #drawing the ball
    ball.draw(win)
    
    #drawing the paddles
    for paddle in paddles:
        paddle.draw(win)
    
    # drawing the spotted center line
    for i in range(10, HEIGHT, HEIGHT//24):
        if i % 2 ==1:
            pygame.draw.rect(win, WHITE, (WIDTH//2 - 2, i, 5, HEIGHT//24))
                                                   
    # in order to actually draw on the screen, the display must update. we will be updating at the speed of the FPS
    pygame.display.update()


#pause = False

#def pause_menu():
    #pause_text = MAIN_FONT.render("PAUSED", 1, WHITE)
    #while pause == True:
       # WIN.fill(BLACK)
        #WIN.blit(pause_text, (WIDTH/2 - pause_text.get_width()/2, HEIGHT//2 - 30))
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_ESCAPE]:
            #pause = False
        
        
def main():
    clock = pygame.time.Clock()
    run = True
    
    WINNING_SCORE = 10

    player_vel = 6

    ball = Ball(WIDTH//2, HEIGHT // 2 , BALL_RADIUS )
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    # MAIN LOOP handles everything going on in our game constantley such as collision.
    left_score = 0
    right_score = 0

    while run == True:
        # every time clock.tick(FPS) is ran, draw() is also ran. we run at 60fps
        clock.tick(FPS)
        
        # calling the draw() function so the display actually shows our objects and other elements. class objects must be in the draw() parameters.
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB] and left_paddle.y - player_vel > 0: #left UP
            left_paddle.y -= player_vel
        if keys[pygame.K_CAPSLOCK] and left_paddle.y + player_vel + PADDLE_HEIGHT < HEIGHT: #left DOWN
            left_paddle.y += player_vel
        if keys[pygame.K_BACKSLASH] and right_paddle.y - player_vel > 0: #right UP
            right_paddle.y -= player_vel
        if keys[pygame.K_RETURN] and right_paddle.y + player_vel + PADDLE_HEIGHT < HEIGHT: #right DOWN
            right_paddle.y += player_vel
        #if keys[pygame.K_ESCAPE]:
            #pause_menu()

        ball.move()
        handle_collision(ball, right_paddle, left_paddle)

        if ball.x < -20:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH + 20:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"
        if won:
            text = POINT_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0 
            right_score = 0
            

        for event in pygame.event.get():
            # 256 is the event 'int' for pygame.QUIT() but for some reason, when pygame.QUIT() is put in place of 256 we get a TypeError
            if event.type == 256:
                run = False
                break
    quit()
    
INST_FONT = pygame.font.SysFont("arial", 15)    
def main_menu():
    run = True
    while run:
        WIN.fill(BLACK)
        left_title = POINT_FONT.render("L", 1, WHITE)
        left_instructions = INST_FONT.render("Tab: Up | CapsLock: Down", 1, WHITE)
        right_title = POINT_FONT.render("R", 1, WHITE)
        right_instructions = INST_FONT.render("Backslash: Up | Return: Down", 1, WHITE)
        pong_title = MAIN_FONT.render("PONG", 1, WHITE)
        start_inst = INST_FONT.render("(Press  \'space\'  to start)", 1, WHITE)

        WIN.blit(pong_title, (WIDTH/2 - pong_title.get_width()/2, 80))
        WIN.blit(start_inst, (WIDTH//2 - start_inst.get_width()/2, pong_title.get_height() * 2))
        WIN.blit(left_title, (WIDTH//4 - left_title.get_width()/2, HEIGHT // 2 - 50))
        WIN.blit(left_instructions, (WIDTH//4 - left_instructions.get_width()/2, HEIGHT // 2))
        WIN.blit(right_title, (WIDTH * (3/4) - right_title.get_width()/2, HEIGHT // 2 - 50))
        WIN.blit(right_instructions, (WIDTH * (3/4) - right_instructions.get_width()/2, HEIGHT // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
                main()
    pygame.quit()

# if __name__ == "__main__": makes sure that this file is only being ran as its own project and not being imported as a module in another project.
if __name__=="__main__":
    main_menu()
