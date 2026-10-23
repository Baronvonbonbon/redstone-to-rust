# Lesson 6.6: Adders in HDL (Project 2, Part 1)

**Time:** 2 sessions of 45 min · **You need:** a terminal; `~/lab/n2t`;
Thonny; the learner's Lesson 4.10 and 4.11 drawings, if they kept them;
the HDL card · **New words:** half adder, full adder, carry, ripple,
incrementer

## Goal *(read this to the learner)*

> In Stage 4 you built a 4-bit adder in Digital, by drawing. Now you'll
> build a 16-bit one in HDL: big enough for every number the Hack
> computer uses, negative ones too. And then a chip that adds 1, which
> your computer will use to count its way through a program.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Project 1 should be finished (Lesson 6.4).

## Warm-up (5 min)

On paper, add `0110 + 0111` in binary, with carries. *(`1101`.)* "Which
gate makes the sum bit of two bits?" *(XOR.)* "Which makes the carry?"
*(AND.)*

## Activity

### Session 1: half and full adders

1. **A new folder.**
   ```
   cd ~/lab/n2t/projects/2
   ls
   ```
   **They should see:** `HalfAdder`, `FullAdder`, `Add16`, `Inc16` and
   `ALU` files, but no Not or And. **Say:** "Your Project 1 chips aren't in
   this folder, so the simulator uses its own built-in ones instead. That
   way, if one of yours had a hidden mistake, it can't spoil Project 2."

2. **HalfAdder.** `cat HalfAdder.hdl` and `cat HalfAdder.cmp`. **They
   should see:** two outputs, `sum` and `carry` (the test calls the
   column `car`, because it's narrow). **Say:** "It's exactly your half
   adder from Lesson 4.10." Write it (two parts), test it
   (`hardware HalfAdder.tst`), commit it.

3. **FullAdder.** Three inputs: `a`, `b` and `c`, the carry coming in
   from the column to the right. **Say:** "In Lesson 4.11, you made a full
   adder from two half adders and one more gate. Can you remember how?"
   Draw it before writing. Hints, one at a time:
   - "Add `a` and `b` with the first half adder. What comes out?" *(A sum
     and a carry.)*
   - "Add that sum to `c` with the second half adder." *(Its sum is the
     final sum.)*
   - "Now there are two carries. Can they both be 1 at once?" *(No. So
     the final carry is 1 if either one is: OR.)*

   Write it (three parts), test, commit.

### Session 2: sixteen columns, and adding one

4. **Add16.** `cat Add16.hdl`. The comment says the last carry is
   *ignored*. **Say:** "It's sixteen columns, like adding long numbers on
   paper, from right to left. The carry out of each column goes into the
   next one. That's called a **ripple** adder, because the carry ripples
   along."

   Draw the first two and the last column on paper:
   - Bit 0 has no carry coming in, so it only needs a **half** adder.
   - Bits 1 to 15 each need a **full** adder, with `c` connected to the
     carry from the bit before.
   - The carry out of bit 15 goes nowhere. Give it a name (`overflow`,
     say) and don't connect it to anything. **Say:** "That's the
     overflow from Lesson 6.5: the bit that falls off the end."

   Use Python to write the fifteen full adder lines, like in Lesson 6.4.
   Each line needs *two* numbers: the bit, and the bit before (for the
   carry wire). Test, commit.

5. **Read the test's answers.** `cat Add16.cmp`. Find the row
   `1111111111111111 + 1111111111111111 = 1111111111111110`. **Say:** "Use
   Lesson 6.5: what's that in ordinary numbers?" *(−1 + −1 = −2. The
   adder did negative numbers without even trying!)*

6. **Inc16.** It adds 1 to a 16-bit number. **Say:** "You have an adder.
   What's the simplest way to add 1?" *(Add16, with `b` set to 1.)* "How
   do you make a bus that's 1?" Look at the HDL card: `true` is a wire
   that's always 1, and inputs that aren't connected are 0. So one wire of
   `b` connected to `true`, and the rest left alone, makes the number 1.
   *(Guide: which wire? Bit 0, the ones.)* One part. Test, commit.

   Look at `Inc16.cmp`: −1 + 1 = 0, and −5 + 1 = −4.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `In HDL file ..., car is not a pin in HalfAdder` | The test's column says `car`, but the pin is `carry` | The pins are `sum` and `carry`: check the HDL card's table. |
| `An internal pin may only be fed once by a part's output pin` | Two adders' carries have the same name | Each carry needs its own name: `c0`, `c1`, ... |
| `Comparison failure` on the row with `1111111111111111` | A carry isn't connected to the next adder | Check each full adder's `c=` is the carry from the bit *before*. |
| `Comparison failure` at the first row of Add16 | Bit 0's carry or the `out` wires are mixed up | Check `out[0]` comes from bit 0's sum. |
| `In HDL file ..., A pin name is expected` | `1` was used instead of `true` | Write `true` or `false`, not `1` or `0`. |

## Talk about it

- Why does bit 0 only need a half adder?
- What happens to the carry out of bit 15? Why is that OK?
- How can Inc16 be just one part?

## Challenge *(if there's time, or for next time)*

- In Python, write `add16(a, b)` that adds two 16-bit strings column by
  column, right to left, with a carry, like the chip. Check it against
  every row of `Add16.cmp`.
- How many NANDs are in your Add16, all the way down?

## Checkpoint

The learner can, without help:
- [ ] Build half and full adders in HDL, and explain the carry
- [ ] Explain how Add16 ripples the carry, and what happens to the last one
- [ ] Use `true` to set a wire to 1
- [ ] Show that Add16 adds negative numbers correctly

## Lab notebook

Draw the full adder, and the first, second and last columns of Add16.
Commit. Add *ripple*, *carry* and *incrementer* to `dictionary.md`.

## Guide's background *(optional reading)*

A ripple-carry adder is simple but slow in real hardware: the last sum
isn't right until the carry has rippled through all sixteen columns.
Real CPUs use "carry look-ahead" adders that work out the carries in
parallel. The simulator doesn't model delays, so for Hack the simple
version is fine.

Because of two's complement, Add16 doesn't care whether its inputs are
positive or negative: the same circuit adds both. That's the whole
reason two's complement is used, and the next lesson's ALU depends on
it.
