import re

SYMBOL_RE = r'[^\w.\s]'
PART_NUMBER_RE = r'[\d]+'

def is_overlapping(bb, point):
    check_start = (bb.tl.x <= point.tl.x and point.tl.x <= bb.br.x and bb.tl.y <= point.tl.y and point.tl.y <= bb.br.y)
    check_end = (bb.tl.x <= point.br.x and point.br.x <= bb.br.x and bb.tl.y <= point.br.y and point.br.y <= bb.br.y)
    
    if check_start or check_end:
        return True
    
    return False

class Coord:
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Coord'):
        x = self.x + other.x
        y = self.y + other.y
        return Coord(x, y)
    
    def __add__(self, other: int):
        x = self.x + other
        y = self.y + other
        return Coord(x, y)
    
    def __sub__(self, other: 'Coord'):
        x = self.x - other.x
        y = self.y - other.y
        return Coord(x, y)
    
    def __sub__(self, other: int):
        x = self.x - other
        y = self.y - other
        return Coord(x, y)
    
    def __str__(self):
        return f'({self.x}, {self.y})'

class Symbol:
    
    def __init__(self, icon: str, coords: Coord):
        self.icon = icon
        self.coords = coords
        self.part_numbers = []

        self.bounding_box = None
        self.set_bbox()

    def __str__(self):
        return f'{self.icon} @ {self.coords}'
    
    def set_bbox(self):
        global width
        global height
        
        upper_left = Coord(
            max(self.coords.x-1 ,0),
            max(self.coords.y-1, 0)
            )
        lower_right = Coord(
            min(self.coords.x+1, width-1),
            min(self.coords.y+1, height-1)
            )
        
        self.bounding_box = BoundingBox(upper_left, lower_right)

class PartNumber:
    
    def __init__(self, num: int, coords: Coord):
        self.num = num
        self.len = len(str(num))
        self.coords = coords
        
        self.bounding_box = None
        self.set_bbox()
    
    def __str__(self):
        return f'{self.num} @ {self.coords}'
    
    def __repr__(self):
        return self.__str__()
    
    def set_bbox(self):
        global width
        global height
        
        self.bounding_box = BoundingBox(self.coords, Coord(self.coords.x + self.len-1, self.coords.y))

class BoundingBox:
    
    def __init__(self, tl: Coord, br: Coord):
        self.tl = tl
        self.br = br

# get total dimensions of schematic
width = 0
height = 0

lines = []
with open('input.txt', 'r') as f:
    lines = f.readlines()

width = len(lines)
height = len(lines[0])

print(f'The dimensions of the schematic are: {width}x{height}')

# Get symbols and part nums and their coords
symbols = []
part_numbers = []
for row, line in enumerate(lines):
    for symbol_match in re.finditer(SYMBOL_RE, line):
        icon = symbol_match.group(0)
        coord = Coord(symbol_match.start(0), row)
        
        symbols.append(Symbol(icon, coord))
    
    for part_num_match in re.finditer(PART_NUMBER_RE, line):
        num = part_num_match.group(0)
        coord = Coord(part_num_match.start(0), row)
        
        part_numbers.append(PartNumber(num, coord))

# Determine sum of overlapping
sum_overlap = 0
for part_number in part_numbers:
    for symbol in symbols:
        if is_overlapping(symbol.bounding_box, part_number.bounding_box):
            symbol.part_numbers.append(part_number)
            sum_overlap += int(part_number.num)

print(f'The total sum of real part numbers: {sum_overlap}')

sum_ratios = 0
for symbol in symbols:
    if len(symbol.part_numbers) == 2:
        sum_ratios += int(symbol.part_numbers[0].num) * int(symbol.part_numbers[1].num)
        print(f'Part numbers for {symbol}\n\t{symbol.part_numbers}')

print(f'The total sum of gear ratios: {sum_ratios}')