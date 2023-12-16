import re

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

class Game:

    ID_RE = r'Game\s*(\d*):'
    RED_RE = r'(\d*)\s*red'
    GREEN_RE = r'(\d*)\s*green'
    BLUE_RE = r'(\d*)\s*blue'
    
    MIN_RED = 0
    MIN_GREEN = 0
    MIN_BLUE = 0

    def __init__(self, line):
        self._line = line
        self.id = 0
        self.pulls = []
        self.possible = True
        
        self.set_id()
        self.populate_pulls_v2()

    def set_id(self):
        match = re.match(self.ID_RE, self._line)
        if match:
            self.id = int(match.group(1))
    
    # Part 1
    def populate_pulls_v1(self):
        pull_lines = self._line.split(';')
        for pull in pull_lines:
            red = 0
            green = 0
            blue = 0
            
            red_match = re.search(self.RED_RE, pull)
            green_match = re.search(self.GREEN_RE, pull)
            blue_match = re.search(self.BLUE_RE, pull)
            
            if red_match:
                red = int(red_match.group(1))
            if green_match:
                green = int(green_match.group(1))
            if blue_match:
                blue = int(blue_match.group(1))
            
            self.pulls.append((red, green, blue))
            
            if red > MAX_RED or green > MAX_GREEN or blue > MAX_BLUE:
                self.possible = False
    
    # Part 2
    def populate_pulls_v2(self):
        pull_lines = self._line.split(';')
        for pull in pull_lines:
            red = 0
            green = 0
            blue = 0
            
            red_match = re.search(self.RED_RE, pull)
            green_match = re.search(self.GREEN_RE, pull)
            blue_match = re.search(self.BLUE_RE, pull)
            
            if red_match:
                red = int(red_match.group(1))
            if green_match:
                green = int(green_match.group(1))
            if blue_match:
                blue = int(blue_match.group(1))
            
            self.pulls.append((red, green, blue))
            
            # Keep track of fewest num cubes to make game possible
            if red > self.MIN_RED:
                self.MIN_RED = red
            if green > self.MIN_GREEN:
                self.MIN_GREEN = green
            if blue > self.MIN_BLUE:
                self.MIN_BLUE = blue
    
    def fewest_cubes(self):
        return (self.MIN_RED, self.MIN_GREEN, self.MIN_BLUE)
    
    def cube_powers(self):
        return self.MIN_RED * self.MIN_GREEN * self.MIN_BLUE

games = []
with open('input.txt', 'r') as f:
    for line in f.readlines():
        games.append(Game(line.strip()))

id_sum = 0
for game in games:
    
    # Part 1
    # if game.possible:
    #     id_sum += game.id
    
    # Part 2
    id_sum += game.cube_powers()

print(f'The sum of game powers is {id_sum}')