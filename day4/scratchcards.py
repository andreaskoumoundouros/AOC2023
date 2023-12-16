import re
from queue import Queue

LINE_RE = r'Card\s*([\d]+):([\d ]*)[\|]([\d ]*)'

class ScratchCard:
    
    def __init__(self, number, winning_nums, own_nums):
        self.number = number
        self.winning_nums = winning_nums
        self.own_nums = own_nums
    
    def __str__(self):
        return f'Card {self.number}: {self.winning_nums} | {self.own_nums}'
    
    def get_next_cards(self) -> list:
        global game
        winners = 0
        for own_num in self.own_nums:
            if own_num in self.winning_nums:
                winners += 1
        return [x for x in range(self.number + 1, min(winners + self.number + 1, game.num_cards+1))]

class Game:
    def __init__(self, num_cards):
        self.num_cards = num_cards
        self.cards = {}
        
        for i in range(num_cards):
            self.cards[i+1] = None

lines = []
with open('input.txt', 'r') as f:
    lines = [x.strip() for x in f.readlines()]

game = Game(len(lines))
points = 0
for line in lines:
    match = re.match(LINE_RE, line, flags=re.IGNORECASE)
    
    if match:
        number = int(match.group(1))
        winning_nums = {int(num) for num in match.group(2).strip().replace('  ', ' ').split(' ')}
        own_nums = [int(num) for num in match.group(3).strip().replace('  ', ' ').split(' ')]
        
        if number in game.cards:
            game.cards[number] = ScratchCard(
                number,
                winning_nums,
                own_nums
            )
        else:
            print(f'What in tarnation {number}')
            exit(1)
        
        winners = 0
        for own_num in own_nums:
            if own_num in winning_nums:
                winners += 1
        
        if winners > 0:
            points += 2**(winners-1)

print(f'Total points {points}')

queue = Queue()
[queue.put(card) for key, card in game.cards.items()]
copied_cards = 0
while not queue.empty():
    card = queue.get()
    # print(card)
    next_cards = card.get_next_cards()
    # print(next_cards)
    for card_num in next_cards:
        copied_cards += 1
        queue.put(game.cards[card_num])

print(f'There are {copied_cards} copied cards')
print(f'there are {copied_cards+game.num_cards} total cards')