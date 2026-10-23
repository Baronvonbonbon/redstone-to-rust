# Lesson 6.3: Choosing Machines: Mux and DMux (Project 1, Part 2)

**Time:** 2 sessions of 40 min · **You need:** a terminal; `~/lab/n2t`;
squared paper; the HDL card · **New words:** multiplexor (Mux),
demultiplexor (DMux), select

## Goal *(read this to the learner)*

> A computer is always choosing: which number to add, which memory box to
> read, which instruction comes next. The chip that chooses is called a
> **multiplexor**, or **Mux** for short. It has two inputs and a
> **select** wire that picks which one goes through, like a rail switch
> in Minecraft. Today you'll build it, and its mirror image, the **DMux**,
> which sends one input down one of two tracks.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Not, And, Or and Xor should pass their tests (Lesson 6.2).

## Warm-up (5 min)

"In Lesson 4.14, how did you turn a truth table into gates?" *(An AND
for every row where the output is 1, then OR them all together.)*

## Activity

### Session 1: the Mux

1. **What it does.** `cat Mux.hdl` in `~/lab/n2t/projects/1`. The
   comment says: *if (sel = 0) out = a, else out = b*. **Say:** "`sel` is
   the select wire. It's the rail switch: when it's 0, `a` goes through;
   when it's 1, `b` goes through. The other input is ignored."

   Act it out: the guide holds up a card in each hand (`a` and `b`); the
   learner says "sel is 0" or "sel is 1", and the guide shows only that
   card.

2. **The truth table.** Fill in all eight rows on paper, with the rule:

   | a | b | sel | out |
   |---|---|---|---|
   | 0 | 0 | 0 | 0 |
   | 0 | 0 | 1 | 0 |
   | 0 | 1 | 0 | 0 |
   | 0 | 1 | 1 | 1 |
   | 1 | 0 | 0 | 1 |
   | 1 | 0 | 1 | 0 |
   | 1 | 1 | 0 | 1 |
   | 1 | 1 | 1 | 1 |

   *(For each row, look at `sel`: 0 means copy `a`, 1 means copy `b`.)*
   Check it against the answers: `cat Mux.cmp`.

3. **The gates.** The Lesson 4.14 way works, but it gives four 3-input
   ANDs: a lot of gates. **Say:** "Let's think about it instead. When does
   `a` get through?" *(When `a` is 1 and `sel` is 0.)* "Write that as
   gates." *(`a AND (NOT sel)`.)* "And when does `b` get through?" *(`b
   AND sel`.)* "And the output is 1 if either of those is 1, so..."
   *(`OR` them.)*

   Draw it, name the wires, write the HDL, and test:
   ```
   hardware Mux.tst
   ```
   *(Guide: four parts: a Not, two Ands and an Or.)* Commit it.

4. **Try it in the simulator.** Load `Mux.hdl` in `hardware`. Set `a` to
   1, `b` to 0, and flip `sel` between 0 and 1 (Eval each time). Watch
   `out` follow whichever input is selected.

### Session 2: the DMux

5. **What it does.** `cat DMux.hdl`. **Say:** "A DMux is the Mux turned
   around. One input, `in`, and two outputs, `a` and `b`. `sel` chooses
   which output gets `in`; the other output is 0. It's a mail sorter: it
   sends the letter to one box or the other."

6. **The truth table.**

   | in | sel | a | b |
   |---|---|---|---|
   | 0 | 0 | 0 | 0 |
   | 0 | 1 | 0 | 0 |
   | 1 | 0 | 1 | 0 |
   | 1 | 1 | 0 | 1 |

   Ask: "When is `a` 1?" *(When `in` is 1 and `sel` is 0.)* "When is `b`
   1?" *(When `in` is 1 and `sel` is 1.)* Each output is one AND. Draw it,
   write it, test it (`hardware DMux.tst`), commit it. *(Guide: a Not and
   two Ands.)*

7. **Mux and DMux together.** On paper, draw a DMux whose two outputs go
   into a Mux, with the *same* `sel` wire on both. **Say:** "What comes out
   at the end?" *(Whatever went in: the DMux sends it down one track, and
   the Mux picks that same track.)* "That's how a computer's memory works:
   a DMux sends a number to one memory box, and a Mux reads it back. We'll
   build exactly that in Lesson 6.9."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Comparison failure at line 2` straight away | Probably an earlier chip (Not, And or Or) isn't finished | Test those again: `hardware Not.tst` and so on. |
| The Mux passes half the rows | `a` and `b` are swapped, or the Not is on the wrong side | Check: `a` should go through when `sel` is **0**. |
| `In HDL file ..., out is not a pin in DMux` | DMux's outputs are called `a` and `b` | `DMux(in=..., sel=..., a=..., b=...)` |

## Talk about it

- What does `sel` do in a Mux? In a DMux?
- Why didn't we use the Lesson 4.14 method for the Mux?
- Where might a computer need to choose between two numbers?

## Challenge *(if there's time, or for next time)*

- Count the NANDs inside your Mux, all the way down.
- Build an Xor using only Mux chips, and `true` and `false` wires.
  *(It takes two Muxes: one of them makes a Not.)* Do it in a new practice
  file, not in `Xor.hdl`: copy `Xor.hdl`, `Xor.tst` and `Xor.cmp` into
  `~/lab/n2t/practice/`, then change the copy.

## Checkpoint

The learner can, without help:
- [ ] Explain what a Mux and a DMux do, with the rail-switch or mail picture
- [ ] Write the truth table for each
- [ ] Build both, with passing tests

## Lab notebook

Draw the Mux and DMux with their truth tables, and the DMux-into-Mux
drawing. Commit. Add *multiplexor*, *demultiplexor* and *select* to
`dictionary.md`.

## Guide's background *(optional reading)*

Multiplexors are everywhere in a CPU: they pick an input for the
arithmetic unit, choose the next instruction's address, and read one
word out of memory. A demultiplexor routes one signal to one of several
destinations, which is how a single "write" signal reaches only the
memory word being written.

The "sum of products" method from Lesson 4.14 always works, but it
doesn't always give the smallest circuit. Reasoning about what the chip
*means* ("`a` when sel is 0, `b` when sel is 1") usually gives a simpler
one. Both are legitimate; the test decides.
