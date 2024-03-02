from typing import Optional

#from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
#from ...util import get_direction
from game.models import Board
from game.logic.Processors.Processor import Processor


class DiamondProcessor(Processor): 
    def __init__(self): 
        super().__init__()

    def isInventoryRed(self, board_bot: GameObject) -> bool:
        if(board_bot.properties.diamonds == 4):
            return True
        else:
            return False

    def redDiamond(self, arr: list[GameObject]) -> list[GameObject]: 
        ans = []
        for i in arr: 
            if(i.properties.points == 2): 
                ans.append(i)
        return ans
    
    def blueDiamond(self, arr: list[GameObject]) -> list[GameObject]: 
        ans = [] 
        for i in arr: 
            if(i.properties.points == 1): 
                ans.append(i) 
        return ans
    
    def nearestDiamond(self, blue: list[GameObject], red: list[GameObject], board_bot: GameObject) ->tuple[int, Position]:
        if not red:
            closestRed = GameObject(0, Position(1000, 1000), None, None)
        else:
            closestRed = min(
                red,
                key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
            )

        if not blue:
            closestBlue = GameObject(0, Position(1000, 1000), None, None)
        else:
            closestBlue = min(
                blue,
                key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
            )

        closeToRed: int = abs(closestRed.position.x - board_bot.position.x) + abs(closestRed.position.y - board_bot.position.y) 
        closeToBlue: int = abs(closestBlue.position.x - board_bot.position.x) + abs(closestBlue.position.y - board_bot.position.y) 

        if(board_bot.properties.diamonds == 4):
            return closeToBlue, closestBlue.position
        else:
            if(closeToRed < closeToBlue):
                return closeToRed, closestRed.position
            else:
                return closeToBlue, closestBlue.position
                
    def process(self, board_bot: GameObject, board: Board) -> Optional[list[tuple[int, Position]]]:
        game_objects = board.game_objects
        return [self.nearestDiamond(self.blueDiamond(game_objects), self.redDiamond(game_objects), board_bot)]
    
        

