import pygame
import sys
import random

# Game settings
WINDOW_SIZE = 400
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Snake:
    def __init__(self):
        self.body = [(5, 5)]
        self.direction = (1, 0)

    def move(self):
        head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def change_direction(self, dir):
        if (dir[0] * -1, dir[1] * -1) != self.direction:
            self.direction = dir

    def collides(self):
        head = self.body[0]
        return (
            head[0] < 0 or head[0] >= WINDOW_SIZE // CELL_SIZE or
            head[1] < 0 or head[1] >= WINDOW_SIZE // CELL_SIZE or
            head in self.body[1:]
        )

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (
            random.randint(0, WINDOW_SIZE // CELL_SIZE - 1),
            random.randint(0, WINDOW_SIZE // CELL_SIZE - 1)
        )

    def draw(self, surface):
        rect = pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        snake.move()
        if snake.body[0] == food.position:
            snake.grow()
            food.position = food.random_position()

        if snake.collides():
            break

        screen.fill(BLACK)
        for segment in snake.body:
            rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)
        food.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    print("Game Over!")

if __name__ == "__main__":
    main()
