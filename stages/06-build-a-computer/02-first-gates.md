# Lesson 6.2: First Gates (Project 1, Part 1)

**Time:** 2 sessions of 45 min · **You need:** a terminal; nano or vim;
`~/lab/n2t`; the HDL card; the learner's Lesson 4.9 drawings, if they
kept them · **New words:** project, built-in chip

## Goal *(read this to the learner)*

> NAND is the only chip you're given. Everything else in the computer,
> you make. Today you build the first four gates, NOT, AND, OR and XOR,
> out of NAND alone, the same way you did in Digital in Stage 4, but
> written in HDL. From now on, every chip you make is built from the ones
> you made before.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Find the learner's drawings from Lesson 4.9 (NOT, AND and OR from
      NAND), if they're in the notebook.

## Warm-up (5 min)

From memory, write the truth tables for NOT, AND, OR and XOR. "Which
one is the 'one or the other, but not both' gate?" *(XOR.)*

## Activity

### Session 1: NOT, AND and OR

1. **The project folder.**
   ```
   cd ~/lab/n2t/projects/1
   ls *.hdl
   cat Not.hdl
   ```
   **They should see:** fifteen chips, and a `Not.hdl` with its pins
   written and an empty `PARTS:` section (the comment says *Replace this
   comment with your code*). **Say:** "Project 1 is fifteen chips. Each one
   is waiting for its parts. We build them in order, because each one uses
   the ones before."

2. **Why order matters.** Run a test on a chip before building it:
   ```
   hardware Not.tst
   ```
   **They should see:** `Comparison failure at line 2`. **Say:** "An
   empty chip has nothing inside, so its outputs are always 0. And
   watch out: if `And` uses `Not`, and your `Not` is still empty, then
   `And` will fail too, even if `And` itself is right."

3. **NOT.** Look at the Lesson 4.9 drawing, or work it out again: "What
   does NAND do when both its inputs are the same?" *(NAND of 0 and 0 is
   1; NAND of 1 and 1 is 0. That's NOT!)* Open `Not.hdl`, replace the
   comment with one part, and test:
   ```
   nano Not.hdl
   hardware Not.tst
   ```
   **They should see:** `End of script - Comparison ended successfully`.
   *(Guide: one Nand, with the chip's `in` connected to both of its
   inputs.)*

4. **Save it.**
   ```
   git add Not.hdl
   git commit -m "Not, from one Nand"
   ```
   **Say:** "One commit per chip that passes. Then if you break something,
   you can always go back."

5. **AND.** "NAND is 'not and'. So how do you get AND?" *(Undo the 'not':
   a NAND, then your own Not.)* Write it, test it (`hardware And.tst`),
   commit it.

6. **OR.** This one needs De Morgan, from Lesson 4.8: "OR is 1 when `a`
   is 1 or `b` is 1. When is NAND 1?" *(When its inputs are NOT both 1.)*
   "So what should go into the NAND?" *(NOT a and NOT b.)* Check it on
   paper with a truth table first:

   | a | b | not a | not b | Nand(not a, not b) |
   |---|---|---|---|---|
   | 0 | 0 | 1 | 1 | 0 |
   | 0 | 1 | 1 | 0 | 1 |
   | 1 | 0 | 0 | 1 | 1 |
   | 1 | 1 | 0 | 0 | 1 |

   The last column is OR! Write it (three parts), test, commit.

### Session 2: XOR, and looking inside

7. **XOR.** `cat Xor.hdl`. The comment gives the formula:
   `(a and Not(b)) or (Not(a) and b)`. **Say:** "Turn the formula into a
   drawing first, then the drawing into HDL. Name every wire in the
   middle." Draw it together: two Nots, two Ands, one Or, and four
   internal wires. Then write the five parts, test and commit.

   *(Guide: if it fails, ask the learner to read one line aloud and say
   what each wire carries. Mixed-up wires are the usual problem.)*

8. **Look inside in the simulator.** Open `hardware`, load
   `projects/1/Xor.hdl` (Load Chip), and set `a` to 1 and `b` to 0, then
   Eval (calculator). Look at the **Internal pins**: every wire you named
   is there, with its value. **Say:** "When a chip fails, this is how you
   find the wire that's wrong: set the inputs from the failing row, and
   check each internal pin against your drawing."

9. **Count the NANDs.** **Say:** "Your Xor is made of Nots, Ands and an
   Or. But each of those is made of NANDs. How many NANDs are inside your
   Xor, all the way down?" Count on paper together. *(Two Nots = 2, two
   Ands = 4, one Or = 3: 9 NANDs.)* "Everything in a computer is just lots
   and lots of these."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Comparison failure at line 2`, but the chip looks right | It uses a chip that's still empty (an empty chip always outputs 0) | Build and test the chips in order: Not, And, Or, Xor. |
| `Chip not is not found in the working and built in folders` | A chip name in lowercase | `Not`, `And`, `Nand`, with capital letters. |
| `In HDL file ..., x is not a pin in Not` | Not's pins are `in` and `out`, not `a` and `b` | Check the [HDL card](../../labs/n2t/HDL-CARD.md)'s table. |
| `Can't connect gate's output pin to part` | The chip's `out` is used as an input to another part | Make an internal pin, like `out=x`, and use `x`. |
| `An internal pin may only be fed once by a part's output pin` | Two parts have the same `out=` name | Each wire needs its own name. |
| The test passes in the folder, but `git status` shows `Not.out` | The `.gitignore` is missing | It's in `~/lab/n2t/.gitignore` from Lesson 6.1. Check `cat ~/lab/n2t/.gitignore`. |

## Talk about it

- Why must the chips be built in order?
- How did De Morgan's law help with OR?
- How many NANDs are in an AND? In an OR?

## Challenge *(if there's time, or for next time)*

- Build XOR from just **four** NANDs, with no Nots, Ands or Ors. It's a
  famous puzzle. Hint: start with `Nand(a=a, b=b, out=n)`, and use `n`
  more than once. Keep your first Xor safe in git, and use the test to
  check the new one.
- Which uses fewer NANDs in total: your Xor, or the four-NAND one?

## Checkpoint

The learner can, without help:
- [ ] Build NOT, AND and OR from NAND, and explain each
- [ ] Turn a formula into a gate drawing, and the drawing into HDL
- [ ] Find a wrong wire using the simulator's internal pins
- [ ] Commit each chip once it passes

## Lab notebook

Draw all four chips, with their NAND counts. Commit. Add *project* and
*built-in chip* to `dictionary.md`.

## Guide's background *(optional reading)*

The simulator looks for a chip's `.hdl` file in the same folder first,
and only uses its own **built-in** version if there's no file. The
project folders come with empty files for every chip, so in
`projects/1`, the learner's own chips are always used: a mistake in Not
shows up in every chip that uses Not. That's realistic: a faulty part
breaks everything built on it. In the next project folders, earlier
chips are *not* there, so the simulator uses its own reliable built-in
versions, and an old mistake can't spoil a new project.

The hints in brackets describe each design without giving the HDL: this
course follows the Nand to Tetris authors' request that solutions aren't
published. The learner built NOT, AND and OR from NAND in Digital in
Lesson 4.9, so these first ones are a translation of their own work.
