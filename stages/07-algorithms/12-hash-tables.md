# Lesson 7.12: Hash Tables: How Dictionaries Find Things Fast

**Time:** 2–3 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
about 20 index cards or sticky notes; 10 cups, bowls or envelopes,
numbered 0 to 9 · **New words:** hash, hash function, bucket,
collision, hash table, method

## Goal *(read this to the learner)*

> In Stage 3 you used dictionaries: `health["creeper"]` finds the
> creeper's health instantly, even in a dictionary with a million mobs.
> Binary search would need 20 looks. How can a dictionary do it in
> about *one*? The secret is to work out, from the key itself, exactly
> where it should be stored. That's a **hash table**, and today you'll
> build your own.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Write a mob name on each of 14 cards: pig, cow, sheep, creeper,
      zombie, skeleton, spider, enderman, witch, ghast, blaze, bee, wolf,
      cat.
- [ ] Line up the 10 cups, numbered 0 to 9.

## Warm-up (5 min)

"What's the Big-O of binary search?" *(O(log n).)* "And of looking at
`items[500]` in a Python list?" *(O(1): it jumps straight there.)*
"Today: how to jump straight to a *word*, not just a position."

## Activity

### Session 1: buckets

1. **A rule for where things go.** **Say:** "Imagine a library with ten
   shelves. If we had a rule that turns any book's title into a shelf
   number, we'd never have to search: just work out the number and go
   there." Pick a rule together: *count the letters in the mob's name,
   and use the last digit*. So "creeper" (7 letters) goes in cup 7, and
   "iron golem" (10, with the space) in cup 0.

   The learner sorts all 14 cards into the cups with that rule. Then the
   guide asks, "Is the witch here?", and the learner works out the cup
   and looks in *just that one*.

   **Ask:** "Which cups got crowded? Which are empty?" *(Cups 3 and 5 get
   four mobs each, and cups 0, 1, 2 and 9 get none.)* **Say:** "When two
   keys land in the same cup, that's a **collision**. A crowded cup means
   more looking. A good rule spreads things out evenly."

2. **A better rule.** **Say:** "In Stage 4, you saw that every letter has
   a number: its ASCII code. `ord("a")` is 97. What if we add up the
   codes of all the letters?" New file, `~/lab/algo/letter_hash.py`:
   ```python
   def letter_hash(word):
       """Adds up the letters' codes."""
       total = 0
       for letter in word:
           total = total + ord(letter)
       return total


   mobs = ["pig", "cow", "sheep", "creeper", "zombie", "skeleton", "spider",
           "enderman", "witch", "ghast", "blaze", "bee", "wolf", "cat"]

   buckets = []
   for i in range(10):
       buckets.append([])

   for mob in mobs:
       number = letter_hash(mob) % 10
       buckets[number].append(mob)

   for number in range(10):
       print(number, buckets[number])
   ```
   **Say:** "`% 10` is the remainder after dividing by 10, so it's always
   0 to 9: a cup number. Each cup is called a **bucket**." Run it. **They
   should see:**
   ```
   0 ['pig', 'bee', 'wolf']
   1 []
   2 ['creeper', 'enderman', 'cat']
   3 ['sheep', 'witch']
   4 []
   5 ['ghast']
   6 ['zombie', 'blaze']
   7 ['spider']
   8 []
   9 ['cow', 'skeleton']
   ```
   **Say:** "More spread out than counting letters, but not perfect. A
   rule that turns a key into a number like this is called a **hash
   function**, and the number is its **hash**."

3. **Python's own hash.** In the terminal, run this twice:
   ```
   python3 -c 'print(hash("creeper"))'
   ```
   **They should see:** a huge number, possibly negative, and a
   *different* one the second time. **Say:** "Python's hash function
   scrambles words much more thoroughly than ours, so they spread out
   evenly. It even changes every time Python starts, which stops
   attackers from planning collisions on purpose. Numbers are simpler:
   try `hash(42)`." *(42.)*

### Session 2: a hash table of our own

4. **Methods.** **Say:** "We'll make a class, `HashTable`, with its own
   functions inside it. A function inside a class is called a
   **method**, like `.append()` belongs to lists. Every method gets
   `self` first: the table it's working on." New file,
   `~/lab/algo/hashtable.py`:
   ```python
   class HashTable:
       """A dictionary of our own: each key goes in a bucket chosen by its hash."""

       def __init__(self):
           self.buckets = []
           for i in range(1000):
               self.buckets.append([])
           self.count = 0

       def bucket_for(self, key):
           return self.buckets[hash(key) % len(self.buckets)]

       def put(self, key, value):
           bucket = self.bucket_for(key)
           for pair in bucket:
               if pair[0] == key:
                   pair[1] = value
                   return
           bucket.append([key, value])
           self.count = self.count + 1
   ```
   **Say:** "Each bucket is a list of `[key, value]` pairs. `put` finds
   the right bucket. If the key's already there, it changes the value.
   If not, it adds a new pair, and counts it."

