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
        if ((board_bot.properties.milliseconds_left <= ((abs(base.x - board_bot.position.x) + abs(base.y - board_bot.position.y))*2000) and board_bot.properties.diamonds !=0) or board_bot.properties.diamonds == 5):
            return [999, base]
        else: 
            return [None,None] #no need to go home immediately
        
    #TODO: kalo udah 3 diamonds cari sekitar base aja
    def searchAroundHome(self, board_bot: GameObject, board: Board) -> Optional[list[int, Position]]:
        base = board_bot.properties.base
        closestToBase = min(
                    board.diamonds,
                    key = lambda x: abs(x.position.x - base.x) + abs(x.position.y - base.y)
                )
        distance = abs(closestToBase.position.x - base.x) + abs(closestToBase.position.y - base.y);
        if (board_bot.properties.diamonds == 4 and (distance <= 6)):
            return ([distance*1000/6, closestToBase.position]) 
        elif (board_bot.properties.diamonds == 3 and (distance <= 4)): #karena sisa 4, cari yang deket banget aja
            return ([distance*1000/4, closestToBase.position]) 
        else:
            return ([500, base]) #mending balik

    def process(self, board_bot: GameObject, board: Board) -> Optional[list[tuple[int, Position]]]:
        a = self.goHomeImmediately(board_bot)
        b = self.searchAroundHome(board_bot, board)
        if (a != [None,None]):
            return a
        else:
            return b

