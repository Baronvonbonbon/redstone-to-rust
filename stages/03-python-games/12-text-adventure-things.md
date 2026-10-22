# Lesson 3.12: Text Adventure, Part 2: Things

**Time:** 2–3 sessions of 45 min · **You need:** Thonny; the map and
`fuzzlewood.py` from Lesson 3.11 · **New words:** state, puzzle, split,
playtest

## Goal *(read this to the learner)*

> Right now, Fuzzlewood is a place to walk around, but there's nothing to
> *do*. Today you'll add things to pick up, a room that's too dark to see
> in, and a locked front door. Then there's a puzzle to solve, and a way to
> win. Finally, you'll get someone else to play it.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Back up the learner's working game:
      `cp ~/lab/python/adventure/fuzzlewood.py ~/lab/python/adventure/fuzzlewood-part1.py`

## Warm-up (5 min)

"Here's the puzzle we're going to build. The front door is locked. The key
is in Principal Pickles' office. But the office is pitch dark, so you need
a torch, and the torch is in the gym's lost-property box. Add these to the
map." The learner writes **torch** in the gym and **key** in the office on
the paper map, and adds a **sandwich** in the cafeteria and a **book** in
the library, just for fun.

## Activity

### Session 1: things in rooms

1. **Give rooms some items.** Add an `"items"` list to every room. Rooms
   with nothing get an empty list `[]`. For example:
   ```python
       "gym": {
           "description": "Climbing ropes hang in the gloom. A lost-property box overflows in the corner.",
           "exits": {"west": "hallway"},
           "items": ["torch"],
       },
   ```
   Put `"book"` in the library, `"sandwich"` in the cafeteria, `"key"` in
   the office, and `[]` everywhere else.

2. **Splitting commands.** In the Shell:
   ```python
   "take torch".split()
   "go north".split()
   "look".split()
   ```
   *(`['take', 'torch']`, `['go', 'north']`, `['look']`.)* **Say:**
   "`split` chops a string into a list of words, at the spaces. Then the
   first word is the **verb** (what to do) and the second is the **noun**
   (what to do it to)."

3. **The full game.** Here's the whole of `fuzzlewood.py` with things
   added. The learner can type in the changes, or the guide can show the
   whole program and they go through it together, piece by piece:
   ```python
   rooms = {
       "library": {
           "description": "Rows of books loom in the dark. You must have fallen asleep in the beanbag.",
           "exits": {"east": "hallway"},
           "items": ["book"],
       },
       "hallway": {
           "description": "A long hallway lined with coat pegs. Somebody has left a single sock.",
           "exits": {"west": "library", "north": "cafeteria", "east": "gym", "south": "entrance"},
           "items": [],
       },
       "cafeteria": {
           "description": "It smells of fish fingers and mystery custard.",
           "exits": {"south": "hallway"},
           "items": ["sandwich"],
       },
       "gym": {
           "description": "Climbing ropes hang in the gloom. A lost-property box overflows in the corner.",
           "exits": {"west": "hallway"},
           "items": ["torch"],
       },
       "entrance": {
           "description": "The front entrance. Big glass doors lead outside. A door to the east says OFFICE.",
           "exits": {"north": "hallway", "east": "office"},
           "items": [],
       },
       "office": {
           "description": "Principal Pickles' office. A huge desk, and a framed photo of a prize-winning marrow.",
           "exits": {"west": "entrance"},
           "items": ["key"],
       },
   }

   current = "library"
   inventory = []
   moves = 0

   def show_room():
       room = rooms[current]
       print()
       print(current.upper())
       if current == "office" and "torch" not in inventory:
           print("It's pitch dark. You can't see a thing. You could trip over a marrow.")
       else:
           print(room["description"])
           if room["items"]:
               print("You can see:", ", ".join(room["items"]))
       print("Exits:", ", ".join(room["exits"]))

   print("LOCKED IN AT FUZZLEWOOD")
   print("You wake up in the dark. Everyone has gone home!")
   print("Commands: north/south/east/west, take ..., drop ..., eat ...,")
   print("          inventory, look, quit")
   show_room()

   while True:
       words = input("> ").lower().split()
       if not words:
           continue
       verb = words[0]
       noun = words[-1]
       room = rooms[current]
       moves += 1

       if verb == "quit":
           print("You curl up in a beanbag and wait for morning.")
           break

       elif verb in ["north", "south", "east", "west"]:
           if current == "entrance" and verb == "south":
               if "key" in inventory:
                   print()
                   print("The key turns with a CLUNK. You push the doors open and run")
                   print("out into the cool night air. FREEDOM!")
                   print("High above you, a pair of enormous underpants flaps from")
                   print("the flagpole. But that's a mystery for another day...")
                   print(f"You escaped in {moves} moves. YOU WIN!")
                   break
               else:
                   print("The front doors are locked. You need a key.")
           elif verb in room["exits"]:
               current = room["exits"][verb]
               show_room()
           else:
               print("You can't go that way.")

       elif verb == "look":
           show_room()

       elif verb == "take":
           if current == "office" and "torch" not in inventory:
               print("You fumble around in the dark, but can't find anything.")
           elif noun in room["items"]:
               room["items"].remove(noun)
               inventory.append(noun)
               print(f"You take the {noun}.")
           else:
               print(f"There's no {noun} here.")

       elif verb == "drop":
           if noun in inventory:
               inventory.remove(noun)
               room["items"].append(noun)
               print(f"You drop the {noun}.")
           else:
               print(f"You haven't got a {noun}.")

       elif verb == "eat":
           if noun == "sandwich" and "sandwich" in inventory:
               inventory.remove("sandwich")
               print("Cheese and pickle. Delicious. You feel ready for anything.")
           elif noun in inventory:
               print(f"You can't eat the {noun}!")
           else:
               print(f"You haven't got a {noun}.")

       elif verb in ["inventory", "i"]:
           if inventory:
               print("You are carrying:", ", ".join(inventory))
           else:
               print("You aren't carrying anything.")

       else:
           print("I don't understand that.")
   ```

