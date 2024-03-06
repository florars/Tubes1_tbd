from typing import Optional

#from game.logic.base import BaseLogic
#from ...util import get_direction
from game.models import GameObject, Board, Position
from game.logic.Processors.Processor import Processor
import random

class SelfDefense(Processor):
    def __init__(self):
        super().__init__()
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def run(self, board_bot: GameObject, board: Board, nearest: int) -> list[tuple[int, Position]]:
        wrong_move: list[tuple[int, Position]] = []
        added_ind: list[int] = [False, False, False, False]
        for game_object in board.bots:
            if abs(board_bot.position.x - game_object.position.x) + \
                    abs(board_bot.position.y - game_object.position.y) == nearest:
                for ind in range(4):
                    if added_ind[ind]:
                        continue
                    dir_x, dir_y = self.directions[ind]
                    if abs(board_bot.position.x + dir_x - game_object.position.x) + \
                            abs(board_bot.position.y + dir_y - game_object.position.y) < nearest:
                        wrong_move.append((-1, Position(dir_y, dir_x)))
                        added_ind[ind] = True
        return wrong_move


    def attack(self, board_bot: GameObject, nearest_enemy: GameObject) -> tuple[int, Position]:
        return 1000, nearest_enemy.position

    def threatened(self, board_bot: GameObject, nearest_enemy: GameObject) -> int:
        distance = abs(nearest_enemy.position.x - board_bot.position.x) + abs(
            nearest_enemy.position.y - board_bot.position.y)
        return distance

    def process(self, board_bot: GameObject, board: Board) -> Optional[list[tuple[int, Position]]]:
        props = board_bot.properties
        # Analyze new state
        # Check safety
        if len(board.bots) == 1:
            return []
        nearest_enemy = min(
            [d for d in board.bots if d.id != board_bot.id],
            key=lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        safety = self.threatened(board_bot, nearest_enemy)
        if (safety == 1 and props.diamonds < 3):
            return [self.attack(board_bot, nearest_enemy)]
        elif (safety == 2 or (safety == 1 and props.diamonds >= 3)):
            return self.run(board_bot, board, safety)
        else:
            # Safe, return nothing
            return []


