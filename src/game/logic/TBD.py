import random
from typing import Optional

from ..logic.base import BaseLogic
from ..models import GameObject, Board, Position
#from ..util import get_direction
from ..logic.Processors.selfdefenseprocess import SelfDefense
from ..logic.Processors.DiamondProcessor import DiamondProcessor
from ..logic.Processors.GoHomeProcessor import GoHomeProcessor
from ..logic.Processors.TeleporterProcessor import Teleporter
import functools

class TBDLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.SelfDefenseProcessor: SelfDefense = SelfDefense()
        self.DiamondProcessor: DiamondProcessor = DiamondProcessor()
        self.TeleportProcessor: Teleporter = Teleporter()
        self.GoHomeProcessor: GoHomeProcessor = GoHomeProcessor()
        self.TackleCounter = 0
        self.TackleTarget = None
        self.OldPos: Optional[Position] = None

    def next_move(self, board_bot: GameObject, board: Board):
        possible_moves: list[tuple[int, Position]] = []
        listSelfD = self.SelfDefenseProcessor.process(board_bot, board)
        if len(listSelfD) > 0 and listSelfD[0][0] == -2:
            self.OldPos = board_bot.position
            if ((self.TackleTarget is not None and
                 self.TackleTarget == listSelfD[0][1].properties.name
                and self.TackleCounter == 0) or self.TackleTarget is None or self.TackleTarget !=
                    listSelfD[0][1].properties.name):
                self.TackleTarget = listSelfD[0][1].properties.name
                self.TackleCounter += 1
                print(self.TackleTarget, self.TackleCounter)
                return listSelfD[0][1].position.x - board_bot.position.x, listSelfD[0][1].position.y - board_bot.position.y
        self.TackleTarget = None
        self.TackleCounter = 0
        listDia = self.DiamondProcessor.process(board_bot, board)
        listGoHome = self.GoHomeProcessor.process(board_bot, board)
        possible_moves.extend(listDia)
        possible_moves.extend(listGoHome)
        if not listDia:
            score_dia = 0
        else:
            score_dia = listDia[0][0]
        if not listGoHome:
            dist = 0
        else:
            dist = listGoHome[0][0]
        possible_moves.extend(self.TeleportProcessor.process(board_bot, board, score_dia, dist))
        #print(possible_moves)
        #print(board_bot.properties.diamonds)
        """
                for prio, pos in possible_moves:
            if prio == -1:
                for ind in range(4):
                    dir_x, dir_y = self.directions[ind]
                    if pos.x == dir_x and pos.y == dir_y:
                        wrong_moves[ind] = True
            else:
                real_moves.append((prio, pos))
        
        """
        wrong_moves = [False, False, False, False]
        cnt_wrong_mv = 0
        if board_bot.position.x == 14:
            wrong_moves[0] = True
            cnt_wrong_mv += 1
        if board_bot.position.x == 0:
            wrong_moves[2] = True
            cnt_wrong_mv += 1
        if board_bot.position.y == 14:
            wrong_moves[1] = True
            cnt_wrong_mv += 1
        if board_bot.position.y == 0:
            wrong_moves[3] = True
            cnt_wrong_mv += 1
        real_moves: list[tuple[int, Position]] = list(filter(lambda x: x[0] != -1, possible_moves))
        """
        minOnes = list(filter(lambda x: x[0] == -1, possible_moves))
        for noMove in minOnes:
            if noMove == self.directions[0] and not wrong_moves[0]:
                wrong_moves[0] = True
                cnt_wrong_mv += 1
            elif noMove == self.directions[1] and not wrong_moves[1]:
                wrong_moves[1] = True
                cnt_wrong_mv += 1
            elif noMove == self.directions[2] and not wrong_moves[2]:
                wrong_moves[2] = True
                cnt_wrong_mv += 1
            elif noMove == self.directions[3] and not wrong_moves[3]:
                wrong_moves[3] = True
                cnt_wrong_mv += 1
        """
        real_moves.sort(key=lambda x: x[0], reverse=True)
        #print(possible_moves)
        #print(real_moves)
        #print(wrong_moves)
        #print(board_bot.position.x, board_bot.position.y)
        #print(board_bot.properties.diamonds)
        for prio, pos in real_moves:
            for ind in range(4):
                if wrong_moves[ind]:
                    continue
                dist_x, dist_y = self.directions[ind]
                cur_dist = abs(board_bot.position.x - pos.x) + abs(board_bot.position.y - pos.y)
                after_dist = abs(board_bot.position.x + dist_x - pos.x) + abs(board_bot.position.y + dist_y - pos.y)
                if after_dist < cur_dist:
                    self.goal_position = pos
                    return self.directions[ind]
        self.goal_position = None
        for i in range(4):
            if not wrong_moves[i]:
                return self.directions[i]
        return 0, 0
