from dataclasses import dataclass

from PIL import Image


@dataclass
class Position:
    symbol: str
    coord: tuple
    next = None
    prev = None
    is_start: bool = False
    
    def calc_moves(self, positions: dict):
        # Check if this is a valid 'movement' symbol
        if self.symbol not in SYMBOL_MAP:
            if self.symbol == 'S':
                self.is_start = True
            return
        
        global maze_width
        global maze_height
        
        coord1, coord2 = travel(self.coord, get_sym_direction(self.symbol)), travel(self.coord, get_sym_direction(self.symbol, False))
        if coord1[0] >= 0 and coord1[0] < maze_width and coord1[1] >= 0 and coord1[1] < maze_height:
            self.next = positions[coord1]
        if coord2[0] >= 0 and coord2[0] < maze_width and coord2[1] >= 0 and coord2[1] < maze_height:
            self.prev = positions[coord2]

SYMBOL_MAP = {
    '┘': ('U', 'L'),
    'J': ('U', 'L'),
    '┌': ('R', 'D'),
    'F': ('R', 'D'),
    '└': ('U', 'R'),
    'L': ('U', 'R'),
    '┐': ('L', 'D'),
    '7': ('L', 'D'),
    '─': ('L', 'R'),
    '-': ('L', 'R'),
    '│': ('U', 'D'),
    '|': ('U', 'D'),
}

SYMBOL_COLORS = {
    '┘': 0xFF0000,
    'J': 0xFF0000,
    '┌': 0x00FF00,
    'F': 0x00FF00,
    '└': 0x0000FF,
    'L': 0x0000FF,
    '┐': 0xFF00FF,
    '7': 0xFF00FF,
    '─': 0xFFFF00,
    '-': 0xFFFF00,
    '│': 0x00FFFF,
    '|': 0x00FFFF,
    '.': 0x000000,
    'S': 16777215,
}

def norm_val(val: int, min: int, max: int) -> int:
    return int(((val-min) / (max-min))*0xFFFFFF)

def convert_coord_to_flat(coord: tuple) -> int:
    return coord[0] * coord[1]

def travel(coord: tuple, dir: str):
    if dir == 'U':
        return (coord[0], coord[1]-1)
    elif dir == 'D':
        return (coord[0], coord[1]+1)
    elif dir == 'L':
        return (coord[0]-1, coord[1])
    elif dir == 'R':
        return (coord[0]+1, coord[1])
    else:
        return (-1, -1)

def get_symbol(coord: tuple, lines: list):
    return lines[coord[1]][coord[0]]

def print_symbol(coord: tuple, lines: list):
    print(lines[coord[1]][coord[0]])

def get_sym_direction(sym: str, primary: bool=True) -> str:
    if sym not in SYMBOL_MAP:
        return ''
    
    if primary:
        return SYMBOL_MAP[sym][0]
    else:
        return SYMBOL_MAP[sym][1]

def get_opposite_dir(dir: str):
    if dir == 'U':
        return 'D'
    elif dir == 'D':
        return 'U'
    elif dir == 'L':
        return 'R'
    elif dir == 'R':
        return 'L'

filename = 'input'

lines = [x.strip() for x in open(f'{filename}.txt', encoding='utf-8').readlines()]
maze_width = len(lines[0])
maze_height = len(lines)


# Set start as the 'S'
start = None
for i in range(maze_width):
    for j in range(maze_height):
        if lines[j][i] == 'S':
            start = (i, j)

# Create a representation of the maze
maze_map = {}
maze_map[start] = Position('S', start)
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        coord = (j, i)
        symbol = char
        
        maze_map[coord] = Position(symbol, coord)

for pos in maze_map:
    maze_map[pos].calc_moves(maze_map)

# Travel through each loop until back at s or done

visited = {}
last_visited = maze_map[travel(maze_map[start].coord, 'D')]
visited[last_visited.coord] = last_visited
while not last_visited.is_start:
    next_visit = last_visited.prev
    
    if next_visit.coord in visited:
        next_visit = last_visited.next
    
    if not next_visit:
        print('What in tarnation')
        print(last_visited)
        exit(1)
    
    visited[last_visited.coord] = last_visited
    last_visited = next_visit

# Add the start
visited[last_visited.coord] = last_visited

print(f'Part1: {len(visited)//2}')
# im = Image.new('RGBA', (maze_width, maze_height))
# # img_data = [SYMBOL_COLORS[x] if x in SYMBOL_COLORS else 0x000000 for i, x in enumerate(''.join(lines))]
# # img_data2 = [SYMBOL_COLORS[x]//2 + norm_val(i, 0, maze_width*maze_height)//2 if x in SYMBOL_COLORS else 0x000000 for i, x in enumerate(''.join(lines))]

# img_data = []
# for i in range(maze_width):
#     for j in range(maze_height):
#         coord = (i, j)
#         if maze_map[coord].symbol == '.':
#             img_data.append((0,0,0,0))
#         else:
#             img_data.append((255,0,0,255))
        
#         if coord in visited:
#             img_data[-1] = (0,255,0,255)

# im.putdata(img_data)

# im.save(f'{filename}.png', 'PNG')

# Part 2

def is_point_inside_polygon(x, y, polygon):
    """
    Determine if the point (x, y) is inside the closed polygon.

    Args:
    x, y -- x and y coordinates of the point.
    polygon -- a list of tuples [(x1, y1), (x2, y2), ..., (xn, yn)] representing the vertices of the polygon.

    Returns:
    True if the point is inside the polygon, False otherwise.
    """

    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

import matplotlib.pyplot as plt


def plot_polygon_and_point(polygon, points):
    # Unzip the polygon coordinates for plotting
    x_poly, y_poly = zip(*polygon)

    # Create a new figure
    plt.figure()

    # Plot the polygon
    plt.plot(x_poly + (x_poly[0],), y_poly + (y_poly[0],), 'b-', label='Polygon')

    # Plot the point
    for pt, ins in points:
        if ins:
            point_color = 'green' if ins else 'red'
            plt.scatter(*pt, color=point_color)

    # Set plot labels and legend
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Point in Polygon')
    plt.legend()
    
    plt.gca().invert_yaxis()


    # Show the plot
    plt.show()

# convert path to coords
path_coords = [x for x in visited]

# Example usage
polygon = path_coords  # A square
point = (3, 3)  # Inside the square

inside = is_point_inside_polygon(point[0], point[1], polygon)  # Using the previously defined function

count = 0
inside_coords = []
for i in range(maze_width):
    for j in range(maze_height):
        coord = (i, j)
        if coord not in visited:
            if is_point_inside_polygon(i, j, polygon):
                inside_coords.append((coord, True))
                count += 1
            else:
                inside_coords.append((coord, False))

# Plotting
print(f'Part2: There are {count} points inside the loop')
plot_polygon_and_point(polygon, inside_coords)