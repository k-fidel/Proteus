# Project
# Group: GermanWings
# Group members: K. Griesebner & R. Strasser
# Date: 12/01/2017

import random
from deuces import Card
from deuces import Evaluator
import ClientBase

# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 6000
BUFFER_SIZE = 1024

# Agent
POKER_CLIENT_NAME = 'GermanWings'
POKER_BLIND = 10
POKER_HAND_TYPE = 'High Card'
DEUCES_EVALUATOR = Evaluator()

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
    poker_hand = []

    ########### EVALUATE HAND ###########
    print '=== EVALUATION ==='

    for n in _hand:
        poker_hand.append(Card.new(n))

    Card.print_pretty_cards(poker_hand)

    score = DEUCES_EVALUATOR.evaluate([], poker_hand)
    rank = DEUCES_EVALUATOR.class_to_string(DEUCES_EVALUATOR.get_rank_class(score))
    print "Rank = " + rank
    ########### / EVALUATE HAND ###########

    ########### ESTIMATE WIN CHANCE ###########
    chance = round((float(1) - Evaluator.get_five_card_rank_percentage(DEUCES_EVALUATOR, score)), 2)
    print "Chance to win =", chance*100, "%"
    ########### / ESTIMATE WIN CHANCE ###########

    ########### ACTION DEPENDS ON WIN CHANCE ###########

    print("======= OPENING ACTION =======")

    # chance to win < 22%: Bet 1 coin up to 2% of stack size
    if (chance < 0.22):
        action = ClientBase.BettingAnswer.ACTION_OPEN, \
                 int(random.randint(0, round(0.05 * _playersRemainingChips) + 1) + _minimumPotAfterOpen)
    # chance to win < 33%: Bet 1 coin up to 10% of stack size
    elif (chance < 0.33):
        action = ClientBase.BettingAnswer.ACTION_OPEN, \
                 int(random.randint(0, round(0.1 * _playersRemainingChips) + 1) + _minimumPotAfterOpen)
    # chance to win < 66%: Bet 15% of stack size up to 20% of stack size
    elif (chance < 0.66):
        action = ClientBase.BettingAnswer.ACTION_OPEN, \
                 int(random.randint(round(0.15 * _playersRemainingChips),
                                    round(0.2 * _playersRemainingChips) + 1) + _minimumPotAfterOpen)
    # If chance is higher - check remaining chip stack:
    else:
        # Chip stack < 40: Go all in
        if (_playersRemainingChips < 0.4):
            action = ClientBase.BettingAnswer.ACTION_ALLIN
        # Otherwise: Bet 25% of stack size up to 30% of stack size
        else:
            action = ClientBase.BettingAnswer.ACTION_OPEN, \
                     int(random.randint(round(0.25 * _playersRemainingChips),
                                        round(0.3 * _playersRemainingChips) + 1) + _minimumPotAfterOpen)
    print 'GermanWings:', action
    return action

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
    poker_hand = []

    ########### EVALUATE HAND ###########
    print '=== EVALUATION ==='

    for n in _hand:
        poker_hand.append(Card.new(n))

    Card.print_pretty_cards(poker_hand)

    score = DEUCES_EVALUATOR.evaluate([], poker_hand)
    rank = DEUCES_EVALUATOR.class_to_string(DEUCES_EVALUATOR.get_rank_class(score))
    print "Rank = " + rank
    ########### / EVALUATE HAND ###########

    ########### ESTIMATE WIN CHANCE ###########
    chance = round((float(1) - Evaluator.get_five_card_rank_percentage(DEUCES_EVALUATOR, score)), 2)
    print "Chance to win =", chance*100, "%"
    ########### / ESTIMATE WIN CHANCE ###########

    ########### ACTION DEPENDS ON WIN CHANCE ###########

    print("======= CALL/RAISE ACTION =======")

    # chance to win < 10%: Fold
    if chance < 0.1:
        action = ClientBase.BettingAnswer.ACTION_FOLD

    # chance to win: 10% <= w < 20%
    elif chance < 0.2:
        # Opponent raise > 20 coins: Fold
        if (_maximumBet > 20):
            action = ClientBase.BettingAnswer.ACTION_FOLD
        # Otherwise: Call
        else:
            action = ClientBase.BettingAnswer.ACTION_CALL

    # chance to win: 20% <= w < 40%
    elif (chance < 0.40):
        # bet < 10% of player stack size: Raise up to 2% of stack size
        if _maximumBet < 0.10 * _playersRemainingChips:
            action = ClientBase.BettingAnswer.ACTION_RAISE, int(_minimumAmountToRaiseTo + 0.02 * _playersRemainingChips)
        # bet < 15% of player stack size: Call
        elif _maximumBet < 0.15 * _playersRemainingChips:
            action = ClientBase.BettingAnswer.ACTION_CALL
        # for higher bets: Fold
        else:
            action = ClientBase.BettingAnswer.ACTION_FOLD

    # chance to win: 40% <= w < 60%
    elif (chance < 0.6):
        # bet < 20% of player stack size: Raise up to 5% of stack size
        if _maximumBet < 0.2 * _playersRemainingChips:
            action = ClientBase.BettingAnswer.ACTION_RAISE, int(_minimumAmountToRaiseTo + 0.05 * _playersRemainingChips)
        # bet < 50% of player stack size: Call
        elif _maximumBet < 0.5 * _playersRemainingChips:
            action = ClientBase.BettingAnswer.ACTION_CALL
        # for higher bets: go Allin
        else:
            action = ClientBase.BettingAnswer.ACTION_ALLIN

    # chance to win: 60% <= w < 80%
    elif (chance < 0.8):
        # bet < 60% of player stack size: Raise up to 10% of stack size
        if (_maximumBet < 0.6 * _playersRemainingChips):
            action = ClientBase.BettingAnswer.ACTION_RAISE, int(_minimumAmountToRaiseTo + 0.1 * _playersRemainingChips)
        # player stack size > minimum amount to raise: Call
        elif (_playersRemainingChips > _minimumAmountToRaiseTo):
            action = ClientBase.BettingAnswer.ACTION_CALL
        # Otherwise: go AllIn
        else:
            action = ClientBase.BettingAnswer.ACTION_ALLIN

    # chance to win: w >= 80%
    else:
        # player stack size > (minimum amount to raise + 20% of stack size): Raise up to 15% of stack size
        if (_playersRemainingChips > _minimumAmountToRaiseTo + 0.2 * _playersRemainingChips):
            action = ClientBase.BettingAnswer.ACTION_RAISE, int(_minimumAmountToRaiseTo + 0.15 * _playersRemainingChips)
        # Otherwise: go AllIn
        else:
            action = ClientBase.BettingAnswer.ACTION_ALLIN

    ########### / ACTION ###########

    print 'GermanWings:', action
    return action

