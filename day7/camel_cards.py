import math

VALUES = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}
VALUES_J = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 0,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}

N = len(VALUES)
R = 5


def hand_score(hand: str, joker=False):
    value = {}
    for card in hand:
        value[card] = value.get(card, 0) + 1

    if joker:
        print(f"Converting jokers in {hand} to ", end="")
        if "J" in value and len(value) > 1:
            value.pop("J")
        hand = hand.replace("J", max(value, key=value.get))
        print(hand)

        value = {}
        for card in hand:
            value[card] = value.get(card, 0) + 1

    hand_type = len(value)
    max_reps = max(value.values())

    # Five of a kind
    if hand_type == 1:
        return 6
    # Four of a kind, Full house
    if hand_type == 2:
        if max_reps == 4:
            return 5
        else:
            return 4
    # Three of a kind, Two pair
    if hand_type == 3:
        if max_reps == 3:
            return 3
        else:
            return 2
    # One pair
    if hand_type == 4:
        return 1
    # High card
    if hand_type == 5:
        return 0


def compare_hands(h1: list, h2: list):
    if hand_score(h1[1]) < hand_score(h2[1]):
        return -1
    elif hand_score(h1[1]) > hand_score(h2[1]):
        return 1
    else:
        # They are the same type, go through individual letters
        for c1, c2 in zip(h1[1], h2[1]):
            if VALUES[c1] < VALUES[c2]:
                return -1
            elif VALUES[c1] > VALUES[c2]:
                return 1
        return 0


def compare_hands_joker(h1: list, h2: list):
    if hand_score(h1[1], True) < hand_score(h2[1], True):
        return -1
    elif hand_score(h1[1], True) > hand_score(h2[1], True):
        return 1
    else:
        # They are the same type, go through individual letters
        for c1, c2 in zip(h1[1], h2[1]):
            if VALUES_J[c1] < VALUES_J[c2]:
                return -1
            elif VALUES_J[c1] > VALUES_J[c2]:
                return 1
        return 0


lines = open("input.txt", "r").readlines()
ranks = []

for line in lines:
    line = line.split()
    hand = line[0]
    bid = int(line[1])

    value = {}
    for card in hand:
        value[card] = value.get(card, 0) + 1

    ranks.append([bid, hand])

from functools import cmp_to_key

ranks = sorted(ranks, key=cmp_to_key(compare_hands))

from pprint import pprint

pprint(ranks)
total_winnings = 0
for i, (bid, hand) in enumerate(ranks):
    total_winnings += (i + 1) * bid

print(f"The total winnings are {total_winnings}")

ranks = sorted(ranks, key=cmp_to_key(compare_hands_joker))

from pprint import pprint

pprint(ranks)
total_winnings = 0
for i, (bid, hand) in enumerate(ranks):
    total_winnings += (i + 1) * bid

print(f"FOR PART 2 The total winnings are {total_winnings}")
