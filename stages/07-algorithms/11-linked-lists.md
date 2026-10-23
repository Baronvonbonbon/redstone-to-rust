# Lesson 7.11: Linked Lists: Following Pointers

**Time:** 2–3 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
6 sticky notes or index cards; a few hiding places around the house;
squared paper; the Hack card from Stage 6 · **New words:** class,
object, `self`, node, linked list, head

## Goal *(read this to the learner)*

> A Python list keeps its items side by side, so adding one at the front
> means shuffling everything along. A **linked list** is different: each
> item is a little box that holds a value and the *address of the next
> box*, like a treasure hunt where each clue says where to find the next
> one. To build the boxes, you'll make your own kind of Python thing
> with a **class**. And you'll see that the pointers from your Hack
> computer were linked lists waiting to happen.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Make a treasure hunt: 5 clue cards, each with a Minecraft mob
      name and the hiding place of the next card ("creeper: look under
      the sofa"). The last card says "zombie: THE END". Hide them, and
      keep the first one in your hand.

## Warm-up (5 min)

"Why is `pop(0)` slow on a Python list?" *(Every other item has to
slide along one place.)* "In your Hack computer, what did `A=M` do?"
*(Used the number in memory as the next address: a pointer.)*

## Activity

### Session 1: chains in memory

1. **The treasure hunt.** Give the learner the first card. They follow
   the chain, reading out each mob, until "THE END". **Ask:**
   - "Could you jump straight to the fourth card?" *(No: you have to
     follow the chain from the start.)*
   - "How would you add a new card at the *start* of the hunt?" *(Write
     a new card that points to the old first card, and hand that one
     over instead. Nothing else changes!)*

   **Say:** "That's a **linked list**. Each card is a **node**: a value,
   and where the next node is. The first node is called the **head**.
   The last one points to nothing."

2. **A linked list in RAM.** On squared paper, draw RAM boxes numbered
   100 to 107, like the Hack computer's memory. Each node takes two
   boxes: the value, then the address of the next node (0 means "the
   end").

   | Address | 100 | 101 | 102 | 103 | 104 | 105 | 106 | 107 |
   |---|---|---|---|---|---|---|---|---|
   | Holds | 7 | 104 | 9 | 0 | 3 | 102 | | |

   **Ask:** "The head is at 100. What are the values, in order?" *(7,
   then go to 104: 3, then go to 102: 9, then 0: the end. So 7, 3, 9.)*
   "The nodes aren't in order in memory, but the chain is!"

   **Ask:** "Put 5 at the front, using boxes 106 and 107." *(106 holds 5,
   107 holds 100, and the head is now 106.)*

3. **A class.** **Say:** "Python has no ready-made node, so we'll make
   one. A **class** is a blueprint for a new kind of thing, like a block
   type in Minecraft. Each thing made from it is an **object**, like each
   block you place." New file, `~/lab/algo/linked.py`:
   ```python
   class Node:
       """One link in the chain: a value, and the next Node (or None)."""

       def __init__(self, value, next=None):
           self.value = value
           self.next = next
   ```
   **Say:** "`__init__` (two underscores each side) runs when a new Node
   is made. `self` means 'the node being made'. `self.value = value`
   stores the value *inside* that node. `next=None` means: if you don't
   say what's next, it's `None`: the end."

4. **Make a chain.** In the shell:
   ```
   >>> from linked import Node
   >>> c = Node("skeleton")
   >>> b = Node("zombie", c)
   >>> a = Node("creeper", b)
   >>> a.value
   'creeper'
   >>> a.next.value
   'zombie'
   >>> print(a.next.next.next)
   None
   >>> a
   <linked.Node object at 0x7f...>
   ```
   **Say:** "`a.next` is the zombie node, so `a.next.value` is its value.
   That last line shows a Node's address in memory: Python's pointers
   are real addresses, like the RAM boxes."

   Draw it: three boxes with arrows, `a` pointing at the first.

### Session 2: walking the chain

5. **Length.** **Say:** "To do anything with the whole list, walk along
   it, like the treasure hunt: start at the head, and keep going to
   `next` until you reach `None`." Add to `linked.py`:
   ```python
   def length(head):
       count = 0
       node = head
       while node is not None:
           count = count + 1
           node = node.next
       return count
   ```
   **Say:** "`node = node.next` is the important line: it moves our
   finger to the next card. Without it, we'd count the same card
   forever."

6. **Your turn.** The learner writes three more, in `linked.py`, each a
   walk like `length`:
   - `to_list(head)`: gives back an ordinary Python list of the values.
     *(Start with `result = []`, and `append` each `node.value`.)*
   - `contains(head, value)`: `True` if the value is somewhere in the
     chain. *(Give back `True` as soon as it's found, and `False` after
     the loop.)*
   - `push_front(head, value)`: puts a new node at the front, and gives
     back the new head. *(Remember the treasure hunt: the new card
     points to the old head. It's one line: `return Node(value, head)`.)*

   Then:
   ```
   python3 check.py linked
   ```
   **They should see:** `Node, length, to_list, push_front and contains:
   right every time.` and `ALL GOOD!` Commit.

### Session 3: when linked lists win

7. **Adding at the front.** New file, `~/lab/algo/front.py`:
   ```python
   import time
   from linked import push_front

   n = 100_000

   items = []
   start = time.perf_counter()
   for i in range(n):
       items.insert(0, i)
   print(f"list, insert(0, ...): {time.perf_counter() - start:.3f} seconds")

   head = None
   start = time.perf_counter()
   for i in range(n):
       head = push_front(head, i)
   print(f"linked, push_front:   {time.perf_counter() - start:.3f} seconds")
   ```
   **They should see** something like:
   ```
   list, insert(0, ...): 1.985 seconds
   linked, push_front:   0.068 seconds
   ```
   **Say:** "Adding at the front of a Python list shuffles everything
   along: O(n) each time. For a linked list, it's one new node: O(1)."

8. **Which is better?** Fill in the table together:

   | Job | Python list | Linked list |
   |---|---|---|
   | Get item number 500 | O(1): jump straight there | O(n): walk 500 steps |
   | Add at the front | O(n): shuffle along | O(1): one new node |
   | Add at the end | O(1) | O(n), unless you remember the tail |
   | Find a value | O(n) | O(n) |

   **Say:** "No data structure is best at everything. Choosing the right
   one for the job is a big part of programming."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: that took more than 10 seconds. Is there a loop that never stops?` | A walk is missing `node = node.next`, so it never moves on | Add it as the last line inside the `while`. |
| `NOT YET: push_front should give back the new first Node, but it gave None.` | `push_front` makes the node but doesn't `return` it | `return Node(value, head)`. |
| `AttributeError: 'NoneType' object has no attribute 'next'` | The loop says `while node.next is not None`, and crashes on an empty list | `while node is not None`. |
| `AttributeError: 'Node' object has no attribute 'nxt'. Did you mean: 'next'?` | A spelling mistake | Use the names from `__init__`: `value` and `next`. |
| `TypeError: Node.__init__() missing 1 required positional argument: 'value'` | `Node()` was made with no value | Give it one: `Node("pig")`. |
| `__init__` doesn't seem to run | It's spelled `_init_` or `__init` | Two underscores on each side. |

## Talk about it

- What's in a node? What's the head?
- What does `self` mean inside a class?
- When is a linked list better than a Python list? When is it worse?

## Challenge *(if there's time, or for next time)*

- Write `show(head)`, which prints the chain as
  `creeper -> zombie -> skeleton -> None`.
- Write `reverse(head)`, which reverses the chain by changing the
  arrows, and gives back the new head. Draw the boxes and arrows first!
  *(Walk along, keeping the previous node: point each node back at the
  previous one.)*
- Build a stack from a linked list: push is `push_front`, and pop takes
  the head off. Both are O(1).

## Checkpoint

The learner can, without help:
- [ ] Explain a linked list with the treasure hunt and RAM boxes
- [ ] Write a class with `__init__`, and make objects from it
- [ ] Walk a linked list with `node = node.next`
- [ ] Pass `python3 check.py linked`, and compare lists with linked lists

## Lab notebook

Draw the RAM boxes from step 2, with arrows. Copy the table from
step 8. Commit. Add *class*, *object*, *self*, *node*, *linked list* and
*head* to `dictionary.md`.

## Guide's background *(optional reading)*

A **linked list** stores items in nodes scattered around memory, each
holding a **pointer** (memory address) to the next. It's the simplest
pointer-based data structure, and the classic place where pointer bugs
happen: in C (Stage 8), forgetting to move along, or following a pointer
to memory that's been freed, crashes the program or worse. Rust
(Stage 9) is famous for making linked lists hard to write, precisely
because its rules prevent those bugs.

**Classes** are how Python (and many languages) let programmers define
new types. This lesson uses just enough for data: `__init__` and
attributes. Lesson 7.12 adds **methods**, functions that belong to a
class. Rust uses `struct` and `impl` for the same two ideas.

In practice, Python programmers rarely write linked lists, because
`list` and `deque` cover most needs; but trees (Lesson 7.13) and graphs
(Lesson 7.14) are linked structures, built exactly the same way.
