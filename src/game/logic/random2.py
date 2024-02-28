import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class RandomLogic2(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def run(self, board_bot: GameObject, nearest_enemy: GameObject):
        x = nearest_enemy.position.x - board_bot.position.x
        y = nearest_enemy.position.y - board_bot.position.y
        current_position = board_bot.position
        if (self.goal_position):
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        if (x == 0):
            if (delta_x and delta_x != 0):
                return delta_x, 0
            elif (delta_y and delta_y != y - 1):
                return 0, delta_y
            else:
                return 1, 0
        elif (y == 0):
            if (delta_y and delta_y != 0):
                return 0, delta_y
            elif (delta_x and delta_x != x - 1):
                return delta_x, 0
            else:
                return 0, 1
        else:
            if (delta_x and -x == delta_x):
                return delta_x, 0
            elif (delta_y and -y == delta_y):
                return 0, delta_y
            else:
                return -x, 0

    def attack(self, board_bot: GameObject, nearest_enemy: GameObject):
        x = nearest_enemy.position.x - board_bot.position.x
        y = nearest_enemy.position.y - board_bot.position.y
        return x, y

    def threatened(self, board_bot: GameObject, nearest_enemy: GameObject) -> int:
        distance = abs(nearest_enemy.position.x - board_bot.position.x) + abs(
            nearest_enemy.position.y - board_bot.position.y)
        return distance

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        # Check safety
        nearest_enemy = min(
            [d for d in board.bots if d.id != board_bot.id],
            key=lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        safety = self.threatened(board_bot, nearest_enemy)
        if (safety == 1 and props.diamonds < 3):
            delta_x, delta_y = self.attack(board_bot, nearest_enemy)
        elif (safety == 2 or (safety == 1 and props.diamonds >= 3)):
            delta_x, delta_y = self.run(board_bot, nearest_enemy)
        else:
            # Safe
            if props.diamonds == 5:
                # Move to base
                base = board_bot.properties.base
                self.goal_position = base
            else:
                nearest_diamon = min(
                    [d for d in board.diamonds],
                    key=lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
                )
                self.goal_position = nearest_diamon.position

            current_position = board_bot.position
            if self.goal_position:
                # We are aiming for a specific position, calculate delta
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
            else:
                # Roam around
                delta = self.directions[self.current_direction]
                delta_x = delta[0]
                delta_y = delta[1]
                if random.random() > 0.6:
                    self.current_direction = (self.current_direction + 1) % len(
                        self.directions
                    )
        return delta_x, delta_y
