from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction
from Processor import Processor

class SelfDefense(Processor):
    def __init__(self):
        super.__init__(self)
        pass

    def run(self, board_bot: GameObject, board: Board):
        nearest_enemy = min(
            [d for d in board.bots if d.id!=self.id],
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        x = nearest_enemy.position.x - board_bot.position.x
        y = nearest_enemy.position.y - board_bot.position.y
        if (x==0):
            return (1, 0) # buat distance di x-axis, tapi entah cara milih gerak ke mana w/ regards to current goal
        elif (y==0):
            return (0, 1) # buat distance di y-axis, tapi entah cara milih gerak ke mana w/ regards to current goal
        else:
            return (-x,0) # entahlah, gerak ke wherever yang penting jauh dari musuh
        

    def attack(self, board_bot: GameObject, board: Board):
        nearest_enemy = min(
            [d for d in board.bots if d.id!=self.id],
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        x = nearest_enemy.position.x - board_bot.position.x
        y = nearest_enemy.position.y - board_bot.position.y
        return (x,y)

    def threatened(self, board_bot: GameObject, board: Board):
        nearest_enemy = min(
            [d for d in board.bots if d.id!=self.id],
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        distance = abs(nearest_enemy.position.x - board_bot.position.x) + abs(nearest_enemy.position.y - board_bot.position.y)
        if (distance == 2):
            return self.run
        elif (distance == 1):
            return self.attack
        



