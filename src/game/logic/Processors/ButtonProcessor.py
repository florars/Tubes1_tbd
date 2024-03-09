from ...models import Board, Bot, GameObject, Position
from typing import Optional


class ButtonProcessor:
    bot: Bot
    further_but_not_far_enough = 50
    closer = 30
    find_rad = 4

    def get_bot_pos(self, board: Board) -> (int, int):
        for game_object in board.game_objects:
            if game_object.type == "BotGameObject" and game_object.id == self.bot.id:
                return game_object.position.x, game_object.position.y
        return -1, -1

    def __init__(self):
        pass

    def eval_button(self, dist_but: int, dist_dia: int, likelihood: int, multiplier: int) -> int:
        return likelihood + multiplier * (dist_dia - dist_but)

    def process(self, board_bot: GameObject, board: Board) -> list[tuple[int, Position]]:
        funcGO = lambda x, y: abs(x.x - y.x) + abs(x.y - y.y)
        closestDiamonds = list(filter(lambda g: g.type == "DiamondGameObject" and funcGO(g.position, board_bot.position) <= self.find_rad, board.game_objects))
        num_of_dia = len(closestDiamonds)
        buttonNow: list[GameObject] = list(filter(lambda g: g.type == "DiamondButtonGameObject" and funcGO(g.position, board_bot.position) <= self.find_rad, board.game_objects))
        num_button: int = len(buttonNow)
        if num_button == 0:
            return []
        multiplier = 0
        likelihood = 0
        invNow = board_bot.properties.diamonds
        if invNow == 0:
            likelihood = 100
        elif invNow == 1:
            likelihood = 70
            multiplier = 20
        elif invNow == 2:
            likelihood = 30
            multiplier = 30
        elif invNow >= 3:
            likelihood = 10
        dist_dia = 5
        dist_but = funcGO(buttonNow[0].position, board_bot.position)
        if num_of_dia != 0:
            nearest_dia = min(closestDiamonds, key=lambda g: funcGO(g.position, board_bot.position))
            dist_dia = funcGO(nearest_dia.position, board_bot.position)
        return [(self.eval_button(dist_but, dist_dia, likelihood, multiplier), buttonNow[0].position)]
