import copy
import os
import time
import queue
from tqdm import tqdm
from dataclasses import dataclass, field
from enum import Enum

class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    
    @staticmethod
    def get_char(val: 'Direction') -> str:
        if val == Direction.RIGHT:
            return '>'
        elif val == Direction.LEFT:
            return '<'
        elif val == Direction.UP:
            return '^'
        elif val == Direction.DOWN:
            return 'v'

@dataclass
class Beam:
    direction: Direction = Direction.RIGHT
    coord: tuple = (0, 0)
    
    def travel(self):
        """
        Travel a single unit in the current travel direction
        """
        if self.direction == Direction.RIGHT:
            self.coord = (self.coord[0]+1, self.coord[1])
        elif self.direction == Direction.LEFT:
            self.coord = (self.coord[0]-1, self.coord[1])
        elif self.direction == Direction.UP:
            self.coord = (self.coord[0], self.coord[1]-1)
        elif self.direction == Direction.DOWN:
            self.coord = (self.coord[0], self.coord[1]+1)

class TileType(Enum):
    EMPTY = ord('.')
    MIRROR_L = ord('/')
    MIRROR_R = ord('\\')
    SPLITTER_V = ord('|')
    SPLITTER_H = ord('-')

@dataclass
class Tile:
    kind: TileType
    visits: dict = field(default_factory=lambda: {x: False for x in Direction})
    
    def __str__(self):
        if self.kind == TileType.EMPTY:
            num_visits = sum([1 for key, value in self.visits.items() if value])
            if num_visits == 0:
                return chr(TileType.EMPTY.value)
            elif num_visits == 1:
                val = ''
                for key, value in self.visits.items():
                    if value:
                        return Direction.get_char(key)
            elif num_visits > 1:
                return f'{num_visits}'

        else:
            return f'{chr(self.kind.value)}'
    
    def __repr__(self) -> str:
        return self.__str__()

    def reset(self):
        for key in self.visits:
            self.visits[key] = False

    def is_energized(self) -> bool:
        return any([self.visits[key] for key in self.visits])

    def visit(self, beam: Beam) -> list:
        """Visit the tile, return the next beam(s)
        to be added to the queue

        Args:
            beam (Beam): beam that is visiting
            the tile

        Returns:
            list[Beam]: A list of the beams that exited
            this tile
        """
        direction = beam.direction
        
        if self.visits[direction]:
            # Return an empty list if this tile
            # has already been visited in the same dir (loop/cycle)
            return []
        else:
            # Mark the direction as having been visited
            # the keep track of loops/cycles
            self.visits[direction] = True
            
            
            # Handle each of the types of tiles
            if self.kind == TileType.EMPTY:
                beam.travel()
                return [beam]
            elif self.kind == TileType.MIRROR_L:
                # /
                if direction == Direction.RIGHT:
                    beam.direction = Direction.UP
                elif direction == Direction.LEFT:
                    beam.direction = Direction.DOWN
                elif direction == Direction.UP:
                    beam.direction = Direction.RIGHT
                elif direction == Direction.DOWN:
                    beam.direction = Direction.LEFT
                
                beam.travel()
                return [beam]
            
            elif self.kind == TileType.MIRROR_R:
                # \
                
                if direction == Direction.RIGHT:
                    beam.direction = Direction.DOWN
                elif direction == Direction.LEFT:
                    beam.direction = Direction.UP
                elif direction == Direction.UP:
                    beam.direction = Direction.LEFT
                elif direction == Direction.DOWN:
                    beam.direction = Direction.RIGHT
                
                beam.travel()
                return [beam]
                
            elif self.kind == TileType.SPLITTER_V:
                
                # |
                if direction == Direction.UP or direction == Direction.DOWN:
                    # if travel parallel to splitter, just continue as normal
                    beam.travel()
                    return [beam]
                else:
                    # Otherwise, split the beam into up and down
                    beam.direction = Direction.UP
                    beam2 = Beam(direction=Direction.DOWN, coord=beam.coord)
                    beam.travel()
                    beam2.travel()
                    return [beam, beam2]
            elif self.kind == TileType.SPLITTER_H:
                
                # -
                if direction == Direction.LEFT or direction == Direction.RIGHT:
                    # if travel parallel to splitter, just continue as normal
                    beam.travel()
                    return [beam]
                else:
                    # Otherwise, split the beam into left and right
                    beam.direction = Direction.LEFT
                    beam2 = Beam(coord=beam.coord)
                    beam.travel()
                    beam2.travel()
                    return [beam, beam2]
            else:
                return []

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def reset_grid(grid) -> list:
    for i, row in enumerate(grid):
        for key in row:
            grid[i][key].reset()

