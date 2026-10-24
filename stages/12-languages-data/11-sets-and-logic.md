# Lesson 12.11: Sets and Logic

**Time:** 2 sessions of 45 min · **You need:** a terminal;
`~/lab/lang/python`; `~/lab/sql/minecraft.db` (Lesson 5.14); paper,
two hoops or loops of string, mob cards (write mob names on index cards)
· **New words:** set, element, union, intersection, difference, subset,
Venn diagram, truth table, De Morgan's law

## Goal *(read this to the learner)*

> The second half of this stage is about data: how to keep it, and
> how to ask questions about it. Underneath every database are two bits
> of mathematics: sets (collections of things) and logic (true and
> false, `and`, `or`, `not`). Today you'll sort mobs into hoops, prove
> a law of logic with every possible case, and ask a database
> questions with set operations.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Mob cards: creeper, zombie, skeleton, spider, ghast, blaze, piglin,
      wither, bee, parrot, pig, cow.
- [ ] `ls ~/lab/sql/minecraft.db` exists. If not, as the learner:
      `cd ~/lab/sql && sqlite3 minecraft.db < minecraft.sql` (the `sql`
      lab from Stage 5).

## Warm-up (5 min)

"In Pickaxe, what does `true and false` give? `true or false`? `!true`?"
*(false, true, false.)* "Which logic gates were those, in Stage 4?"
*(AND, OR, NOT.)*

## Activity

### Session 1: sets

1. **Hoops.** Lay out two overlapping hoops: one labelled **hostile**,
   one **nether**. The learner places each mob card. **Ask:** "Where do
   ghast and blaze go?" *(In the overlap: both hostile and in the
   nether.)* "Where do pig and cow go?" *(Outside both.)* **Say:** "Each
   hoop is a **set**: a collection where each thing is in or out, with
   no order and no repeats. The things are its **elements**. This
   picture is a **Venn diagram**." Point to the regions:
   - Everything in either hoop: the **union** (`or`).
   - Just the overlap: the **intersection** (`and`).
   - Hostile, but not in the nether part: the **difference**.

2. **Sets in Python.** In `~/lab/lang/python`, make `sets.py`:
   ```python
   hostile = {"zombie", "skeleton", "creeper", "spider", "ghast", "blaze"}
   nether = {"ghast", "blaze", "piglin", "wither"}
   flying = {"ghast", "blaze", "bee", "parrot"}

   print("hostile or nether:", sorted(hostile | nether))
   print("hostile and nether:", sorted(hostile & nether))
   print("hostile, not nether:", sorted(hostile - nether))
   print("Is a creeper hostile?", "creeper" in hostile)
   print("How many hostile?", len(hostile))
   print("Hostile, in the nether, and flying:", sorted(hostile & nether & flying))
   ```
   `python3 sets.py`. **They should see:**
   ```
   hostile or nether: ['blaze', 'creeper', 'ghast', 'piglin', 'skeleton', 'spider', 'wither', 'zombie']
   hostile and nether: ['blaze', 'ghast']
   hostile, not nether: ['creeper', 'skeleton', 'spider', 'zombie']
   Is a creeper hostile? True
   How many hostile? 6
   Hostile, in the nether, and flying: ['blaze', 'ghast']
   ```
   Check each against the hoops. **Say:** "`|` is union, `&` is
   intersection, `-` is difference. `sorted` puts them in order to
   print, because a set has no order of its own." Try `print(hostile)`
   two or three times, running the program each time. **Ask:** "Why
   does the order change?" *(Python mixes up its hashes every time it
   starts: Lesson 7.12! A set is a hash table with only keys.)*

3. **No repeats.** In `python3`:
   ```python
   set("BANANA")
   sorted(set("MISSISSIPPI"))
   {"a", "b"} <= {"a", "b", "c"}
   {2, 4, 6} == {6, 4, 2}
   ```
   **They should see** `{'B', 'A', 'N'}` (in some order), `['I', 'M',
   'P', 'S']`, `True`, `True`. **Say:** "Repeats vanish. `<=` asks 'is
   every element of this one also in that one?': a **subset**. Two sets
   are equal if they have the same elements, in any order."

### Session 2: logic

4. **Truth tables.** On paper, a table with every possible case of `a`
   and `b`:

   | a | b | a and b | a or b | not a |
   |---|---|---|---|---|
   | false | false | false | false | true |
   | false | true | false | true | true |
   | true | false | false | true | false |
   | true | true | true | true | false |

   **Say:** "This is a **truth table**, like the gate tables from Stage
   4. Two inputs, so four rows: every possible case."

