__author__ = 'fyt'

import random

import ClientBase
from deuces import Card
from deuces import Evaluator


# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 6000
BUFFER_SIZE = 1024

# Agent
POKER_CLIENT_NAME = 'ALPINE_TEAM'
POKER_HAND = []
POKER_CHANCETOWIN = 0
POKER_EVALUATION = Evaluator()
POKER_BLIND = 10
POKER_HAND_TYPE = 'High Card'

class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0

'''
* Gets the name of the player.
* @return  The name of the player as a single word without space. <code>null</code> is not a valid answer.
'''
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

'''
* Modify queryOpenAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what open
* action to choose.
* @param minimumPotAfterOpen   the total minimum amount of chips to put into the pot if the answer action is
*                              {@link BettingAnswer#ACTION_OPEN}.
* @param playersCurrentBet     the amount of chips the player has already put into the pot (dure to the forced bet).
* @param playersRemainingChips the number of chips the player has not yet put into the pot.
* @return                      An answer to the open query. The answer action must be one of
*                              {@link BettingAnswer#ACTION_OPEN}, {@link BettingAnswer#ACTION_ALLIN} or
*                              {@link BettingAnswer#ACTION_CHECK }. If the action is open, the answers
*                              amount of chips in the anser must be between <code>minimumPotAfterOpen</code>
*                              and the players total amount of chips (the amount of chips alrady put into
*                              pot plus the remaining amount of chips).
'''
def queryOpenAction(_hand, _minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):

    evaluateHand(_hand)

    print("--- OPEN ACTION ---")
   

    win_chance = POKER_CHANCETOWIN

    if(win_chance < 20):
        resp = ClientBase.BettingAnswer.ACTION_OPEN,  int(random.randint(0, round(0.02*_playersRemainingChips)+1) + _minimumPotAfterOpen)
    elif(win_chance < 35):
        resp = ClientBase.BettingAnswer.ACTION_OPEN,  int(random.randint(0, round(0.1*_playersRemainingChips)+1) + _minimumPotAfterOpen)
    elif(win_chance < 65):
        resp = ClientBase.BettingAnswer.ACTION_OPEN,  int(random.randint(round(0.1*_playersRemainingChips), round(0.15*_playersRemainingChips)+1) + _minimumPotAfterOpen)
    else:
        if(_playersRemainingChips < 50):
            resp = ClientBase.BettingAnswer.ACTION_ALLIN
        else:
            resp = ClientBase.BettingAnswer.ACTION_OPEN,  int(random.randint(round(0.15*_playersRemainingChips), round(0.2*_playersRemainingChips)+1) + _minimumPotAfterOpen)

    print 'ALPINE_TEAM:', resp
    return resp

'''
* Modify queryCallRaiseAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what call/raise
* action to choose.
* @param maximumBet                the maximum number of chips one player has already put into the pot.
* @param minimumAmountToRaiseTo    the minimum amount of chips to bet if the returned answer is {@link BettingAnswer#ACTION_RAISE}.
* @param playersCurrentBet         the number of chips the player has already put into the pot.
* @param playersRemainingChips     the number of chips the player has not yet put into the pot.
* @return                          An answer to the call or raise query. The answer action must be one of
*                                  {@link BettingAnswer#ACTION_FOLD}, {@link BettingAnswer#ACTION_CALL},
*                                  {@link BettingAnswer#ACTION_RAISE} or {@link BettingAnswer#ACTION_ALLIN }.
*                                  If the players number of remaining chips is less than the maximum bet and
*                                  the players current bet, the call action is not available. If the players
*                                  number of remaining chips plus the players current bet is less than the minimum
*                                  amount of chips to raise to, the raise action is not available. If the action
*                                  is raise, the answers amount of chips is the total amount of chips the player
*                                  puts into the pot and must be between <code>minimumAmountToRaiseTo</code> and
*                                  <code>playersCurrentBet+playersRemainingChips</code>.
'''
def queryCallRaiseAction(_hand, _maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):

    evaluateHand(_hand)

    print("--- CALL/RAISE ACTION ---")
    #Card.print_pretty_cards(POKER_HAND)

    #print 'chips:',_playersRemainingChips
    #print 'maxbet:',_maximumBet
    #print 'toraise: min=',_minimumAmountToRaiseTo,'max=',_playersCurrentBet+_playersRemainingChips
    #print 'currentbet:',_playersCurrentBet

    win_chance = POKER_CHANCETOWIN

    # < 5% winrate (weak high card)
    if win_chance < 5:
        resp = ClientBase.BettingAnswer.ACTION_FOLD

    # 5% < winrate < 20% (high card, weak pairs)
    elif win_chance < 20:
        # opponent raised by more than 25 chips
        if(_maximumBet > 25):
            resp = ClientBase.BettingAnswer.ACTION_FOLD
        # check or only small raise
        else:
            resp = ClientBase.BettingAnswer.ACTION_CALL

    # 20% < winrate < 45% (pairs++)
    elif(win_chance < 45):
        # raise target < 15% of stack
        if _maximumBet < 0.15*_playersRemainingChips:
            # raise to minimum + 5% of stack
            resp = ClientBase.BettingAnswer.ACTION_RAISE, int(_minimumAmountToRaiseTo+0.05*_playersRemainingChips)
        
        elif _maximumBet < 0.2*_playersRemainingChips:
            resp = ClientBase.BettingAnswer.ACTION_CALL
        else:
            resp = ClientBase.BettingAnswer.ACTION_FOLD

    # 45% < winrate < 60%
    elif(win_chance < 60):
        # maxbet < 15% of stack
        if _maximumBet < 0.2*_playersRemainingChips:
            # raise to minimum + 10% of stack
            resp = ClientBase.BettingAnswer.ACTION_RAISE, int(_minimumAmountToRaiseTo+0.1*_playersRemainingChips)
        
        elif _maximumBet < 0.5*_playersRemainingChips:
            resp = ClientBase.BettingAnswer.ACTION_CALL
        else:
            resp = ClientBase.BettingAnswer.ACTION_ALLIN

    # 60% < winrate < 80%
    elif(win_chance < 80):
        if(_maximumBet < 0.6*_playersRemainingChips):
            resp = ClientBase.BettingAnswer.ACTION_RAISE, int(_minimumAmountToRaiseTo+0.1*_playersRemainingChips)
        elif(_playersRemainingChips > _minimumAmountToRaiseTo):
            resp = ClientBase.BettingAnswer.ACTION_CALL
        else:
            resp = ClientBase.BettingAnswer.ACTION_ALLIN

    # winrate > 80%
    else:
        if(_playersRemainingChips > _minimumAmountToRaiseTo+0.2*_playersRemainingChips):
            resp = ClientBase.BettingAnswer.ACTION_RAISE, int(_minimumAmountToRaiseTo+0.2*_playersRemainingChips)
        else:
            resp = ClientBase.BettingAnswer.ACTION_ALLIN

    print 'ALPINE_TEAM:', resp
    return resp

