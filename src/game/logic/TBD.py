import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
#from ..util import get_direction
from game.logic.Processors.selfdefenseprocess import SelfDefense
from game.logic.Processors.DiamondProcessor import DiamondProcessor


class TBDLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.SelfDefenseProcessor: SelfDefense = SelfDefense()
        self.DiamondProcessor: DiamondProcessor = DiamondProcessor()


    def next_move(self, board_bot: GameObject, board: Board):
        possible_moves: list[tuple[int, Position]] = []
        possible_moves.extend(self.SelfDefenseProcessor.process(board_bot, board))
        possible_moves.extend(self.DiamondProcessor.process(board_bot, board))
        wrong_moves = [False, False, False, False]
        real_moves: list[tuple[int, Position]] = []
        for prio, pos in possible_moves:
            if prio == -1:
                for ind in range(4):
                    dir_x, dir_y = self.directions[ind]
                    if pos.x == dir_x and pos.y == dir_y:
                        wrong_moves[ind] = True
            else:
                real_moves.append((prio, pos))
        real_moves.sort(key=lambda x: x[0])
        #print(wrong_moves)
        for prio, pos in real_moves:
            for ind in range(4):
                if wrong_moves[ind]:
                    continue
                dist_x, dist_y = self.directions[ind]
                cur_dist = abs(board_bot.position.x - pos.x) + abs(board_bot.position.y - pos.y)
                after_dist = abs(board_bot.position.x + dist_x - pos.x) + abs(board_bot.position.y + dist_y - pos.y)
                if after_dist < cur_dist:
                    return self.directions[ind]
        return self.directions[0]
