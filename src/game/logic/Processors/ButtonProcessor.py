"""

from ...models import Board, Bot, GameObject, Position
from typing import Optional


class ButtonProcessor:
    bot: Bot
    further_but_not_far_enough = 50
    closer = 30

    def get_bot_pos(self, board: Board) -> (int, int):
        for game_object in board.game_objects:
            if game_object.type == "BotGameObject" and game_object.id == self.bot.id:
                return game_object.position.x, game_object.position.y
        return -1, -1

    def __init__(self, _bot: Bot):
        self.bot = _bot

    def eval_button(self, bot_x: int, bot_y: int, button: GameObject, nearest_dia: GameObject) -> float:
        dist_but: int = abs(button.position.x - bot_x) + abs(button.position.y - bot_y)
        dist_dia: int = abs(nearest_dia.position.x - bot_x) + abs(nearest_dia.position.y - bot_y)
        ratio: float = dist_dia / dist_but
        if dist_but < dist_dia and dist_dia - dist_but >= 5:
            return 100 + (dist_dia - dist_but) * 10
        elif dist_but < dist_dia:
            return ratio * self.further_but_not_far_enough
        else:
            return ratio * self.closer

    def process(self, board: Board) -> list[tuple[int, Position]]:
        bot_x, bot_y = self.get_bot_pos(board)
        if bot_x == -1:
            return []
        diamonds = [game_object for game_object in board.game_objects if game_object.type == "DiamondGameObject"]
        but_l: list[GameObject] = [game_object for game_object in board.game_objects
                              if game_object.type == "DiamondButtonGameObject"]
        if not but_l:
            return []
        button: GameObject = but_l[0]
        if not diamonds:
            return [(67, button.position)]
        nearest_dia = min([game_object for game_object in board.game_objects
                           if game_object.type == "DiamondGameObject"],
                          key=lambda g: abs(bot_x - g.position.x) + abs(bot_y - g.position.y))
        return round(self.eval_button(bot_x, bot_y, button, nearest_dia))



"""