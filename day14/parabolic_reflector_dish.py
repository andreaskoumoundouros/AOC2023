import functools
from functools import cache
from tqdm import tqdm
import matplotlib.pyplot as plt
import collections.abc as collections

class hash_list(list): 
    def __init__(self, *args): 
        if len(args) == 1 and isinstance(args[0], collections.Iterable): 
            args = args[0] 
        super().__init__(args) 
         
    def __hash__(self): 
        return hash(e for e in self)

def print_lines(lines: tuple):
    for row in lines:
        for char in row:
            print(char, end='')
        print()

# Check if any rocks can roll!
# 0 = N
# 1 = W
# 2 = S
# 3 = E
@cache
def rock_can_roll(lines: tuple, direction: int=0) -> bool:
    if direction == 0:
        for i in range(1, len(lines)):
            for j in range(len(lines[0])):
                char = lines[i][j]
                if char == 'O':
                    if lines[i-1][j] == '.':
                        return True
    
    if direction == 1:
        for i in range(len(lines)):
            for j in range(1, len(lines[0])):
                char = lines[i][j]
                if char == 'O':
                    if lines[i][j-1] == '.':
                        return True
    
    if direction == 2:
        for i in range(len(lines)-1):
            for j in range(len(lines[0])):
                char = lines[i][j]
                if char == 'O':
                    if lines[i+1][j] == '.':
                        return True
    
    if direction == 3:
        for i in range(len(lines)):
            for j in range(len(lines[0])-1):
                char = lines[i][j]
                if char == 'O':
                    if lines[i][j+1] == '.':
                        return True
    
    
    return False
# direction
# 0 = N
# 1 = W
# 2 = S
# 3 = E
@cache
def roll_rocks(lines: tuple, direction: int=0) -> list:
    new_lines = [[y for y in x] for x in lines]
    
    if direction == 0:
        for i in range(1, len(lines)):
            for j in range(len(lines[0])):
                char = lines[i][j]
                if char == 'O' and new_lines[i-1][j] == '.':
                    new_lines[i-1][j] = 'O'
                    new_lines[i][j] = '.'
        
    if direction == 1:
        for i in range(len(lines)):
            for j in range(1, len(lines[0])):
                char = lines[i][j]
                if char == 'O' and lines[i][j-1] == '.':
                        new_lines[i][j-1] = 'O'
                        new_lines[i][j] = '.'
    
    if direction == 2:
        for i in range(len(lines)-1):
            for j in range(len(lines[0])):
                char = lines[i][j]
                if char == 'O' and lines[i+1][j] == '.':
                        new_lines[i+1][j] = 'O'
                        new_lines[i][j] = '.'
    
    if direction == 3:
        for i in range(len(lines)):
            for j in range(len(lines[0])-1):
                char = lines[i][j]
                if char == 'O' and lines[i][j+1] == '.':
                        new_lines[i][j+1] = 'O'
                        new_lines[i][j] = '.'
        
    return tuple(tuple(y for y in x) for x in new_lines)

def calc_load(lines: tuple) -> int:
    load = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            char = lines[i][j]
            if char == 'O':
                load += len(lines) - i

    return load

def guess_seq_len(seq):
    guess = 1
    max_len = len(seq) // 2
    for x in range(2, max_len):
        if seq[0:x] == seq[x:2*x] :
            return x

    return guess

def guess_seq_len2(seq, verbose=False):
    seq_len = 1
    initial_item = seq[0]
    butfirst_items = seq[1:]
    if initial_item in butfirst_items:
        first_match_idx = butfirst_items.index(initial_item)
        if verbose:
            print(f'"{initial_item}" was found at index 0 and index {first_match_idx}')
        max_seq_len = min(len(seq) - first_match_idx, first_match_idx)
        for seq_len in range(max_seq_len, 0, -1):
            if seq[:seq_len] == seq[first_match_idx:first_match_idx+seq_len]:
                if verbose:
                    print(f'A sequence length of {seq_len} was found at index {first_match_idx}')
                break
    
    return seq_len

def index_repeating(seq, index, offset = 0) -> int:
    adj_index = index - offset
    seq_len = len(seq)
    
    return seq[adj_index%seq_len-1]

lines = [[y for y in x.strip()] for x in open('input.txt', 'r').readlines()]

p1_lines = tuple(tuple(y for y in x) for x in lines)
while rock_can_roll(p1_lines):
    p1_lines = roll_rocks(p1_lines)

print(f'PART1: The total load on the support beams is: {calc_load(p1_lines)}')

# Part2
p2_lines = tuple(tuple(y for y in x) for x in lines)
cycles = 1000
full_cycles = 1000000000
x = []
y = []
for _ in tqdm(range(cycles+1), desc='Calculating cycles...'):
    for i in range(4):
        while rock_can_roll(p2_lines, i):
            p2_lines = roll_rocks(p2_lines, i)

    x.append(_)
    y.append(calc_load(p2_lines))

offset = 0
subset = y
seq_len = guess_seq_len(subset)
while seq_len <= 1:
    offset+= 1
    subset = y[offset:]
    seq_len = guess_seq_len(subset)

print(f'The supposed sequence length is {seq_len} with offset of {offset}\n{subset[:seq_len]}')
value = index_repeating(subset[:seq_len], full_cycles, offset)
print(f'PART2: The total load on the support beams is: {value}')
