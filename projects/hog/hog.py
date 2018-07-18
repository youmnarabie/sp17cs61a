"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


# ######################
# # Phase 1: Simulator #
# ######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled (capped at 11 - NUM_ROLLS).
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    #BEGIN PROBLEM 1
    rolls = []
    magic = num_rolls
    while magic > 0:
        roll = dice()
        rolls.append(roll)    
        magic -= 1
    num_ones = rolls.count(1)
    sum_score = sum(rolls)   
    if 1 in rolls and num_ones <= num_rolls:
        return min(11 - num_rolls, num_ones)
    elif 1 not in rolls: 
        return sum_score
     # END PROBLEM 1




    # total = 0
    # poggo = 0
    # piggies = 0
    # rolls = 0
    # while rolls < num_rolls:
    #     result = dice()
    #     if result == 1:
    #         poggo = 1
    #         piggies += 1
    #     else:
    #         total += result
    #     rolls += 1
    # if piggies > (11 - num_rolls):
    #     piggies = (11 - num_rolls)
    # if poggo == 1:
    #     return piggies
    # else:
    #     return total
    # # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    return 1 + max(opponent_score // 10, opponent_score % 10)
    # END PROBLEM 2

def is_prime(n):
    if n == 1:
        return False
    even = 2
    while even < n:
        if n % even == 0:
            return False
        even += 1
    return True

def next_prime(n):
    if is_prime(n):
        new = n + 1
        while new > 1 and is_prime(new) == False:
            is_prime(n)
            new += 1
        return new


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    div = 2
    points = 0
    prime = False
    if num_rolls == 0:
        points = free_bacon(opponent_score)
    else:
        points = roll_dice(num_rolls, dice)
    if points == 1:
        return points
    while div != points:
        if points % div == 0 and div != points:
            return points
        div += 1
    div = 2
    points = points + 1
    while prime != True:
        while points % div != 0:
            div += 1
        if div == points:
            return points
        div = 2
        points += 1
    # END PROBLEM 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).
    """
    # BEGIN PROBLEM 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END PROBLEM 3

def is_swap(score0, score1):
    """Returns whether one of the scores is double the other.
    """
    # BEGIN PROBLEM 4
    if score0 == (2 * score1) or score1 == (2 * score0):
        return True
    else:
        return False
    # END PROBLEM 4

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    dice = six_sided
    while (score0 < goal and score1 < goal):
        if player == 0:
            dice = select_dice(score0, score1)
            strat0 = strategy0(score0, score1)
            result0 = take_turn(strat0, score1, dice)
            score0 += result0
            player = other(0)
            if is_swap(score0, score1):
                orig_score0 = score0
                orig_score1 = score1
                score0 = orig_score1
                score1 = orig_score0
        if score0 >= goal or score1 >= goal:
            return score0, score1
        if player == 1:
            dice = select_dice(score1, score0)
            strat1 = strategy1(score1, score0)
            result1 = take_turn(strat1, score0, dice)
            score1 += result1
            player = other(1)
            if is_swap(score0, score1):
                orig_score0 = score0
                orig_score1 = score1
                score0 = orig_score1
                score1 = orig_score0
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    score0 = 0
    while score0 < goal:
        score1 = 0
        num_rolls = strategy(score0, score1)
        validity = check_strategy_roll(score0, score1, num_rolls)
        if validity != None:
            return validity
        while score1 < goal:
            num_rolls = strategy(score0, score1)
            validity = check_strategy_roll(score0, score1, num_rolls)
            if validity != None:
                return validity
            score1 += 1
        score0 += 1
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    def averaging(*args):
        results = 0
        num_call = 0
        while num_call < num_samples:
            result = fn(*args)
            results += result
            num_call += 1
        return results / num_samples
    return averaging
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    result = 0
    num_call = 0
    num_rolls = 1
    roll_result = []
    num_rollss = []
    while num_rolls <= 10 and num_call < num_samples:
        num_call += 1
        function = make_averaged(roll_dice, num_samples)
        result = function(num_rolls, dice)
        roll_result.append(result)
        num_rollss.append(num_rolls)
        num_rolls += 1
    largest_score = max(roll_result)
    index = roll_result.index(largest_score)
    largest_number = num_rollss[index]
    return largest_number
    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))
    if True:
        print('Final Strategy', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    if is_prime(free_bacon(opponent_score)) and next_prime(free_bacon(opponent_score)) >= margin:
        num_rolls = 0
    elif free_bacon(opponent_score) >= margin:
        num_rolls = 0
    else:
        num_rolls = num_rolls
    return num_rolls
    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    is_bacon_good = bacon_strategy(score, opponent_score, margin, num_rolls)
    if is_bacon_good == 0:
        return 0
    elif is_swap(score, opponent_score) == True:
        orig_score0 = score
        orig_score1 = opponent_score
        score = orig_score1
        opponent_score = orig_score0
        if score > opponent_score:
            return 0
        else:
            return num_rolls
    else:
        return num_rolls
    # END PROBLEM 10
check_strategy(swap_strategy)


def final_strategy(score, opponent_score, dice = six_sided):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 11
    margin = 8
    num_rolls = 6
    die_used = select_dice(score, opponent_score)
    if die_used == four_sided:
        margin = 3
        num_rolls = 4
        return swap_strategy(score, opponent_score, margin, num_rolls)
    if opponent_score - 5 > score:
        margin += 2
        num_rolls = 5
    if opponent_score - 15 > score:
        margin += 2
        num_rolls = 7
    if opponent_score - 25 > score:
        margin += 4
        num_rolls = 8
    if opponent_score - 35 > score:
        margin = 15
        num_rolls = 9
    possible_new_score = bacon_strategy(score, opponent_score, margin, num_rolls)
    if is_prime(possible_new_score):
        possible_new_score = next_prime(possible_new_score)
    if possible_new_score + score >= 100:
        return 0
    should_swap = swap_strategy(score, opponent_score, margin, num_rolls)
    return should_swap

#     # END PROBLEM 11
# check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
