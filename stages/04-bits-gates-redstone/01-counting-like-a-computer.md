# Lesson 4.1: Counting Like a Computer

**Time:** 2 sessions of 40 min · **You need:** the dot cards from Lesson
0.6 (or 8 new index cards); squared paper; Thonny · **New words:** place
value, base, bit, byte

## Goal *(read this to the learner)*

> Way back in Stage 0 you learned the computer's secret way of counting,
> with dot cards and finger binary. Now you know Python, so you can make
> the computer show you its own numbers. By the end of today you'll be
> able to read and write any number up to 255 in binary, and you'll know
> why a byte stops at 255.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Find the dot cards from Lesson 0.6 (1, 2, 4, 8 and 16 dots). Make
      three more: **32, 64 and 128**. You don't have to draw 128 dots:
      write the number big, and draw the dots as 8 rows of 16 if you like.
- [ ] Make a folder for this stage, as the learner:
      `mkdir -p ~/lab/python/binary`

## Warm-up (5 min): finger binary

"Show me 5 on finger binary." *(Thumb and middle finger: 1 + 4.)* Then
6, 9 and 31. "What's the biggest number on one hand?" *(31.)*

## Activity

### Session 1: places and bits

1. **How our numbers work.** Write `352` big on paper. **Say:** "What
   does the 3 mean?" *(Three hundreds.)* "The 5?" *(Five tens.)* "The 2?"
   *(Two ones.)* Draw boxes over the digits:

   ```
   [hundreds] [tens] [ones]
        3        5      2      = 300 + 50 + 2
   ```

   **Say:** "Each place is worth **ten times** the place to its right.
   That's called **place value**. If you watch Numberblocks, it's how One
   Hundred is made of ten Tens. Because we use ten digits, 0 to 9, our
   numbers are called **base ten**."

2. **Binary has places too.** Lay out all 8 dot cards, biggest on the
   left:

   ```
   [128] [64] [32] [16] [8] [4] [2] [1]
   ```

   **Say:** "In binary, each place is worth **two times** the place to its
   right. And there are only two digits, 0 and 1. So binary is **base
   two**." Make 100 with the cards. *(64 + 32 + 4, so `01100100`.)* Then
   make 42 and 200.

3. **Bits and bytes.** **Say:** "Each 0 or 1 is a **bit**. Eight bits
   together is a **byte**." On squared paper, draw a row of 8 boxes with
   the place values above them. That's a byte. Fill it with all 1s. "What
   number is that?" *(128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255.)* **Say:**
   "So one byte can hold any number from 0 to 255. That's 256 different
   numbers. Remember 255; you'll see it everywhere."

4. **Python knows binary.** Open Thonny. In the Shell:
   ```python
   bin(5)
   bin(100)
   bin(255)
   0b101
   0b11111111
   int("1100100", 2)
   ```
   **They should see:** `'0b101'`, `'0b1100100'`, `'0b11111111'`, then
   `5`, `255` and `100`.

   **Say:** "`bin` turns a number into binary writing. The `0b` at the
   front is Python's way of saying 'this is binary, not an ordinary
   number'. Typing `0b101` gives you the number 5. And
   `int("1100100", 2)` reads the text as base 2." Check the cards from
   step 2 the same way: `bin(42)`, `bin(200)`.

### Session 2: counting machine

5. **A counting machine.** New file, saved as
   `~/lab/python/binary/count.py`:
   ```python
   for n in range(32):
       print(n, f"{n:05b}")
   ```
   **They should see:** 32 lines, from `0 00000` to `31 11111`.

   **Say:** "`:05b` inside an f-string means: show this number in
   **b**inary, **5** places wide, filling the empty places with **0**s.
   Compare it with your table from Stage 0."

6. **Spot the patterns.** Look down each column of bits:
   - The right-hand bit goes 0, 1, 0, 1... "Which numbers end in 1?"
     *(The odd ones! A number is odd exactly when its last bit is 1. That's
     the `% 2` remainder from Stage 3.)*
   - The next bit goes 0, 0, 1, 1, 0, 0, 1, 1... and the next in fours.
   - Change `32` to `256` and `05b` to `08b`. Scroll to the end. **They
     should see:** `255 11111111`.

7. **Times two is easy.** In the Shell:
   ```python
   bin(5)
   bin(10)
   bin(20)
   bin(40)
   ```
   **They should see:** `0b101`, `0b1010`, `0b10100`, `0b101000`.

   **Say:** "In our numbers, times ten puts a 0 on the end: 5, 50, 500.
   In binary, times **two** puts a 0 on the end. Computers love doubling
   and halving for exactly this reason."

8. **Finger binary speed round.** The guide calls a number from 0 to 31;
   the learner shows it on one hand as fast as they can. Then swap: the
   learner shows, the guide reads it.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ValueError: invalid literal for int() with base 2: '102'` | The text has a digit that isn't 0 or 1 | Binary only uses 0 and 1. |
| `SyntaxError: invalid digit '2' in binary literal` | `0b102` was typed | Same thing: only 0 and 1 after `0b`. |
| `TypeError: 'str' object cannot be interpreted as an integer` | `bin("5")`, with quotes | `bin` wants a number: `bin(5)`. |
| `int("101")` gives 101, not 5 | Without the `, 2`, Python reads it as an ordinary number | `int("101", 2)`. |
| The counting machine prints `0 0`, `1 1`, `2 10`... with no zeros in front | The `05` is missing | It's `{n:05b}`: a zero, then the width. |

## Talk about it

- Our numbers have ten digits and binary has two. What would a number
  system with eight digits look like? *(Places worth 1, 8, 64... It's
  called octal, and it exists!)*
- Why is the biggest byte 255 and not 256? *(Because 0 counts too: 0 to
  255 is 256 numbers.)*
- How can you tell from the binary if a number is odd?

## Challenge *(if there's time, or for next time)*

- Finger binary on **two** hands: the left thumb is 32. What's the
  biggest number now? *(1023.)*
- Write your age, the year, and your house number in binary. Check them
  with `bin`.
- Make `count.py` count down from 31 to 0 instead. *(`range(31, -1, -1)`.)*

## Checkpoint

The learner can, without help:
- [ ] Explain place value in base ten and base two
- [ ] Turn an 8-bit number into an ordinary number, and back, with the
      cards or on paper
- [ ] Use `bin()` and `int(..., 2)` to check their answers
- [ ] Say what a bit and a byte are, and the biggest number a byte holds

## Lab notebook

Draw the byte boxes with their place values. Write 42, 100 and 255 in
binary. Add *place value*, *base*, *bit* and *byte* to the dictionary.

## Guide's background *(optional reading)*

Every number system with place value works the same way; only the
"base" changes. In base ten the places are 1, 10, 100, 1000 (powers of
ten). In base two they are 1, 2, 4, 8, 16 (powers of two). The learner
already knows this from Stage 0; this lesson connects it to the place
value they meet in maths, and to Python.

A byte is 8 bits by long tradition, and it's the size most computers use
for one small number, one letter, or one colour channel of one pixel.
That's why 255 shows up so often: colour codes, IP addresses and file
formats are full of bytes.

The f-string format `{n:05b}` is a small new piece of Python; there's no
need to explain the format mini-language beyond "b means binary, 05
means five places, filled with zeros".