5. **A law, proved by every case.** **Ask:** "Is `not (a and b)` the
   same as `(not a) or (not b)`?" Guess, then test every row. Make
   `truth.py`:
   ```python
   # Every row of the truth table: is De Morgan's rule always right?
   for a in [False, True]:
       for b in [False, True]:
           left = not (a and b)
           right = (not a) or (not b)
           print(f"a={a!s:5}  b={b!s:5}  not (a and b)={left!s:5}  (not a) or (not b)={right!s:5}")
   ```
   **They should see:**
   ```
   a=False  b=False  not (a and b)=True   (not a) or (not b)=True
   a=False  b=True   not (a and b)=True   (not a) or (not b)=True
   a=True   b=False  not (a and b)=True   (not a) or (not b)=True
   a=True   b=True   not (a and b)=False  (not a) or (not b)=False
   ```
   **Say:** "The same in every row, and there are no other rows. So it's
   always true: a proof by checking every case. It's called **De
   Morgan's law**. In words: 'not (hostile and nether)' means 'not
   hostile, or not in the nether'." *(`!s:5` makes each word 5 letters
   wide, so the columns line up.)* **Ask:** "What would the other law
   be, swapping `and` and `or`?" *(`not (a or b)` is `(not a) and (not
   b)`. Change `truth.py` to check it.)* In Stage 4, this law meant a
   NAND gate is an OR gate with NOT on its inputs.

6. **Sets and logic in SQL.** **Say:** "A database table is a set of
   rows. SQL can do set operations too." In `~/lab/sql`:
   ```
   sqlite3 -box minecraft.db
   ```
   ```sql
   SELECT name FROM mobs WHERE behaviour = 'hostile'
   INTERSECT
   SELECT name FROM mobs WHERE dimension = 'nether';
   ```
   **They should see:**
   ```
   ┌───────┐
   │ name  │
   ├───────┤
   │ blaze │
   │ ghast │
   └───────┘
   ```
   Then `EXCEPT` (difference) and `UNION`:
   ```sql
   SELECT name FROM mobs WHERE dimension = 'nether'
   EXCEPT
   SELECT name FROM mobs WHERE behaviour = 'hostile';
   SELECT name FROM mobs WHERE behaviour = 'boss'
   UNION
   SELECT name FROM mobs WHERE dimension = 'end';
   ```
   **They should see** `piglin` and `wither`; then `ender dragon`,
   `enderman` and `wither`. **Ask:** "How could you get the
   `INTERSECT` answer with one `SELECT`?" *(`WHERE behaviour = 'hostile'
   AND dimension = 'nether'`: intersection is `and`.)* Try one with
   `NOT` and `OR`:
   ```sql
   SELECT name FROM mobs WHERE NOT (behaviour = 'passive' OR legs = 4);
   ```
   **They should see** 12 mobs, starting `bee`, `iron golem`, `enderman`.
   **Ask:** "Use De Morgan: how else could you write that `WHERE`?"
   *(`behaviour != 'passive' AND legs != 4`. Try it: the same 12.)*
   `.quit` to leave. Commit the Python files.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `TypeError: unsupported operand type(s) for \|: 'list' and 'set'` | One of them was made with `[ ]` (a list), not `{ }` | Sets use curly brackets. |
| `{}` makes a dictionary, not an empty set | Python's `{}` was taken by dictionaries first | An empty set is `set()`. |
| `Parse error: no such table: mobs` | `sqlite3` made a new, empty database: wrong folder | `.quit`, `cd ~/lab/sql`, try again. |
| `Parse error: near "INTERSECT"` | The first `SELECT` ended with a `;` | Only one `;`, at the very end. |
| The columns of `truth.py` don't line up | `!s:5` is missing | Copy the f-string exactly. |

## Talk about it

- What's a set? How is it different from a list?
- What are union, intersection and difference, in hoops and in Python?
- How did checking four rows *prove* De Morgan's law?
- Which SQL words match `and`, `or` and `not`?

## Challenge *(if there's time, or for next time)*

- Three hoops: hostile, nether, flying. Which region is empty? Check
  with Python.
- How many rows does a truth table for three inputs need? Four? *(8, 16:
  powers of 2, from Stage 4.)* Change `truth.py` to check that `a and (b
  or c)` equals `(a and b) or (a and c)`.
- Write `my_union(a, b)` and `my_intersection(a, b)` with loops, without
  `|` and `&`.

## Checkpoint

The learner can, without help:
- [ ] Sort cards into a Venn diagram, and name the regions
- [ ] Use `|`, `&`, `-`, `in` and `<=` on Python sets
- [ ] Prove De Morgan's law by checking every row
- [ ] Use `INTERSECT`, `EXCEPT` and `UNION`, and the same idea with
      `AND`, `OR` and `NOT`

## Lab notebook

Draw the Venn diagram with the mobs in it, and label union,
intersection and difference. Copy the truth table and De Morgan's law.
Commit. Add *set*, *element*, *union*, *intersection*, *difference*,
*subset*, *truth table* and *De Morgan's law* to `dictionary.md`.

## Guide's background *(optional reading)*

This is the discrete mathematics part of the stage's math gate: Oscar
Levin's *Discrete Mathematics: An Open Introduction*, Chapter 0 (sets
and logic), and *Book of Proof*, Chapters 1–3, cover it properly, and
are in the math track ([MATH-TRACK.md](../../docs/MATH-TRACK.md)).
Checking every row is a valid proof here because there are only
finitely many cases; it's called **proof by exhaustion**. For infinitely
many cases (every whole number), induction (Lesson 12.10) does the job.

The **relational model** of databases (E. F. Codd, 1970) is built on
sets: a table is a set of rows (a **relation**), and SQL's `UNION`,
`INTERSECT` and `EXCEPT` are set operations. Real SQL tables can
actually hold duplicate rows unless a key forbids it, which is one of
the places SQL departs from pure set theory; `UNION` removes duplicates,
and `UNION ALL` keeps them.
