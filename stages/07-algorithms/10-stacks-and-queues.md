# Lesson 7.10: Stacks and Queues

**Time:** 2 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
a pile of plates, books or blocks; a few toys to stand in a line ·
**New words:** data structure, stack, push, pop, queue, LIFO, FIFO

## Goal *(read this to the learner)*

> The way you store things changes what's quick to do with them. A
> **data structure** is a way of arranging data. Today, two simple ones
> that are everywhere. A **stack** is like a pile of plates: you add and
> take from the top. A **queue** is like a line at a shop: you join at
> the back and leave from the front. You'll make an undo button, a
> bracket checker that Thonny itself would be proud of, and find out why
> one kind of queue is a hundred times faster than another.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"In Lesson 7.5, what was the pile of function calls waiting to finish
called?" *(The call stack.)* "Which call finished first: the first one
made, or the last?" *(The last one made.)*

## Activity

### Session 1: stacks

1. **A pile of plates.** Make a pile of plates or books. **Say:** "You
   can only add to the top, which is called **push**, or take from the
   top, which is called **pop**. That's a **stack**." Push three, pop one,
   push two more, pop them all, saying each name.

   **Ask:** "Which comes off first: the first one in, or the last one
   in?" *(The last one in.)* **Say:** "Last In, First Out: **LIFO**. The
   call stack works this way: the last call made is the first to
   finish."

2. **A Python list is a stack.** **Say:** "`append` pushes onto the end,
   and `pop()` takes off the end and gives it back." New file,
   `~/lab/algo/undo.py`:
   ```python
   placed = []

   while True:
       command = input("Place a block (or 'undo', or 'quit'): ")
       if command == "quit":
           break
       elif command == "undo":
           if placed == []:
               print("Nothing to undo!")
           else:
               block = placed.pop()
               print(f"Took back the {block}.")
       else:
           placed.append(command)
       print("Built so far:", placed)
   ```
   Run it. Type `stone`, `glass`, `tnt`, then `undo` twice. **They should
   see:** `Took back the tnt.`, then `Took back the glass.`, and
   `Built so far: ['stone']`. **Say:** "Every undo button in every program
   is a stack of things you did."

3. **The bracket problem.** **Say:** "In Python, every `(` needs a `)`,
   every `[` a `]`, and every `{` a `}`, in the right order." Write these
   on paper, and decide together which are OK:
   - `print(len([1, 2]))` *(OK)*
   - `print(len([1, 2])` *(not OK: a `(` never closes)*
   - `([)]` *(not OK: the `[` must close before the `)`)*
   - `{[()()]}` *(OK)*

   **Ask:** "When you get to a closing bracket, which opening bracket
   must it match?" *(The most recent one that's still open.)* **Say:**
   "Most recent: last in, first out. A stack!"

4. **The bracket checker.** With the pile of plates: go along
   `{[()()]}` one bracket at a time. Opening bracket: push a plate with
   it written on a sticky note. Closing bracket: pop the top plate; it
   must be the partner. At the end, the pile must be empty.

   New file, `~/lab/algo/stacks.py`:
   ```python
   def brackets_ok(text):
       """True if every bracket is closed, in the right order."""
       partner = {")": "(", "]": "[", "}": "{"}
       stack = []
       for ch in text:
           if ch in "([{":
               stack.append(ch)
           elif ch in ")]}":
               if stack == []:
                   return False
               if stack.pop() != partner[ch]:
                   return False
       return stack == []
   ```
   **Say:** "`partner` is a dictionary from each closing bracket to its
   opening one. There are three ways to fail: a closing bracket with
   nothing open; a closing bracket that doesn't match the top; and
   brackets still open at the end." Then:
   ```
   python3 check.py brackets
   ```
   **They should see:** `brackets_ok: right every time.` and `ALL GOOD!`
   Commit.

### Session 2: queues

5. **A line.** Stand three toys in a line for a villager's trades.
   **Say:** "New toys join at the back. The villager serves the front.
   That's a **queue**: First In, First Out, or **FIFO**." Act it out:
   join, join, serve, join, serve, serve.

   **Ask:** "Where do queues happen in a computer?" *(Keys you type wait
   in a queue until the program reads them; songs in a playlist;
   documents waiting for the printer; messages on a network.)*

