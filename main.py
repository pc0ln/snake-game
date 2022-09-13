import pygame, random
from pygame.math import Vector2

WIDTH, HEIGHT = 500, 600 
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) #Window
pygame.display.set_caption("Snake :P") #Name of Window
#Game grid
cell_size = 16
cell_number = 25
grass_surface = pygame.Surface((cell_size * cell_number,cell_size * cell_number))


# Making a fruit object
class FRUIT:
    def __init__(self):
        #Position of Fruit
        self.position()
        #Draw fruit
    def draw_fruit(self):
        #Create a fruit rectangle
        fruit_rect = pygame.Rect(self.pos.x*cell_size+50,self.pos.y*cell_size+75, cell_size, cell_size)
        pygame.draw.rect(WIN, BLUE,fruit_rect)
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
        self.facing = Vector2(1,0)
        self.eat = False
    def draw_snake(self):
        # Drawing the body by creating and drawing rectangles
        for block in self.body:
            snake_rect = pygame.Rect(block.x*cell_size+50,block.y*cell_size+75, cell_size, cell_size)
            pygame.draw.rect(WIN, YELLOW,snake_rect)
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
    # Check if the head of the snake eats the fruit
    def check_eat(self):
        if self.berry.pos == self.viper.body[0]:
            # Spawn in a new fruit/Remakes the fruit
            self.berry.position()
            # Add length to snake
            self.viper.lengthen()
    def check_lose(self):
        # Check if the snake hits a wall
        if self.viper.body[0].x < 0 or self.viper.body[0].x > cell_number-1:
            self.game_end()
        if self.viper.body[0].y < 0 or self.viper.body[0].y > cell_number-1:
            self.game_end()
        for body in self.viper.body[1:]:
            if body == self.viper.body[0]:
                self.game_end()
        
    def game_end(self):
        pygame.quit()

# Making a timer that'll continuosly move the snake after a certain amount of time
MOVE_TIMER = pygame.USEREVENT
pygame.time.set_timer(MOVE_TIMER,150)


x_pos = 50
y_pos = 75

WHITE = (255, 248, 225)
GREEN = (85, 139, 47)
RED = (191, 54, 12)
BROWN = (78, 52, 46)
BLUE = (49, 27, 146)
YELLOW = (255, 235, 59)
FPS = 60

def draw_window():
    WIN.fill(WHITE)
    grass_surface.fill(GREEN)
    WIN.blit(grass_surface,(50,75))
    game.draw_game()
    pygame.display.update()

game = MAIN()

def main():
    global y_pos
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