'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):

    worse_cards = []
    thrown_cards = ''
    card_range = range(0, 5)

    ########### EVALUATE HAND ###########
    print '=== EVALUATION ==='

    poker_hand = []

    for n in _hand:
        poker_hand.append(Card.new(n))

    Card.print_pretty_cards(poker_hand)

    score = DEUCES_EVALUATOR.evaluate([], poker_hand)
    rank = DEUCES_EVALUATOR.get_rank_class(score)
    ########### / EVALUATE HAND ###########

    print("======= THROW CARDS ACTION =======")

    ########### SEARCH FOR COMBINATIONS ###########

    # Search for High Card
    def search_highCard(cards):
        max = 0
        k = 0
        for i in card_range:
            current = ((cards[i] & 0xF00) >> 8)
            if current > max:
                max = current
                k = i
        return k

    # Search for Pair combination
    def search_pair(cards):
        for i in range(0, 4):
            for j in range(i + 1, 5):
                if (cards[i] & 0xF00) == (cards[j] & 0xF00):
                    return [i, j]
        return []

    # Search for Two Pair combination
    def search_twoPair(cards):
        [k, l] = search_pair(cards)
        for i in range(k + 1, 4):
            for j in range(i + 1, 5):
                if (cards[i] & 0xF00) == (cards[j] & 0xF00):
                    return [k, l, i, j]
        return []

    # Search for Three of a Kind combination
    def search_threeKind(cards):
        [k, l] = search_pair(cards)
        for i in range(l + 1, 5):
            if (cards[i] & 0xF00) == (cards[l] & 0xF00):
                return [k, l, i]
        return []

    # Search for Four of a Kind combination
    def search_fourKind(cards):
        [k, l] = search_pair(cards)
        if k != 0:
            return 1
        else:
            for i in range(1, 5):
                if (cards[i] & 0xF00) != (cards[0] & 0xF00):
                    return i

    ########### / SEARCH ###########

    ########### ACTION DEPENDS HAND RANK ###########

    # For Four of a Kind: Keep the four of a kind a throw the rest away
    if rank == 2:
        worse_cards = [Card.int_to_str(poker_hand[search_fourKind(poker_hand)])]
    # For Three of a Kind: Keep the three of a kind and throw the rest away
    elif rank == 6:
        keep_cards = set(search_threeKind(poker_hand))
        throw_away = filter(lambda x: x not in keep_cards, card_range)
        worse_cards = [Card.int_to_str(poker_hand[throw_away[0]]), Card.int_to_str(poker_hand[throw_away[1]])]
    # For Two Pair: Keep the two pair and throw the rest away
    elif rank == 7:
        keep_cards = set(search_twoPair(poker_hand))
        throw_away = filter(lambda x: x not in keep_cards, card_range)
        worse_cards = [Card.int_to_str(poker_hand[throw_away[0]])]
    # For Pair: Keep the pair and throw the rest away
    elif rank == 8:
        keep_cards = set(search_pair(poker_hand))
        throw_away = filter(lambda x: x not in keep_cards, card_range)
        worse_cards = [Card.int_to_str(poker_hand[throw_away[0]]),
                       Card.int_to_str(poker_hand[throw_away[1]]),
                       Card.int_to_str(poker_hand[throw_away[2]])]
    # For High Card: Keep the high card and throw the rest away
    elif rank == 9:
        keep_cards = [search_highCard(poker_hand)]
        throw_away = filter(lambda x: x not in keep_cards, card_range)
        worse_cards = [Card.int_to_str(poker_hand[throw_away[0]]),
                       Card.int_to_str(poker_hand[throw_away[1]]),
                       Card.int_to_str(poker_hand[throw_away[2]]),
                       Card.int_to_str(poker_hand[throw_away[3]])]

    ########### / ACTION ###########

    # Create string of thrown away cards:
    for i in range(0, len(worse_cards)):
        thrown_cards += worse_cards[i] + ' '
    print('Weakest cards are thrown away: ' + thrown_cards)

    return thrown_cards

