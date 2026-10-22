# Lesson 4.2: The Doubling Machine

**Time:** 2 sessions of 40 min · **You need:** Thonny; a chessboard (or
a drawing of one); a cup of rice or dried beans (optional) · **New
words:** power, exponent, kilobyte

## Goal *(read this to the learner)*

> 1, 2, 4, 8, 16... Doubling starts small and then goes completely wild.
> Today you'll find out how big doubling gets, why a Minecraft stack is
> 64, how many guesses you need to find a number up to a million, and
> what "kilobyte" really means.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] If you're doing the rice demonstration, put a small pile on a plate
      next to the chessboard.

## Warm-up (5 min)

"What are the place values in a byte?" *(128, 64, 32, 16, 8, 4, 2, 1.)*
"What's the pattern?" *(Each is double the one to its right.)*

## Activity

### Session 1: powers of two

1. **The doubling table.** On paper, the learner writes two columns and
   fills them in by doubling, as far as they can without a computer:

   ```
   times doubled    number
        0              1
        1              2
        2              4
        3              8
       ...            ...
       10            1024
   ```

   **Say:** "Doubling 1 four times gives 16. Mathematicians write that as
   2⁴, 'two to the power of four'. The small raised number is the
   **exponent**: how many 2s are multiplied together. 2 × 2 × 2 × 2 = 16."

2. **Python's power button.** In the Shell:
   ```python
   2 ** 4
   2 ** 10
   2 ** 8
   ```
   **They should see:** `16`, `1024`, `256`. **Say:** "Two stars is 'to
   the power of'." Check every row of the paper table.

3. **The chessboard story.** Tell it (or read it):

   > Long ago, a clever inventor showed a king the game of chess. The king
   > was so pleased that he said, "Name your reward!" The inventor said,
   > "Just some rice, please. Put one grain on the first square of the
   > board, two on the second, four on the third, and keep doubling to the
   > last square." The king laughed. "Only rice? Done!"

   If you have rice, start putting grains on the squares together. Stop
   when it gets silly (around square 7 or 8). "Do you think the king can
   pay?" Then find out. New file, `~/lab/python/binary/chessboard.py`:
   ```python
   total = 0
   for square in range(1, 65):
       grains = 2 ** (square - 1)
       total = total + grains
       print(f"Square {square}: {grains} grains")
   print(f"Total: {total} grains")
   ```
   **They should see:** the last square has
   `9223372036854775808` grains, and the total is
   `18446744073709551615`.

   **Say:** "That's about 18 **quintillion** grains: more rice than the
   whole world has ever grown. The king could not pay! Doubling is
   called **exponential** growth, and it always surprises people."

4. **Spot something.** Look at the total: `18446744073709551615`. Then in
   the Shell: `2 ** 64`. *(18446744073709551616: one more!)* **Say:** "The
   total of all the squares is always one less than the next square.
   1 + 2 + 4 = 7, one less than 8. That's the same as binary: `111` is
   7, and `1000` is 8."

### Session 2: doubling and halving everywhere

5. **How many numbers do bits make?** Fill in this table together, using
   the dot cards if needed:

   | Bits | Different numbers | Biggest |
   |---|---|---|
   | 1 | 2 | 1 |
   | 2 | 4 | 3 |
   | 3 | 8 | 7 |
   | 4 | 16 | 15 |
   | 8 | 256 | 255 |
   | 16 | 65,536 | 65,535 |

   **Say:** "Every extra bit **doubles** how many numbers you can make.
   With `n` bits you get `2 ** n` numbers, from 0 to `2 ** n - 1`."

6. **Powers of two in games.** Talk about where they turn up:
   - A Minecraft stack holds **64** (2⁶) blocks.
   - A Minecraft chunk is **16 × 16** blocks. Luanti stores its world in
     blocks of **16 × 16 × 16**.
   - Each colour in a colour code (Stage 2) goes from 0 to **255**: one
     byte each for red, green and blue.
   - Old games had 8-bit and 16-bit consoles: the size of the numbers
     their processors worked with.

