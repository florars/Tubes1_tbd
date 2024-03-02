from typing import Optional

#from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
#from ...util import get_direction
from game.models import Board
from game.logic.Processors.Processor import Processor


class GoHomeProcessor(Processor): 
    def __init__(self): 
        super().__init__()

    def goHomeImmediately(self, board_bot: GameObject) -> Optional[list[int, Position]]:
        base = board_bot.properties.base
        if (board_bot.properties.milliseconds_left <= ((abs(base.x - board_bot.position.x) + abs(base.y - board_bot.position.y))*2000) or board_bot.properties.diamonds == 5):
            return [1, base] #TODO: figure out priorities
        else: 
            return [None,None] #no need to go home immediately
        
    #TODO: kalo udah 3 diamonds wander sekitar base aja
    def wanderAroundHome(self, board_bot: GameObject, board: Board) -> Optional[list[int, Position]]:
        closestToBase = min(
                    board.diamonds,
                    key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
                )
        if (board_bot.properties.diamonds >= 3):
            return ([1, closestToBase.position]) #TODO: figure out priorities
        else:
            return ([None,None])

    def process(self, board_bot: GameObject, board: Board) -> Optional[list[tuple[int, Position]]]:
        a = self.goHomeImmediately(board_bot)
        b = self.wanderAroundHome(board_bot, board)
        if (a != [None,None]):
            return a
        elif (b != [None,None]):
            return b
        else:
            return []
