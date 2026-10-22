# Lesson 3.8: The Mob Book

**Time:** 45 min · **You need:** Thonny; a dictionary (the book kind) ·
**New words:** dictionary, key, value

## Goal *(read this to the learner)*

> A list keeps things in order, by number. But sometimes you want to look
> things up by **name**: "what does a creeper do?", "how much health has
> a zombie?". Python's **dictionary** does exactly that. Today you'll build
> your own mob encyclopedia, and then use a dictionary to count things.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

Look up a word in the paper dictionary. "How did you find it? Did you
start at page 1?" *(No, you jump straight to it by the word.)* "The word
you look up is the **key**. What you find next to it is the **value**."

## Activity

1. **Make a dictionary.** In the Shell:
   ```python
   mobs = {
       "creeper": "sneaks up and explodes",
       "zombie": "groans, and burns in daylight",
       "enderman": "teleports, and hates being looked at",
   }
   mobs["creeper"]
   mobs["enderman"]
   ```
   **Say:** "Curly brackets make a dictionary. Each line is a **key**, a
   colon, and a **value**. To look something up, put the key in square
   brackets, just like a list's slot number, but with a name instead."

2. **Add, change, and check.**
   ```python
   mobs["chicken"] = "lays eggs, and is quite nice really"
   mobs["zombie"] = "groans, burns in daylight, and drops rotten flesh"
   len(mobs)
   "ghast" in mobs
   mobs.get("ghast", "I've never heard of that one")
   ```
   **Say:** "Putting a value in a new key adds it. Putting a value in an old
   key replaces it. `in` checks for a key. And `get` looks something up
   safely: if the key isn't there, it gives back your second choice instead
   of an error."

3. **Loop through it.**
   ```python
   for name in mobs:
       print(name)

   for name, info in mobs.items():
       print(f"{name.upper()}: {info}")
   ```
   **Say:** "A loop over a dictionary gives you the keys. `.items()` gives
   you each key *and* its value, together."

4. **Values can be numbers.** Health, in half-hearts (from Minecraft Java
   Edition):
   ```python
   health = {"zombie": 20, "creeper": 20, "spider": 16, "chicken": 4, "enderman": 40}
   health["spider"]
   max(health, key=health.get)
   ```
   *(16, then `'enderman'`, the toughest.)* Ask: "How many hits would it
   take to beat a spider if every hit does 4?" *(4: 16 ÷ 4.)*

5. **The Mob Book program.** New file, `~/lab/python/stage3/mobbook.py`.
   The learner writes their *own* facts, at least five mobs (or animals,
   or Numberblocks, or Pokémon: anything they know lots about):
   ```python
   mobs = {
       "creeper": "sneaks up and explodes",
       "zombie": "groans, and burns in daylight",
       "enderman": "teleports, and hates being looked at",
       "chicken": "lays eggs, and is quite nice really",
       "skeleton": "shoots arrows from far away",
   }

   print(f"THE MOB BOOK. I know about {len(mobs)} mobs.")
   print("Type a mob's name, 'list' to see them all, or 'quit'.")

   while True:
       name = input("> ").lower().strip()
       if name == "quit":
           break
       elif name == "list":
           for mob in sorted(mobs):
               print(f"  {mob}")
       elif name in mobs:
           print(f"The {name} {mobs[name]}.")
       else:
           info = input(f"I don't know the {name}. What does it do? ")
           mobs[name] = info
           print("Thanks! I'll remember that.")
   ```
   **Say:** "The last part is clever: if the book doesn't know a mob, it
   asks you, and adds it. The book learns!" Then: "When you quit and run it
   again, has it remembered?" *(No! It forgets when it stops. Lesson 3.10
   fixes that.)*

6. **Counting with a dictionary.** New file, `votes.py`:
   ```python
   votes = ["creeper", "pig", "creeper", "axolotl", "pig", "creeper", "axolotl", "axolotl", "axolotl"]

   counts = {}
   for vote in votes:
       counts[vote] = counts.get(vote, 0) + 1

   print(counts)
   for mob, number in counts.items():
       print(f"{mob}: {'#' * number}")
   ```
   **They should see:** `{'creeper': 3, 'pig': 2, 'axolotl': 4}` and a
   little bar chart made of `#`s.

   **Say:** "`counts.get(vote, 0)` means 'how many have we counted so far?
   Zero if we haven't seen it before.' Then add one. This is one of the most
   useful tricks in programming. In the Underpants Heist, `sort | uniq -c`
   did the same job."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `KeyError: 'ghast'` | Looked up a key that isn't in the dictionary | Check with `if name in mobs:` first, or use `mobs.get(name, ...)`. |
| `KeyError` with capitals, like `'Creeper'` | Keys must match exactly, capitals too | Use `.lower()` on what's typed, and keep keys in lower case. |
| `SyntaxError` in the dictionary | A missing colon, comma or quote mark | Every line is `"key": "value",` with the comma at the end. |
| `KeyError: 0` | Used `mobs[0]` as if it were a list | Dictionaries are looked up by key, not by number. |
| Only the last value is there for a key | Keys are unique: adding the same key again replaces it | Use different keys, or a list as the value. |

## Talk about it

- What's the difference between a list and a dictionary?
  *(A list is in order and you get things by number; a dictionary is
  looked up by key.)*
- What's a key, and what's a value?
- Why does the Mob Book forget new mobs when it stops?

## Challenge *(if there's time, or for next time)*

- **Rock, Paper, Scissors, neater:** a dictionary of what each move beats:
  ```python
  beats = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
  ```
  Then the whole winning rule is `if beats[player] == computer:`. Rewrite
  your game from Lesson 3.4 with it. For five moves, make each value a
  list of two moves, and use `if computer in beats[player]:`.
- Count the letters in a sentence: which letter is most common in English?
- A translator: a dictionary from English words to made-up "creeper
  language" words.

## Checkpoint

The learner can, without help:
- [ ] Make a dictionary and look values up by key
- [ ] Add and change entries, and check for a key with `in`
- [ ] Loop through a dictionary with `.items()`
- [ ] Count things with `counts.get(thing, 0) + 1`

## Lab notebook

Draw a dictionary as a two-column table: keys on the left, values on the
right. Write "list = by number, dictionary = by name". Add *dictionary*,
*key* and *value* to the dictionary (the irony!).

## Guide's background *(optional reading)*

Dictionaries (called **hash maps** or **maps** in many other languages,
including Rust) are one of the most powerful tools in programming. They
can look things up almost instantly, however big they get, by working out
from the key itself where it's stored. Stage 7 explains how that works.

The counting pattern (`counts.get(x, 0) + 1`) turns up everywhere: word
counts, votes, inventories, statistics. Python also has a ready-made
`collections.Counter` that does it in one line, but writing it by hand
first shows what's going on.

Lists and dictionaries can hold each other. A dictionary whose values are
dictionaries is how the text adventure in Lessons 3.11 and 3.12 stores its
whole world, and it's also the shape of JSON, the format most web data
travels in.
