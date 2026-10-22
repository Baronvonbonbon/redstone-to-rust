# Lesson 4.6: True or False Machines

**Time:** 2 sessions of 40 min · **You need:** Thonny; paper and
coloured pencils; 2 or 3 helpers for the "people gates" game (optional) ·
**New words:** logic gate, input, output, truth table, NOT, AND, OR, XOR

## Goal *(read this to the learner)*

> In rock, paper, scissors you used `and`, `or` and `not` in Python. Deep
> inside the computer, those are real things: tiny machines called
> **logic gates**, made of switches, with wires going in and a wire coming
> out. Every single thing a computer does is built from them. Today you'll
> meet the gates, draw them, *be* them, and make Python print their
> secrets.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Practise drawing the three gate shapes in step 2.

## Warm-up (5 min)

"In rock, paper, scissors, when did the player win?" *(When, for example,
they chose rock **and** the computer chose scissors.)* "What does `and`
need to be true?" *(Both sides.)* "`or`?" *(At least one.)* "`not`?" *(It
flips true and false.)*

## Activity

### Session 1: gates on paper

1. **Ones and zeros are true and false.** **Say:** "In a computer, a wire
   with electricity on it is a **1**, and a wire without is a **0**. We
   can also call them **true** and **false**, or **on** and **off**. They
   all mean the same thing."

2. **Meet the gates.** Draw each gate big, with its **truth table**: a
   list of every possible input and what comes out.

   **NOT** (a triangle with a little circle on its nose). One input, and
   it flips it:

   | in | out |
   |---|---|
   | 0 | 1 |
   | 1 | 0 |

   **AND** (a D shape). Out is 1 only when **both** inputs are 1:

   | a | b | out |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 0 |
   | 1 | 0 | 0 |
   | 1 | 1 | 1 |

   **OR** (a curved shield shape, pointy at the front). Out is 1 when **at
   least one** input is 1:

   | a | b | out |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 1 |
   | 1 | 0 | 1 |
   | 1 | 1 | 1 |

   **Say:** "Inputs go in on the left, the output comes out on the right.
   The little circle always means NOT: flip it."

   (If you're not sure how they look: the Digital simulator in Lesson 4.9
   has pictures of all of them, under **Components → Logic**.)

3. **The people gates game** *(with helpers)*. Each person is a gate.
   Inputs are hands: hand up is 1, down is 0.
   - The AND person puts their hand up only if **both** neighbours have a
     hand up.
   - The OR person puts their hand up if **either** neighbour does.
   - The NOT person does the **opposite** of their one neighbour.

   The guide calls out inputs ("left hand up, right hand down!") and
   everyone checks the output. Then chain two people: the output of the
   AND person is the input of the NOT person. "What does this pair do?"
   *(It's 0 only when both inputs are 1. That's called NAND, and it's
   very important in Lesson 4.9.)*

4. **Gates for real life.** Design these on paper, with gate drawings.
   Write a truth table for each.
   - A **car alarm** goes off when the door is opened **and** the alarm is
     switched on.
   - A **porch light** comes on when someone walks past **and** it's
     **not** daytime. *(Two gates: NOT, then AND.)*
   - A **doorbell** rings if the front button **or** the back button is
     pressed.

### Session 2: gates in Python

5. **Gate functions.** New file, `~/lab/python/binary/gates.py`:
   ```python
   def NOT(a):
       if a == 1:
           return 0
       return 1

   def AND(a, b):
       if a == 1 and b == 1:
           return 1
       return 0

   def OR(a, b):
       if a == 1 or b == 1:
           return 1
       return 0

   def table(name, gate):
       print(name)
       print("a b | out")
       for a in [0, 1]:
           for b in [0, 1]:
               print(a, b, "|", gate(a, b))
       print()

   table("AND", AND)
   table("OR", OR)
   ```
   **They should see:** the AND and OR truth tables, matching the paper.

   **Say:** "Look at `table("AND", AND)`. We're giving the `table`
   function a whole other *function* as its knob! Inside `table`, `gate`
   is the AND function, so `gate(a, b)` calls it. The loop inside a loop
   tries all four combinations."

   Function names are usually lower case. These are in capitals because
   that's how gates are written, and because `and`, `or` and `not` are
   already taken by Python.