6. **A queue in Python.** **Say:** "A list *can* be a queue: `append` to
   join, and `pop(0)` to take from the front. But watch this." New file,
   `~/lab/algo/lines.py`:
   ```python
   import time
   from collections import deque

   n = 100_000

   queue = list(range(n))
   start = time.perf_counter()
   while queue != []:
       queue.pop(0)
   print(f"list, pop(0):     {time.perf_counter() - start:.3f} seconds")

   queue = deque(range(n))
   start = time.perf_counter()
   while len(queue) > 0:
       queue.popleft()
   print(f"deque, popleft(): {time.perf_counter() - start:.3f} seconds")
   ```
   **They should see** something like:
   ```
   list, pop(0):     1.867 seconds
   deque, popleft(): 0.014 seconds
   ```
   **Say:** "Over a hundred times faster! A list keeps its items side by
   side in memory, like the RAM in your Hack computer. Taking the first
   one means sliding *every other item* one place left: O(n) each time.
   A **deque** (say 'deck': a double-ended queue) is built so both ends
   are quick: O(1)."

7. **Using a deque.** In the shell:
   ```
   >>> from collections import deque
   >>> line = deque()
   >>> line.append("Alex")
   >>> line.append("Sam")
   >>> line.append("Steve")
   >>> line.popleft()
   'Alex'
   >>> line
   deque(['Sam', 'Steve'])
   ```
   **Say:** "Remember `deque`: Lesson 7.14 uses one to explore a maze."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: brackets_ok('(') gave True, but it should be False.` | The last line is `return True`, so brackets left open don't count | `return stack == []`: only OK if nothing's still open. |
| `IndexError: pop from empty list` | A closing bracket came with nothing open, and the code popped anyway | Check `if stack == []: return False` *before* popping. |
| `NOT YET: brackets_ok('(]') gave True, but it should be False.` | Closing brackets aren't checked against their partner | Compare what `pop()` gives with `partner[ch]`. |
| `KeyError: '('` | `partner` was looked up with an opening bracket | Only look up `partner[ch]` when `ch` is a *closing* bracket. |
| `lines.py` takes ages | `n` is bigger than 100,000 | Use the lesson's number: `pop(0)` gets slow fast. |

## Talk about it

- What's the difference between a stack and a queue? LIFO and FIFO?
- Why is a stack the right tool for checking brackets?
- Why is `pop(0)` on a list slow, but `popleft()` on a deque fast?

## Challenge *(if there's time, or for next time)*

- Add **redo** to `undo.py`: a second stack. Undo pushes the block onto
  it; redo pops it back. (What should happen to the redo stack when a
  new block is placed? Try it in a drawing program to find out.)
- Make the bracket checker say *where* the problem is: the position of
  the bad bracket.
- Reverse a word with a stack: push every letter, then pop them all.

## Checkpoint

The learner can, without help:
- [ ] Explain stacks (LIFO) and queues (FIFO), with real examples
- [ ] Use a list as a stack, with `append` and `pop`
- [ ] Write `brackets_ok` and pass `python3 check.py brackets`
- [ ] Use a `deque` as a queue, and explain why it beats a list

## Lab notebook

Draw the plates for `{[()()]}`, after each bracket. Write the race
times. Commit. Add *data structure*, *stack*, *push*, *pop*, *queue*,
*LIFO* and *FIFO* to `dictionary.md`.

## Guide's background *(optional reading)*

Stacks and queues are the simplest **abstract data types**: they're
defined by what you can do (push and pop, or join and leave), not by how
they're stored. The same stack can be built on a list, a linked list
(Lesson 7.11) or an array in a computer's RAM.

Stacks are everywhere in computing: the call stack, undo, the back
button in a browser, and checking brackets in compilers. In Stage 8 the
learner builds a **stack machine**, the Nand to Tetris virtual machine,
where every calculation pushes and pops: `push 2`, `push 3`, `add`
leaves 5 on the stack. Queues are just as common: in operating systems
(Stage 10), processes wait in queues for the CPU, and in networks
(Stage 11), packets wait in queues at every router.

A Python list is a **dynamic array**: items sit side by side in memory,
so reaching any item by position is O(1), but inserting or removing at
the front is O(n). `collections.deque` is built from linked blocks, so
both ends are O(1).
