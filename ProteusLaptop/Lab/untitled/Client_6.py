__author__ = 'fyt'  # Originally by fyt and modified by LaurenChan & AlexLuo

import socket
import random
import ClientBase

# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 6000
BUFFER_SIZE = 1024

# Agent
POKER_CLIENT_NAME = 'Agent6_Kun'
CURRENT_HAND = []

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
* @param playersCurrentBet     the amount of chips the player has already put into the pot (due to the forced bet).
* @param playersRemainingChips the number of chips the player has not yet put into the pot.
* @return                      An answer to the open query. The answer action must be one of
*                              {@link BettingAnswer#ACTION_OPEN}, {@link BettingAnswer#ACTION_ALLIN} or
*                              {@link BettingAnswer#ACTION_CHECK }. If the action is open, the answers
*                              amount of chips in the answer must be between <code>minimumPotAfterOpen</code>
*                              and the players total amount of chips (the amount of chips already put into
*                              pot plus the remaining amount of chips).
'''
def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose an opening action.")

    if _playersRemainingChips >= 200:
        return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen + 10
    elif 200 > _playersRemainingChips >= 160:
        return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen + 8
    elif 160 > _playersRemainingChips >= 120:
        return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen + 6
    elif 120 > _playersRemainingChips >= 80:
        return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen + 4
    elif 80 > _playersRemainingChips >= 40:
        return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen + 2
    elif 40 > _playersRemainingChips >= 0:
        return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen + 1


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
def queryCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):

    print("Player requested to choose a call/raise action.")

    if _maximumBet < _playersRemainingChips:
        print "_maximumBet < _playersRemainingChips---------------"
        if _playersRemainingChips >= 200:
            # print "--------------->=200---------------"
            return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + 5

        elif 200 > _playersRemainingChips >= 160:
            # print "---------------160&&200--------------"
            return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + 4

        elif 160 > _playersRemainingChips >= 120:
            # print "---------------120&&160--------------"
            return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + 3

        elif 120 > _playersRemainingChips >= 80:
            # print "---------------80&&120---------------"
            return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + 2

        elif 80 > _playersRemainingChips >= 40:
            # print "---------------40&&80---------------"
            return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + 1

        elif 40 > _playersRemainingChips >= 0:
            # print "---------------0&&40---------------"
            return ClientBase.BettingAnswer.ACTION_ALLIN
        else:
            print "Error!!!!!!!!!!!!!!!!!!"

    else:
        print "------Because _maximumBet >= _playersRemainingChips------"

        """
        if _playersCurrentBet >= 100 and _maximumBet >= 150:
            print "1"
            return ClientBase.BettingAnswer.ACTION_ALLIN

        elif _playersCurrentBet < 100 and _maximumBet >= 500:
            print "2"
            return ClientBase.BettingAnswer.ACTION_FOLD

        elif _playersCurrentBet < 100 and _maximumBet < 150:
            print "3"
            return ClientBase.BettingAnswer.ACTION_CALL

        elif _playersCurrentBet >= 100 and _maximumBet < 150:
            print "4"
            return ClientBase.BettingAnswer.ACTION_CALL

        else:
            print "5"
            return ClientBase.BettingAnswer.ACTION_ALLIN
        """

        return ClientBase.BettingAnswer.ACTION_ALLIN


'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(Hand_):
    print("Requested information about what cards to throw")
    print(Hand_)

    Rank = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    Suit = {
        'd': 1, 'c': 2, 'h': 3, 's': 4
    }

    # Get the type of Hand
    def evaluateHand(Hand_):
        count = 0
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    count += 1

        return count

    # Use the "count" to analyse hand
    count_ = evaluateHand(Hand_)

    sub1 = 0
    score = [' ', ' ', ' ']

    if count_ == 12:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 3:
                # For 4OfAKind
                ## hand_strength = 8 * 100 + int(Rank[card1[0]])
                return 'no card'

    elif count_ == 8:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 1:
                sub1 = 0
            if sub1 == 2:
                # For FullHouse
                ## hand_strength = 7 * 100 + int(Rank[card1[0]])
                return 'no card'

    elif count_ == 6:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 2:
                score = ['3OfAKind', card1[0]]
                ## hand_strength = 4 * 100 + int(Rank[card1[0]])
                break

        for card1 in Hand_:
            for card2 in Hand_:
                if card1 != card2 and Rank[card1[0]] != Rank[score[1]] and Rank[card2[0]] != Rank[score[1]]:
                    # For 3OfAKind
                    return card1 + ' ' + card2

    elif count_ == 4:
        needCard1 = ['', '']
        needCard2 = ['', '']
        for card1 in Hand_:
            for card2 in Hand_:
                # card1 keep the first hand card, card1 use every card to compare the card1
                if card1[0] == card2[0] and card1[1] != card2[1]:
                    if Suit[card1[1]] > Suit[card2[1]]:
                        if needCard1 == ['', '']:
                            needCard1 = card1
                    else:
                        if needCard1 == ['', '']:
                            needCard1 = card2
                if card1[0] == card2[0] and card1[1] != card2[1] \
                        and card1[0] != needCard1[0] and card2[0] != needCard1[0]:
                    if Suit[card1[1]] > Suit[card2[1]]:
                        if needCard2 == ['', '']:
                            needCard2 = card1
                    else:
                        if needCard2 == ['', '']:
                            needCard2 = card2
        if Rank[needCard1[0]] > Rank[needCard2[0]]:
            score = ['TwoPairs', needCard1[0], needCard1[1]]
            ## hand_strength = 3 * 100 + int(Rank[needCard1[0]])
        else:
            score = ['TwoPairs', needCard2[0], needCard2[1]]
            ## hand_strength = 3 * 100 + int(Rank[needCard2[0]])

        for card in Hand_:
            if Rank[card[0]] != Rank[needCard1[0]] and Rank[card[0]] != Rank[needCard2[0]]:
                return card + ' '

    elif count_ == 2:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] > card2[1]):
                    sub1 += 1
            if sub1 == 1:
                score = ['OnePair', card1[0], card1[1]]
                ## hand_strength = 2 * 100 + int(Rank[card1[0]])
                break

        biu = []
        for card in Hand_:
            if Rank[card[0]] != Rank[score[1]]:
                biu.append(card)
        return biu[0] + ' ' + biu[1] + ' ' + biu[2]

    elif count_ == 0:

        def sortHand(Hand_):
            for card1 in Hand_:
                for card2 in Hand_:
                    for card3 in Hand_:
                        for card4 in Hand_:
                            for card5 in Hand_:
                                if Rank[card1[0]] < Rank[card2[0]] < Rank[card3[0]] < Rank[card4[0]] < Rank[card5[0]]:
                                    sortedHand_ = [card1, card2, card3, card4, card5]
                                    return sortedHand_

        Hand_ = sortHand(Hand_)

        if Hand_[0][1] == Hand_[1][1] == Hand_[2][1] == Hand_[3][1] == Hand_[4][1]:
            # For Flush
            ## hand_strength = 6 * 100 + int(Rank[Hand_[4][0]])
            return 'no card'

        elif (Rank[Hand_[4][0]] - Rank[Hand_[3][0]] == 1) \
                and (Rank[Hand_[3][0]] - Rank[Hand_[2][0]] == 1) \
                and (Rank[Hand_[2][0]] - Rank[Hand_[1][0]] == 1) \
                and (Rank[Hand_[1][0]] - Rank[Hand_[0][0]] == 1):
            # For Straight & StraightFlush
            ## hand_strength = 666
            return 'no card'

            # if Hand_[0][1] == Hand_[1][1] == Hand_[2][1] == Hand_[3][1] == Hand_[4][1]:
            #     score = ['StraightFlush', Hand_[4][0], Hand_[4][1]]

        else:
            score = ['HighCard', Hand_[4][0], Hand_[4][1]]
            ## hand_strength = 1 * 100 + int(Rank[Hand_[4][0]])
            return Hand_[3] + ' ' + Hand_[2] + ' ' + Hand_[1] + ' ' + Hand_[0]

    # return Hand_[0] + ' ' + Hand_[1]
    return 'Error!'


# InfoFunction:

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(_round):
    # nrTimeRaised = 0
    print('Starting Round: ' + _round)

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
    print("Player " + _playerName + " made a forced bet of " + _forcedBet + " chips.")


'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(_playerName, _openBet):
    print("Player " + _playerName + " opened, has put " + _openBet + " chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(_playerName):
    print("Player " + _playerName + " checked.")

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(_playerName, _amountRaisedTo):
    print("Player " + _playerName + " raised to " + _amountRaisedTo + " chips.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(_playerName):
    print("Player " + _playerName + " called.")

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(_playerName):
    print("Player " + _playerName + " folded.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(_playerName, _allInChipCount):
    print("Player " + _playerName + " goes all-in with a pot of " + _allInChipCount + " chips.")

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(_playerName, _cardCount):
    print("Player " + _playerName + " exchanged " + _cardCount + " cards.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(_playerName, _hand):
    print("Player " + _playerName + " hand " + str(_hand))

'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player " + _playerName + " won " + _winAmount + " chips undisputed.")

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(_playerName, _winAmount):
    print("Player " + _playerName + " won " + _winAmount + " chips.")

