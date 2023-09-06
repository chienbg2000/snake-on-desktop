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
    def __init__(self, idx, x=0, y=0):
        self.idx = idx
        self.x = x
        self.y = y


desktop = EasyDesktop()
item_count = desktop.get_item_count()
print("item_count", item_count)
screen_width, screen_height = desktop.get_screen_size()
print("screen", screen_width, screen_height)
step_size = 50
game_width = screen_width // step_size * step_size
game_height = screen_height // step_size * step_size
print("game screen", game_width, game_height)


def clear_desktop():
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
        food.x = random.randrange(1, game_width // step_size) * step_size
        food.y = random.randrange(1, game_height // step_size) * step_size
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


if __name__ == '__main__':
    time.sleep(5)
    clear_desktop()
    game_over = False
    snake = []
    idx = 0
    snake_head = Item(idx, (game_width // step_size // 2) * step_size, (game_height // step_size // 2) * step_size)
    snake.append(snake_head)
    idx += 1
    food = random_food(idx, snake)
    idx += 1

    draw_food(food)
    direction = random.choice(list(Direction))
    while not game_over:
        if keyboard.is_pressed('q'):
            game_over = True
        elif keyboard.is_pressed('w') and direction != Direction.DOWN:
            direction = Direction.UP
        elif keyboard.is_pressed('a') and direction != Direction.RIGHT:
            direction = Direction.LEFT
        elif keyboard.is_pressed('s') and direction != Direction.UP:
            direction = Direction.DOWN
        elif keyboard.is_pressed('d') and direction != Direction.LEFT:
            direction = Direction.RIGHT

        tempItem = Item(0)
        for i, item in enumerate(snake):
            x = item.x
            y = item.y
            if i == 0:
                if direction == Direction.UP:
                    item.y -= step_size
                if direction == Direction.LEFT:
                    item.x -= step_size
                if direction == Direction.RIGHT:
                    item.x += step_size
                if direction == Direction.DOWN:
                    item.y += step_size
            else:
                item.x = tempItem.x
                item.y = tempItem.y

            tempItem.x = x
            tempItem.y = y


        if snake[0].x == food.x and snake[0].y == food.y:
            food.x = tempItem.x
            food.y = tempItem.y
            snake.append(food)
            food = random_food(idx, snake)
            draw_food(food)
            idx += 1

        if is_game_over(snake):
            game_over = True
            continue

        draw_snake(snake)

        time.sleep(0.1)