5. **Your turn.** The learner adds two methods, with hints:
   - `get(self, key)`: gives back the value for `key`, or `None` if it
     isn't there. *(Find the bucket with `self.bucket_for(key)`, then
     look through its pairs, like `put` does.)*
   - `size(self)`: how many keys are in the table. *(`return
     self.count`.)*

   Try it in the shell:
   ```
   >>> from hashtable import HashTable
   >>> health = HashTable()
   >>> health.put("creeper", 20)
   >>> health.put("iron golem", 100)
   >>> health.get("creeper")
   20
   >>> print(health.get("ghast"))
   None
   >>> health.size()
   2
   >>> health.bucket_for("creeper")
   [['creeper', 20]]
   ```
   Then the checker:
   ```
   python3 check.py hash
   ```
   **They should see** something like:
   ```
   Checking HashTable, in hashtable.py...
     put, get and size: right every time, even with 5000 keys.
     1000 buckets; the longest holds 13 keys; 5 are empty.
   ALL GOOD!
   ```
   *(The bucket numbers change a little each run, because Python's hash
   for words changes.)* Commit.

### Session 3: why it's fast

6. **The number of buckets matters.** New file,
   `~/lab/algo/buckets_race.py`:
   ```python
   import time
   from hashtable import HashTable

   for number_of_buckets in [1, 10, 1000]:
       table = HashTable()
       table.buckets = []
       for i in range(number_of_buckets):
           table.buckets.append([])
       start = time.perf_counter()
       for i in range(10_000):
           table.put(i, i * i)
       for i in range(10_000):
           table.get(i)
       seconds = time.perf_counter() - start
       print(f"{number_of_buckets:5} buckets: {seconds:.3f} seconds")
   ```
   **Ask first:** "With just 1 bucket, what is the hash table really?"
   *(One long list: every `get` is a linear search.)* Run it. **They
   should see** something like:
   ```
       1 buckets: 2.925 seconds
      10 buckets: 0.317 seconds
    1000 buckets: 0.013 seconds
   ```
   **Say:** "With plenty of buckets, each bucket holds only a few keys,
   so `put` and `get` take about the same time however big the table
   gets: O(1). Python's real dictionaries add more buckets as they fill
   up, so the buckets never get crowded."

7. **What can be a key?** In the shell:
   ```
   >>> hash([1, 2])
   ```
   **They should see:** `TypeError: unhashable type: 'list'`. **Say:**
   "A key must never change, or it would be in the wrong bucket! Lists
   can change, so they can't be keys. Words, numbers and tuples can."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: get('creeper') after changing it to 25 gave 20, but it should be 25.` | `put` adds a second pair instead of changing the first | Keep the `for pair in bucket:` loop in `put` that changes an existing key's value. |
| `TypeError: HashTable.put() takes 2 positional arguments but 3 were given` | `self` is missing from `def put(...)` | Every method starts with `self`: `def put(self, key, value):`. |
| `UnboundLocalError: cannot access local variable 'count' where it is not associated with a value` | `count` instead of `self.count` | Things stored in the table need `self.`: `self.count = self.count + 1`. |
| `NOT YET: after 5000 puts, get(...) gave None...` | `get` gives up after looking at the first pair in the bucket | `return None` goes *after* the loop, not inside it. |
| `NameError: name 'bucket_for' is not defined` | A method was called without `self.` | `self.bucket_for(key)`. |
| `HashTable has no method called get yet.` | It's missing, misspelled, or not indented inside the class | Methods are indented under `class HashTable:`. |

## Talk about it

- What's a hash function? What makes a good one?
- What's a collision? Why do lots of collisions make a hash table slow?
- Why are dictionary lookups O(1), but binary search O(log n)?

## Challenge *(if there's time, or for next time)*

- Make the table *grow*: when `self.count` gets bigger than the number
  of buckets, make twice as many buckets and put every pair back in.
  *(Every pair has to be moved, because `% len(self.buckets)` changes.)*
- Python's `set` is a hash table with keys and no values. Use one to
  find which mobs appear in both of two lists.
- Find two words that collide in `letter_hash` with *any* number of
  buckets. *(Anagrams, like "listen" and "silent", always have the same
  total!)*

## Checkpoint

The learner can, without help:
- [ ] Explain hashing with cups and cards: hash, bucket and collision
- [ ] Write a class with methods that use `self`
- [ ] Pass `python3 check.py hash`
- [ ] Explain why a dictionary is O(1), and why lists can't be keys

## Lab notebook

Draw the cups with the mob cards in them, for the letter-counting rule
and for `letter_hash`. Write the bucket race times. Commit. Add *hash*,
*hash function*, *bucket*, *collision*, *hash table* and *method* to
`dictionary.md`.

## Guide's background *(optional reading)*

A **hash table** stores key-value pairs in an array of buckets, using a
**hash function** to turn each key into a bucket number. With a good
hash function and enough buckets, each bucket holds about the same small
number of keys, so lookups take constant time on average. This version
uses **chaining** (a list in each bucket). Python's own `dict` uses a
different scheme, called open addressing, where a collision moves on to
another slot in the same array, but the idea is the same.

Python randomizes the hash of strings each time it starts (you can see
this with `hash("creeper")`), because attackers once crashed web servers
by sending thousands of keys built to collide, turning O(1) lookups into
O(n). This is a nice first example of how algorithms and security meet,
which comes back in Stage 11. Rust's `HashMap` uses a randomized hash for
the same reason. Hash functions designed to be impossible to reverse,
like SHA-256, are the basis of passwords and of git's commit IDs.
