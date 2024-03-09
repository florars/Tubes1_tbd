from .models import Position
from game.models import GameObject, Board, Position
from game.models import Board

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def get_direction(current_x, current_y, dest_x, dest_y):
    delta_x = clamp(dest_x - current_x, -1, 1)
    delta_y = clamp(dest_y - current_y, -1, 1)
    if delta_x != 0:
        delta_y = 0
    return (delta_x, delta_y)

def get_dist(pa: Position, pb: Position) -> int:
    return abs(pa.x - pb.x) + abs(pa.y - pb.y)


def position_equals(a: Position, b: Position):
    return a.x == b.x and a.y == b.y

def position_of_objects(board: Board, tipe: str) -> list[GameObject]:
    ans: list[GameObject] = []
    for game_object in board.game_objects:
        if game_object.type == tipe:
            ans.append(game_object)
    return ans

def Diamonds(board: Board) -> list[GameObject]: 
    ans = []
    for item in board.game_objects: 
        if(item.type == "DiamondGameObject"): 
            ans.append(item)
    return ans

def nearestDiaGeneral(diamondList: list[GameObject], board_bot: GameObject) -> tuple[int, Position]:
    if diamondList:
        closest = min(
        diamondList,
        key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        return 1, closest.position
    return 1000, None