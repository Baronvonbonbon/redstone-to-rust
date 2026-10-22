# Lesson 4.10: Adding with Gates

**Time:** 2–3 sessions of 45 min · **You need:** paper; Digital; Luanti
and the **redstone-lab** world; Thonny · **New words:** carry, half
adder, sum

## Goal *(read this to the learner)*

> Computers are famous for doing sums incredibly fast. But a computer is
> only gates, and gates only know 0 and 1. So how does it add? Today you'll
> do binary addition on paper, spot that the answer is made of two gates
> you already know, and build an adding machine: in Digital, in Python,
> and as a giant glowing machine in Luanti.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Practise one binary sum on paper (step 2), so you can show the carry.
- [ ] For Session 3, look at the Luanti plan in step 7 and pick a clear,
      flat spot in the world.

## Warm-up (5 min)

Do `27 + 15` on paper, the column way. "What happens in the ones
column?" *(7 + 5 = 12, so write 2 and **carry** the 1.)* "Why can't we
write 12 in one column?" *(Each column only holds one digit, 0 to 9.)*

## Activity

### Session 1: binary sums on paper

1. **The four binary facts.** **Say:** "In binary, each column can only
   hold 0 or 1. So adding two bits has just four possibilities." Fill
   them in together:

   ```
   0 + 0 = 0
   0 + 1 = 1
   1 + 0 = 1
   1 + 1 = 10     (that's 2: write 0, carry 1)
   ```

   **Say:** "1 + 1 is two, but there's no digit 2 in binary. So we write 0
   and **carry** 1 into the next column, just like 7 + 5 in base ten."

2. **Column addition in binary.** Add `0101 + 0011` (5 + 3), right to
   left, writing carries above:

   ```
   carries:  1 1 1
             0 1 0 1      (5)
           + 0 0 1 1      (3)
           ---------
             1 0 0 0      (8)
   ```

   Check with the dot cards: 8. ✓ Try `0110 + 0111` *(1101, 13)* and
   `1001 + 0110` *(1111, 15)*. Check each one in Python with `bin(6 + 7)`.

3. **Spot the gates.** Write the four facts from step 1 as a table, with
   the answer split into two bits, the **carry** and the **sum**:

   | A | B | carry | sum |
   |---|---|---|---|
   | 0 | 0 | 0 | 0 |
   | 0 | 1 | 0 | 1 |
   | 1 | 0 | 0 | 1 |
   | 1 | 1 | 1 | 0 |

   **Say:** "Look at the sum column. Have you seen that pattern before?"
   *(0, 1, 1, 0: it's XOR, the stair light!)* "And the carry column?"
   *(0, 0, 0, 1: AND!)* **Say:** "So adding two bits is just an XOR and an
   AND, side by side. That little circuit is called a **half adder**."

### Session 2: the half adder in Digital and Python

4. **Build it in Digital.** New circuit. Two inputs **A** and **B**, an
   **XOr** gate and an **And** gate (both in Components → Logic), and two
   outputs, **S** (sum) and **C** (carry). Each input needs two wires: one
   to the XOr, one to the And. Add this test case:

   ```
   A B C S
   0 0 0 0
   0 1 0 1
   1 0 0 1
   1 1 1 0
   ```

   Run the tests until they pass. Save as `half_adder.dig` in
   `lab/circuits`. You'll need it next lesson.

5. **And in Python.** Add to `gates.py`, before the `table` lines:
   ```python
   def half_adder(a, b):
       return AND(a, b), XOR(a, b)
   ```
   And at the end:
   ```python
   for a in [0, 1]:
       for b in [0, 1]:
           carry, total = half_adder(a, b)
           print(f"{a} + {b} = carry {carry}, sum {total}")
   ```
   **They should see:** `1 + 1 = carry 1, sum 0` on the last line.

   **Say:** "A function can return **two** things, with a comma between
   them, and you can catch them in two boxes: `carry, total = ...`."

6. **Why is it only *half*?** Look back at the paper sum from step 2. In
   the middle columns there are **three** things to add: the A bit, the B
   bit, *and* the carry from the column before. **Say:** "A half adder can
   only add two bits. To add three, we need a *full* adder. That's next
   lesson."

### Session 3: a half adder in Luanti

7. **The big build.** In Luanti, build this with two switches (`A`, `B`),
   an **xor** gate (`X`), an **and** gate (`&`), wires (`=`) and two
   lightstones (`S` for sum, `C` for carry). Stand at the **bottom** of the
   picture, facing up, when you place the two gates, so their outputs
   point right.

   ```
   seen from above (you stand at the bottom):

   B====
   .=..=
   .=..&=C
   .=..=
   .=.A=
   .=..=
   .=..X=S
   .====
   ```

   Each character is one block, and `.` is an empty block. The `A` switch
   is right next to the wire between the two gates, so it feeds both
   gates. The `B` wire goes all the way round the outside to reach the
   other side of both gates.

   Test all four combinations. **They should see:** with both switches on,
   the **C** lamp glows and **S** is dark: 1 + 1 = 10. Put a sign next to
   each lamp (search `sign`) to label it.

   **Say:** "Every computer ever made adds numbers with circuits like
   this one, just billions of times smaller."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| A sum on paper is wrong | A carry was forgotten | Write the carries above the columns, every time. |
| Digital: the S output acts like OR | An Or gate was used instead of XOr | XOr has an extra curved line at the back. |
| Digital: one gate ignores an input | Only one wire from that input | Each input needs two wires, from the same pin: one to each gate. |
| Python: `NameError: name 'XOR' is not defined` | `half_adder` is above `XOR` in the file, and runs before it exists, or XOR wasn't added in Lesson 4.6 | Put `half_adder` below the other gates, and check `XOR` is there. |
| Luanti: a lamp never lights | A gate is facing the wrong way | The picture on top must point right, towards the lamps. Dig it and place it again facing up the picture. |
| Luanti: both lamps act strangely | The `B` wire touches the `A` wire or the middle wire | Keep the empty gaps exactly as in the picture. |

## Talk about it

- Why does 1 + 1 need two bits to write the answer?
- Which gate makes the sum, and which makes the carry?
- What's missing from a half adder?

## Challenge *(if there's time, or for next time)*

- Add a third switch and work out what a **full** adder's truth table must
  be: A, B and a carry-in, with a carry-out and a sum (8 rows). Next
  lesson builds it!
- In Python, what does `print(half_adder(1, 1))` show, and why the
  brackets? *(`(1, 0)`. It's a **tuple**: two values stuck together.)*

## Checkpoint

The learner can, without help:
- [ ] Add two 4-bit binary numbers on paper, with carries
- [ ] Explain why the sum bit is XOR and the carry bit is AND
- [ ] Build and test a half adder in Digital
- [ ] Write a Python function that returns two values

## Lab notebook

Copy the half adder truth table and circle the XOR and AND columns. Draw
the Digital half adder. Add *carry*, *sum* and *half adder* to the
dictionary.

## Guide's background *(optional reading)*

The half adder is the "aha" moment of this stage: arithmetic, which
seems like a completely different kind of thing from logic, turns out to
be logic. The sum bit of two bits is their XOR, and the carry is their
AND. Chaining these with carries (next lesson) adds numbers of any size.

The Luanti build was checked by the course's automated tests, with the
gates placed facing the same way as the picture. If your learner prefers
to design their own layout, let them: the only rule is that each input
must reach one side of *both* gates, without touching the other input's
wire.

Python functions returning `a, b` actually return one **tuple**, which
the caller "unpacks" into two variables. It's a common and handy pattern
that will come back often.
