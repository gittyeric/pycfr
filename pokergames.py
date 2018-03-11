from pokertrees import *
from card import *

def holdem_eval(hc, board):
    assert(False) # Not supported yet
    return hc[0].rank

def holdem_rules(players):
    deck = []
    for rank in range(2, 15):
        for suit in range(1, 5):
            deck.append(Card(rank, suit))
    ante = 0
    blinds = [1, 2]
    rounds = [RoundInfo(holecard_count=2, boardcard_count=0, betsize=1, maxbets=[1, 0]),
              RoundInfo(holecard_count=0, boardcard_count=3, betsize=1, maxbets=[1, 0]),
              RoundInfo(holecard_count=0, boardcard_count=1, betsize=1, maxbets=[1, 0]),
              RoundInfo(holecard_count=0, boardcard_count=1, betsize=1, maxbets=[1, 0])]
    return GameRules(players, deck, rounds, ante, blinds, handeval=holdem_eval, infoset_format=holdem_format)

def holdem_format(player, holecards, board, bet_history):
    cards = ""
    for card in (holecards + board):
        cards += Card.RANK_TO_STRING[card.rank] + Card.SUIT_TO_STRING[card.suit]
    return "{0}:{1}:".format(cards, bet_history)

def kuhn_eval(hc, board):
    return hc[0].rank

def half_street_kuhn_rules():
    players = 2
    deck = [Card(14,1),Card(13,1),Card(12,1)]
    ante = 1
    blinds = None
    rounds = [RoundInfo(holecard_count=1, boardcard_count=0, betsize=1, maxbets=[1, 0])]
    return GameRules(players, deck, rounds, ante, blinds, handeval=kuhn_eval, infoset_format=leduc_format)

def half_street_kuhn_gametree():
    rules = half_street_kuhn_rules()
    tree = GameTree(rules)
    tree.build()
    return tree

def half_street_kuhn_publictree():
    rules = half_street_kuhn_rules()
    tree = PublicTree(rules)
    tree.build()
    return tree

def kuhn_rules():
    players = 2
    deck = [Card(14,1),Card(13,1),Card(12,1)]
    ante = 1
    blinds = None
    rounds = [RoundInfo(holecard_count=1, boardcard_count=0, betsize=1, maxbets=[1, 1])]
    return GameRules(players, deck, rounds, ante, blinds, handeval=kuhn_eval, infoset_format=leduc_format) 

def kuhn_gametree():
    rules = kuhn_rules()
    tree = GameTree(rules)
    tree.build()
    return tree

def kuhn_publictree():
    rules = kuhn_rules()
    tree = PublicTree(rules)
    tree.build()
    return tree

def leduc_format(player, holecards, board, bet_history):
    cards = holecards[0].RANK_TO_STRING[holecards[0].rank]
    if len(board) > 0:
        cards += board[0].RANK_TO_STRING[board[0].rank]
    return "{0}:{1}:".format(cards, bet_history)

def leduc_eval(hc,board):
    hand = hc + board
    if hand[0].rank == hand[1].rank:
        return 15*14+hand[0].rank
    return max(hand[0].rank, hand[1].rank) * 14 + min(hand[0].rank, hand[1].rank)

def leduc_rules():
    players = 2
    deck = [Card(13,1),Card(13,2),Card(12,1),Card(12,2),Card(11,1),Card(11,2)]
    ante = 1
    blinds = None
    rounds = [RoundInfo(holecard_count=1, boardcard_count=0, betsize=2, maxbets=[2, 2]), RoundInfo(holecard_count=0, boardcard_count=1, betsize=4, maxbets=[2, 2])]
    return GameRules(players, deck, rounds, ante, blinds, handeval=leduc_eval, infoset_format=leduc_format)

def leduc_gametree():
    rules = leduc_rules()
    tree = GameTree(rules)
    tree.build()
    return tree

def leduc_publictree():
    rules = leduc_rules()
    tree = PublicTree(rules)
    tree.build()
    return tree

def royal_format(player, holecards, board, bet_history):
    cards = holecards[0].RANK_TO_STRING[holecards[0].rank]
    for i in range(len(board)):
        cards += board[i].RANK_TO_STRING[board[i].rank]
        if board[i].suit == holecards[0].suit:
            cards += 's'
        else:
            cards += 'o'
    return "{0}:{1}:".format(cards, bet_history)

def royal_eval(hc,board):
    hand = hc + board
    # Flush
    if hand[0].suit == hand[1].suit and hand[0].suit == hand[2].suit:
        return 10000 + hc[0].rank
    # Straight
    ranks = [h.rank for h in hand]
    if Card.RANK_QUEEN in ranks and Card.RANK_KING in ranks:
        if Card.RANK_ACE in ranks:
            return 1000 + Card.RANK_ACE
        if Card.RANK_JACK in ranks:
            return 1000 + Card.RANK_JACK
    # Holecard used in a pair
    if hand[0].rank == hand[1].rank or hand[0].rank == hand[2].rank:
        return 100+hand[0].rank
    return hand[0].rank

def royal_rules():
    players = 2
    deck = [Card(14,1),Card(14,2),Card(13,1),Card(13,2),Card(12,1),Card(12,2),Card(11,1),Card(11,2)]
    ante = 1
    blinds = None
    preflop = RoundInfo(holecard_count=1, boardcard_count=0, betsize=2, maxbets=[2, 2])
    flop = RoundInfo(holecard_count=0, boardcard_count=1, betsize=4, maxbets=[2, 2])
    turn = RoundInfo(holecard_count=0, boardcard_count=1, betsize=4, maxbets=[2, 2])
    rounds = [preflop,flop,turn]
    return GameRules(players, deck, rounds, ante, blinds, handeval=royal_eval, infoset_format=royal_format)

def royal_gametree():
    rules = royal_rules()
    tree = GameTree(rules)
    tree.build()
    return tree

def royal_publictree():
    rules = royal_rules()
    tree = PublicTree(rules)
    tree.build()
    return tree   