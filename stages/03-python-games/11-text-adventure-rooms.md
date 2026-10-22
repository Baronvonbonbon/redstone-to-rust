# Lesson 3.11: Text Adventure, Part 1: Rooms

**Time:** 2 sessions of 45 min · **You need:** Thonny; squared paper ·
**New words:** text adventure, data structure, game loop, nested

## Goal *(read this to the learner)*

> Before games had pictures, they had words. You typed `go north`, and the
> game told you what you saw. Today you'll play the very first one, from
> the 1970s, and then start building your own: **Locked In at
> Fuzzlewood**, set in the same school as the Great Underpants Heist.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Try `adventure` in a terminal yourself for a couple of minutes, so
      you know what it looks like. (It asks "Would you like
      instructions?" Answer `no`. To stop, type `quit`, then `yes`.)
- [ ] Make a folder: `mkdir -p ~/lab/python/adventure`

## Warm-up (10 min): the first adventure

In a terminal:
```
adventure
```
Answer `no` to the instructions. Then try commands like `east`, `enter
building`, `take lamp`, `look`, `inventory`. Most commands are one or two
words. Play for about 10 minutes, then type `quit` and answer `yes`.

**Say:** "This game is called *Colossal Cave Adventure*. It was written in
1976, and every adventure game since, and even the idea of exploring
caves in Minecraft, owes something to it. It's made of only two things:
**rooms** joined by directions, and **things** you can pick up. Let's
build that."

## Activity

### Session 1: the map

1. **Draw the map.** On squared paper, draw these places as boxes, with
   lines between the ones that connect, and the direction on each line:

   ```
                 [cafeteria]
                      |
   [library] ---- [hallway] ---- [gym]
                      |
                 [entrance] ---- [office]
                      |
               (the front door: locked!)
   ```

   **Say:** "The story: you fell asleep in the library during reading time.
   When you woke up, it was dark, and everyone had gone home. You need to
   get out of Fuzzlewood Elementary."

2. **Rooms as a dictionary.** **Say:** "Each room needs a description, and
   a list of exits: which direction leads to which room. That's a
   dictionary, *inside* a dictionary." New file,
   `~/lab/python/adventure/fuzzlewood.py`:
   ```python
   rooms = {
       "library": {
           "description": "Rows of books loom in the dark. You must have fallen asleep in the beanbag.",
           "exits": {"east": "hallway"},
       },
       "hallway": {
           "description": "A long hallway lined with coat pegs. Somebody has left a single sock.",
           "exits": {"west": "library", "north": "cafeteria", "east": "gym", "south": "entrance"},
       },
       "cafeteria": {
           "description": "It smells of fish fingers and mystery custard.",
           "exits": {"south": "hallway"},
       },
       "gym": {
           "description": "Climbing ropes hang in the gloom. A lost-property box overflows in the corner.",
           "exits": {"west": "hallway"},
       },
       "entrance": {
           "description": "The front entrance. Big glass doors lead outside. A door to the east says OFFICE.",
           "exits": {"north": "hallway", "east": "office"},
       },
       "office": {
           "description": "Principal Pickles' office. A huge desk, and a framed photo of a prize-winning marrow.",
           "exits": {"west": "entrance"},
       },
   }
   ```
   **Say:** "`rooms["hallway"]` is the hallway's own little dictionary.
   `rooms["hallway"]["exits"]` is its exits. And
   `rooms["hallway"]["exits"]["north"]` is `"cafeteria"`. Dictionaries
   inside dictionaries are called **nested**." Try those in the Shell after
   running the file.

   Check it against the paper map: every line on the map needs an exit in
   *both* rooms (east from the library, *and* west from the hallway).

### Session 2: the game loop

3. **Walking around.** Add below the rooms:
   ```python
   current = "library"

   print("LOCKED IN AT FUZZLEWOOD")
   print("You wake up in the dark. Everyone has gone home!")
   print("Type north, south, east or west to move, or quit to give up.")

   while True:
       room = rooms[current]
       print()
       print(current.upper())
       print(room["description"])
       print("Exits:", ", ".join(room["exits"]))

       command = input("> ").lower().strip()

       if command == "quit":
           print("You curl up in a beanbag and wait for morning.")
           break
       elif command in room["exits"]:
           current = room["exits"][command]
       elif command in ["north", "south", "east", "west"]:
           print("You can't go that way.")
       else:
           print("I don't understand that.")
   ```
   **Say:** "This is the **game loop**: show where you are, ask what to
   do, change things, and go round again. `current` holds the name of the
   room you're in. Moving is just putting a new room's name in that box!
   And `", ".join(...)` sticks a list of words together, with a comma
   between each."

4. **Test the map.** Walk to every room and back. Check every exit on the
   paper map works, in both directions. Try walking into walls, and typing
   nonsense.

5. **Make it theirs.** Rewrite the descriptions in their own words (silly
   is good). Add at least one new room of their own: the music room, the
   caretaker's cupboard, the playground... Remember: it needs exits both
   ways, and it must go on the paper map too.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `KeyError: 'cafetería'` (or another room name) | An exit leads to a room name that isn't in `rooms`, maybe a spelling mistake | Every exit's room name must exactly match a key in `rooms`. |
| You can go somewhere but not get back | The exit only exists in one direction | Add the return exit to the other room. |
| `SyntaxError` somewhere in the rooms | A missing comma, colon, quote, or bracket | Each room ends with `},`. Check the line *before* the one in the error too. |
| `KeyError: 'description'` | A room is missing its description, or it's spelled differently | Every room needs exactly `"description"` and `"exits"`. |
| `n` doesn't work for north | Only full words are understood | That's in the challenge! |

## Talk about it

- How does the game know which room you're in? *(The `current` variable
  holds the room's name.)*
- What's the game loop? Name its steps.
- Why is the map a dictionary of dictionaries?

## Challenge *(if there's time, or for next time)*

- Understand `n`, `s`, `e` and `w`, and `go north`. *(Hint: a dictionary
  `shortcuts = {"n": "north", ...}`, and `command.split()` turns
  `"go north"` into `["go", "north"]`.)*
- Add `up` and `down` exits: a staircase to a second floor, or a hatch to
  the boiler room.
- Count the moves, and print the total when the player quits.

## Checkpoint

The learner can, without help:
- [ ] Draw the map, and point to where each room and exit is in the code
- [ ] Add a new room with exits both ways
- [ ] Explain the game loop

## Lab notebook

Glue in the map. Write the steps of the game loop. Add *text adventure*,
*game loop* and *nested* to the dictionary.

## Guide's background *(optional reading)*

The big idea of this lesson is separating **data** from **code**. The whole
school is described in the `rooms` dictionary (the data), and a short
loop (the code) works for any map at all. To add a room, you don't change
the loop; you only add data. Professional game developers work this way:
levels, maps and items are data files, and the game engine reads them.

*Colossal Cave Adventure* was written by Will Crowther in 1976, partly
based on a real cave system in Kentucky, and expanded by Don Woods. The
`adventure` in bsdgames is a version of the original.

Part 2 adds things to pick up, a dark room and a locked door, which turns
the map into a puzzle.
