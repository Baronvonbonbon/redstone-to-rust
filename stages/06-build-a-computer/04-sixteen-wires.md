# Lesson 6.4: Sixteen Wires at Once (Project 1, Part 3)

**Time:** 3 sessions of 45 min · **You need:** a terminal; `~/lab/n2t`;
Thonny or Python; squared paper; the HDL card · **New words:** bus,
16-bit, sub-bus, tree

## Goal *(read this to the learner)*

> The Hack computer works with 16-bit numbers. One wire carries one bit,
> so a 16-bit number needs sixteen wires side by side. A bundle of wires
> like that is called a **bus**. Today you'll build gates that work on
> whole buses at once, and multiplexors that choose between four or eight
> numbers. That's the last nine chips of Project 1.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Not, And, Or, Xor, Mux and DMux should all pass (Lessons 6.2 and
      6.3). Check: `cd ~/lab/n2t/projects/1` then `hardware Mux.tst`.

## Warm-up (5 min)

"How many bits in a byte?" *(8.)* "What's the biggest number in 16 bits?"
*(65535, or 2¹⁶ − 1.)* "In `1010`, which bit is bit 0?" *(The one on the
right: it's worth 1.)*

## Activity

### Session 1: buses, and four easy chips

1. **Bus syntax.** `cat Not16.hdl`. **They should see:** `IN in[16];`.
   **Say:** "`in[16]` is a bus of 16 wires. `in[0]` is the right-hand bit,
   the ones, and `in[15]` is the left-hand one. Not16 is sixteen Nots side
   by side: each `out` wire is the Not of the `in` wire with the same
   number." Look at the test's answers: `head -4 Not16.cmp`. Every bit is
   flipped.

2. **Sixteen lines.** Not16 needs sixteen Not parts, one for each wire:
   the first connects `in[0]` to `out[0]`, the next `in[1]` to `out[1]`,
   and so on. **Say:** "Typing sixteen nearly identical lines is boring, and
   it's easy to make a typo. A programmer would write a program to type
   them!" In Thonny, here's how it works for a pretend chip with switches
   and lamps:
   ```python
   for i in range(4):
       print(f"    Light(in=switch[{i}], out=lamp[{i}]);")
   ```
   **They should see:**
   ```
       Light(in=switch[0], out=lamp[0]);
       Light(in=switch[1], out=lamp[1]);
       Light(in=switch[2], out=lamp[2]);
       Light(in=switch[3], out=lamp[3]);
   ```
   Now the learner changes the program to print Not16's sixteen parts,
   runs it, and copies the output into `Not16.hdl` (select it, copy, and
   paste into nano with **Ctrl+Shift+V**). Test, commit.

3. **And16, Or16 and Mux16.** The same idea, with two input buses (`a`
   and `b`). Mux16 has one `sel` wire that goes to all sixteen Muxes:
   **Say:** "One rail switch that moves sixteen tracks at once." Change the
   program for each, test each, commit each.

### Session 2: Or8Way and the four-way Mux

4. **Or8Way.** `cat Or8Way.hdl`: eight inputs, one output, which is 1 if
   *any* input is 1. **Say:** "Or only takes two inputs. How can we OR
   together eight?" Draw it: OR the first two; OR that with the third;
   and so on, in a chain. *(Seven Ors.)* Name the wires in the middle,
   write it, test, commit.

5. **Two select wires.** `cat Mux4Way16.hdl`. **They should see:**
   `sel[2]`, and a comment saying `a` if sel is `00`, `b` if `01`, `c` if
   `10`, `d` if `11`. **Say:** "With two select wires, there are four
   choices: 00, 01, 10, 11. That's counting in binary! The right-hand
   digit is `sel[0]` and the left one is `sel[1]`."

6. **A tree of Muxes.** On paper, draw a tournament:
   ```
   a ─┐
      ├─ Mux16 (sel[0]) ─┐
   b ─┘                  │
                         ├─ Mux16 (sel[1]) ── out
   c ─┐                  │
      ├─ Mux16 (sel[0]) ─┘
   d ─┘
   ```
   Check it with the table: for sel `10`, `sel[0]` is 0, so the top Mux
   picks `a` and the bottom one picks `c`; `sel[1]` is 1, so the last Mux
   picks the bottom one: `c`. Correct! Try `01` and `11` on paper too.

   To connect one wire of the `sel` bus, write `sel=sel[0]`. Write the
   three parts, test (`hardware Mux4Way16.tst`), commit.

### Session 3: bigger trees

7. **Mux8Way16.** Eight inputs, three select wires: `000` is `a`, up to
   `111` for `h`. **Say:** "You've just built a chip that chooses from
   four. Can you use two of them, and one more Mux16?" Draw the tree
   first. Hints, one at a time:
   - "Which inputs does each Mux4Way16 choose between?" *(a to d, and e
     to h.)*
   - "Which select wires do they need?" *(The lower two: `sel[0..1]`,
     part of a bus, called a **sub-bus**.)*
   - "And which wire picks between their answers?" *(`sel[2]`.)*

   Test, commit.

8. **DMux4Way and DMux8Way.** The mirror images: one input, sent to one
   of four (or eight) outputs. Draw the tree the other way round: the
   first DMux splits by the *left-hand* select wire, then each half is
   split again by the right-hand one. Check every row of the table on
   paper before writing the HDL. Test, commit.

9. **Project 1 is done!** Run every test, one after another:
   ```
   for t in *.tst; do echo -n "$t: "; hardware $t; done
   ```
   **They should see:** fifteen lines, all `End of script - Comparison
   ended successfully`. Celebrate, and commit: `git commit -am "Project
   1: all fifteen chips pass"`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `In HDL file ..., a(1) and a(16) have different bus widths` | A whole bus (`a`) is connected to a one-wire pin | Use one wire: `a=a[3]`. |
| `in(1) and x(16) have different bus widths` | A 16-wire internal pin is going into a one-wire pin | Check which part made `x`: it was a 16-bit chip. |
| `sel(1) and sel(2) have different bus widths` | All of `sel` went into a part that wants one wire | `sel=sel[0]` or `sel=sel[1]`. |
| `a[16]: the specified sub bus is not in the bus range` | Wire numbers go from 0 to 15 | There's no `a[16]`. Check the Python `range`. |
| `x[0..3]: sub bus of an internal node may not be used` | Part of an internal bus was used | Name the part when it comes out: `out[0..3]=x` (see the HDL card, "Several outputs"). |
| A four-way chip passes some rows, but `b` and `c` are swapped | `sel[0]` and `sel[1]` are the wrong way round | `sel[0]` is the **right-hand** digit. Check the tree on paper with sel `01`. |
| The loop prints `hardware: command not found` | The links from Lesson 6.1 are missing | `ls -l ~/bin`, then make them again. |

## Talk about it

- What's a bus? Why does the Hack computer need 16-wire buses?
- How is a Mux4Way16 like a tournament?
- Why is `sel[0]` the right-hand digit?

## Challenge *(if there's time, or for next time)*

- Or8Way as a **tree** instead of a chain: OR pairs, then pairs of
  pairs. It's still seven Ors. Why might a tree be faster in a real
  chip? *(Each signal goes through only three gates, not seven.)*
- How many NANDs are in a Mux16? In a Mux8Way16?

## Checkpoint

The learner can, without help:
- [ ] Explain buses, `a[3]`, and sub-buses like `sel[0..1]`
- [ ] Use a program to write repetitive HDL
- [ ] Build a multi-way Mux or DMux as a tree, and check it on paper
- [ ] Pass all fifteen Project 1 tests

## Lab notebook

Draw the Mux8Way16 tree and the DMux8Way tree. Commit. Add *bus*,
*16-bit*, *sub-bus* and *tree* to `dictionary.md`. Tick
Project 1 on the passport's Nand to Tetris climb.

## Guide's background *(optional reading)*

Real hardware description languages (Verilog and VHDL) have loops for
repeated parts; the course's simple HDL doesn't, so the learner either
types the lines or, better, writes a program that writes them. Programs
that write other programs are an important idea: compilers, coming in
Stage 8, are exactly that.

The four-way and eight-way chips are where the select bits are
easiest to mix up. The test tables show `sel` written as a binary
number, so the right-hand digit is `sel[0]`. Checking one or two rows by
hand on the drawing, before typing any HDL, catches nearly every
mistake.
