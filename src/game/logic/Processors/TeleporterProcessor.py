from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction
from ...models import Board
from .Processor import Processor
from .DiamondProcessor import DiamondProcessor


class Teleporter(Processor): 
    def __init__(self): 
        super.__init__(self)
        pass

    def teleportPosition(self, board: Board, tipe: str) -> list[GameObject]:
        teleporter: list[GameObject]

        for game_object in board.game_objects:
            if game_object.type == tipe:
                teleporter.append(game_object)
        return teleporter

    def nearTeleport(self, teleporter: list[GameObject], board_bot: GameObject) -> tuple[int, GameObject.position]:
        closestTeleport = min(
            teleporter,
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y) 
        )
        dist: int = abs(closestTeleport.position.x - board_bot.position.x) + abs(closestTeleport.position.y - board_bot.position.y)
        return [dist,closestTeleport]

    def nearTeleDia(self, teleporter: list[GameObject], diamond: list[GameObject]) -> tuple[int, GameObject, GameObject]:
        ans: tuple[GameObject, GameObject]

        closestTeleport1 = min(
            diamond, 
            key= lambda x: abs(teleporter[0].position.x - x.position.x) + abs(teleporter[0].position.y - x.position.y)
        )    

        closestTeleport2 = min(
            diamond, 
            key= lambda x: abs(teleporter[1].position.x - x.position.x) + abs(teleporter[1].position.y - x.position.y)
        )

        closestDiamondTeleport = min(
            teleporter, 
            key = lambda x: abs(x.position.x - diamond.position.x) + abs(x.position.y - diamond.position.y)
        )

        nearTele1: int = abs(closestTeleport1.position.x - closestDiamondTeleport.position.x) + abs(closestTeleport1.position.y - closestDiamondTeleport.position.y)
        nearTele2: int = abs(closestTeleport2.position.x - closestDiamondTeleport.position.x) + abs(closestTeleport2.position.y - closestDiamondTeleport.position.y)

        if(nearTele1 < nearTele2): 
            return [nearTele1, closestTeleport1, closestDiamondTeleport]
        else:
            return [nearTele2, closestTeleport1, closestDiamondTeleport]

        
    def TeleOrDia(self, botTele: tuple[int, GameObject.position], nearestDia: tuple[int, GameObject.position], nearestTele: tuple[int, GameObject, GameObject]) -> GameObject.position:
        distDia, _ = nearestDia
        distTele: int = botTele[0] + nearestTele[0]

        if(distDia < distTele):
            return botTele[1]
        else:
            return nearestDia[1]


