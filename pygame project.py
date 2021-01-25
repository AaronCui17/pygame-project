# Flappy Bird 2.0

import pygame
import random

# ----- CONSTANTS
SKY_BLUE = (79, 208, 219)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

BIRD_WIDTH = 78
BIRD_HEIGHT = 47
JUMP_SPEED = 10
BIRD_ACCELERATION = 0.55

PIPE_WIDTH = 92
PIPE_HEIGHT = 529
PIPE_SPEED = 3
Y_DISTANCE_BETWEEN_PIPES = 200
X_DISTANCE_BETWEEN_PIPES = 300 # MUST BE MULTIPLE OF PIPE_SPEED

TITLE = "Flappy Bird 2.0"


# Make bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Create appearance and adjust size
        self.image = pygame.image.load("flappy bird images/bird.png")
        self.image = pygame.transform.scale(self.image, (BIRD_WIDTH, BIRD_HEIGHT))

        # Initial velocity of bird
        self.vel = 0

        self.rect = self.image.get_rect()

    def update(self):
        # Make bird move down at the velocity
        self.rect.y += self.vel

        # Increase the velocity to give bird acceleration
        self.vel += BIRD_ACCELERATION


# Make top pipe class
class Top_pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Create appearance and adjust size
        self.image = pygame.image.load("flappy bird images/flappy-bird-pipe-top.png")
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        # Velocity of pipe
        self.vel = PIPE_SPEED

        self.rect = self.image.get_rect()

    def update(self):
        # Make pipe move down at the velocity
        self.rect.x -= self.vel


# Make bottom pipe class
class Bottom_pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Create appearance and adjust size
        self.image = pygame.image.load("flappy bird images/flappy-bird-pipe-bottom.png")
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        # Velocity of pipe
        self.vel = PIPE_SPEED

        self.rect = self.image.get_rect()

    def update(self):
        # Make pipe move down at the velocity
        self.rect.x -= self.vel


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    spawn_first_pipe_counter = 0
    game_over = False

    # Sprite group creation
    all_sprites_group = pygame.sprite.Group()
    pipes_group = pygame.sprite.Group()
    top_pipes_group = pygame.sprite.Group()
    no_bird_group = pygame.sprite.Group()
    bird_group = pygame.sprite.Group()


    # Bird creation
    bird = Bird()

    # Bird location
    bird.rect.x = SCREEN_WIDTH/3 - BIRD_WIDTH/2
    bird.rect.y = SCREEN_HEIGHT/7*3 - BIRD_HEIGHT/2

    # Add bird to group
    all_sprites_group.add(bird)
    bird_group.add(bird)


    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Only if game is not over
            if game_over == False:

                # Make bird go up if key pressed
                if event.type == pygame.KEYDOWN:
                    bird.vel = -JUMP_SPEED
                    spawn_first_pipe_counter += 1


        # Spawn first pipe
        if spawn_first_pipe_counter == 3:

            # Create pipes
            top_pipe = Top_pipe()
            bottom_pipe = Bottom_pipe()

            # Pipe location
            top_pipe.rect.x = SCREEN_WIDTH
            top_pipe.rect.y = random.randrange(-PIPE_HEIGHT + 60, SCREEN_HEIGHT - PIPE_HEIGHT - 60 - Y_DISTANCE_BETWEEN_PIPES )

            bottom_pipe.rect.x = SCREEN_WIDTH
            bottom_pipe.rect.y = top_pipe.rect.y + PIPE_HEIGHT + Y_DISTANCE_BETWEEN_PIPES

            # Add Pipe to groups
            pipes_group.add(top_pipe)
            pipes_group.add(bottom_pipe)

            top_pipes_group.add(top_pipe)

            all_sprites_group.add(top_pipe)
            all_sprites_group.add(bottom_pipe)

            no_bird_group.add(top_pipe)
            no_bird_group.add(bottom_pipe)

            # Don't spawn more first pipes
            spawn_first_pipe_counter = 4


        # Spawn more pipes
        for top_pipe in top_pipes_group:

            # When the pipe reaches a certain point on the screen
            if top_pipe.rect.x == SCREEN_WIDTH - X_DISTANCE_BETWEEN_PIPES:

                # Create pipes
                top_pipe = Top_pipe()
                bottom_pipe = Bottom_pipe()

                # Pipe location
                top_pipe.rect.x = SCREEN_WIDTH
                top_pipe.rect.y = random.randrange(-PIPE_HEIGHT + 60, SCREEN_HEIGHT - PIPE_HEIGHT - 60 - Y_DISTANCE_BETWEEN_PIPES)

                bottom_pipe.rect.x = SCREEN_WIDTH
                bottom_pipe.rect.y = top_pipe.rect.y + PIPE_HEIGHT + Y_DISTANCE_BETWEEN_PIPES

                # Add Pipe to groups
                pipes_group.add(top_pipe)
                pipes_group.add(bottom_pipe)

                top_pipes_group.add(top_pipe)

                all_sprites_group.add(top_pipe)
                all_sprites_group.add(bottom_pipe)

                no_bird_group.add(top_pipe)
                no_bird_group.add(bottom_pipe)


        # Keep bird in screen
        if bird.rect.y > SCREEN_HEIGHT - BIRD_HEIGHT:
            bird.rect.y = SCREEN_HEIGHT - BIRD_HEIGHT

        # Kill off screen pipes
        for pipe in pipes_group:
            if pipe.rect.right < 0:
                pipe.kill()


        if pygame.sprite.spritecollide(bird, pipes_group, False):
            game_over = True


        # ----- DRAW
        screen.fill(SKY_BLUE)
        all_sprites_group.draw(screen)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)


        # ----- LOGIC

        # Only move pipes if game not over
        if game_over == False:
            no_bird_group.update()

        # Always move bird
        bird_group.update()


    pygame.quit()


if __name__ == "__main__":
    main()