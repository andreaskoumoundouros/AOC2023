import regex as re

fmatch = r'[0-9]{1}?'
conv_match = r'(one|two|three|four|five|six|seven|eight|nine|1|2|3|4|5|6|7|8|9)'

conversions = {
    "one" : '1',
    "two" : '2',
    "three" : '3',
    "four" : '4',
    "five" : '5',
    "six" : '6',
    "seven" : '7',
    "eight" : '8',
    "nine" : '9',
    "1" : '1',
    "2" : '2',
    "3" : '3',
    "4" : '4',
    "5" : '5',
    "6" : '6',
    "7" : '7',
    "8" : '8',
    "9" : '9',
}

def get_nums(line: str):
    matches = re.findall(conv_match, line, overlapped=True)
    nums = []
    for match in matches:
        nums.append(conversions[match])
    return nums

vals = []
with open('input.txt', 'r') as f:
    first = 0
    second = 0
    for line in f.readlines():
        nums = get_nums(line.strip())
        if nums:
            first = nums[0]
            second = first
            second = nums[-1]
            vals.append((first,second))

sum = 0
for first, second in vals:
    comb = f'{first}{second}'
    print(comb)
    sum = sum + int(comb)
    
print(f'the resulting sum is {sum}')