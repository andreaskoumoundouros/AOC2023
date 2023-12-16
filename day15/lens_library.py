import re

def aoc_hash(values: list) -> int:
    sum = 0
    for char in values:
        sum += char
        sum = sum*17
        sum = sum%256
    
    return sum

def print_boxes(boxes: list):
    for i, box in enumerate(boxes):
        if len(box) > 0:
            print(f'Box {i}: ', end='')
            for key, value in box.items():
                print(f'[{key} {value}]', end=' ')
            print()

def calc_focusing_power(boxes: list) -> int:
    power = 0
    for i, box in enumerate(boxes):
        if len(box) > 0:
            for j, (key, value) in enumerate(box.items()):
                power += (i+1) * (j+1) * value
    
    return power

strings = [x for x in open('input.txt', 'r').readlines()[0].strip().split(',')]
sequences = [[ord(y) for y in x] for x in strings]

sum_tot = 0
for seq in sequences:
    sum_tot += aoc_hash(seq)

print(f'Part 1: The sum for the hash algorithm is: {sum_tot}')

# Part2

seq_re = r'([a-z]+)([=-])([0-9]{1})?'

box_list = []
for i in range(256):
    box_list.append({})
for seq in strings:
    match = re.match(seq_re, seq)
    label = match.groups()[0]
    box_hash = aoc_hash([ord(x) for x in label])
    operation = match.groups()[1]
    focal_length = match.groups()[2] if len(match.groups()) > 2 else None
    
    if operation == '-':
        # Remove from box
        if label in box_list[box_hash]:
            box_list[box_hash].pop(label)
    elif operation == '=':
        # Add box, replace if existing
        box_list[box_hash][label] = int(focal_length)

focusing_power = calc_focusing_power(box_list)

print(f'Part 2: The focusing power is: {focusing_power}')