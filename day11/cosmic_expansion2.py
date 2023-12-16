import numpy as np

def get_dist(p1: tuple, p2: tuple) -> int:
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

lines = [x.strip() for x in open('input.txt', 'r').readlines()]

increase_const = 1000000

new_lines = []
for i, line in enumerate(lines):
    if all([x == '.' for x in line]):
        new_lines.append([(1,increase_const) for _ in line])
    else:
        new_lines.append([(1,1) if char == '.' else char for char in line])

lines = new_lines

# Initial list is constructed with height expansions, determine which columns need expansion
occ_cols = {}
for row in lines:
    for i, val in enumerate(row):
        if val == '#':
            occ_cols[i] = True

for j, row in enumerate(lines):
    for i, val in enumerate(row):
        if i not in occ_cols:
            if isinstance(val, tuple):
                lines[j][i] = (increase_const, val[1])

galaxies = []
counter = 0
x = 0
y = 0
for i, line in enumerate(lines):
    x = 0
    for j, char in enumerate(line):
        if char == '#':
            galaxies.append((counter, x, y, {}))
            counter+=1
            x += 1
        else:
            x += char[0]
    
    # If there is a # on the row
    if any([True if x == '#' else False for x in line]):
        y += 1
    else:
        y += line[0][1]

sum = 0
for ind, (id1, x1, y1, dists1) in enumerate(galaxies):
    for id2, x2, y2, dists2 in galaxies[ind+1:]:
        galaxies[ind][3][id2] = get_dist((x1,y1), (x2,y2))
    
    for dist in dists1:
        sum += dists1[dist]

print(f'PART2: {sum}')