lines = open('input.txt', 'r').readlines()
times = [int(x) for x in lines[0].split() if x.isdigit()]
distances = [int(x) for x in lines[1].split() if x.isdigit()]

print(times)
print(distances)

winning_hold_list = []
for time, distance in zip(times, distances):
    num_winning_holds = 0
    for hold_time in range(1, time):
        if distance < hold_time*(time-hold_time):
            num_winning_holds+=1
    winning_hold_list.append(num_winning_holds)

p1_result = 1
for i in winning_hold_list:
    p1_result = p1_result*i

print(f'Result for part 1: {p1_result}')

# Part 2

time = int(''.join([str(x) for x in times]))
distance = int(''.join([str(x) for x in distances]))

print(time)
print(distance)
num_winning_holds = 0
for hold_time in range(1, time):
    if distance < hold_time*(time-hold_time):
        num_winning_holds+=1

print(f'Result for part 2: {num_winning_holds}')