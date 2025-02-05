"""Import module."""
from random import randrange

import pygame
import pygame.docs

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    The main class of the game.
    """

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Method for drawing snake or apple.
        """


class Apple(GameObject):
    """
    Describes the apple and actions with it.
    The apple should be displayed in random cells of the playing field.
    """

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color
        super().__init__(position, body_color)

    def randomize_position(self):
        """
        Sets the random position of the apple on the playing field.
        """
        self.position = (
            randrange(0, SCREEN_WIDTH, GRID_SIZE),
            randrange(0, SCREEN_HEIGHT, GRID_SIZE),
        )

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Describes the snake and its behavior.
    This class controls its movement, drawing, and
    also handles user actions.
    """

    def __init__(self, position, direction, body_color):
        self.length = 1
        self.positions = [position]
        self.direction = direction
        self.next_direction = None
        self.body_color = body_color
        self.last = None
        super().__init__(position, body_color)

    def update_direction(self):
        """Updates the snake's direction of movement."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, direction):
        """
        Updates the snake's position (coordinates of each section)
        by adding a new head to the top of the positions list and
        deleting the last element if the length of the snake has not increased.
        """
        new_position = (
            self.positions[0][0] + GRID_SIZE * direction[0],
            self.positions[0][1] + GRID_SIZE * direction[1],
        )

        if new_position[0] > SCREEN_WIDTH:
            new_position = (0, self.positions[0][1] + GRID_SIZE * direction[1])
        if new_position[0] < 0:
            new_position = (
                SCREEN_WIDTH,
                self.positions[0][1] + GRID_SIZE * direction[1],
            )
        if new_position[1] > SCREEN_HEIGHT:
            new_position = (self.positions[0][0] + GRID_SIZE * direction[0], 0)
        if new_position[1] < 0:
            new_position = (
                self.positions[0][0] + GRID_SIZE * direction[0],
                SCREEN_HEIGHT,
            )

        self.positions.insert(0, new_position)
        self.last = self.positions[-1]
        self.positions.pop(len(self.positions) - 1)

    def append_nail(self, direction, is_apple_eat):
        """
        Increases the length of the snake by 1 square when eating an apple.
        """
        if is_apple_eat is True and direction == RIGHT:
            self.positions.append(
                (self.positions[-1][0] - GRID_SIZE, self.positions[-1][1])
            )
            self.length += 1
        elif is_apple_eat is True and direction == LEFT:
            self.positions.append(
                (self.positions[-1][0] + GRID_SIZE, self.positions[-1][1])
            )
            self.length += 1
        elif is_apple_eat is True and direction == UP:
            self.positions.append(
                (self.positions[-1][0], self.positions[-1][1] + GRID_SIZE)
            )
            self.length += 1
        elif is_apple_eat is True and direction == DOWN:
            self.positions.append(
                (self.positions[-1][0], self.positions[-1][1] - GRID_SIZE)
            )
            self.length += 1

    def draw(self):
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Returns the position of the snake's head.
        """
        return self.positions[0]

    def reset(self):
        """
        Resets the snake to its initial state after a collision with itself.
        """
        self.length = 1
        self.positions = [
            (int(GRID_WIDTH / 2) * GRID_SIZE, int(GRID_HEIGHT / 2) * GRID_SIZE)
        ]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


def handle_keys(game_object):
    """Processes keystrokes to change the direction of the snake's movement"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Main Function.
    """
    # Инициализация PyGame:
    pygame.init()

    snake = Snake(
        (int(GRID_WIDTH / 2) * GRID_SIZE, int(GRID_HEIGHT / 2) * GRID_SIZE),
        RIGHT,
        SNAKE_COLOR,
    )
    apple = Apple(
        (randrange(0, SCREEN_WIDTH, GRID_SIZE),
         randrange(0, SCREEN_HEIGHT, GRID_SIZE)),
        APPLE_COLOR,
    )

    while True:
        handle_keys(snake)

        snake.update_direction()

        snake.move(snake.direction)

        if snake.positions[0] == apple.position:
            snake.append_nail(snake.direction, True)
            apple.randomize_position()
        else:
            snake.append_nail(snake.direction, False)

        for position in snake.positions[1:-1]:
            if snake.positions[0] == position and snake.length > 1:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()

        clock.tick(SPEED)
        pygame.display.update()


if __name__ == "__main__":
    main()
