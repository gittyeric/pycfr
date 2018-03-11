from functools import lru_cache

from card import Card

def sort_cards(cards):
    if len(cards) == 1:
        return cards
    if len(cards) == 2:
        if (cards[0].rank * 4 + cards[0].suit) > (cards[1].rank * 4 + cards[1].suit):
            return cards
        return (cards[1], cards[0])

    assert(False) # No support yet for true sorting beyond 2 cards

def range_size(rules):
    hole_count = rules.roundinfo[0].holecard_count
    if hole_count == 1:
        return len(rules.deck)
    elif hole_count == 2:
        return (52*51)/2

    assert(False)

def cards_to_range_index(rules, cards):
    if len(cards) == 2:
        return cards_to_range_index_2(cards)
    elif len(cards) == 1:
        return cards_to_range_index_1(rules, cards)
    assert(False)

def range_index_to_cards(rules, index):
    hole_count = rules.roundinfo[0].holecard_count
    if hole_count == 2:
        return range_index_to_cards_2(index)
    elif hole_count == 1:
        return range_index_to_cards_1(rules, index)
    assert (False)

# Break down into 13 x 102 dual index (exclude Ace for left card)
# Then map to a single index up to 1325
@lru_cache(maxsize=int(52*51/2))
def cards_to_range_index_2(cards):
    index = 0
    max_card_index = 12 * 4 + 4
    sorted = sort_cards(cards)
    c_indicies = [(((card.rank - 2) * 4) + (card.suit - 1)) for card in sorted]

    count_so_far = 0
    for i in range(0, 52):
        for j in range(i+1, 52):
            if c_indicies[0] == i and c_indicies[1] == j:
                return count_so_far
            count_so_far += 1

    count_so_far = 0
    for j in range(0, 52):
        for i in range(j + 1, 52):
            if c_indicies[0] == i and c_indicies[1] == j:
                return count_so_far
            count_so_far += 1

    assert(False)

@lru_cache(maxsize=int(52))
def cards_to_range_index_1(rules, cards):
    card = cards[0]
    for i in range(0, len(rules.deck)):
        if rules.deck[i] == card:
            return i
    assert(False)

@lru_cache(maxsize=int(52*51/2))
def range_index_to_cards_2(index):
    count_so_far = 0
    for i in range(0, 52):
        for j in range(i + 1, 52):
            if count_so_far == index:
                i_suit = i % 4 + 1
                j_suit = j % 4 + 1
                i_rank = int((i >> 2)) + 2
                j_rank = int((j >> 2)) + 2
                return ( Card( i_rank, i_suit), Card( j_rank, j_suit ) )
            count_so_far += 1

    count_so_far = 0
    for j in range(0, 52):
        for i in range(j + 1, 52):
            if count_so_far == index:
                i_suit = i % 4 + 1
                j_suit = j % 4 + 1
                i_rank = int((i >> 2)) + 2
                j_rank = int((j >> 2)) + 2
                return (Card(i_rank, i_suit), Card(j_rank, j_suit))
            count_so_far += 1

    assert (False)

@lru_cache(maxsize=int(52 * 51 / 2))
def range_index_to_cards_2(index):
    count_so_far = 0
    for i in range(0, 52):
        for j in range(i + 1, 52):
            if count_so_far == index:
                i_suit = i % 4 + 1
                j_suit = j % 4 + 1
                i_rank = int((i >> 2)) + 2
                j_rank = int((j >> 2)) + 2
                return (Card(i_rank, i_suit), Card(j_rank, j_suit))
            count_so_far += 1

    count_so_far = 0
    for j in range(0, 52):
        for i in range(j + 1, 52):
            if count_so_far == index:
                i_suit = i % 4 + 1
                j_suit = j % 4 + 1
                i_rank = int((i >> 2)) + 2
                j_rank = int((j >> 2)) + 2
                return (Card(i_rank, i_suit), Card(j_rank, j_suit))
            count_so_far += 1

@lru_cache(maxsize=52)
def range_index_to_cards_1(rules, index):
    return (rules.deck[index],)

# @lru_cache(maxsize=52*52)
# def build_player_ranges(rules, known_cards):
#     card_count = len(rules.deck)
#     hole_count = rules.roundinfo[0].holecard_count
#     combo_count = math.pow(card_count, hole_count) / hole_count
#     hand_prob = 1.0 / (combo_count - (len(known_cards) * (card_count-1) * hole_count ) )
#     ranges = np.ones((rules.players, combo_count), np.longdouble) * hand_prob
#
#     possible_mask = np.ones((rules.players, combo_count), np.longdouble)
#
#     return ranges * possible_mask