# InfoFunction:

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(_round):
    #_nrTimeRaised = 0
    print('Starting Round: ' + _round )

'''
* Called when the poker server informs that the game is completed.
'''
def infoGameOver():
    print('The game is over.')

'''
* Called when the server informs the players how many chips a player has.
* @param playerName    the name of a player.
* @param chips         the amount of chips the player has.
'''
def infoPlayerChips(_playerName, _chips):
    print('The player ' + _playerName + ' has ' + _chips + 'chips')

'''
* Called when the ante has changed.
* @param ante  the new value of the ante.
'''
def infoAnteChanged(_ante):
    print('The ante is: ' + _ante)

'''
* Called when a player had to do a forced bet (putting the ante in the pot).
* @param playerName    the name of the player forced to do the bet.
* @param forcedBet     the number of chips forced to bet.
'''
def infoForcedBet(_playerName, _forcedBet):
    print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")


'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(_playerName, _openBet):
    print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(_playerName):
    print("Player "+ _playerName +" checked.")

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(_playerName, _amountRaisedTo):
    print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(_playerName):
    print("Player "+_playerName +" called.")

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(_playerName):
    print("Player "+ _playerName +" folded.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(_playerName, _allInChipCount):
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(_playerName, _cardCount):
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(_playerName, _hand):
    print("Player "+ _playerName +" hand " + str(_hand))

'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(_playerName, _winAmount):
    print("Player "+ _playerName +" won " + _winAmount + " chips.")