# Lesson 4.11: The Adding Machine

**Time:** 2–3 sessions of 45 min · **You need:** Digital, with
`half_adder.dig` from Lesson 4.10 in `~/lab/circuits/`; Thonny;
`gates.py` · **New words:** full adder, ripple carry, sub-circuit,
abstraction

## Goal *(read this to the learner)*

> A half adder adds two bits. But to add real numbers, every column needs
> to add *three* bits: A, B, and the carry from the column before. Today
> you'll build a **full adder** out of two half adders, then chain four of
> them together into a machine that adds any two numbers from 0 to 15.
> You'll be using your own circuits as building blocks, the way real chip
> designers do.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check `ls ~/lab/circuits` shows `half_adder.dig`, and that its tests
      pass.

## Warm-up (5 min)

On paper: `0111 + 0011`. *(1010.)* "In the second column from the right,
how many 1s did you add?" *(Three: 1 + 1 + the carry.)* "What's 1 + 1 + 1
in binary?" *(11: sum 1, carry 1.)*

## Activity

### Session 1: the full adder

1. **The full adder's job.** It adds three bits, **A**, **B** and **Cin**
   (carry in), and gives **S** (sum) and **Cout** (carry out). Fill in the
   truth table on paper by counting the 1s in each row:

   | A | B | Cin | Cout | S |
   |---|---|---|---|---|
   | 0 | 0 | 0 | 0 | 0 |
   | 0 | 0 | 1 | 0 | 1 |
   | 0 | 1 | 0 | 0 | 1 |
   | 0 | 1 | 1 | 1 | 0 |
   | 1 | 0 | 0 | 0 | 1 |
   | 1 | 0 | 1 | 1 | 0 |
   | 1 | 1 | 0 | 1 | 0 |
   | 1 | 1 | 1 | 1 | 1 |

   *(No 1s: 00. One 1: 01. Two 1s: 10. Three 1s: 11.)*

2. **The plan: two half adders.** **Say:** "To add three numbers, add the
   first two, then add the third to the answer. A full adder is: half
   adder for A and B, then a second half adder for that sum and Cin. If
   *either* half adder made a carry, there's a carry out." Draw it:

   ```
          ┌─────┐            ┌─────┐
     A ──►│     │── S ──────►│     │── S ────────► S
          │ HA1 │            │ HA2 │
     B ──►│     │    Cin ───►│     │
          └─────┘            └─────┘
             │ C                │ C
             │     ┌──────┐     │
             └────►│  OR  │◄────┘
                   └──────┘
                       │
                       └───────────────────────► Cout
   ```

   - Half adder 1 adds **A** and **B**.
   - Half adder 2 adds half adder 1's **S** and **Cin**. Its **S** is the
     answer's sum.
   - An **Or** gate takes **both** half adders' **C**. Its output is
     **Cout**.

3. **Your circuit becomes a part.** In Digital, **File → New**, then
   immediately **File → Save As**, as `full_adder.dig` in `lab/circuits`
   (the same folder as `half_adder.dig`). Now open **Components →
   Custom**. **They should see:** `half_adder` in the list!

   **Say:** "Digital lets you use any circuit saved in the same folder as a
   part in a new circuit. Its inputs and outputs become pins on a box,
   labelled A, B, C and S. You don't have to look inside it any more: you
   know what it does. That's called **abstraction**, and it's the most
   important idea in all of computing."

