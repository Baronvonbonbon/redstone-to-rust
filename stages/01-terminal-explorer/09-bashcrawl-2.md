# Lesson 1.9: Bashcrawl, Part 2

**Time:** 45 min (or two sessions) · **New words:** variable, source code

## Goal *(read this to the learner)*

> Back to the dungeon! Find the hidden rooms, collect the treasure, and
> reach the deepest parts of the catacombs. Then peek behind the curtain
> and see how the game works.

## Before the lesson *(guide, 2 min)*

- [ ] Find where they stopped last time, in the lab notebook.

## Warm-up (5 min)

"Look at your dungeon map. What's the command to see hidden rooms? To use
an item?"

## Activity

1. **Back in.** Open a terminal. `cd` to the room they reached last time
   (Tab completion helps!), and `cat scroll` again to remember.
   If the alias is gone (it is, in a new terminal), set it again:
   `alias ls='ls -F'`.

2. **Explore for 25 to 30 minutes.** Use the same guide approach as last
   time: ask, don't tell. Remind them to check **every** room with `ls -a`.

3. **Behind the curtain.** When they've explored enough, open an item's
   code on purpose:
   ```
   cat treasure
   ```
   (Do it in a room that has a treasure.) **Say:** "This is the program's
   **source code**. It's just text! Lines starting with `#` are notes for
   humans, called comments. Can you find where it says what you picked up?"

   Look for words with a dollar sign, like `$I`: "Words with `$` are
   **variables**: labelled boxes that hold a value. Bashcrawl keeps your
   whole inventory in a variable called `I`."
   ```
   echo $I
   ```
   Also look for lines like `mv ../.chapel ../chapel`. **Ask:** "What does
   that do?" *(It renames a hidden room so it isn't hidden any more. That's
   how finding treasure opens up new rooms!)*

4. **Wrap up.** Finish the main quest, or decide that the dungeon map is
   good enough. Either way is fine. Bashcrawl can stay as free play.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `echo $I` prints nothing | The inventory is empty in *this* terminal | The scrolls show how to add treasure with `export I=...`. A new terminal starts with an empty inventory. |
| They're stuck on a puzzle | | Read the scroll in that room again; try `ls -a`; read the code of nearby items. |
| They're bored | | Stop. Move on to Lesson 1.10, and leave bashcrawl for free play. |

## Talk about it

- What's source code? *(The text a program is made from.)*
- What's a variable? *(A labelled box that holds a value.)*
- If you could add a room to the dungeon, what would it be?

## Challenge

**Add your own room** to *your copy* of the dungeon:
```
mkdir ~/bashcrawl/entrance/dragon-lair
nano ~/bashcrawl/entrance/dragon-lair/scroll
```
Write a scroll for it. Can your guide find it and read it?

## Checkpoint

The learner can, without help:
- [ ] Find a hidden room on their own
- [ ] Open an item with `cat`, and point out one comment and one variable

## Lab notebook

Finish the dungeon map. Write: "**Source code** is the text a program is
made of. A **variable** holds a value, like my inventory, `$I`."

## Guide's background *(optional reading)*

The "aha" here, that programs are just text files someone wrote, is a big
one. Your learner will write their first programs in Stage 2 (Python),
and their first shell scripts like these in Stage 5.
