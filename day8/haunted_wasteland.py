import math

lines = open('input.txt', 'r').readlines()

instructions = lines[0].strip()
instr_len = len(instructions)

element_re = r'([A-Z]{3})[\s=]+\(([A-Z]{3})[,\s]+([A-Z]{3})\)'
elements = {}
for line in lines[2:]:
    id = line[0:3]
    left = line[7:10]
    right = line[12:15]
    
    elements[id] = {
        'id': id,
        'L': left,
        'R': right
    }

curr_element = elements['AAA']
counter = 0

while curr_element['id'] != 'ZZZ':
    curr_element = elements[curr_element[instructions[counter%instr_len]]]
    counter+=1

print(f'Part1: Took {counter} steps to reach ZZZ')

# Part 2
start_nodes = [elements[x] for x in elements if x.endswith('A')]
counters = []

for start_node in start_nodes:
    curr_element = elements[start_node['id']]
    counter = 0

    while not curr_element['id'].endswith('Z'):
        curr_element = elements[curr_element[instructions[counter%instr_len]]]
        counter+=1
    
    counters.append(counter)


# Calculate Lowest Common Multiple of individual paths
print(f'Part2: Took {math.lcm(*counters)} steps to reach XXZ')
