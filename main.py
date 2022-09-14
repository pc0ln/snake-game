import pygame, random
from pygame.math import Vector2

pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 500, 600 
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #Window
pygame.display.set_caption("Snake :P") #Name of Window
#Game grid
cell_size = 16
cell_number = 25
# Assets
grass_surface = pygame.image.load('Assets/grass.png')
plum = pygame.image.load('Assets/berrry.png').convert_alpha()
WHITE = (255, 248, 225)
BLACK = (53, 57, 53)
FPS = 60
score_font = pygame.font.Font('Assets/Daydream.ttf',25)
# Making a timer that'll continuosly move the snake after a certain amount of time
MOVE_TIMER = pygame.USEREVENT
pygame.time.set_timer(MOVE_TIMER,150)



# Making a fruit object
class FRUIT:
    def __init__(self):
        #Position of Fruit
        self.position()
        #Draw fruit
    def draw_fruit(self):
        #Create a fruit rectangle
        fruit_rect = pygame.Rect(self.pos.x*cell_size+50,self.pos.y*cell_size+75, cell_size, cell_size)
        WIN.blit(plum, fruit_rect)
        # pygame.draw.rect(WIN, BLUE,fruit_rect)
        # Fruit position 
    def position(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
         #Defining position as a vector
        self.pos = Vector2(self.x,self.y)

# Making the snake
class SNAKE:
    def __init__(self):
        # Initial body
        self.body = [Vector2(13,13),Vector2(13,12)]
        self.facing = Vector2(0,0)
        self.eat = False
        # Importing the snake body
        self.viper_head = pygame.image.load('Assets/head.png').convert_alpha()
        self.viper_tail = pygame.image.load('Assets/tail.png').convert_alpha()
        self.viper_body_nt = pygame.image.load('Assets/body-nt.png').convert_alpha()
        self.viper_body_t = pygame.image.load('Assets/body-t.png').convert_alpha()
    def draw_snake(self):
        # Call function to update the snake
        self.update_head()
        self.update_tail()


        # Drawing the body by creating and drawing rectangles
        for index,block in enumerate(self.body):
            # Rect for position
            snake_rect = pygame.Rect(block.x*cell_size+50,block.y*cell_size+75, cell_size, cell_size)
            # Head
            if index == 0:
                WIN.blit(self.head,snake_rect)
            # Tail is similar to head but last index
            elif index == len(self.body) -1:
                WIN.blit(self.tail, snake_rect)
            else:
                # Takes the previous block and subtracts current block to get relation vector
                prev_part = self.body[index +1] - block
                # Takes the previous block and subtracts current block to get relation vector
                next_part = self.body[index -1] - block
                if prev_part.x == next_part.x:
                    WIN.blit(self.viper_body_nt, snake_rect)
                elif prev_part.y == next_part.y:
                    WIN.blit(pygame.transform.rotate(self.viper_body_nt,90), snake_rect)
                # Turning blocks
                else:
                    if prev_part.x == 1 and next_part.y == -1 or prev_part.y == -1 and next_part.x == 1:
                        WIN.blit(self.viper_body_t, snake_rect)
                    elif prev_part.x == 1 and next_part.y == 1 or prev_part.y == 1 and next_part.x == 1:
                        WIN.blit(pygame.transform.rotate(self.viper_body_t,270), snake_rect)
                    elif prev_part.x == -1 and next_part.y == 1 or prev_part.y == 1 and next_part.x == -1:
                        WIN.blit(pygame.transform.rotate(self.viper_body_t,180), snake_rect)
                    elif prev_part.x == -1 and next_part.y == -1 or prev_part.y == -1 and next_part.x == -1:
                        WIN.blit(pygame.transform.rotate(self.viper_body_t,90), snake_rect)

    # Determine direction of head 
    def update_head(self):
        head_rel = self.body[1]-self.body[0]
        if head_rel == Vector2(1,0):
                    self.head = pygame.transform.rotate(self.viper_head, 270)
        elif head_rel == Vector2(-1,0):
                    self.head = pygame.transform.rotate(self.viper_head, 90)
        elif head_rel == Vector2(0,1):
                    self.head = pygame.transform.rotate(self.viper_head, 180)
        elif head_rel == Vector2(0,-1):
                    self.head = self.viper_head
            
    def update_tail(self):
        tail_rel = self.body[-1]-self.body[-2]
        if tail_rel == Vector2(1,0):
                    self.tail = pygame.transform.rotate(self.viper_tail, 270)
        elif tail_rel == Vector2(-1,0):
                    self.tail = pygame.transform.rotate(self.viper_tail, 90)
        elif tail_rel == Vector2(0,1):
                    self.tail = pygame.transform.rotate(self.viper_tail, 180)
        elif tail_rel == Vector2(0,-1):
                    self.tail = self.viper_tail
        
        # Moving the snake
    def move_snake(self):
            # Checks if the snake ate
            if self.eat:
                new_body = self.body[:] # No slice of last block
            # Didn't eat so last block is sliced
            else:
                new_body = self.body[:-1] # Slice the last block off
            # Making the head
            new_body.insert(0,new_body[0]+self.facing) # Simmulate movement by vector addition
            self.body = new_body
            self.eat = False
    # Adds to the length when the snake eats a fruit
    def lengthen(self):
        self.eat = True
    def reset(self):
        self.body = [Vector2(13,13),Vector2(13,12)]
        self.facing = Vector2(0,0)

# Making a main class to hold the logic
class MAIN:
    def __init__(self):
        self.viper = SNAKE()
        self.berry = FRUIT()
    # Update the game
    def update(self):
        self.viper.move_snake()
        self.check_eat()
        self.check_lose()
    # Draw the elements
    def draw_game(self):
        self.berry.draw_fruit()
        self.viper.draw_snake()
        self.draw_score()
    # Check if the head of the snake eats the fruit
    def check_eat(self):
        if self.berry.pos == self.viper.body[0]:
            # Spawn in a new fruit/Remakes the fruit
            self.berry.position()
            # Add length to snake
            self.viper.lengthen()
        # Prevent the fruit from spawning in the snake
        for block in self.viper.body[1:]:
            if block == self.berry.pos:
                self.berry.position()
    def check_lose(self):
        # Check if the snake hits a wall
        if self.viper.body[0].x < 0 or self.viper.body[0].x > cell_number-1:
            self.game_end()
        if self.viper.body[0].y < 0 or self.viper.body[0].y > cell_number-1:
            self.game_end()
        # Check if snake is hitting itself
        for body in self.viper.body[1:]:
            if body == self.viper.body[0]:
                self.game_end()
    # Lose function    
    def game_end(self):
        self.viper.reset()
    def draw_score(self):
        score = "SCORE: " + str(len(self.viper.body)-2)
        score_text = score_font.render(score,True,BLACK)
        WIN.blit(score_text,(250,30))


def draw_window():
    WIN.fill(WHITE)
    WIN.blit(grass_surface,(50,75))
    game.draw_game()
    pygame.display.update()

game = MAIN()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # Closes game if window is closed
            if event.type == pygame.QUIT:
                run = False
            # Moves the snake per the timer
            if event.type == MOVE_TIMER:
                game.update()
            # Start taking user inputs
            if event.type == pygame.KEYDOWN:
                # Make the snake go up 
                if event.key == pygame.K_UP and game.viper.facing != Vector2(0,1):
                    game.viper.facing = Vector2(0,-1)
                if event.key == pygame.K_DOWN and game.viper.facing != Vector2(0,-1):
                    game.viper.facing = Vector2(0,1)
                if event.key == pygame.K_LEFT and game.viper.facing != Vector2(1,0):
                    game.viper.facing = Vector2(-1,0)
                if event.key == pygame.K_RIGHT and game.viper.facing != Vector2(-1,0):
                    game.viper.facing = Vector2(1,0)
    
        draw_window()
        

    pygame.quit()


if __name__ == "__main__":
    main()