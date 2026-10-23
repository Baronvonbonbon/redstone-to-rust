# Lesson 6.8: Remembering: Bits and Registers (Project 3, Part 1)

**Time:** 2 sessions of 45 min · **You need:** a terminal; `~/lab/n2t`;
squared paper; the HDL card; Lesson 4.12's latch drawing and Lesson
4.13's seal-in rung, if they're in the notebook · **New words:** clock,
tick, tock, DFF, clocked, register

## Goal *(read this to the learner)*

> Every chip so far forgets everything the moment its inputs change. A
> computer that forgets can't count, or run a program, or remember your
> high score. Today you'll add **time**. A clock ticks, and a tiny chip
> called a **DFF** remembers its input from one tick to the next. From
> that you'll build a **Bit** that remembers for as long as you like,
> and a **Register** that remembers a whole 16-bit number.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Projects 1 and 2 should be finished.

## Warm-up (5 min)

"In Lesson 4.12, how did the latch remember?" *(Two gates feeding
each other in a loop.)* "In Lesson 4.13, what kept the motor running
after the start button was let go?" *(The seal-in: the motor's own
contact feeding back.)* "What do those have in common?" *(A loop: the
output comes back to the input.)*

## Activity

### Session 1: the clock, and the Bit

1. **Ticks and tocks.** **Say:** "Inside a computer, a clock ticks
   billions of times a second. In the simulator, the clock is slow: you
   press a button. Each beat has two halves, called **tick** and
   **tock**. On the tick, chips with memory look at their inputs. On the
   tock, their outputs change."

   **Say:** "A Minecraft redstone clock is the same idea: a loop of
   repeaters that pulses again and again. Real CPUs use a crystal that
   vibrates instead."

2. **The DFF: a one-step memory.** **Say:** "The only memory chip you're
   given is the **DFF** (data flip-flop). Its rule: what comes *out* now
   is what went *in* on the last clock beat. It's always one step behind."
   Draw a timeline on squared paper:

   | Time | 1 | 2 | 3 | 4 | 5 |
   |---|---|---|---|---|---|
   | in | 1 | 0 | 0 | 1 | 1 |
   | out | ? | 1 | 0 | 0 | 1 |

   **Say:** "`out` is `in`, moved one step to the right. It only remembers
   for one step, though. How can we make it remember for as long as we
   want?"

3. **The Bit: remembering forever.** `cd ~/lab/n2t/projects/3/a` and
   `cat Bit.hdl`. The rule: if `load` is 1, remember the new `in`;
   otherwise, keep the old value. **Say:** "Keep the old value... where is
   the old value?" *(Coming out of the DFF!)* "So what if the DFF's
   output was fed back into its own input?" *(It would keep it forever:
   like the seal-in rung.)* "And when `load` is 1, we want `in` to go into
   the DFF instead. Which chip chooses between two things?" *(A Mux.)*

   Draw it: a Mux whose output goes into a DFF; the DFF's output comes
   out as `out` *and* loops back into one of the Mux's inputs. `load` is
   the Mux's `sel`. *(Guide: two parts. The DFF's output needs two names,
   `out=out` and another for the loop: the "Several outputs" trick from
   the HDL card.)*

   Write it and test it:
   ```
   hardware Bit.tst
   ```
   Commit.

4. **Watch it remember.** Open `hardware` and load `Bit.hdl`. **They
   should see:** `Bit (Clocked)` as the chip's name, and `Time : 0`. Set
   `in` to 1 and `load` to 1. Click the **clock** button once (tick):
   `Time : 0+`, and `out` is still 0. Click it again (tock): `Time : 1`,
   and `out` is 1.

   Now set `load` to 0 and `in` to 0. Click the clock twice. **They
   should see:** `out` is *still* 1. It's remembering! Set `load` back to
   1, and click twice: now it changes to 0.

### Session 2: the Register

5. **Sixteen Bits.** `cat Register.hdl`. **Say:** "A Register is sixteen
   Bits side by side, all sharing one `load` wire. It remembers a 16-bit
   number." Use the Python trick from Lesson 6.4 to write the sixteen
   lines, test (`hardware Register.tst`), and commit.

6. **Read the test.** `head -12 Register.cmp`. **They should see:** a
   `time` column with `0+`, `1`, `1+`, `2`... and `in`, `load` and `out`,
   written as ordinary numbers (like `-32123`: the two's complement from
   Lesson 6.5). **Say:** "Find a row where `load` is 1 and `in` changes. On
   which row does `out` change?" *(The next whole number of time: after the
   tock.)*

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `This chip has a circle in its parts connections` | The loop doesn't go through a DFF | Every loop must go through a DFF: that's what stops it going round and round forever. |
| `Comparison failure at line 7` | The Bit ignores `load`: it always takes `in` | `load` must be the Mux's `sel`. |
| `Can't connect gate's output pin to part` | The chip's `out` is used as the loop wire | Give the DFF's output a second name for the loop. |
| In the window, the clock button is grey | The loaded chip has no memory (no DFF inside) | Load `Bit.hdl` or `Register.hdl`. |
| `out` doesn't change after one click | That was only the tick | Click again for the tock. |

## Talk about it

- What does a DFF do? What's it missing on its own?
- How is the Bit's loop like the seal-in rung?
- Why do loops need a DFF?

## Challenge *(if there's time, or for next time)*

- A **toggle**: a chip with no inputs except the clock, whose output
  flips every beat: 0, 1, 0, 1. Build it in `practice` with a DFF and a
  Not, and watch it in the window. (No test file: watch it work.)
- Draw a timeline for a Bit with `load` 1 at time 1 and 4 only, and
  `in` 1 at times 1 and 2. What does `out` show at times 1 to 6?

## Checkpoint

The learner can, without help:
- [ ] Explain the clock, tick and tock, and what a DFF does
- [ ] Explain how the Bit's loop and Mux make it remember
- [ ] Build Bit and Register, with passing tests
- [ ] Watch a Bit remember in the simulator, using the clock

## Lab notebook

Draw the Bit (Mux, DFF and loop) next to the Lesson 4.13 seal-in rung.
Commit. Add *clock*, *tick*, *tock*, *DFF*, *clocked* and *register* to
`dictionary.md`.

## Guide's background *(optional reading)*

Chips without memory are called **combinational**: their outputs depend
only on their inputs right now. Chips with memory are **sequential**:
their outputs also depend on what happened before. The DFF is the one
sequential chip Nand to Tetris gives you, built in. (It can be built
from NAND gates, using latches like Lesson 4.12's, but that needs
careful timing that the simulator doesn't model.)

The rule that every loop must pass through a DFF is what makes digital
circuits predictable: the clock breaks every loop into steps. For a
controls engineer, the Bit is a seal-in circuit with a "load" in place
of start and stop, and the clock is the PLC's scan: inputs are read, and
outputs are updated once per scan.