4. **Build it.** Place two `half_adder` boxes and one **Or** gate. Add
   inputs **A**, **B** and **Cin**, and outputs **S** and **Cout**. Wire it
   as the plan shows. Add the test case (it's the table from step 1):

   ```
   A B Cin Cout S
   0 0 0 0 0
   0 0 1 0 1
   0 1 0 0 1
   0 1 1 1 0
   1 0 0 0 1
   1 0 1 1 0
   1 1 0 1 0
   1 1 1 1 1
   ```

   Run the tests until they pass, and save.

### Session 2: four bits

5. **Chain them.** **Say:** "Each column of a sum is one full adder. The
   carry out of each column goes into the carry in of the next one, to its
   left. With four full adders, we can add two 4-bit numbers." Draw the
   chain on paper:

   ```
          A3 B3      A2 B2      A1 B1      A0 B0
           │  │       │  │       │  │       │  │
   C4 ◄──[ full ]◄──[ full ]◄──[ full ]◄──[ full ]◄── C0 (0)
             │          │          │          │
             S3         S2         S1         S0
   ```

6. **Build the adding machine.** New file, save it straight away as
   `adder4.dig` in `lab/circuits`. Place four `full_adder` boxes from
   **Components → Custom**. Add eight inputs, **A0** to **A3** and **B0**
   to **B3** (A0 and B0 are the ones bits), one input **C0**, and five
   outputs, **S0** to **S3** and **C4**. Wire each column, and the carries
   from right to left. Use **L** to place lots of inputs quickly, and
   label them carefully.

   Test case (each row is a real sum: 5 + 3 = 8, 7 + 1 = 8, 9 + 6 = 15,
   15 + 1 = 16, 0 + 0 = 0, 15 + 15 = 30, 6 + 6 = 12, 10 + 5 = 15):

   ```
   C0 A3 A2 A1 A0 B3 B2 B1 B0 C4 S3 S2 S1 S0
   0 0 1 0 1 0 0 1 1 0 1 0 0 0
   0 0 1 1 1 0 0 0 1 0 1 0 0 0
   0 1 0 0 1 0 1 1 0 0 1 1 1 1
   0 1 1 1 1 0 0 0 1 1 0 0 0 0
   0 0 0 0 0 0 0 0 0 0 0 0 0 0
   0 1 1 1 1 1 1 1 1 1 1 1 1 0
   0 0 1 1 0 0 1 1 0 0 1 1 0 0
   0 1 0 1 0 0 1 0 1 0 1 1 1 1
   ```

   **They should see:** all eight rows pass. Then run it (▶) and add your
   own numbers by clicking the inputs. Read the answer on the outputs,
   with C4 as the 16s bit.

   **Say:** "This is called a **ripple carry** adder, because the carry
   ripples along from right to left, like a wave."

7. **Look inside the real one.** Digital has its own ready-made adder:
   **Components → Arithmetic → Adder**. **Say:** "Now you know what's
   inside that box: full adders, made of half adders, made of XOR, AND and
   OR, which can all be made of NAND."

### Session 3: build it again, in Python

8. **A full adder in Python.** Add to `gates.py`, below `half_adder`:
   ```python
   def full_adder(a, b, carry_in):
       carry1, sum1 = half_adder(a, b)
       carry2, total = half_adder(sum1, carry_in)
       return OR(carry1, carry2), total
   ```

9. **A 4-bit adder in Python.** Add below it:
   ```python
   def add4(a_bits, b_bits):
       carry = 0
       result = ""
       for i in [3, 2, 1, 0]:
           carry, total = full_adder(int(a_bits[i]), int(b_bits[i]), carry)
           result = str(total) + result
       return str(carry) + result
   ```
   **Say:** "The bits are text, like `"0101"`, with the ones bit at the
   end, position 3. So the loop goes from the right, 3, 2, 1, 0, carrying
   as it goes, just like you do on paper."

   And at the end of the file, test it against Python's own adding for
   **every** pair of 4-bit numbers:
   ```python
   for x in range(16):
       for y in range(16):
           assert add4(f"{x:04b}", f"{y:04b}") == f"{x + y:05b}"
   print("The adding machine is right for all 256 sums!")
   print(add4("0101", "0011"))
   ```
   **They should see:** the message, then `01000` (8).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `half_adder` isn't in **Components → Custom** | The new circuit isn't saved yet, or it's in a different folder | Save the new circuit in `lab/circuits` first, next to `half_adder.dig`. Then click **Components → Custom → Update**. |
| The custom box has no labels on its pins | The half adder's inputs and outputs weren't labelled | Open `half_adder.dig`, label A, B, S and C, and save it. |
| Some full adder rows fail | A wire goes to the wrong pin of a box, or the OR is missing | Hover over a box's pins to see their names. Check the carries both go into the OR. |
| The 4-bit tests fail on some rows | A carry goes the wrong way, or two inputs are swapped | Carries go **left**, from C0 to C4. Check every label: A0 and B0 are the ones column. |
| `Test signal C0 not found in the circuit!` | An input or output has a different label | Labels must match the test's first line exactly. |
| Python: `IndexError: string index out of range` | The bits are shorter than 4, like `"101"` | Always use 4 bits: `f"{x:04b}"`, or `"0101"`. |
| Python: the adder is right except for the top bit | The final carry wasn't added to the front | It's `return str(carry) + result`. |

## Talk about it

- Why do we need full adders, not just half adders?
- What does "abstraction" mean? Where else have you used it? *(Functions
  in Python! You call `is_prime` without thinking about how it works.)*
- How would you make an 8-bit adder? *(Eight full adders, or two 4-bit
  adders chained.)*

## Challenge *(if there's time, or for next time)*

- Make an 8-bit adder in Digital out of two `adder4` boxes. How big is
  the biggest sum? *(255 + 255 = 510.)*
- Count the gates: how many XOR, AND and OR gates are in the 4-bit adder?
  *(4 full adders × (2 XOR, 2 AND, 1 OR) = 8 XOR, 8 AND, 4 OR.)* How many
  NANDs, if each gate were made of NANDs?
- In Python, make `add8` that works for any length: use `len(a_bits)`
  instead of the fixed `[3, 2, 1, 0]`.

## Checkpoint

The learner can, without help:
- [ ] Explain a full adder's truth table by counting 1s
- [ ] Build a full adder from two half adder sub-circuits and an OR
- [ ] Explain how the carries ripple in a 4-bit adder
- [ ] Test the Python adder against Python's own `+`

## Lab notebook

Draw the full adder plan and the 4-bit chain. Write "abstraction: using a
thing without needing to look inside it". Add *full adder*, *ripple
carry*, *sub-circuit* and *abstraction* to the dictionary.

## Guide's background *(optional reading)*

The full adder is the first circuit the learner builds out of their own
circuits, and the step from "gates" to "boxes made of gates" is the big
idea here. Every layer of a computer works like this: gates make adders,
adders make an arithmetic unit, that makes a processor, and so on. In
Stage 6, the Nand to Tetris course builds exactly this tower, one layer
at a time, and the learner's 4-bit adder becomes a 16-bit one.

The ripple carry adder is simple but slow, because each column must wait
for the carry from the one before. Real processors use cleverer "carry
lookahead" designs, which work out the carries in parallel. Digital's
examples folder has one (`FullAdderCLA.dig`) for a curious learner.

The Python version follows the circuit exactly: `full_adder` is two
`half_adder` calls and an `OR`, and `add4` is the chain of four. Testing
it against all 256 possible pairs of 4-bit inputs is an **exhaustive
test**: for small inputs, you can check every single case, which really
does prove the function correct for 4 bits.
