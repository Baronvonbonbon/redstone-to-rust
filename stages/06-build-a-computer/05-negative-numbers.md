# Lesson 6.5: Negative Numbers in Binary

**Time:** 2 sessions of 40 min · **You need:** paper and pencil; Thonny;
a clock face drawn on paper (see below) · **New words:** negative,
two's complement, sign bit, overflow

## Goal *(read this to the learner)*

> Minecraft's world goes down to y = −64. Bank balances go below zero.
> But a computer only has 0s and 1s, with no minus sign. So how does it
> store −64? The answer is a clever trick called **two's complement**,
> and it's so clever that the computer can subtract using only an adder.
> Today you'll learn the trick, prove it works on paper and in Python,
> and find out what happens when a number gets too big.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] The learner should be comfortable with negative numbers (adding
      and subtracting them on a number line). If not, spend a session on
      that first: it's the math for this stage.
- [ ] Draw a big circle on paper with 16 marks around it, like a clock
      with 16 hours. Label the top `0000`, and go clockwise: `0001`,
      `0010`, ..., all the way round to `1111`, next to `0000`.

## Warm-up (5 min)

"What's 5 + (−5)?" *(0.)* "What's 3 − 7?" *(−4.)* "If a car's
odometer shows `000` and you drive backwards one mile, what does it
show?" *(`999`.)*

## Activity

### Session 1: the trick

1. **The odometer.** **Say:** "A three-digit odometer that goes backwards
   from `000` shows `999`. So `999` is acting like −1. Let's check: what's
   `999 + 1` on the odometer?" *(`1000`, but there are only three digits,
   so it shows `000`. Just like −1 + 1 = 0!)* "What would −2 be?" *(`998`.)*

2. **The binary clock.** Use the 16-mark circle. **Say:** "This is a
   4-bit computer. Counting up goes clockwise. What's one step
   *anticlockwise* from `0000`?" *(`1111`.)* "So `1111` is −1. What's −2?"
   *(`1110`.)* Label the left half of the circle with −1 to −8, going
   anticlockwise from the top, and the right half with 0 to 7.

   **They should see:** every number whose left-hand bit is 1 is
   negative. **Say:** "That left bit is called the **sign bit**. 0 means
   positive (or zero), 1 means negative. This way of storing numbers is
   called **two's complement**."

3. **Making a number negative.** **Say:** "Here's the rule for turning a
   number into its negative: **flip every bit, then add 1**." Try it with
   5 in 4 bits:
   ```
     5        0101
     flip     1010
     add 1    1011     <- that's -5
   ```
   Check on the clock: `1011` is five steps anticlockwise from `0000`.
   Then try 3 and 7. And the other way: flip `1011` and add 1. *(`0101`,
   5 again!)*

4. **Why it's magic: subtraction with an adder.** **Say:** "6 − 2 is the
   same as 6 + (−2). Let's add them in binary, exactly like in Lesson
   4.10."
   ```
       0110      (6)
     + 1110      (-2)
     ------
      10100
   ```
   **Say:** "Only 4 bits fit, so the extra 1 on the left falls off the end,
   like the odometer. What's left?" *(`0100`: 4. Correct!)* "The computer
   never needs a subtracting circuit. It flips the bits, adds 1, and uses
   the adder you already know how to build."

   Try `0101 + 1011` (5 + −5). *(`10000`: drop the extra 1, and it's
   `0000`. Zero!)*

### Session 2: 16 bits, Python, and overflow

5. **The Hack computer's numbers.** **Say:** "Hack uses 16 bits, so the
   clock has 65,536 marks. Half are negative." Work out together:
   - the biggest positive number: `0111111111111111` *(32767)*
   - the most negative: `1000000000000000` *(−32768)*
   - −1: *(all sixteen bits are 1)*

