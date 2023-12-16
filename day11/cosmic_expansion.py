import numpy as np

def get_dist(p1: tuple, p2: tuple) -> int:
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

lines = [x.strip() for x in open('input.txt', 'r').readlines()]

new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if all([x == '.' for x in line]):
        new_lines.append(line)

lines = np.asarray([[z for z in x] for x in new_lines])

verts_ind = []
for i, line in enumerate(lines.T):
    if all([x == '.' for x in line]):
        verts_ind.append(i+len(verts_ind))

for ind in verts_ind:
    lines = np.insert(lines, ind, '.', axis=1)

galaxies = []
counter = 0
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == '#':
            galaxies.append((counter, x, y, {}))
            counter+=1
print(galaxies)
sum = 0
for ind, (id1, x1, y1, dists1) in enumerate(galaxies):
    for id2, x2, y2, dists2 in galaxies[ind+1:]:
        galaxies[ind][3][id2] = get_dist((x1,y1), (x2,y2))
    
    for dist in dists1:
        sum += dists1[dist]

print(f'PART1: {sum}')