4. **Walk through the new parts together.** Ask, and find the answer in the
   code:
   - "Where does the game remember what you're carrying?" *(`inventory`.)*
   - "What happens when you `take torch`?" *(It's removed from the room's
     list and added to the inventory.)*
   - "How does the office know whether it's dark?"
   - "What stops you leaving without the key?"
   - "Why `words[-1]` for the noun?" *(So `take the torch` works too: the
     last word is the thing.)*

5. **Solve it.** Play through and escape. Then play again and try to break
   it: drop the torch in the office, try to eat the book, take things that
   aren't there, type nothing at all.

### Session 2 (and 3): make it theirs

6. **Design a new puzzle.** The learner adds at least one more puzzle of
   their own, on paper first. Ideas:
   - The cafeteria is guarded by a grumpy lunch robot that only lets you
     through if you give it the book. (`give book`.)
   - A new room behind a door that needs a password, which is written
     inside the book. (`read book`.)
   - A sleeping caretaker who wakes up if you go into the gym without
     eating the sandwich first (you'd be too noisy with your rumbling
     tummy).

   Each one needs: a new verb or a new room, an `if` that checks something
   in the inventory or the room, and a message for each outcome.

7. **Playtest.** Someone who hasn't seen the code plays the game, while the
   learner watches *without helping*. They write down: where did the player
   get stuck? What did they type that the game didn't understand? Then fix
   the most common problems.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `KeyError: 'items'` | A room is missing its `"items"` list | Every room needs `"items": [...]`, even if it's `[]`. |
| `IndexError: list index out of range` | Pressed Enter with nothing typed | The `if not words: continue` line handles this. Check it's there. |
| `take torch` says "There's no torch here" in the gym | The item is spelled differently in the room's list | Match the spelling exactly, in lower case. |
| You can see the key in the dark office | The darkness check is missing from `show_room`, or the order is wrong | The `if current == "office" and "torch" not in inventory` must come before the description. |
| You can walk south from the entrance without the key | The locked-door check comes *after* the normal exits check | The special case must come first. |
| `UnboundLocalError: cannot access local variable 'current'` | A function tried to *change* `current` | In this program, only the main loop changes `current`. Functions just read it. |

## Talk about it

- What's the game's **state**? What does it need to remember?
  *(Which room you're in, what you're carrying, what's in each room, and
  how many moves.)*
- What makes a good puzzle? What makes a bad one?
- What did your playtester do that you didn't expect?

## Challenge *(if there's time, or for next time)*

- **Save and load** with `json` (Lesson 3.10): `save` writes `current`,
  `inventory` and `rooms` to a file; `load` reads them back.
- Move the room data into a separate file, `rooms.json`, so someone can
  make a whole new adventure without changing any code.
- Add a score: points for each item found, and for escaping in few moves.

## Checkpoint

The learner can, without help:
- [ ] Explain the game's state and where each part is stored
- [ ] Use `split` to turn a command into a verb and a noun
- [ ] Add a new item and a new puzzle that checks the inventory
- [ ] Run a playtest and fix something it found

## Lab notebook

Write the walkthrough: the shortest list of commands that wins. Write
the playtester's notes. Add *state*, *verb*, *noun*, *split* and
*playtest* to the dictionary.

## Guide's background *(optional reading)*

This is the biggest program so far: around 120 lines. It's manageable
because the data (`rooms`) is separate from the logic (the loop), and
because each command is its own `elif` block that can be read on its own.
When the learner adds a feature, they add a block, without touching the
others.

The game's **state** (`current`, `inventory`, the items in each room, and
`moves`) is everything that changes while it runs. Saving a game is just
writing the state to a file. This idea, "a program is state plus rules for
changing it", comes back throughout the course: a CPU's registers in
Stage 6, and a PLC's memory, are the same thing.

**Playtesting** teaches the most important lesson in making software:
users don't do what you expect. Watching silently while someone struggles
with your program is hard, and very valuable.

The `UnboundLocalError` row is there because a learner who tries to move
the movement code into a function will meet it. The fix (passing values in
and returning them, or using `global`) is a good conversation, but it's
fine to keep the movement in the main loop for now.
