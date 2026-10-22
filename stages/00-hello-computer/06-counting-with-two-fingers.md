# Lesson 0.6: Counting with Two Fingers

**Time:** 40 min · **You need:** 5 index cards, a marker, pencil and paper.
No computer · **New words:** binary, bit, digit

## Goal *(read this to the learner)*

> Inside a computer there are only two kinds of signals: ON and OFF. Like
> a light switch. That's all! So how does a computer count to a million?
> Today you'll learn its secret way of counting, called **binary**.

## Before the lesson *(guide, 10 min)*

- [ ] Make 5 **dot cards**. On the front of each card, draw dots: **1, 2,
      4, 8 and 16** (draw the dots in neat groups, so they're easy to
      count). Leave the backs blank.
- [ ] Practise once yourself: lay them out in a row, biggest on the
      **left**:

      ```
      [16]  [8]  [4]  [2]  [1]
      ```

      Showing dots means 1 (ON); turned face down means 0 (OFF).

## Warm-up (5 min)

Look at the cards together, smallest first: 1, 2, 4, 8... "What's the
pattern? What would the next card be?" *(Each one is double the one
before, so the next is 32.)* If your learner watches **Numberblocks**:
"These are like Numberblocks that keep doubling: One, Two, Four, Eight,
Sixteen!"

## Activity

1. **Make numbers.** Start with every card face down. "Show me 5 dots,
   using only these cards. You can't use a card twice." *(4 + 1 face up.)*
   Then do 3, 6, 10 and 15.

2. **Write it in binary.** For each number, write a **1** under each
   face-up card and a **0** under each face-down card:

   ```
   [16] [8] [4] [2] [1]
     0   0   1   0   1      = 5
   ```

   Say: "**00101** is how a computer writes 5. Each 1 or 0 is called a
   **bit**."

3. **Count up.** Count from 0 to 15 together, flipping cards. Write each
   one down in a table:

   ```
   0  = 00000      4 = 00100      8 = 01000     12 = 01100
   1  = 00001      5 = 00101      9 = 01001     13 = 01101
   2  = 00010      6 = 00110     10 = 01010     14 = 01110
   3  = 00011      7 = 00111     11 = 01011     15 = 01111
   ```

   Point out the pattern: the 1s card flips *every* time, the 2s card
   every second time, the 4s card every fourth time...

4. **Mystery numbers.** You write a binary number; they turn it into
   ordinary numbers using the cards. Try `01001` *(9)*, `10000` *(16)*,
   `10101` *(21)* and `11111` *(31)*.

5. **The biggest number.** "What's the biggest number with these 5
   cards?" *(31, with all of them face up.)* "What if we added a 32 card?"
   *(63.)*

6. **Finger binary** *(the fun bit!)*. On one hand, the thumb is 1, the
   pointer is 2, the middle finger is 4, the ring finger is 8 and the
   pinky is 16. Raised means 1. Count to 31 on one hand! (Careful with 4:
   only the middle finger up. Giggling is allowed.)

## If something goes wrong

| What happens | What to do |
|---|---|
| Uses a card twice (two 4s for 8) | "Each card only once. Is there a card that already has 8 dots?" |
| Writes the bits backwards | Keep the cards on the table, biggest on the left, and write under them. |
| Finds it too easy | Jump to the challenge. |

## Talk about it

- Why might a computer use only 0 and 1? *(Its tiny switches can only be
  ON or OFF.)*
- How many different numbers can 5 cards make? *(32: from 0 up to 31.)*
- Our normal numbers use ten digits (0 to 9). Binary uses how many? *(Two.)*

## Challenge

- Add a 32 card and a 64 card. What's `1100100`? *(100!)*
- Write your age, and today's date, in binary.
- A **byte** is 8 bits. What's the biggest number one byte can hold? *(255.)*

## Checkpoint

The learner can, without help:
- [ ] Count from 0 to 15 in binary using the cards
- [ ] Turn a 5-bit binary number into an ordinary number

## Lab notebook

Copy the 0 to 15 table. Write your age in binary. Draw finger binary
for your favourite number.

## Guide's background *(optional reading)*

Our normal numbers are "base 10": each place is worth ten times the place
to its right (ones, tens, hundreds). Binary is "base 2": each place is
worth *two* times the place to its right (ones, twos, fours, eights). The
dot cards make that visible.

Computers use binary because a wire either has electricity on it or
doesn't, and a switch is either on or off. Two states are easy to build
reliably. One binary digit is a **bit**, and 8 bits make a **byte**.
Everything a computer stores (numbers, letters, pictures, music) is
eventually just patterns of bits. Stage 4 builds on this directly, and
in Stage 6 your learner will build circuits that add binary numbers.
