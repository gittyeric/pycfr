from hand_ranges import *
from pokergames import holdem_rules

rules = holdem_rules(2)
indicies = []
seen = {}
for i, suit1 in Card.SUIT_TO_STRING.items():
    for j, rank1 in Card.RANK_TO_STRING.items():
        for i2, suit2 in Card.SUIT_TO_STRING.items():
            for j2, rank2 in Card.RANK_TO_STRING.items():
                c1 = sort_cards((Card(j, i), Card(j2, i2)))
                hand_key = str(c1[0]) + str(c1[1])
                if hand_key not in seen:
                    seen[hand_key] = True
                    if rank1 != rank2 or suit1 != suit2:
                        cards = cards_to_range_index(rules, c1)
                        indicies.append(cards)

indicies.sort()
for i in range(0, 1326):
    assert(indicies[i] == i)
    as_cards = range_index_to_cards(rules, indicies[i])
    assert( cards_to_range_index( rules, as_cards ) == i )

print("2 hand ranges works")