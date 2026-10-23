# Lesson 6.7: The ALU (Project 2, Part 2)

**Time:** 3 sessions of 45 min · **You need:** a terminal; `~/lab/n2t`;
Thonny; squared paper; the HDL card and the Hack card · **New words:**
ALU, control bit, flag

## Goal *(read this to the learner)*

> The **ALU**, the Arithmetic Logic Unit, is the part of the computer
> that does the working out. Give it two numbers, `x` and `y`, and six
> **control bits**, and it can work out eighteen different things: x + y,
> x − y, x + 1, x AND y, and more. It does all that with an adder, some
> NOTs, and some Muxes. It's the biggest chip so far, and the heart of
> your computer.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] HalfAdder, FullAdder, Add16 and Inc16 should pass (Lesson 6.6).
      The ALU uses the learner's own Add16 from the same folder.
- [ ] Have Lesson 6.5's flip-and-add-1 trick ready to remind them of.

## Warm-up (5 min)

"How do you make a number negative in binary?" *(Flip every bit, add
1.)* "What does a Mux16 do?" *(Chooses one of two 16-bit numbers.)*

## Activity

### Session 1: how the ALU thinks

1. **Read the plan.** `cd ~/lab/n2t/projects/2` and `cat ALU.hdl`. Read
   the comment's six steps together:
   ```
   if (zx == 1) sets x = 0
   if (nx == 1) sets x = !x
   if (zy == 1) sets y = 0
   if (ny == 1) sets y = !y
   if (f == 1)  sets out = x + y
   if (f == 0)  sets out = x & y
   if (no == 1) sets out = !out
   ```
   **Say:** "`!` means NOT: flip every bit. Each control bit switches one
   step on or off. `zx` is 'zero the x', `nx` is 'not the x', `f` is the
   function, add or AND, and `no` is 'not the output'. Six switches, in
   that order."

2. **A paper ALU in Python.** Before building it, try it out. New file,
   `~/lab/python/binary/alu.py`:
   ```python
   def alu(x, y, zx, nx, zy, ny, f, no):
       """The Hack ALU, on ordinary Python numbers kept to 16 bits."""
       if zx: x = 0
       if nx: x = ~x
       if zy: y = 0
       if ny: y = ~y
       if f:
           out = x + y
       else:
           out = x & y
       if no: out = ~out
       out = (out + 32768) % 65536 - 32768   # keep it in 16 bits
       return out

   print(alu(5, 3, 0, 0, 0, 0, 1, 0))   # x + y
   print(alu(5, 3, 0, 1, 0, 0, 1, 1))   # x - y
   ```
   **They should see:** `8`, then `2`. **Say:** "Python's `~` flips every
   bit, like `!`. Look at the second one: it never subtracts! It flips
   `x`, adds `y`, and flips the answer. And out comes 5 − 3."

3. **Why that works.** On paper, with the Lesson 6.5 rule (negative =
   flip and add 1, so flipping is the same as "negative, take away 1"):
   - flip x: −x − 1 *(−6)*
   - add y: −x − 1 + y *(−3)*
   - flip that: −(−x − 1 + y) − 1 = x − y *(2)*

   It's fine if this is a stretch. The point: six simple switches give
   real arithmetic.

4. **Find the settings.** The [Hack card](../../labs/n2t/HACK-CARD.md)'s
   *comp* table has all eighteen settings: the six c-bits are zx, nx, zy,
   ny, f and no, in order. (In that table, `D` plays the part of `x` and
   `A` the part of `y`.) Try some with the Python ALU, with `x = 5` and
   `y = 3`:
   - `0` is `101010`: `alu(5, 3, 1, 0, 1, 0, 1, 0)` *(0)*
   - `x+1` is `011111` *(6)*
   - `-y` is `110011` *(−3)*
   - `x|y` is `010101` *(7)*

   **Say:** "That's eighteen functions from one machine with six switches."

### Session 2: building `out`

5. **Plan it on paper.** Draw the ALU as a row of stages, left to right,
   one for each step. For each step, ask: "How do you make a chip that
   *sometimes* changes the number, depending on one bit?" Hints, one at a
   time:
   - "Which chip chooses between two numbers, using one bit?" *(Mux16.)*
   - "For `zx`: what are the two numbers to choose between?" *(`x`, or
     0. And 0 as a bus is `false`.)*
   - "For `nx`: what are the two choices?" *(The number so far, or a
     Not16 of it.)*
   - "For `f`: what are the two choices?" *(And16 of the two, or Add16 of
     the two.)*

   Draw every stage, and name every wire between stages (like `x1`, `x2`).
   *(Guide: about ten parts in all. Every stage is a Mux16 choosing
   between "unchanged" and "changed".)*

