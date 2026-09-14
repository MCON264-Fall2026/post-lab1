# Post-lab1: Summary and Review

Every pattern below showed up in at least one submission, and most of them showed up in several.

Keep this. It doubles as your review sheet for the concepts Lab 1 was actually testing.

---

## The headline

| | |
|---|---|
| Submissions received | 6 |
| Passed all 8 checks in `check_cards.py` | 6 of 6 |
| `war.py` plays a full game | 6 of 6 |
| Completed the `deal_hands()` stretch | 1 of 6 |
| Attempted it and shipped code that crashes | **1 of 6** |

First, credit where it is due. Everybody's checker printed `All eight done`, and everybody's game plays start to finish. That is a clean sweep on everything the lab actually required.

`deal_hands()` was marked in your starter file as **"TODO 8"**. So if you left it as `pass`, you did exactly what the file told you was fine. Nobody is in trouble.

Here is the interesting part. One submission did attempt it, and the code in it raises `TypeError` the moment it is called. Nothing caught that. Not the checker, not the game, not the author.

From the outside, an unfinished `pass` and a crash-on-first-call looked identical. Both printed `All eight done`. That is the lesson, and it is the exact reason Module 2 exists.

---

## The thing nothing tested

`check_cards.py` never mentions `deal_hands`. Go and look: open the file and search for it. It is not there.

`war.py` does not call it either. It deals with a list comprehension instead:

```python
alice = [deck.deal() for _ in range(half)]
bob   = [deck.deal() for _ in range(half)]
```

So `deal_hands()` sat in the middle of your file with nothing watching it. Four left it as `pass`, which the starter said was fine. One wrote code that crashes. One worked. All six printed the same green result.

**A green checkmark means "the things I checked passed." It never means "your code is correct."** Anything a test does not touch is a place bugs live rent free.

Which raises a better question than "who finished the stretch": *how would you have known?* You could not have, with the tools you had. That is what changes today.

This is what we fix today. In Lab 2 you write the tests yourself, and you will find that writing the test is where you discover what you actually meant.

---

## What went well

**Everybody got the object model right.** All six submissions store rank and suit on the instance, all six use `self`, and all six correctly separate the Card (the data) from the Deck (the structure that holds it). That was the hardest conceptual jump in Module 1 and the class cleared it.

**`__repr__` was understood.** Five of six return exactly the format the spec asked for. Nobody printed `<Card object at 0x7f...>` at the end.

**`value()` used the list as the ranking.** Every submission worked out that `RANKS.index(self.rank)` gives you the ordering for free, because the list is already in order. That is a genuinely good instinct: the arrangement of the data was doing work for you.

**Two different correct approaches to building the deck.** Some used a nested loop, some used a comprehension:

```python
# both of these build all 52 cards
self.cards = []
for suit in SUITS:
    for rank in RANKS:
        self.cards.append(Card(rank, suit))

self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
```

Neither is better. The second is shorter, the first is easier to read at 1am. Use whichever one you can still understand next week.

---

## What to review

Seven things, in rough order of how much they will cost you later.

### 1. `deal_hands()`, the round robin

Worth sitting down and writing even though it was optional, because it exercises four separate things at once. Five of six submissions still need it.

The spec said: deal one card at a time, going round the table, the way a person deals. Not the whole hand to one player, then the whole hand to the next.

**What appeared in the one submission that attempted it:**

```python
def deal_hands(self, players, per_player):
    for i in per_player:      # per_player is a NUMBER, not a list
        players.deal()        # players is a NUMBER, it has no .deal()
```

Two separate mistakes stacked, and no `return` at all, so the caller gets `None` even if the loop had worked.

**What it should look like:**

```python
def deal_hands(self, players, per_player):
    hands = [[] for _ in range(players)]   # one empty list per player
    for _ in range(per_player):            # go round the table this many times
        for hand in hands:                 # one card to each player, in turn
            hand.append(self.deal())
    return hands
```

Read the loop order out loud. The outer loop is rounds. The inner loop is players. Swap them and you have dealt the whole hand to player one before player two gets anything, which is a different function.

### 2. A number is not a sequence

```python
for i in per_player:        # TypeError: 'int' object is not iterable
for i in range(per_player): # correct
```

`for` needs something with items in it. `5` is not a container holding five things. `range(5)` is.

### 3. Know what your variables are

```python
def deal_hands(self, players, per_player):
    players.deal()          # players is an int. Ints do not deal cards.
```

`players` is how many people are at the table. The thing that deals is `self`, the Deck. When a line reads oddly out loud (*"the number four, deal a card"*) that is your signal.

### 4. A method that changes something usually returns nothing

Three submissions wrote:

```python
def shuffle(self):
    return random.shuffle(self.cards)   # returns None
```

This works, so nothing broke. But it is worth knowing why it works: `random.shuffle` rearranges the list **in place** and hands back `None`. There is nothing to return. The `return` is doing nothing.

```python
def shuffle(self):
    random.shuffle(self.cards)          # say what you mean
```

Same pattern trips people with `.sort()` and `.append()` and `.reverse()`. They all change the thing and return `None`. Compare with `sorted()`, which leaves the original alone and gives you a new list back. We will use that distinction in Module 2.

### 5. `pass` after a `return` is dead code

One submission had seven of these:

```python
def value(self):
    return RANKS.index(self.rank)
    pass                                # never runs
```

`pass` is a placeholder meaning *this block is deliberately empty*. Once you have written the real code, delete it. Nothing breaks if you leave it, but it tells a reader (and me) that the scaffolding was never cleaned up.

### 6. Match the output format exactly

One `__repr__` returned `A, ♠` rather than `A♠`:

```python
return f"{self.rank}, {self.suit}"      # A, ♠
return f"{self.rank}{self.suit}"        # A♠
```

The checker accepted it, because the checker only asked *did you return a string*. A stricter test would have caught it. When a spec shows you exact output, that output is part of the requirement.

### 7. Use your own front door

One submission implemented `deal_hands` by reaching straight into the list:

```python
cards_per_player[player] += [self.cards.pop()]   # bypasses your own deal()
hand.append(self.deal())                          # uses it
```

Both work today. But `deal()` is the Deck's promise about how a card leaves the deck. If you later change `deal()` to log a card, or to refuse when the deck is empty, every caller gets that for free except the one that went around it.

This is the has-a idea from Module 1 in practice: the Deck **has** a list, and everything outside `deal()` should go through the Deck's own methods rather than poking at the list directly.

---

## One more thing

Look at your own `deal()`. Most of you wrote one of these:

```python
return self.cards.pop()       # takes the LAST card
return self.cards.pop(0)      # takes the FIRST card
```

Both are correct. Both pass every check. Both play a complete game of War.

They do not cost the same, and the gap between them grows with the size of the deck. The comment in your starter file told you this was coming:

> Which end is 'the top'? Either works, but one of them is O(1) and the other is O(n). We find out which in Module 2.

---

## Disclaimer and Next Steps

The full answer key is posted alongside this summary. It is ONE VERSION of the correct solution with the reasoning written into the comments, keyed back to Module 1. Read it next to your own file rather than instead of it.

In terms of next steps, you can:

1. Finish `deal_hands()` in your Lab 1 repo, and push it.
2. Delete any leftover `pass` that sits after real code.
3. Look at which end your `deal()` takes from, and hold on to the answer.

Questions about any of the above or future lab related questions go in the #labs channel on Discord, so the answer reaches everyone.