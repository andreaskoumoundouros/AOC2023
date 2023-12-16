import re

def largest_contiguous(rec: str) -> tuple:
    
    start = 0
    end = 0
    counter = -1
    for i, char in enumerate(rec):
        if char == '#':
            counter+=1
        elif char == '?' or char == '.':
            if counter > 0:
                new_start = i-counter
                new_end = i-1
                if (end-start) < (new_end-new_start):
                    start = new_start
                    end = new_end
                counter = 0

    if counter:
        new_start = i-counter
        new_end = i-1
        if (end-start) < (new_end-new_start):
            start = new_start
            end = new_end
        counter = 0

    return (start, end)

def get_brokes(rec: str) -> list:
    broke_re = r'([#]+)+'
    brokes = []
    for match in re.finditer(broke_re, rec):
        brokes.append((match.span()[0], match.span()[1], match.span()[1]-match.span()[0]))
        
    return brokes

def get_first_broke(rec: str) -> tuple:
    broke_re = r'([?]+)+'
    for match in re.finditer(broke_re, rec):
        return (match.span()[0], match.span()[1], match.span()[1]-match.span()[0])

def create_perms(num: int, size: int) -> list:
    curr_pos = 0
    perms = []
    while curr_pos+num < size:
        perms.append(''.join(['#' if curr_pos <= i < curr_pos+num  else '.' for i in range(size)]))
        curr_pos += num
    return perms

def const_perms(conts: list, rec: str) -> str:
    
    # Stopping condition
    # record is exhausted
    if len(rec) < 1:
        return ''
    
    # Get first element
    num = conts[0]
    
    # Check if the first instance in the 
    # record list can satisfy the current
    # num
    first_broke = get_first_broke(rec)
    print(first_broke)
    if not first_broke:
        return ''
    elif first_broke[2] == num:
        # Exact size
        print('#'*first_broke[2], end='==')
        return '#'*first_broke[2] + const_perms(conts[1:], rec[first_broke[2]:])
    elif first_broke[2] > num:
        # must create permutations
        perms = create_perms(num, first_broke[2])
        print(perms)
        for perm in perms:
            print(perm, end='>')
            return perm + const_perms(conts[1:], rec[first_broke[2]:])
    else:
        print('What in tarnation!')
        print(conts)
        print(rec)
        exit(1)

# Fuck this. This shit bork.
# test = '?###???????? 3,2,1'
lines = [x.strip() for x in open('test.txt', 'r').readlines()]
for line in lines:
    spring_list, contiguous_list = line.strip().split()

    contiguous_list = [int(x) for x in contiguous_list.split(',')]

    print(spring_list)
    print(contiguous_list)

    combinations = []
    things = const_perms(contiguous_list, spring_list)
