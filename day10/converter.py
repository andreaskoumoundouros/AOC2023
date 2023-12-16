filename = 'test'

lines = open(f'{filename}.txt', 'r').readlines()

with open(f'{filename}_convert.txt', 'w', encoding='utf-8') as r:
    for line in lines:
        line = line.replace('J', '┘').replace('F', '┌').replace('7', '┐').replace('L', '└').replace('-', '─').replace('|', '│')
        r.write(line)

# 217	┘ -> J
# 218	┌ -> F
# 191	┐ -> 7
# 192	└ -> L
# ┌┐
# └┘