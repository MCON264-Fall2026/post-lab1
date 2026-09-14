"""
MCON 264 - Lab 1 ANSWER KEY
Data Structures I, Fall 2026

This is ONE Version of the correct solutions, written the way Module 1 taught it. Your version
may look different and still be right. Read this alongside the Lab 1 summary.

Every comment below points back at something we did in Module 1, so this file
doubles as a walk back through the module. The code is short. The comments are
not, and that is deliberate.
"""

import random

# Module 1: a data structure is an arrangement of data, plus the
# operations that arrangement makes cheap. These two lists are arrangements.
# RANKS is not in alphabetical order and not in any order Python chose. It is
# in PLAYING ORDER, weakest to strongest, because somebody decided that. Hold
# on to that fact; it does real work for us in Card.value() below.
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["\u2660", "\u2665", "\u2666", "\u2663"]  # spades, hearts, diamonds, clubs


class Card:
    """A single playing card. Knows its rank and suit, and nothing else.

    Module 1, slides 50 to 54. A class is a blueprint. It is not a card.
    Nothing exists yet when Python reads this line. Cards start existing when
    somebody writes Card("A", "spades"), and each one of those is an OBJECT
    built from this blueprint.
    """

    def __init__(self, rank, suit):
        # TODO 1 --------------------------------------------------------------
        #
        # __init__ is a dunder method: double underscore before, double
        # underscore after. You never call it yourself. Python calls it for
        # you, once, at the moment an object is built.
        #
        # `self` is THE OBJECT BEING BUILT RIGHT NOW. That is the "flip it
        # over" question from slide 53. When you write:
        #
        #     ace   = Card("A", "\u2660")
        #     deuce = Card("2", "\u2665")
        #
        # __init__ runs twice, and `self` is a different object each time.
        # That is exactly why two cards can hold different values without
        # interfering with each other.
        #
        # `self.rank = rank` means: take the rank that was passed in, and
        # store it ON THIS OBJECT so it is still there later. Drop the `self.`
        # and you have made a local variable that vanishes the moment
        # __init__ finishes.
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        # TODO 2 --------------------------------------------------------------
        #
        # Another dunder. This one answers: what should Python show when it
        # prints this object? Without it you get <Card object at 0x7f9a...>,
        # which is the memory address. Technically true, completely useless.
        #
        # Two things worth knowing:
        #   - __repr__ must RETURN a string. It must not print one. If you
        #     write print(...) here instead of return, the checker will tell
        #     you __repr__ returned None.
        #   - The spec asked for A\u2660, not "A, \u2660" and not "A of spades". When a
        #     spec shows you exact output, that output is the requirement.
        #     One submission used a comma here and the checker let it through,
        #     because the checker only asked "is it a string that contains the
        #     rank". A stricter test would have caught it. This is the Module 2
        #     lesson arriving early.
        return f"{self.rank}{self.suit}"

    def value(self):
        # TODO 3 --------------------------------------------------------------
        #
        # Here is where the arrangement pays for itself.
        #
        # We need 2 to be weakest and A strongest. We could write a dictionary
        # mapping every rank to a number, or a chain of thirteen if statements.
        # We do not have to, because RANKS is already in playing order, so an
        # item's POSITION in that list IS its strength.
        #
        #     RANKS.index("2")  ->  0
        #     RANKS.index("9")  ->  7
        #     RANKS.index("A")  ->  12
        #
        # Same data, arranged deliberately, and a question that would have
        # taken thirteen branches becomes one line. That is the whole thesis of
        # Module 1 in a single method.
        #
        # Worth knowing for Module 2: .index() has to scan the list looking for
        # a match, so it is O(n) in the length of RANKS. RANKS has 13 items and
        # never grows, so nobody cares here. On a list of a million, you would.
        return RANKS.index(self.rank)