7. **Halving.** **Say:** "Doubling's opposite is halving. Remember the
   guessing game in Stage 3? Guessing the middle each time halves the
   numbers that are left." New file, `~/lab/python/binary/halving.py`:
   ```python
   n = int(input("Numbers from 1 to: "))
   halvings = 0
   while n > 1:
       n = n // 2
       halvings = halvings + 1
   print(f"About {halvings} halvings, so at most {halvings + 1} guesses.")
   ```
   Try 100 *(6 halvings, at most 7 guesses)*, 1000 *(9 halvings, 10
   guesses)* and 1000000 *(19 halvings, 20 guesses)*.

   **Say:** "A million numbers, and you only need 20 guesses! That's the
   other side of the doubling magic: 20 doublings make a million, so 20
   halvings get you back down to 1."

8. **Kilobytes.** In the terminal:
   ```
   ls -l /etc/services
   ls -lh /etc/services
   ```
   **They should see:** the size in bytes, then the same size with a `K`
   after it. **Say:** "On computers, 'kilo' usually means 1024, not 1000,
   because 1024 is 2¹⁰. A **kilobyte** is 1024 bytes, a megabyte is 1024
   kilobytes, and a gigabyte is 1024 megabytes." In Python:
   `2 ** 30` *(1073741824 bytes in a gigabyte)*.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `2 ^ 4` gives `6` | `^` isn't "power" in Python (it's something you'll meet in Lesson 4.6) | Use `2 ** 4`. |
| The chessboard numbers start at 2, not 1 | `2 ** square` instead of `2 ** (square - 1)` | The first square is 2⁰ = 1. Check the brackets. |
| `halving.py` says 7 halvings for 100, not 6 | `n / 2` makes decimals like 1.5625, so it takes one extra halving to get below 1 | Use `//`, whole-number division. |
| `ValueError: invalid literal for int()` | Something that isn't a whole number was typed, like `1,000` | Type `1000`, with no comma. |

## Talk about it

- Would you rather have a million coins now, or 1 coin on the first day
  of the month, doubled every day? *(On day 30 alone you'd get over 500
  million coins.)*
- Why does every extra bit double how many numbers you can make?
- How many guesses would a number from 1 to a billion need? *(About 30.)*

## Challenge *(if there's time, or for next time)*

- Find the first power of two bigger than a million. *(2²⁰ = 1,048,576.)*
- Python's `n.bit_length()` tells how many bits a number needs. Try
  `(255).bit_length()` and `(256).bit_length()`. Why the jump?
- Halve backwards: start with 1 and double until you pass the number of
  people in the world (about 8 billion). How many doublings?

## Checkpoint

The learner can, without help:
- [ ] Write the powers of two up to 2¹⁰ = 1024
- [ ] Use `**` in Python
- [ ] Say how many numbers `n` bits can make, and the biggest one
- [ ] Explain why halving finds a number quickly

## Lab notebook

Copy the doubling table to 2¹⁰. Draw the chessboard and write the total.
Write "1 kilobyte = 1024 bytes". Add *power*, *exponent* and *kilobyte* to
the dictionary.

## Guide's background *(optional reading)*

Powers of two are the times tables of computing. Because each bit doubles
the number of possible values, memory sizes, colour depths and screen
sizes tend to be powers of two or sums of them.

Halving is the same idea backwards, and it's what makes *binary search*
(the guessing strategy from Lesson 3.2) so fast: the number of guesses
grows with the number of *bits* needed, not with the size of the range.
Mathematicians call "how many times can I halve this" the **logarithm**,
and the learner will meet it properly in Stage 7. There's no need to use
the word yet.

The "kilo = 1024" convention is a bit messy in real life: hard-drive
makers use 1000, and the strict names for the 1024 versions are kibibyte
(KiB), mebibyte (MiB) and so on. `ls -lh` uses 1024.
