from typing import Optional

from ...logic.base import BaseLogic
from ...models import GameObject, Board, Position
from ...models import Board
from ...logic.Processors.Processor import Processor
from ...util import *
from .DiamondProcessor import DiamondProcessor


class Teleporter(Processor):
    def __init__(self):
        super().__init__()
        self.DiamondProcessor: DiamondProcessor = DiamondProcessor()
        self.multiplier = 2

    """
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
        return dist, closestTeleport.position

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
            return nearTele1, closestTeleport1, teleporter[0]
        else:
            return nearTele2, closestTeleport1, teleporter[1]


    def TeleOrDia(self, botTele: tuple[int, Position], nearestDia: tuple[int, Position], nearestTele: tuple[int, GameObject, GameObject]) -> tuple[int, Position]:
        distDia  = nearestDia[0]
        distTele: int = botTele[0] + nearestTele[0]

        if(distDia > distTele):
            return 1000, botTele[1]
    """

    def process(self, board_bot: GameObject, board: Board, maxi_val: int, dist_to_home: int) -> list[tuple[int, Position]]:
        teleporter = list(filter(lambda x: x.type == "TeleportGameObject", board.game_objects))
        diamonds = list(filter(lambda x: x.type == "DiamondGameObject", board.game_objects))
        if not teleporter:
            return []
        tele1, tele2 = teleporter
        # tele_obj1, tele_obj2 = GameObject(0, tele1.position, ""), GameObject(0, tele2.position, "")
        funcGO = lambda x, y: abs(x.position.x - y.position.x) + abs(x.position.y - y.position.y)
        minDia1 = min(diamonds, key=lambda x: funcGO(x, tele1))
        minDia2 = min(diamonds, key=lambda x: funcGO(x, tele2))
        dtl1 = funcGO(tele1, board_bot)
        dtl2 = funcGO(tele2, board_bot)
        if funcGO(minDia1, tele1) + dtl1 >= len(self.DiamondProcessor.prio_dia):
            max1 = -1
        else:
            max1 = self.DiamondProcessor.prio_dia[funcGO(minDia1, tele1) + dtl1]
        if funcGO(minDia2, tele2) + dtl2 >= len(self.DiamondProcessor.prio_dia):
            max2 = -1
        else:
            max2 = self.DiamondProcessor.prio_dia[funcGO(minDia2, tele2) + dtl2]
        ans = []
        if max1 > 0 and max1 > maxi_val and max1 >= max2:
            ans.append((max1, tele1.position))
        if max2 > 0 and max2 > maxi_val and max2 > max1:
            ans.append((max2, tele2.position))
        dist1_home = dtl1 + abs(board_bot.properties.base.x - tele1.position.x) + \
                     abs(board_bot.properties.base.y - tele1.position.y)
        dist2_home = dtl2 + abs(board_bot.properties.base.x - tele2.position.x) + \
                     abs(board_bot.properties.base.y - tele2.position.y)
        if dist1_home < len(self.DiamondProcessor.prio_dia):
            if self.DiamondProcessor.prio_dia[dist1_home] > dist_to_home:
                ans.append((self.DiamondProcessor.prio_dia[dist1_home], tele1.position))
        if dist2_home < len(self.DiamondProcessor.prio_dia):
            if self.DiamondProcessor.prio_dia[dist2_home] > dist_to_home:
                ans.append((self.DiamondProcessor.prio_dia[dist2_home], tele2.position))
        return ans
