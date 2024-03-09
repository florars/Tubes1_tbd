from typing import Optional

#from game.logic.base import BaseLogic
from ...models import GameObject, Board, Position
#from ...util import get_direction
from ...models import Board
from ...logic.Processors.Processor import Processor

class DiamondProcessor(Processor): 
    def __init__(self):
        self.take_n = 4
        self.rad_consider = 3
        self.return_diamond = 2
        self.prio_dia = [0, 100, 90, 85, 80, 75, 51, 30, 20, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        super().__init__()
    """
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

    def eval_elem(self, diamond: GameObject, diamonds: list[GameObject]):
        cnt: int = 0
        for d in diamonds:
            if abs(d.position.x - diamond.position.x) + abs(d.position.y - diamond.position.y) <= self.rad_consider:
                cnt += 1
        return cnt
    """
    def nearestDiamond(self, diamonds: list[GameObject], board_bot: GameObject) -> list[GameObject]:
        diamonds.sort(key=lambda g: abs(g.position.x - board_bot.position.x) + abs(g.position.y - board_bot.position.y))
        first_n_elem = diamonds[:self.take_n]
        #first_n_elem.sort(key=lambda g: self.eval_elem(g, diamonds), reverse=True)
        return first_n_elem[:self.return_diamond]

    def process(self, board_bot: GameObject, board: Board) -> Optional[list[tuple[int, Position]]]:
        #diamonds = [game_object for game_object in board.game_objects if game_object.type == "DiamondGameObject"]
        diamonds = list(filter(lambda x: x.type == "DiamondGameObject", board.game_objects))
        if not diamonds:
            return []
        if board_bot.properties is not None:
            if board_bot.properties.diamonds == 4:
                diamonds = list(filter(lambda x: x.properties.points == 1, diamonds))
        processed: list[GameObject] = self.nearestDiamond(diamonds, board_bot)
        return [(self.prio_dia[abs(game_object.position.x - board_bot.position.x) + abs(game_object.position.y - board_bot.position.y)],
                 game_object.position) for game_object in processed
                if abs(game_object.position.x - board_bot.position.x) + abs(game_object.position.y - board_bot.position.y) < len(self.prio_dia)]