'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):
    print("--- THROW CARDS ---")

    # make hand
    global POKER_HAND
    POKER_HAND = []
    for h in _hand:
        POKER_HAND.append(Card.new(h))
    Card.print_pretty_cards(POKER_HAND)
    # eval hand
    sc = POKER_EVALUATION.evaluate([],POKER_HAND)
    rank = POKER_EVALUATION.get_rank_class(sc)

    def find_pair(cards):
        for i in range(0,4):
            for j in range (i+1,5):
                if (cards[i]&0xF00) == (cards[j]&0xF00):
                    return [i,j]
        return []

    def find_double_pair(cards):
        [k,l] = find_pair(cards)
        for i in range(k+1,4):
            for j in range (i+1,5):
                if (cards[i]&0xF00) == (cards[j]&0xF00):
                    return [k,l,i,j]
        return []

    def find_four_of_kind(cards):
        [k,l] = find_pair(cards)
        if k != 0:
            return 1
        else:
            for i in range(1,5):
                if (cards[i]&0xF00) != (cards[0] & 0xF00):
                    return i

    def find_tripple(cards):
        [k,l] = find_pair(cards)
        for i in range(l+1,5):
            if (cards[i]&0xF00) == (cards[l] & 0xF00):
                return [k,l,i]
        return []

    def find_high_card(cards):
        max = 0
        k = 0
        for i in ra:
            current = ((cards[i] & 0xF00)>>8)
            if current > max:
                max = current
                k = i
        return k

    card_to_throw = []
    ra = range(0,5)

    if rank == 2:   #   4 of a kind
        card_to_throw = [Card.int_to_str(POKER_HAND[find_four_of_kind(POKER_HAND)])]
    elif rank == 6: #   three of a kind
        hold = set(find_tripple(POKER_HAND))
        throw = filter(lambda x: x not in hold, ra)
        card_to_throw = [Card.int_to_str(POKER_HAND[throw[0]]),  Card.int_to_str(POKER_HAND[throw[1]])]
    elif rank == 7: #   two pair
        hold = set(find_double_pair(POKER_HAND))
        throw = filter(lambda x: x not in hold, ra)
        card_to_throw = [Card.int_to_str(POKER_HAND[throw[0]])]
    elif rank == 8: #   pair
        hold = set(find_pair(POKER_HAND))
        throw = filter(lambda x: x not in hold, ra)
        card_to_throw = [Card.int_to_str(POKER_HAND[throw[0]]),  Card.int_to_str(POKER_HAND[throw[1]]),  Card.int_to_str(POKER_HAND[throw[2]])]
    elif rank == 9: #   high card
        hold = [find_high_card(POKER_HAND)]
        throw = filter(lambda x: x not in hold, ra)
        card_to_throw = [Card.int_to_str(POKER_HAND[throw[0]]),  Card.int_to_str(POKER_HAND[throw[1]]),  Card.int_to_str(POKER_HAND[throw[2]]),  Card.int_to_str(POKER_HAND[throw[3]])]
    # find worst card

    # make string to return from array
    thrower = ''
    for i in range(0,len(card_to_throw)):
        thrower += card_to_throw[i] + ' '

    return thrower


def evaluateHand(_hand):
    global POKER_HAND
    global POKER_CHANCETOWIN
    global POKER_HAND_TYPE

    print '--- EVALUATION ---'

    # convert poker hand format
    POKER_HAND = []
    for h in _hand:
        POKER_HAND.append(Card.new(h))
    Card.print_pretty_cards(POKER_HAND)

    # calculate hand score
    sc = POKER_EVALUATION.evaluate([],POKER_HAND)
    #sc = POKER_EVALUATION._five(POKER_HAND)

    # determine rank class
    POKER_HAND_TYPE = POKER_EVALUATION.class_to_string(POKER_EVALUATION.get_rank_class(sc))
    print "Rank/Class = " + POKER_HAND_TYPE

    # estimate win chance
    POKER_CHANCETOWIN = round((float(1) - Evaluator.get_five_card_rank_percentage(POKER_EVALUATION,sc)) * 100, 1)
    print "Chance to win =", POKER_CHANCETOWIN, "%"