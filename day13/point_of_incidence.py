def count_differences(str1, str2) -> int:
    # Ensure the strings are of the same length
    if len(str1) != len(str2):
        return -1  # or you can handle it differently

    # Count the differences
    diff_count = 0
    for char1, char2 in zip(str1, str2):
        if char1 != char2:
            diff_count += 1

    return diff_count

# Iterate through the cols and check if 
# all chars from curr to start, and curr+1 to curr+1+curr <- distance to start
# Repeat with all the strings reversed
def find_vert_line(pattern: str, diff_allowed: int=0) -> list:
    row_len = len(pattern[0])
    valid_cols = []
    for curr in range(1, row_len):
        span = min(curr, row_len-curr)
        all_match = True
        diffs = 0
        for row in pattern:
            # print(f'curr @ {curr} -> {row[curr]}')
            for i, j in zip(range(span), range(span)):
                l = row[curr - i - 1]
                r = row[curr + j]
                if l != r:
                    diffs += 1
                    if diffs > diff_allowed:
                        all_match = False
                        break
        if all_match:
            valid_cols.append(curr)
    return valid_cols

def find_hor_line(pattern: str, diff_allowed: int=0) -> list:
    valid_rows = []
    for row_num in range(1, len(pattern)):
        # comp = pattern[row_num] == pattern[row_num-1]
        diffs = count_differences(pattern[row_num], pattern[row_num-1])
        dist = min(row_num, len(pattern)-row_num)
        # print(f'Distance is {dist}, {comp} @ row: {row_num}')
        
        # for i, row in enumerate(pattern):
        #     print(row, end=' <--\n' if i == row_num or i == row_num-1 else '\n')
        # print()
    
        # The current and prev rows match, possible mirroring
        if diffs <= diff_allowed:
            all_match = True
            
            for i in range(1, dist):
                diffs += count_differences(pattern[row_num-i-1], pattern[row_num+i])
                if diffs > diff_allowed:
                    all_match = False
                    break
            
            if all_match:
                valid_rows.append(row_num*100)
                # return row_num*100
    
    return valid_rows

lines = open('input.txt', 'r').readlines()

patterns = []
temp = []
for i, line in enumerate(lines):
    if line == '\n':
        patterns.append(temp)
        temp = []
    else:
        temp.append(line.strip())

if temp:
    patterns.append(temp)

rows = []
columns = []
for pattern in patterns:
    col = find_vert_line(pattern)
    row = find_hor_line(pattern)
    if col:
        columns.append(find_vert_line(pattern)[0])
    if row:
        rows.append(find_hor_line(pattern)[0])
    

print(f'Part1: The sum of rows and cols is {sum(columns) + sum(rows)}')

# Part2
# Need to determine which one value, when changed would allow for
# the opposite reflection of then previous, ie vert -> horiz

rows = []
columns = []
for pattern in patterns:
    col = find_vert_line(pattern)
    row = find_hor_line(pattern)
    col2 = find_vert_line(pattern, 1)
    row2 = find_hor_line(pattern, 1)
    
    if col:
        num = col[0]
        if len(col2) > 1:
            if num == col2[1]:
                columns.append(col2[0])
            else:
                columns.append(col2[1])
        else:
            rows.append(row2[0])
    else:
        num = row[0]
        if len(row2) > 1:
            if num == row2[1]:
                rows.append(row2[0])
            else:
                rows.append(row2[1])
        else:
            columns.append(col2[0])

print(f'Part2: The sum of rows and cols is {sum(columns) + sum(rows)}')