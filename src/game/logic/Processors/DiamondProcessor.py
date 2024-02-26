import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction
from ...models import Board
from .Processor import Processor


class DiamondProcessor(Processor): 
    def __init__(self): 
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