6. **The stair-light puzzle.** **Say:** "At the bottom of the stairs there's
   a light switch, and there's another at the top. Flicking *either* switch
   changes the light. If both switches are down, the light is off. What's
   the truth table?" Work it out together:

   | bottom | top | light |
   |---|---|---|
   | 0 | 0 | 0 |
   | 0 | 1 | 1 |
   | 1 | 0 | 1 |
   | 1 | 1 | 0 |

   **Say:** "This is the light being on when **exactly one** switch is up.
   It's called **XOR**, 'exclusive or': one or the other, but not both.
   Can you build it from AND, OR and NOT?" Give time to try on paper.
   *(One answer: "a OR b, AND NOT (a AND b)".)*

   Add it to `gates.py`, above the `table` lines:
   ```python
   def XOR(a, b):
       return AND(OR(a, b), NOT(AND(a, b)))
   ```
   and add `table("XOR", XOR)` at the end. **They should see:** 0, 1, 1, 0.

   **Say:** "XOR is made of **four** smaller gates, and we didn't need any
   new `if`s: it's just gates plugged into gates. That's how the whole
   computer is built."

7. **Python's secret gates.** In the Shell:
   ```python
   1 & 1
   1 & 0
   1 | 0
   1 ^ 1
   ```
   **They should see:** `1`, `0`, `1`, `0`. **Say:** "`&` is AND, `|` is OR
   and `^` is XOR, for bits. Remember in Lesson 4.2 when `2 ^ 4` gave 6?
   Now you can see why: `010` XOR `100` is `110`." Check: `bin(2 ^ 4)`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `SyntaxError: invalid syntax` on `def and(a, b):` | `and` is a Python word and can't be a function name | Use capitals: `AND`. |
| `TypeError: AND() missing 1 required positional argument: 'b'` | Only one input was given to a two-input gate | AND, OR and XOR need two: `AND(1, 0)`. |
| `TypeError: 'NoneType' object...` or `None` in the table | A path through the function doesn't `return` | Check each gate ends with `return 0` or `return 1`. |
| `table("AND", AND())` gives a `TypeError` | The brackets call the function instead of handing it over | Pass the name without brackets: `table("AND", AND)`. |
| The XOR table is wrong | The gates are plugged in the wrong order | Read it from the inside out: `AND(a, b)`, then `NOT` of that, then AND with `OR(a, b)`. |

## Talk about it

- What's the only input pattern that makes AND give 1? And OR give 0?
- What does the little circle on a gate drawing mean?
- Where else might XOR be useful? *(Anything that should happen when two
  things are different: "are these two bits different?")*

## Challenge *(if there's time, or for next time)*

- Write `NAND(a, b)`, which is NOT of AND, and `NOR(a, b)`. Print their
  tables.
- Write `MAJORITY(a, b, c)`, which is 1 when at least two of the three
  inputs are 1 (a voting machine!). Change `table` to make a three-input
  version with three loops.
- **For the guide:** if you have a battery, a bulb or LED (with its
  resistor) and two switches, wire the switches one after the other
  (in **series**): that's AND. Side by side (in **parallel**): that's OR.

## Checkpoint

The learner can, without help:
- [ ] Draw NOT, AND and OR, with their truth tables
- [ ] Explain what XOR does, and build it from the other gates
- [ ] Write gate functions in Python and print a truth table with two loops
- [ ] Design a gate circuit for a real-life rule

## Lab notebook

Draw each gate and its truth table, in colour. Draw the porch-light
circuit. Add *logic gate*, *truth table*, *NOT*, *AND*, *OR* and *XOR* to
the dictionary.

## Guide's background *(optional reading)*

This is **Boolean logic**, invented by George Boole in the 1850s, long
before computers. In 1937, Claude Shannon showed that circuits of
switches could do Boolean logic, which is the idea every digital
computer is built on. A logic gate is a tiny circuit (today, a few
transistors) that computes one of these functions.

If you work with PLCs or relay panels, you already know this lesson in
another form: contacts in series are AND, contacts in parallel are OR,
and a normally closed contact is NOT. Lesson 4.13 makes that link
explicitly, with ladder logic.

Passing a function to another function (`table("AND", AND)`) is a small
but powerful idea: functions are values, just like numbers. It doesn't
need more explanation than "the function goes in the box".

`&`, `|` and `^` are *bitwise* operators: they work on every bit of a
number at once. Python's `and`, `or` and `not` are slightly different
(they work on whole true/false values), but for single bits they agree.
