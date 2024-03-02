from typing import Optional

#from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction, get_dist
from game.models import Board
from game.logic.Processors.Processor import Processor

class GoHomeProcessor(Processor):
    def __init__(self):
        super().__init__()

    def calc_prio(self, dist_home, dist_dia, multiplier, likelihood) -> int:
        return likelihood + multiplier * (dist_dia - dist_home)

    def process(self, board_bot: GameObject, board: Board) -> list[tuple[int, Position]]:
        home_pos: Position = board_bot.properties.base
        diamonds = [game_object for game_object in board.game_objects if game_object.type == "DiamondGameObject"]
        inv_now: int = board_bot.properties.diamonds
        # no diamond, store ke base aja
        if not diamonds:
            return [(inv_now * 100, home_pos)] # kalo inventory = 0 gak ngaruh
        secLeft: int = board_bot.properties.milliseconds_left // 1000
        # kalo waktu dikit -> pulang, takut mubazir, ambil diamond deket base aja
        if secLeft - get_dist(home_pos, board_bot.position) <= 7:
            return [(500, home_pos)]
        likelihood: int = 0
        multiplier: int = 0
        #print("INV_NOW", inv_now)
        if inv_now == 1:
            likelihood = 10
            multiplier = 18
        elif inv_now == 2:
            likelihood = 40
            multiplier = 20
        elif inv_now == 3:
            likelihood = 75
        elif inv_now == 4:
            likelihood = 90
        elif inv_now == 5:
            likelihood = 100
        nearest_diamond: GameObject = min(diamonds, key=lambda y: get_dist(y.position, board_bot.position))
        dist_dia: int = get_dist(nearest_diamond.position, board_bot.position)
        dist_home: int = get_dist(home_pos, board_bot.position)
        priority_home = self.calc_prio(dist_home, dist_dia, multiplier, likelihood)
        if priority_home <= 0:
            return []
        #print("PRIORITY", priority_home)
        return [(priority_home, home_pos)]

