import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game variables
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = -5
PIPE_GAP = 150

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 48)

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.width = 40
        self.height = 30
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.top_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - PIPE_GAP
        self.width = 60

    def move(self):
        self.x += PIPE_SPEED

    def draw(self):
        # Draw top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        # Draw bottom pipe
        pygame.draw.rect(
            screen,
            GREEN,
            (self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height),
        )

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(
            self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height
        )
        return top_rect, bottom_rect

# Game loop
def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 200)]
    score = 0

    running = True
    while running:
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Bird movement
        bird.move()

        # Pipe movement
        for pipe in pipes:
            pipe.move()

        # Check for pipe passage and collision
        if pipes[0].x + pipes[0].width < 0:
            pipes.pop(0)
            pipes.append(Pipe(SCREEN_WIDTH))
            score += 1

        for pipe in pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird.get_rect().colliderect(top_rect) or bird.get_rect().colliderect(
                bottom_rect
            ):
                running = False

        # Check if bird hits the ground or flies too high
        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            running = False

        # Draw everything
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Display score
        score_text = font.render(str(score), True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2, 20))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Game over screen
    game_over_text = font.render("Game Over!", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Run the game
if __name__ == "__main__":
    main()
