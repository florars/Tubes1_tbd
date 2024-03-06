import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class RandomLogic(BaseLogic):
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

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        diamondPos = self.gameObjectPos(board, "DiamondGameObject")
        redDiamondPos = self.redDiamond(diamondPos)
        blueDiamondPos = self.blueDiamond(diamondPos)

        if props.diamonds == 5:
            base = board_bot.properties.base
            self.goal_position = base
        else:
            closeToRed: int = 1000 #Memastikan posisi akan selalu ada meskipun di list tidak terdapat diamond
            closeToBlue: int = 1000
            if redDiamondPos:
                closestRed = min(
                    redDiamondPos,
                    key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
                )
                closeToRed = abs(closestRed.position.x - board_bot.position.x) + abs(closestRed.position.y - board_bot.position.y) 

            if blueDiamondPos:
                closestBlue = min(
                    blueDiamondPos,
                    key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
                ) 
                closeToBlue = abs(closestBlue.position.x - board_bot.position.x) + abs(closestBlue.position.y - board_bot.position.y) 
            if(closeToRed < closeToBlue):
                self.goal_position = closestRed.position
            else: 
                self.goal_position = closestBlue.position


        current_position = board_bot.position
        if self.goal_position:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y
