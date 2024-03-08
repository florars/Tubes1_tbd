import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class GreedyBase(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def gameObjectPos(self, board: Board, tipe: str) -> list[GameObject]:
        ans = []
        for i in board.game_objects: 
            if(i.type == tipe):
                ans.append(i)

        return ans
    
    def homeBase(self, home_base: GameObject, listDiamond: list[GameObject]) -> list[GameObject]: 
        ans: list[GameObject] = []
        for diamond in listDiamond: 
            tempPos = abs(diamond.position.x - home_base.x) + abs(diamond.position.y - home_base.y)
            if(tempPos <= 7): 
                ans.append(diamond)
          
        return ans
        
    def next_move(self, board_bot: GameObject, board: Board):
        diamondPos: list[GameObject] = self.gameObjectPos(board, "DiamondGameObject")
        homeDiamond: list[GameObject] = self.homeBase(board_bot.properties.base, diamondPos)
        if board_bot.properties.diamonds >= 3:
            base = board_bot.properties.base
            self.goal_position = base
        else:
            #Memastikan posisi akan selalu ada meskipun di list tidak terdapat diamond
            base = board_bot.properties.base
            distanceHome: int = abs(base.x - board_bot.position.x) + (base.y - board_bot.position.y)
            if homeDiamond: 
                closestToDiamondBase = min(
                    homeDiamond, 
                    key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y) 
                )
                self.goal_position = closestToDiamondBase.position
            else: 
                if(distanceHome > 7 ):
                    self.goal_position = base
                else:
                    delta = self.directions[self.current_direction]
                    delta_x = delta[0]
                    delta_y = delta[1]
                    if random.random() > 0.6:
                        self.current_direction = (self.current_direction + 1) % len(
                        self.directions
                    )

        current_position = board_bot.position
        if self.goal_position:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        if (delta_x == 0 and delta_y == 0):
            return self.directions[random.randint(0, 3)]
        return delta_x, delta_y
