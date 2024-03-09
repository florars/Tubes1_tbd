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
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            closestRed = min(
                redDiamondPos,
                key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
            )
            closestBlue = min(
                blueDiamondPos,
                key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
            )

            closeToRed = abs(closestRed.position.x - board_bot.position.x) + abs(closestRed.position.y - board_bot.position.y) 
            closeToBlue = abs(closestBlue.position.x - board_bot.position.x) + abs(closestBlue.position.y - board_bot.position.y) 
            if(closeToRed < closeToBlue):
                self.goal_position = closestRed.position
            else: 
                self.goal_position = closestBlue.position
                
        
        # ansTele = self.diamondPos(board, "TeleportGameObject")
        # print("diamon: " + str(ansdiamond))
        # print("teleporter: " +  str(ansTele))

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        return delta_x, delta_y