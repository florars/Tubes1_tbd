from typing import Optional 

from game.models import GameObject, Board, Position
from game.logic.Processors.Processor import Processor 
from ..util import get_direction
from random import random


class greedyTackle(Processor):
    def __init__(self):
        super().__init__()
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def listEnemy(self, board_bot: GameObject, board: Board) -> list[GameObject]: 
            props = board_bot.properties
            listBots: list[GameObject] = []
            if(len(board.bots) == 1):
                return []
            else: 
                for bots in board.bots: 
                    if bots.id != board_bot.id:
                        listBots.append(bots)

            return listBots
    
    def nearestEnemy(self, board_bot: GameObject, listBots: list[GameObject]) -> GameObject:
        nearest_enemy: GameObject = min(
            listBots, 
            key = lambda x: abs(x.position.x - board_bot.position.x) + abs(x.position.y - board_bot.position.y)
        )
        return nearest_enemy
    
    def hasMoreDiamond(self, board_bot: GameObject, listBots: list[GameObject])->GameObject:
        richEnemy: GameObject = listBots[0]
        for bot in listBots: 
            if (bot.properties.diamonds > richEnemy.properties.diamonds): 
                richEnemy = bot
        return richEnemy
    
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds >= 3:
            base = board_bot.properties.base
            self.goal_position = base
        else:
            listBot: list[GameObject] = self.listEnemy(board_bot, board)
            nearest_enemy: GameObject = self.nearestEnemy(board_bot, listBot)
            rich_enemy: GameObject = self.hasMoreDiamond(board_bot, listBot)

            botToEnemy: int = abs(board_bot.position.x - nearest_enemy.position.x) + abs(board_bot.position.y - nearest_enemy.position.y)
            botToRich : int = abs(board_bot.position.x - rich_enemy.position.x) + abs(board_bot.position.y-rich_enemy.position.y)
            if(botToRich < botToEnemy):
                self.goal_position = rich_enemy.position
            else:
                self.goal_position = nearest_enemy.position
        print(self.goal_position)
        current_position: Position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
            return delta_x, delta_y
           
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        if (delta_x == 0 and delta_y == 0):
            return self.directions[random.randint(0, 3)]
        return delta_x, delta_y
            