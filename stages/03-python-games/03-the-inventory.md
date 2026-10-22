# Lesson 3.3: The Inventory

**Time:** 45 min · **You need:** Thonny; a few small objects and a tray, or
a drawn row of inventory slots · **New words:** list, item, append, index

## Goal *(read this to the learner)*

> In Minecraft, your inventory holds lots of things in one place. Python
> has the same thing: a **list**. Today you'll learn to put things in a
> list, take them out, look for them, and count them, and you'll build an
> inventory program you can type commands into.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Put 3 or 4 small objects in a row on a tray (a pencil, a coin, a
      rubber...), and stick a number under each: 0, 1, 2, 3.

## Warm-up (5 min)

"In `name = "Steve"`, what's `name[0]`? And `name[-1]`?" *('S' and 'e'.)*
"Lists work the same way, but each slot holds a whole thing, not one
letter." Point at the tray: "What's in slot 0? Slot 2?"

## Activity

1. **Make a list.** In the Shell:
   ```python
   inventory = ["pickaxe", "torch", "bread"]
   inventory
   inventory[0]
   inventory[-1]
   len(inventory)
   ```
   **Say:** "Square brackets, with commas between the items. Slots are
   numbered from 0, just like letters in a string."

2. **Change it.**
   ```python
   inventory.append("diamond")
   inventory
   inventory.remove("bread")
   inventory
   inventory[0] = "golden pickaxe"
   inventory
   ```
   **Say:** "`append` adds to the end. `remove` takes out the first one
   that matches. And you can swap what's in a slot by putting something
   new in it, like with a variable." Do the same with the objects on the
   tray as you go.

3. **Ask questions about it.**
   ```python
   "torch" in inventory
   "elytra" in inventory
   inventory.count("torch")
   sorted(inventory)
   ```

4. **Loop through a list.**
   ```python
   for item in inventory:
       print(f"- {item}")
   ```
   **Say:** "This is the `for` loop again, but instead of counting, it
   goes through the list one item at a time. Each time round, `item`
   holds the next thing. Remember `range(4)`? That was a list of numbers
   all along, more or less."

5. **Lists of numbers.**
   ```python
   scores = [12, 7, 30, 4, 18]
   sum(scores)
   max(scores)
   min(scores)
   sum(scores) / len(scores)
   ```
   **Say:** "The last one is the **average**: add them all up, and share
   the total out equally."

6. **The inventory program.** New file, `~/lab/python/stage3/inventory.py`:
   ```python
   inventory = ["pickaxe", "torch", "bread"]

   print("INVENTORY. Commands: list, add, drop, quit")

   while True:
       command = input("> ").lower()

       if command == "quit":
           break
       elif command == "list":
           print(f"You are carrying {len(inventory)} things:")
           for item in sorted(inventory):
               print(f"  - {item}")
       elif command == "add":
           item = input("Add what? ")
           inventory.append(item)
           print(f"Added {item}.")
       elif command == "drop":
           item = input("Drop what? ")
           if item in inventory:
               inventory.remove(item)
               print(f"Dropped {item}.")
           else:
               print(f"You don't have any {item}!")
       else:
           print("I don't know that command.")

   print("Goodbye!")
   ```
   **Say:** "Look how this uses last lesson's `while True` menu, with a list
   inside it. And look at `drop`: before removing something, we check it's
   really there. Why?" *(Because `remove` gives an error if it isn't.)*

   Let them play, and then add a new command: `count`, which asks for an
   item and says how many there are.

7. **Watch the list.** Run it again with **View → Variables** open. Add
   and drop things, and watch the list change in the Variables panel.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ValueError: list.remove(x): x not in list` | Removing something that isn't there | Check with `if item in inventory:` first. |
| `IndexError: list index out of range` | Asked for a slot number past the end | The last slot is `len(inventory) - 1`, or use `[-1]`. |
| `NameError: name 'torch' is not defined` | The quote marks around an item are missing | `"torch"`, in quotes. |
| `SyntaxError: invalid syntax. Perhaps you forgot a comma?` | A missing comma between items | `["a", "b", "c"]`: commas between every item. |
| `None` is printed after `.sort()` | `inventory.sort()` sorts the list itself and gives back nothing | Use `sorted(inventory)` to get a sorted copy, or call `inventory.sort()` on its own line. |
| Dropping `Torch` doesn't work | Capitals don't match | Use `.lower()` on what's typed, and keep items in lower case. |

## Talk about it

- What's a list? How do you get the first item? The last?
- What's the difference between `for i in range(5)` and
  `for item in inventory`? *(One goes through numbers, the other through
  the items in a list.)*
- Why do we check `if item in inventory` before removing?

## Challenge *(if there's time, or for next time)*

- A `craft` command: if the inventory has `"stick"` and `"diamond"`,
  remove them both and add `"diamond sword"`.
- Limit the inventory to 9 slots, like a Minecraft hotbar.
- Make a list of 10 random numbers from 1 to 6
  (`rolls.append(random.randint(1, 6))` in a loop), then print the
  biggest, smallest and average.
- Lists can hold lists: `grid = [[1, 2, 3], [4, 5, 6]]`. What's
  `grid[1][0]`? *(4.)*

## Checkpoint

The learner can, without help:
- [ ] Make a list, and get items out by index (including `-1`)
- [ ] Use `append`, `remove`, `in` and `len`
- [ ] Loop through a list with `for item in ...`
- [ ] Use `sum`, `max` and `min` on a list of numbers

## Lab notebook

Draw an inventory as a row of slots numbered from 0. Write the list
commands with an example of each. Add *list*, *item*, *append* and
*average* to the dictionary.

## Guide's background *(optional reading)*

Lists are the most-used way to store a collection of things in Python.
Other languages call them **arrays** (Rust has both arrays and "vectors",
which are like Python lists). Almost every program keeps lists of
something: players, messages, files, high scores.

One subtle point you may run into: some methods change a list *in place*
and give back nothing (`inventory.sort()`, `inventory.append(...)`),
while some functions give back a *new* list and leave the old one alone
(`sorted(inventory)`). Writing `inventory = inventory.sort()` is a classic
mistake that leaves `inventory` holding `None` (Python's "nothing").
