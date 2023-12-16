
import re
from collections import defaultdict

SEED_RE = r'seeds:\s+([\d ]+)'
MAP_RE = r'([a-z]+-to-[a-z]+)[\s]{1}map:[\n]([\d \n]*)\n\n'

class SeedMapping:
    def __init__(self, ranges: list):
        self.range_len = int(ranges[2])
        self.dest_range_start = int(ranges[0])
        self.dest_range_end = self.dest_range_start + self.range_len - 1
        self.src_range_start = int(ranges[1])
        self.src_range_end = self.src_range_start + self.range_len - 1
        self.conv_const = self.dest_range_start - self.src_range_start

    def get_mapping(self, input: int) -> int:
        if self.src_range_start <= input <= self.src_range_end:
            return input + self.conv_const
        else:
            return input

def process_seeds(seeds, mappings):
    results = set()
    for seed in seeds:
        current = seed
        seen = set()
        while current not in seen:
            seen.add(current)
            for map_list in mappings.values():
                for map in map_list:
                    new_current = map.get_mapping(current)
                    if new_current != current:
                        current = new_current
                        break
            else:
                results.add(current)
                break
    return min(results)

def main():
    with open('test.txt', 'r') as file:
        lines = file.readlines()

    seed_match = re.search(SEED_RE, lines[0])
    seeds = [int(x) for x in seed_match.group(1).strip().split(' ')]

    map_matches = [x for x in re.finditer(MAP_RE, ''.join(lines[1:]))]
    maps = {match.group(1): [SeedMapping(x.strip().split(' ')) for x in match.group(2).split('\n')] for match in map_matches}

    lowest = process_seeds(seeds, maps)
    print(f'The lowest mapping was {lowest}')

if __name__ == '__main__':
    main()