6. **Write it, and test it in two steps.** The suite has a first test
   that only checks `out`, and ignores `zr` and `ng`:
   ```
   hardware ALU-basic.tst
   ```
   Build until this one passes, then commit:
   `git commit -am "ALU: out works"`.

### Session 3: the flags

7. **zr and ng.** `zr` must be 1 when `out` is zero, and `ng` when `out`
   is negative. These are called **flags**: little signals that say
   something about the answer. The computer will use them to make
   decisions, like "jump if the answer is negative".
   - "How can you tell a 16-bit number is negative?" *(Its left bit,
     bit 15, the sign bit, is 1.)*
   - "How can you tell it's zero?" *(None of its bits is 1. That's an
     OR of all sixteen bits, then a NOT.)*

8. **The splitting trick.** **Say:** "You can't take `out[15]` from an
   output pin inside the chip, and you can't take part of an internal
   bus. But the last part can send its answer to several places at once."
   Show the HDL card's "Several outputs" section:
   `Mux16(..., out=out, out[15]=top, out[0..7]=low);`. *(Guide: the last
   Mux16 sends to `out`, to `ng` directly, and to two 8-bit halves for two
   Or8Ways.)*

   Test with the full test:
   ```
   hardware ALU.tst
   ```
   **They should see:** `End of script - Comparison ended successfully`.
   Then run all of Project 2 together, and commit:
   ```
   for t in *.tst; do echo -n "$t: "; hardware $t; done
   git commit -am "Project 2: the ALU works"
   ```

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Comparison failure at line 3` in `ALU-basic.tst`, and the chip looks right | Often Add16 isn't finished (an empty chip outputs 0, which happens to be right for the first row) | `hardware Add16.tst`. The ALU uses your Add16. |
| `ALU-basic` passes, but `ALU.tst` fails at line 2 | `zr` or `ng` isn't connected yet | That's step 7. |
| `x1[15]: sub bus of an internal node may not be used` | Part of an internal bus was used | Use the splitting trick: `out[15]=top` on the part that makes it. |
| `Can't connect gate's output pin to part` | The chip's own `out` is used as an input to Or8Way | Split it with `out=out, out[0..7]=low, ...` instead. |
| Some rows pass and others don't | One stage has its Mux inputs swapped | Use the Python ALU and the failing row: set those bits in `hardware`'s window (Load Chip, then the failing row's inputs, Eval) and compare each internal wire with what Python says. |

## Talk about it

- What do the six control bits each do?
- How does the ALU work out x − y without a subtractor?
- What are `zr` and `ng` for?

## Challenge *(if there's time, or for next time)*

- In Python, loop over all 64 combinations of control bits with `x = 5`
  and `y = 3`, and print each result. Which answers appear? Which
  combinations give the same answer?
- Why does the ALU have a `no` at the end, and not just at the start?

## Checkpoint

The learner can, without help:
- [ ] Explain the six control bits, in order
- [ ] Find the control bits for a function on the Hack card, and check
      them with the Python ALU
- [ ] Build the ALU, with both tests passing
- [ ] Explain how the flags are worked out

## Lab notebook

Draw the ALU's stages. Write the settings for x + y, x − y and x + 1.
Commit. Add *ALU*, *control bit* and *flag* to `dictionary.md`. Tick
Project 2 on the passport's Nand to Tetris climb.

## Guide's background *(optional reading)*

The Hack ALU is deliberately simple, but its design is clever: by
choosing to zero and/or flip each input, add or AND them, and flip the
result, it gets constants, copies, negations, increments, decrements,
addition, subtraction, AND and OR from one small circuit. Real ALUs do
more (multiplication, shifts) but follow the same idea. In Lesson 6.12
the CPU feeds six bits of every instruction straight into these control
bits, which is why the Hack card's comp table *is* the ALU's table.

The flags `zr` and `ng` are how the computer makes decisions: a jump
instruction asks "was the last answer zero? negative?" and the flags
answer. Real processors have the same thing, often called the zero and
sign flags.
