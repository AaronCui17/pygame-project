# Flappy Bird 2.0

import pygame
import random

# ----- CONSTANTS
SKY_BLUE = (79, 208, 219)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

BIRD_WIDTH = 78
BIRD_HEIGHT = 47
JUMP_SPEED = 13
BIRD_ACCELERATION = 0.7
FLY_SPEED = 3

PIPE_WIDTH = 92
PIPE_HEIGHT = 529
Y_DISTANCE_BETWEEN_PIPES = 235
X_DISTANCE_BETWEEN_PIPES = 300

FLOOR_WIDTH = SCREEN_WIDTH * 2
FLOOR_HEIGHT = 250 # Adjust based on FLOOR_WIDTH to make appearance normal
FLOOR_DISTANCE_FROM_BOTTOM = 50

DISTANCE_ABOVE_SCREEN_ALLOWED = SCREEN_HEIGHT - PIPE_HEIGHT - FLOOR_DISTANCE_FROM_BOTTOM - 60 - Y_DISTANCE_BETWEEN_PIPES - BIRD_HEIGHT + 1

COUNTER_FONT_SIZE = 120
COUNTER_TEXT_WIDTH = 50
COUNTER_HEIGHT_FROM_TOP = 60

GAME_OVER_WIDTH = 435
GAME_OVER_HEIGHT = 111
GAME_OVER_SPEED = 24
GAME_OVER_ACCELERATION = 1

LOGO_WIDTH = 306
LOGO_HEIGHT = 88
LOGO_DISTANCE_FROM_TOP = 100

TITLE = "Flappy Bird 2.0"

# Set background
BACKGROUND = pygame.image.load("flappy bird images/background.png")
pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))


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
        self.vel = FLY_SPEED

        self.rect = self.image.get_rect()

    def update(self):
        # Make pipe move left at the velocity
        self.rect.x -= self.vel


# Make bottom pipe class
class Bottom_pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Create appearance and adjust size
        self.image = pygame.image.load("flappy bird images/flappy-bird-pipe-bottom.png")
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        # Velocity of pipe
        self.vel = FLY_SPEED

        self.rect = self.image.get_rect()

    def update(self):
        # Make pipe move left at the velocity
        self.rect.x -= self.vel


# Make floor class
class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Create appearance
        self.image = pygame.image.load("flappy bird images/flappy_bird_ground.png")
        self.image = pygame.transform.scale(self.image, (FLOOR_WIDTH, FLOOR_HEIGHT))

        # Velocity of floor
        self.vel = FLY_SPEED

        self.rect = self.image.get_rect()

    def update(self):
        # Make floor move left at the velocity
        self.rect.x -= self.vel


