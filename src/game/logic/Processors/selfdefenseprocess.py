from typing import Optional

#from game.logic.base import BaseLogic
from ...models import GameObject, Board, Position
#from ...util import get_direction
from ...logic.Processors.Processor import Processor
import random

class SelfDefense(Processor):
    def __init__(self):
        super().__init__()
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    """
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
    """

    def process(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        # Check safety
        if len(board.bots) == 1:
            return []
        func_dist = lambda x, y: abs(x.position.x - y.position.x) + abs(x.position.y - y.position.y)
        dist_one = list(filter(lambda x: func_dist(x, board_bot) == 1 and (x.position.x != x.properties.base.x or x.position.y != x.properties.base.y), board.bots))
        if dist_one:
            maxWithDia = max(dist_one, key=lambda x: x.properties.diamonds)
            #move_at = Position(maxWithDia.position.y - board_bot.position.y, maxWithDia.position.x - board_bot.position.x, )
            return [(-2, maxWithDia)]
        return []
        """
        dist_two = list(filter(lambda x: func_dist(x, board_bot) == 2, board.bots))
        if not dist_two:
            # Safe, return nothing
            return []
        restricted_move = []
        for dir_x, dir_y in self.directions:
            new_hyp_pos = GameObject(-1, Position(dir_x + board_bot.position.x, dir_y + board_bot.position.y), "", None)
            ex = False
            for bots in dist_two:
                if func_dist(new_hyp_pos, bots) == 1:
                    ex = True
                    break
            if ex:
                restricted_move.append((-1, Position(dir_x, dir_y)))
        return restricted_move
        """

