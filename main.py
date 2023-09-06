import asyncio
import random
import time
from enum import Enum
import keyboard
from atc_easy_desktop import EasyDesktop

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Item:
    def __init__(self, idx, x=-1, y=-1):
        self.idx = idx
        self.x = x
        self.y = y


desktop = EasyDesktop()
screen_width, screen_height = desktop.get_screen_size()
item_count = desktop.get_item_count()
cell_size = 60
game_width = screen_width // cell_size * cell_size
game_height = screen_height // cell_size * cell_size
key = " "
game_over = False


def clear_item():
    for i in range(item_count):
        desktop.go_to_xy(i, -100, -100)


def draw_snake(snake):
    for segment in snake:
        desktop.go_to_xy(segment.idx, segment.x, segment.y)


def draw_food(food):
    desktop.go_to_xy(food.idx, food.x, food.y)


def random_food(idx, snake):
    is_food_on_snake = True
    food = Item(idx)
    while is_food_on_snake:
        is_food_on_snake = False
        food.x = random.randrange(1, game_width // cell_size) * cell_size
        food.y = random.randrange(1, game_height // cell_size) * cell_size
        for segment in snake:
            if segment.x == food.x and segment.y == food.y:
                is_food_on_snake = True
                break

    return food


def is_game_over(snake):
    snake_head = snake[0]
    if (snake_head.x < 0 or snake_head.x >= game_width or
            snake_head.y < 0 or snake_head.y >= game_height):
        return True
    for i, item in enumerate(snake):
        if i == 0:
            continue
        if item.x == snake_head.x and item.y == snake_head.y:
            return True
    return False


async def game_loop():
    global game_over
    clear_item()
    snake = []
    idx = 0
    snake_head = Item(idx, (game_width // cell_size // 2) * cell_size, (game_height // cell_size // 2) * cell_size)

    snake.append(snake_head)
    idx += 1
    food = random_food(idx, snake)
    idx += 1

    draw_food(food)
    direction = random.choice(list(Direction))
    while not game_over:
        if key == "w" and direction != Direction.DOWN:
            direction = Direction.UP
        elif key == "a" and direction != Direction.RIGHT:
            direction = Direction.LEFT
        elif key == "s" and direction != Direction.UP:
            direction = Direction.DOWN
        elif key == "d" and direction != Direction.LEFT:
            direction = Direction.RIGHT

        snake_head = snake[0]
        snake_tail = snake[len(snake) - 1]
        snake_tail_xy = [snake_tail.x, snake_tail.y]

        for i in range(len(snake) - 1, 0, -1):
            snake[i].x = snake[i - 1].x
            snake[i].y = snake[i - 1].y

        if direction == Direction.UP:
            snake_head.y -= cell_size
        if direction == Direction.LEFT:
            snake_head.x -= cell_size
        if direction == Direction.RIGHT:
            snake_head.x += cell_size
        if direction == Direction.DOWN:
            snake_head.y += cell_size

        if snake_head.x == food.x and snake_head.y == food.y:
            food.x = snake_tail_xy[0]
            food.y = snake_tail_xy[1]
            snake.append(food)
            food = random_food(idx, snake)
            draw_food(food)
            idx += 1

        if is_game_over(snake):
            game_over = True
            continue

        draw_snake(snake)

        await asyncio.sleep(0.2)


async def read_input():
    global key, game_over
    while not game_over:
        if keyboard.is_pressed('q'):
            game_over = True
        if keyboard.is_pressed('w'):
            key = 'w'
        elif keyboard.is_pressed('a'):
            key = 'a'
        elif keyboard.is_pressed('s'):
            key = 's'
        elif keyboard.is_pressed('d'):
            key = 'd'
        await asyncio.sleep(0.05)


async def main():
    input_task = asyncio.create_task(read_input())
    game_task = asyncio.create_task(game_loop())
    await asyncio.gather(input_task, game_task)

time.sleep(5)
asyncio.run(main())