# Make game over sign class
class Game_over(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Create appearance
        self.image = pygame.image.load("flappy bird images/flappyBirdGameOver.png")
        self.image = pygame.transform.scale(self.image, (GAME_OVER_WIDTH, GAME_OVER_HEIGHT))

        # Velocity of game over
        self.vel = GAME_OVER_SPEED

        self.rect = self.image.get_rect()

    def update(self):
        # Make game over sign move down at the velocity
        self.rect.y += self.vel

        # Decelerate until stationary
        if self.vel > 0:
            self.vel -= GAME_OVER_ACCELERATION
        else:
            self.vel = 0

# Make logo class
class Logo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Create appearance
        self.image = pygame.image.load("flappy bird images/flappy-bird-logo.png")
        self.image = pygame.transform.scale(self.image, (LOGO_WIDTH, LOGO_HEIGHT))

        self.rect = self.image.get_rect()


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # SOUNDS
    FLAP_SOUND = pygame.mixer.Sound("flappy bird sounds/wing.mp3")
    POINT_SOUND = pygame.mixer.Sound("flappy bird sounds/point.mp3")
    DEATH_SOUND = pygame.mixer.Sound("flappy bird sounds/hit.mp3")
    BRUH_SOUND = pygame.mixer.Sound("flappy bird sounds/movie_1.mp3")

    # FONT
    COUNTER_FONT = pygame.font.Font("flappy bird fonts/Flappy-Bird.ttf", COUNTER_FONT_SIZE)


    # ----- LOCAL VARIABLES
    clock = pygame.time.Clock()
    number_of_refreshs = 0
    spawn_first_pipe_counter = 0
    score_value = 0
    done = False
    game_over = False
    played_death_sound_already = False
    created_game_over_sign_already = False


    # Sprite group creation
    pipes_and_floor_group = pygame.sprite.Group()

    pipes_group = pygame.sprite.Group()

    top_pipes_group = pygame.sprite.Group()
    bird_group = pygame.sprite.Group()
    floor_group = pygame.sprite.Group()
    game_over_group = pygame.sprite.Group()
    logo_group = pygame.sprite.Group()


    # Bird creation
    bird = Bird()

    # Bird location
    bird.rect.x = SCREEN_WIDTH/3 - BIRD_WIDTH/2
    bird.rect.y = SCREEN_HEIGHT/7*3 - BIRD_HEIGHT/2

    # Add bird to group
    bird_group.add(bird)


    # Logo creation
    logo = Logo()

    # Logo location
    logo.rect.x = SCREEN_WIDTH/2 - LOGO_WIDTH/2
    logo.rect.y = LOGO_DISTANCE_FROM_TOP

    # Add logo to groups
    logo_group.add(logo)


    # ----- MAIN LOOP
    while not done:

        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Make bird go up if key pressed
            if game_over == False:
                if event.type == pygame.KEYDOWN:
                    bird.vel = -JUMP_SPEED
                    spawn_first_pipe_counter += 1

                    # Play flap sound
                    pygame.mixer.Sound.play(FLAP_SOUND)


            # Reset game if game is over, bird has reached the ground, and player presses key to start again
            if game_over == True and bird.rect.y >= SCREEN_HEIGHT - BIRD_HEIGHT - FLOOR_DISTANCE_FROM_BOTTOM:
                if event.type == pygame.KEYDOWN:

                    # Kill on screen pipes and floors
                    for object in pipes_and_floor_group:
                        object.kill()

                    # Kill game over sign
                    for object in game_over_group:
                        object.kill()

                    # Reset bird height and speed and play flap sound
                    bird.rect.y = SCREEN_HEIGHT / 7 * 3 - BIRD_HEIGHT / 2
                    bird.vel = -JUMP_SPEED
                    pygame.mixer.Sound.play(FLAP_SOUND)

                    # Reset variables
                    number_of_refreshs = 0
                    spawn_first_pipe_counter = 0
                    score_value = 0

                    # Reset booleans
                    game_over = False
                    played_death_sound_already = False
                    created_game_over_sign_already = False


        # Spawn floors
        if number_of_refreshs * FLY_SPEED % SCREEN_WIDTH < FLY_SPEED:
            floor = Floor()

            # Floor location
            floor.rect.x = 0
            floor.rect.y = SCREEN_HEIGHT - FLOOR_DISTANCE_FROM_BOTTOM

            # Add floor to groups
            floor_group.add(floor)

            pipes_and_floor_group.add(floor)


        # Spawn first pipes
        if spawn_first_pipe_counter == 3:

            # Create pipes
            top_pipe = Top_pipe()
            bottom_pipe = Bottom_pipe()

            # Pipe location
            top_pipe.rect.x = SCREEN_WIDTH
            top_pipe.rect.y = random.randrange(-PIPE_HEIGHT + 60, SCREEN_HEIGHT - PIPE_HEIGHT - FLOOR_DISTANCE_FROM_BOTTOM - 60 - Y_DISTANCE_BETWEEN_PIPES)

            bottom_pipe.rect.x = SCREEN_WIDTH
            bottom_pipe.rect.y = top_pipe.rect.y + PIPE_HEIGHT + Y_DISTANCE_BETWEEN_PIPES

            # Add Pipe to groups
            top_pipes_group.add(top_pipe)

            pipes_group.add(top_pipe)
            pipes_group.add(bottom_pipe)

            pipes_and_floor_group.add(top_pipe)
            pipes_and_floor_group.add(bottom_pipe)

            # Don't spawn more first pipes
            spawn_first_pipe_counter = 4


        # Spawn more pipes
        for top_pipe in top_pipes_group:

            # When the pipe reaches a certain point on the screen
            if SCREEN_WIDTH - X_DISTANCE_BETWEEN_PIPES - FLY_SPEED / 2 <= top_pipe.rect.x <= SCREEN_WIDTH - X_DISTANCE_BETWEEN_PIPES + FLY_SPEED / 2:

                # Create pipes
                top_pipe = Top_pipe()
                bottom_pipe = Bottom_pipe()

                # Pipe location
                top_pipe.rect.x = SCREEN_WIDTH
                top_pipe.rect.y = random.randrange(-PIPE_HEIGHT + 60, SCREEN_HEIGHT - PIPE_HEIGHT - FLOOR_DISTANCE_FROM_BOTTOM - 60 - Y_DISTANCE_BETWEEN_PIPES)

                bottom_pipe.rect.x = SCREEN_WIDTH
                bottom_pipe.rect.y = top_pipe.rect.y + PIPE_HEIGHT + Y_DISTANCE_BETWEEN_PIPES

                # Add Pipe to groups
                top_pipes_group.add(top_pipe)

                pipes_group.add(top_pipe)
                pipes_group.add(bottom_pipe)

                pipes_and_floor_group.add(top_pipe)
                pipes_and_floor_group.add(bottom_pipe)


        # Play point sound and increase score
        for top_pipe in top_pipes_group:
            if top_pipe.rect.x + PIPE_WIDTH/2 - FLY_SPEED/2 <= bird.rect.x + BIRD_WIDTH <= top_pipe.rect.x + PIPE_WIDTH/2 + FLY_SPEED/2 and not game_over:
                pygame.mixer.Sound.play(POINT_SOUND)
                score_value += 1


        # Keep bird in screen
        # Top screen
        if bird.rect.y < DISTANCE_ABOVE_SCREEN_ALLOWED:
            bird.rect.y = DISTANCE_ABOVE_SCREEN_ALLOWED

            # Play sound to let user know
            pygame.mixer.Sound.play(BRUH_SOUND)

        # Bottom screen
        if bird.rect.y > SCREEN_HEIGHT - BIRD_HEIGHT - FLOOR_DISTANCE_FROM_BOTTOM:
            bird.rect.y = SCREEN_HEIGHT - BIRD_HEIGHT - FLOOR_DISTANCE_FROM_BOTTOM

            # Game over if hits bottom
            game_over = True

            # Play death sound if necessary
            if not played_death_sound_already:
                pygame.mixer.Sound.play(DEATH_SOUND)
                pygame.mixer.Sound.play(BRUH_SOUND)

                # Only play once
                played_death_sound_already = True

            # Show game over sign
            if not created_game_over_sign_already:

                # Create game over sign
                game_over = Game_over()

                # Sign location
                game_over.rect.x = SCREEN_WIDTH/2 - GAME_OVER_WIDTH/2
                game_over.rect.y = -GAME_OVER_HEIGHT

                # Add sign to group
                game_over_group.add(game_over)

                # Only run once
                created_game_over_sign_already = True


        # Kill off screen pipes and floors
        for object in pipes_and_floor_group:
            if object.rect.right < 0:
                object.kill()


        # Game over if player hits pipe
        if pygame.sprite.spritecollide(bird, pipes_group, False):
            game_over = True

            # Play death sound if necessary
            if not played_death_sound_already:
                pygame.mixer.Sound.play(DEATH_SOUND)

                # Don't play repeatedly
                played_death_sound_already = True


        # Stop counting refreshs when game is over
        if game_over == False:
            number_of_refreshs += 1


        # ----- DRAW
        screen.fill(SKY_BLUE)

        # Background
        screen.blit(BACKGROUND, (0,0))

        # Draw pipes
        pipes_group.draw(screen)

        # Draw bird and floor
        floor_group.draw(screen)
        bird_group.draw(screen)

        # Draw logo
        if spawn_first_pipe_counter == 0:
            logo_group.draw(screen)

        # Display score
        score = COUNTER_FONT.render(str(score_value), True, (255, 255, 255))

        if spawn_first_pipe_counter > 0:
            screen.blit(score, (SCREEN_WIDTH/2 - len(str(score_value)) * COUNTER_TEXT_WIDTH/2, COUNTER_HEIGHT_FROM_TOP))

        # Draw game over sign
        game_over_group.draw(screen)

        # ----- LOGIC

        # Only move pipes and floor if game not over
        if game_over == False:
            pipes_and_floor_group.update()

        # Always move bird
        if spawn_first_pipe_counter > 0:
            bird_group.update()

        # Move game over sign
        game_over_group.update()


        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)


    pygame.quit()


if __name__ == "__main__":
    main()
