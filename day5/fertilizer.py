import re
import time
from dataclasses import dataclass

SEED_RE = r'seeds:\s+([\d ]+)'
MAP_RE = r'([a-z]+-to-[a-z]+)[\s]{1}map:[\n]([\d \n]*)\n\n'

@dataclass
class Interval:
    dest_intervals: list
    lengths: list
    length_sums: list
    src_interval_starts: list
    src_interval_start: int = -1
    length: int = 0
    
    def update(self, new):
        if self.src_interval_start == -1:
            self.src_interval_start = new[1]
        self.src_interval_starts.append(new[1])
        self.dest_intervals.append(new[0])
        self.length += new[2]
        self.lengths.append(new[2])
        self.length_sums.append(self.length)

def optimize_map(map: list) -> list:
    new_map = []
    temp = Interval([], [], [], [])
    for int1, int2 in zip(map[:-1], map[1:]):
        # Check if adjacent, if so combine
        temp.update(int1)
        if int1[1] + int1[2] != int2[1]:
            new_map.append(temp)
            temp = Interval([], [], [], [])
    
    # Handle last item
    temp.update(map[-1])
    new_map.append(temp)
    
    return new_map

def part1(seeds, maps) -> int:
    lowest = None
    for seed in seeds:
        for map in maps:
            
            for interval in map:
                if interval.src_interval_start <= seed < interval.src_interval_start + interval.length:
                    # Seed has mapping in THIS interval
                    for i in range(len(interval.lengths)):
                        # Determine which of original intervals this seed maps to
                        if seed < interval.src_interval_start + interval.length_sums[i]:
                            # Perform conversion
                            seed += (interval.dest_intervals[i] - interval.src_interval_starts[i])
                            break
                else:
                    break
        if lowest is None or seed < lowest:
            lowest = seed
    return lowest

def part2(seeds, maps) -> int:
    lowest = None
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        length = seeds[i+1]
        for seed in range(start, start+length):
            for map in maps:
                
                for interval in map:
                    if interval.src_interval_start <= seed:
                        if seed < interval.src_interval_start + interval.length:
                            # Seed has mapping in THIS interval
                            for i in range(len(interval.lengths)):
                                # Determine which of original intervals this seed maps to
                                if seed < interval.src_interval_start + interval.length_sums[i]:
                                    # Perform mapping
                                    seed += (interval.dest_intervals[i] - interval.src_interval_starts[i])
                                    break
                    else:
                        # Seed is lower than lowest
                        break
            if lowest is None or seed < lowest:
                lowest = seed
    return lowest

def main():
    # Common Parsing
    lines = open('input.txt', 'r').readlines()

    # Get list of seeds
    seed_match = re.search(SEED_RE, lines[0])
    seeds = [int(x) for x in seed_match.group(1).strip().split(' ')]

    # Get list of maps
    map_matches = [x for x in re.finditer(MAP_RE, ''.join(lines[1:]))]
    maps = []
    for match in map_matches:
        title = match.group(1)
        mappings = [[int(y) for y in x.split()] for x in match.group(2).split('\n')]
        mappings.sort(key=lambda item : item[1])

        maps.append(mappings)
    
    # Part 2 optimization (can be used for both)
    # Combine intervals of mappings that are adjacent
    reduced_maps = []
    for map in maps:
        reduced_maps.append(optimize_map(map))
        # print(f'{optimize_map(map)}')
    
    # Part 1
    start = time.time_ns()
    lowest = part1(seeds, reduced_maps)
    end = time.time_ns()
    print(f'Part 1 result is: {lowest}, calculation took {(end-start)/1000000}ms')
    # Part 2
    start = time.time_ns()
    lowest = part2(seeds, reduced_maps)
    end = time.time_ns()
    print(f'Part 2 result is: {lowest}, calculation took {(end-start)/1000000}ms')

if __name__ == '__main__':
    main()