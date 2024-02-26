import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction
from ...models import Board


class Processor:

    def __init__(self):
        pass

    @staticmethod
    def position_of_objects(self, board: Board, tipe: str) -> [(int, int)]:
        ans: [(int, int)] = []
        for game_object in board.game_objects:
            if game_object.type == tipe:
                ans.append((game_object.position.x, game_object.position.y))
        return ans