def print_grid(grid):
    for row in grid:
        for tile in row:
            # print(tile, end=' ')
            print(row[tile], end=' ')
        print()

def visualize_travel(beam, grid, timestep=0.01):
    beams = queue.Queue()
    beams.put(beam)

    while not beams.empty():
        beam = beams.get()
        bx, by = beam.coord
        
        if (bx < gx and by < gy) and (bx >= 0 and by >= 0) :
            new_beams = grid[by][(bx, by)].visit(beam)
            
            for new_beam in new_beams:
                beams.put(new_beam)

        cls()
        print_grid(grid)
        time.sleep(timestep)
    
    num_energized = 0
    for row in grid:
        for coord, tile in row.items():
            if tile.is_energized():
                num_energized += 1
    print(f'There are {num_energized} energized tiles in the above configuration')

grid = [{(x, y): Tile(TileType(ord(char))) for x, char in enumerate(row.strip())} for y, row in enumerate(open('input.txt', 'r').readlines())]
gx = len(grid[0])
gy = len(grid)

beams = queue.Queue()
# Start with a single beam
beams.put(Beam())

# Work on the beams in the queue
# Move the beam in it's direction
# and determine if it splits or it's new direction
# (if any).
# Re-add any beams back to the queue if they can still
# validly move (did not re-visit a tile in the same dir)

while not beams.empty():
    beam = beams.get()
    bx, by = beam.coord
    
    if (bx < gx and by < gy) and (bx >= 0 and by >= 0) :
        new_beams = grid[by][(bx, by)].visit(beam)
        
        for new_beam in new_beams:
            beams.put(new_beam)

    # print_grid(grid)
    # time.sleep(0.01)
    # cls()

num_energized = 0
for row in grid:
    for coord, tile in row.items():
        if tile.is_energized():
            num_energized += 1

print(f'Part1: There are {num_energized} tiles energized')

# Part2

possible_beams = []
# Top and Bottom
for i in range(gx):
    bt = Beam(direction=Direction.DOWN, coord=(i, 0))
    bb = Beam(direction=Direction.UP, coord=(i, gy-1))
    possible_beams.append(bt)
    possible_beams.append(bb)

# Left and Right
for i in range(gy):
    bl= Beam(direction=Direction.RIGHT, coord=(0, i))
    br= Beam(direction=Direction.LEFT, coord=(gx-1, i))
    possible_beams.append(bl)
    possible_beams.append(br)

max_energy = 0
best_beam = None

for possible_beam in tqdm(possible_beams):
    reset_grid(grid)
    temp = copy.deepcopy(possible_beam)
    beams = []
    # Start with a single beam
    beams.append(possible_beam)

    # Work on the beams in the queue
    # Move the beam in it's direction
    # and determine if it splits or it's new direction
    # (if any).
    # Re-add any beams back to the queue if they can still
    # validly move (did not re-visit a tile in the same dir)

    while beams:
        beam = beams.pop()
        bx, by = beam.coord
        
        if (bx < gx and by < gy) and (bx >= 0 and by >= 0) :
            new_beams = grid[by][(bx, by)].visit(beam)
            
            for new_beam in new_beams:
                beams.append(new_beam)

    num_energized = 0
    for row in grid:
        for coord, tile in row.items():
            if tile.is_energized():
                num_energized += 1
    
    if num_energized > max_energy:
        max_energy = num_energized
        best_beam = temp

print(f'Part2: the optimal energization config provides {max_energy} energized tiles.')