6. **Python checks the trick.** New file in Thonny,
   `~/lab/python/binary/negative.py`:
   ```python
   def to_bits(n):
       """A number from -32768 to 32767, as 16 bits in two's complement."""
       if n < 0:
           n = n + 65536
       return format(n, "016b")

   def from_bits(bits):
       """16 bits in two's complement, back to an ordinary number."""
       n = int(bits, 2)
       if bits[0] == "1":
           n = n - 65536
       return n

   print(to_bits(5))
   print(to_bits(-5))
   print(to_bits(-1))
   print(from_bits("1111111111111011"))

   for n in [0, 1, -1, 100, -100, 32767, -32768]:
       assert from_bits(to_bits(n)) == n
   print("All the round trips work!")
   ```
   Run it. **They should see:**
   ```
   0000000000000101
   1111111111111011
   1111111111111111
   -5
   All the round trips work!
   ```
   **Say:** "Adding 65,536 is going once round the clock. A negative number
   lands on the left half of the circle, exactly where the flip-and-add-1
   trick puts it." Check that `to_bits(-5)` is `to_bits(5)` with every
   bit flipped, plus 1.

7. **Overflow.** In the Shell:
   ```python
   >>> from_bits(to_bits(32767 + 1))
   ```
   **They should see:** `-32768`. **Say:** "Add 1 to the biggest number,
   and you go round the clock to the most negative. That's called
   **overflow**. The computer doesn't notice: it just keeps the 16 bits."

   Real story: in the arcade game *Pac-Man*, the level number was kept in
   8 bits. At level 256, it overflowed, and half the screen turned into
   garbage. Nobody could finish that level.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| A negative number comes out positive on paper | The "add 1" step was forgotten | Flip, *then* add 1. Check: the number plus its negative should make all zeros (with a carry off the end). |
| Adding gives a 5-bit answer | That's normal: the extra bit falls off | Cross out the leftmost bit; keep the right 4 (or 16). |
| `ValueError: invalid literal for int() with base 2` | The bits string has something other than 0s and 1s, like a space | `from_bits("1111111111111011")`, no spaces. |
| The round-trip `assert` fails for 32768 | 32768 is too big for 16-bit two's complement | Only −32768 to 32767 fit. That's the overflow lesson! |

## Talk about it

- What is the sign bit?
- Why can a computer subtract using only an adder?
- What's overflow? Where else might it cause trouble?

## Challenge *(if there's time, or for next time)*

- Write `negate(bits)` in Python that flips every bit and adds 1, working
  only with the string of bits (no `to_bits`). Test it against
  `to_bits(-n)` with `assert`s.
- In 8 bits, what are the biggest and smallest numbers? *(127 and −128.)*
- Minecraft keeps some numbers in 32 bits. What's the biggest positive
  32-bit number? *(2,147,483,647.)*

## Checkpoint

The learner can, without help:
- [ ] Turn a small number into its negative in 4 bits, and back
- [ ] Say which 16-bit patterns are negative, and the range of 16-bit numbers
- [ ] Show 6 − 2 as an addition in binary
- [ ] Explain overflow

## Lab notebook

Glue in the binary clock. Write: "To make a number negative, ..." in
their own words. Commit `negative.py`. Add *two's complement*, *sign
bit* and *overflow* to `dictionary.md`.

## Guide's background *(optional reading)*

In **two's complement**, the leftmost bit has a *negative* weight: in 4
bits, the place values are −8, 4, 2, 1, so `1011` is −8 + 2 + 1 = −5.
That's another way to read negative numbers, if the learner likes it.
The scheme is used by essentially every computer because addition works
the same for positive and negative numbers, and there's only one zero.

The next two lessons use this directly: Inc16 adds 1, and the ALU
(Lesson 6.7) computes `x − y` by flipping and adding, with no
subtraction circuit at all. Its `ng` output is just the sign bit.

Overflow bugs are real and sometimes serious: the Pac-Man "kill
screen", and the "Year 2038 problem", when 32-bit clocks that count
seconds since 1970 run out. A good discussion question for an older
learner.
