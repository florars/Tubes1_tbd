from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction
from ...models import Board
from .Processor import Processor


class DiamondProcessor(Processor): 
    def __init__(self): 
        super.__init__(self)
        pass

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
    
    def nearestDiamond(blue: list[GameObject], red: list[GameObject], board_bot: GameObject) -> tuple[int, GameObject.position]:
        closestRed = min(
            blue,
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        closestBlue = min(
            red,
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )

        closeToRed: int = abs(closestRed.position.x - board_bot.position.x) + abs(closestRed.position.y - board_bot.position.y) 
        closeToBlue: int = abs(closestBlue.position.x - board_bot.position.x) + abs(closestBlue.position.y - board_bot.position.y) 


        if(closeToRed < closeToBlue):
            return [closeToRed, closestRed.position]
        else: 
            return [closeToBlue, closestBlue.position]