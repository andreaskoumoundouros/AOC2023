lines = open('input.txt', 'r').readlines()
lines = [[int(val) for val in line.strip().split()] for line in lines]

end_sum = 0
total_start_sum = 0
for line in lines:
    max_seq = len(line)-1
    curr_line = line
    
    start_sum = 0
    start_vals = []
    for _ in range(max_seq):
        temp = []
        start_vals.append(curr_line[0])
        for index, value in enumerate(curr_line[:-1]):
            temp.append(curr_line[index+1]-value)
        
        end_sum += curr_line[-1]
        curr_line = temp
        if not any(curr_line):
            break
    start_vals.append(0)
    
    for start_val in reversed(start_vals):
        start_sum = start_val-start_sum
    total_start_sum += start_sum

print(f'Part 1: The sum of extrapolated end values is: {end_sum}')
print(f'Part 2: The sum of extrapolated start values is: {total_start_sum}')