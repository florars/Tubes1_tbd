from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction
from ...models import Board
from .Processor import Processor


class Teleporter(Processor): 
    def __init__(self): 
        super.__init__(self)

    