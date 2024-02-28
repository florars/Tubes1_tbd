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

    def run(self, board_bot: GameObject, board: Board):
        nearest_enemy = min(
            [d for d in board.bots if d.id!=board_bot.id],
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        x = nearest_enemy.position.x - board_bot.position.x
        y = nearest_enemy.position.y - board_bot.position.y
        current_position = board_bot.position
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        if (x==0 and delta_x!=0):
            return (delta_x, 0) # buat distance di x-axis, tapi entah cara milih gerak ke mana w/ regards to current goal
        elif (x==0 and delta_x==0):
            return (1,0)
        elif (y==0 and delta_y!=0):
            return (0, delta_y) # buat distance di y-axis, tapi entah cara milih gerak ke mana w/ regards to current goal
        elif (y==0 and delta_y==0):
            return (0,1)
        else:
            if (-x == delta_x):
                return (delta_x, 0)
            elif (-y == delta_y):
                return (0, delta_y)
            else:
                return (-x,0)
        

    def attack(self, board_bot: GameObject, board: Board):
        nearest_enemy = min(
            [d for d in board.bots if d.id!=board_bot.id],
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        x = nearest_enemy.position.x - board_bot.position.x
        y = nearest_enemy.position.y - board_bot.position.y
        return (x,y)

    def threatened(self, board_bot: GameObject, board: Board) -> int :
        nearest_enemy = min(
            [d for d in board.bots if d.id!=board_bot.id],
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        distance = abs(nearest_enemy.position.x - board_bot.position.x) + abs(nearest_enemy.position.y - board_bot.position.y)
        return distance
        
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        # Check safety
        safety = self.threatened(board_bot, board)
        if safety == 1:
            return self.attack(board_bot, board)
        elif safety == 2:
            return self.run(board_bot, board)
        else:
            #Safe
            if props.diamonds == 5:
                # Move to base
                base = board_bot.properties.base
                self.goal_position = base
            else:
                # Just roam around
                nearest_diamon = min(
                    [d for d in board.diamonds],
                    key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
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