class Deck:
    """A container class: it holds Cards and knows how to manage them.

    Module 1: "is a Deck a kind of list, or does it have one?"

    It HAS one. Notice what this class does NOT say:

        class Deck(list):        # <- we did not do this

    If Deck inherited from list, it would also inherit sort, insert, reverse,
    slicing, and about forty other methods. Any of them would let an outsider
    reach in and do something a deck of cards should not allow. Instead the
    Deck holds a list in self.cards and exposes only four things it is willing
    to promise: build, count, shuffle, deal.

    That is composition. Has-a, not is-a. You will use this exact shape for
    every structure you build this semester, so it is worth staring at.
    """

    def __init__(self):
        # TODO 4 --------------------------------------------------------------
        #
        # A fresh deck is 52 cards: every rank in every suit. Two loops, one
        # nested inside the other. 4 suits times 13 ranks is 52.
        #
        # The comprehension below is the short way to write this:
        #
        #     for suit in SUITS:                   <- outer loop
        #         for rank in RANKS:               <- inner loop
        #             self.cards.append(Card(rank, suit))
        #
        # Read the comprehension left to right and the `for` clauses appear in
        # exactly that same outer-to-inner order. That trips people up, because
        # the Card(rank, suit) part sits at the FRONT even though it happens
        # last.
        #
        # Either version is correct and the checker accepts both. Use whichever
        # one you can still read at 1am.
        #
        # Swapping the two loops (rank outer, suit inner) also gives you all 52
        # cards, just built in a different starting order. Since the next thing
        # anybody does is shuffle, that difference does not matter here.
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]

    def __len__(self):
        # TODO 5 --------------------------------------------------------------
        #
        # A third dunder. This is what makes len(deck) work.
        #
        # Without it, len(deck) raises TypeError: object of type 'Deck' has no
        # len(). With it, Deck plugs into a piece of Python that already
        # existed. You did not modify len. You taught your object how to answer
        # when len asks.
        #
        # That is the ADT idea from slides 40 to 44 pointing the other way:
        # len() does not care what a Deck is made of. It only cares that the
        # object can answer the question.
        #
        # Note we return len(self.cards), the length of the list we hold, not
        # 52. Hard-coding 52 would pass the checker and then lie to you the
        # instant a card is dealt.
        return len(self.cards)

    def shuffle(self):
        # TODO 6 --------------------------------------------------------------
        #
        # random.shuffle rearranges a list IN PLACE. It reaches into the list
        # you gave it, moves things around, and hands back None.
        #
        # So do NOT write:
        #
        #     return random.shuffle(self.cards)     # returns None
        #
        # It works, because nobody uses the return value. But it says something
        # you do not mean. Methods that change a thing usually hand back
        # nothing. The change IS the result.
        #
        # The same pattern applies to .sort(), .append(), .reverse(). All of
        # them change the thing and return None. Compare with sorted(), which
        # leaves the original alone and gives you a NEW list back. We use that
        # distinction properly in Module 2.
        #
        # Why in-place works at all: self.cards is a REFERENCE to a list object
        # (slides 47 and 48). Passing it to random.shuffle does not copy it. It
        # hands over a second way to reach the same list, and shuffle rearranges
        # the original. That is the aliasing lesson being useful rather than
        # dangerous.
        random.shuffle(self.cards)

    def deal(self):
        # TODO 7 --------------------------------------------------------------
        #
        # Remove the top card and return it. Both of those have to happen. A
        # version that returns a card without removing it deals the same card
        # forever.
        #
        # list.pop() with no argument removes and returns the LAST item, so one
        # line does both jobs.
        #
        # Which end is "the top"? Either works for a deck of cards:
        #
        #     return self.cards.pop()      # last item
        #     return self.cards.pop(0)     # first item
        #
        # Both pass the checker. Both play a complete game of War. They do not
        # cost the same, and the gap grows with the size of the pile. That is
        # Module 2, and you measure it yourself in Lab 2.
        #
        # One thing this method deliberately does not do: check whether the
        # deck is empty. Calling deal() on an empty deck raises IndexError. For
        # this lab that is fine, and arguably correct: dealing from an empty
        # deck IS a mistake, and a loud crash beats a silent None.
        return self.cards.pop()

    def deal_hands(self, players, per_player):
        # TODO 8 (stretch) ----------------------------------------------------
        #
        # The starter file said the checker skips this one, and it does. That
        # is exactly why it is worth doing: nothing was watching.
        #
        # Deal one card at a time, round the table, the way a person deals.
        # Not the whole hand to player one, then the whole hand to player two.
        #
        # Step 1: one empty list per player.
        #
        #     hands = [[] for _ in range(players)]
        #
        #   Build it with a comprehension, NOT with [[]] * players. That second
        #   version gives you the SAME list object repeated, so appending to one
        #   hand appends to all of them. That is the aliasing trap from slide 47
        #   wearing a different hat, and it is a genuinely nasty bug because the
        #   card count still comes out right.
        #
        # Step 2: the loops. Outer loop is ROUNDS, inner loop is PLAYERS.
        #   Swap them and you have dealt one player their whole hand before the
        #   next player gets anything. Same number of cards, different game.
        #
        # Step 3: call self.deal(), not self.cards.pop().
        #   Both work today. But deal() is this class's promise about how a card
        #   leaves the deck. If you later change deal() to log the card, or to
        #   refuse when the deck is empty, everything that goes through the
        #   front door gets that for free. Anything that reached past it does
        #   not. Use your own interface.
        #
        # `_` is the conventional name for a loop variable you never use. It is
        # an ordinary variable name, not syntax; it just tells a reader "the
        # count matters, the value does not."
        hands = [[] for _ in range(players)]

        for _ in range(per_player):        # one full trip round the table
            for hand in hands:             # one card to each player, in turn
                hand.append(self.deal())

        return hands


if __name__ == "__main__":
    # This block runs only when you execute this file directly, and not when
    # another file imports it. That is why check_cards.py and war.py can import
    # your classes without this demo firing.
    d = Deck()
    print(f"Deck has {len(d)} cards")          # __len__ answering
    d.shuffle()
    print("Top five:", [d.deal() for _ in range(5)])   # __repr__ answering
    print(f"{len(d)} cards left")

    # deal_hands(), exercised:
    d2 = Deck()
    d2.shuffle()
    hands = d2.deal_hands(4, 5)
    print(f"\nDealt {len(hands)} hands of {len(hands[0])}: {hands[0]}")
    print(f"{len(d2)} cards left in the deck")
