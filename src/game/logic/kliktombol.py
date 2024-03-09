import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class KlikTombol:
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def next_move(self, board_bot: GameObject, board: Board):
        button = list(filter(lambda x: x.type == "DiamondButtonGameObject", board.game_objects))
        button = button[0]
        funcGO = lambda x, y, a, b: abs(x.x + a - y.x) + abs(x.y + b - y.y)
        for dir_x, dir_y in self.directions:
            if funcGO(board_bot.position, button.position, 0, 0) > funcGO(board_bot.position, button.position, dir_x, dir_y):
                return dir_x, dir_y
        return self.directions[0]

