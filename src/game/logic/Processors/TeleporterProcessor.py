from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from game.models import Board
from game.logic.Processors.Processor import Processor
from game.util import *


class Teleporter(Processor):
    def __init__(self):
        super().__init__()
        pass

    def teleportPosition(self, board: Board) -> list[GameObject]:
        teleporter: list[GameObject] = []

        for game_object in board.game_objects:
            if game_object.type == "TeleportGameObject":
                teleporter.append(game_object)
        return teleporter

    # bot teleport
    def nearTeleport(self, teleporter: list[GameObject], board_bot: GameObject) -> tuple[int, Position]:
        closestTeleport = min(
            teleporter,
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        dist: int = abs(closestTeleport.position.x - board_bot.position.x) + abs(closestTeleport.position.y - board_bot.position.y)
        return [dist, closestTeleport.position]

    # nearest diamond teleport
    def nearTeleDia(self, teleporter: list[GameObject], diamond: list[GameObject]) -> tuple[int, GameObject, GameObject]:
        closestTeleport1 = min(
            diamond,
            key= lambda x: abs(teleporter[0].position.x - x.position.x) + abs(teleporter[0].position.y - x.position.y)
        )

        closestTeleport2 = min(
            diamond,
            key= lambda x: abs(teleporter[1].position.x - x.position.x) + abs(teleporter[1].position.y - x.position.y)
        )

        nearTele1: int = abs(closestTeleport1.position.x - teleporter[0].position.x) + abs(closestTeleport1.position.y - teleporter[0].position.y)
        nearTele2: int = abs(closestTeleport2.position.x - teleporter[1].position.x) + abs(closestTeleport2.position.y - teleporter[1].position.y)

        if(nearTele1 < nearTele2):
            return [nearTele1, closestTeleport1, teleporter[0]]
        else:
            return [nearTele2, closestTeleport1, teleporter[1]]


    def TeleOrDia(self, botTele: tuple[int, Position], nearestDia: tuple[int, Position], nearestTele: tuple[int, GameObject, GameObject]) -> tuple[int, Position]:
        distDia  = nearestDia[0]
        distTele: int = botTele[0] + nearestTele[0]

        if(distDia < distTele):
            return 1000, nearestDia[1]
        else:
            return 1000, botTele[1]

    def process(self, board_bot: GameObject, board: Board) -> list[tuple[int, Position]]:
        teleportList: list[GameObject] = self.teleportPosition(board)
        diamondList: list[GameObject] = position_of_objects(board, "DiamondGameObject")
        botTele: tuple[int, Position] = self.nearTeleport(teleportList, board_bot) #teleport paling dekat dengan bot
        nearestTeleToDia: tuple[int, GameObject, GameObject] = self.nearTeleDia(teleportList, diamondList) ## jarak diamond terdekat ke teleport
        nearestDia: tuple[int, GameObject.position] = nearestDiaGeneral(diamondList, board_bot)
        print(self.TeleOrDia(botTele, nearestDia, nearestTeleToDia))
        return [self.TeleOrDia(botTele, nearestDia, nearestTeleToDia)]







