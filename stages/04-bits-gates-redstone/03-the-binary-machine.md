# Lesson 4.3: The Binary Machine

**Time:** 2 sessions of 45 min · **You need:** Thonny; squared paper ·
**New words:** convert, algorithm (again), remainder

## Goal *(read this to the learner)*

> Python's `bin()` can turn numbers into binary, but how does it do it?
> Today you'll work out the trick on paper, then build your own binary
> machine that turns numbers into binary and back again, with tests to
> prove it's right. Then you'll turn it into a quiz game to beat your
> family with.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Try step 1 on paper yourself with the number 13.

## Warm-up (5 min)

"What's 13 divided by 2?" *(6, remainder 1.)* "What's 6 divided by 2?"
*(3, remainder 0.)* "Which numbers have a remainder of 1 when you divide
by 2?" *(The odd ones.)* In Python: `13 // 2` and `13 % 2`.

## Activity

### Session 1: number to binary

1. **The halving trick, on paper.** Turn 13 into binary by halving and
   writing down the remainders:

   ```
   13 ÷ 2 = 6  remainder 1
    6 ÷ 2 = 3  remainder 0
    3 ÷ 2 = 1  remainder 1
    1 ÷ 2 = 0  remainder 1      stop at 0
   ```

   Now read the remainders from the **bottom up**: `1101`. Check it with
   the dot cards: 8 + 4 + 1 = 13. ✓

   **Say:** "Each remainder tells you whether the number was odd, which is
   the last bit. Halving chops that bit off, so the next remainder is the
   next bit along. That's why they come out backwards." Try 6 and 25 on
   paper. *(110 and 11001.)*

2. **Teach Python the trick.** New file,
   `~/lab/python/binary/binary_machine.py`:
   ```python
   def to_binary(n):
       if n == 0:
           return "0"
       bits = ""
       while n > 0:
           bits = str(n % 2) + bits
           n = n // 2
       return bits

   print(to_binary(13))
   ```
   **They should see:** `1101`.

   **Say:** "`n % 2` is the remainder. `str` turns it into text, and we put
   it on the **front** of `bits`, so the bits come out the right way round
   without reading backwards. `n // 2` is the halving."

3. **Test it.** Replace the `print` line with tests. Each `assert` checks
   one answer, like in Lesson 3.5:
   ```python
   assert to_binary(0) == "0"
   assert to_binary(1) == "1"
   assert to_binary(13) == "1101"
   assert to_binary(255) == "11111111"
   for n in range(1000):
       assert to_binary(n) == f"{n:b}"
   print("All the to_binary checks passed!")
   ```
   **They should see:** `All the to_binary checks passed!`

   **Say:** "That last loop checks our machine against Python's own, for
   a thousand numbers. If even one were different, the program would stop
   with an `AssertionError`."

   Break it on purpose: change `n % 2` to `n % 3`. Run it. **They should
   see:** `AssertionError`. Put it back.

### Session 2: binary to number, and a quiz

4. **The doubling trick, on paper.** To read `1101`, start at 0, and for
   each bit from the left: **double, then add the bit**.

   ```
   start          0
   bit 1:  0 × 2 + 1 = 1
   bit 1:  1 × 2 + 1 = 3
   bit 0:  3 × 2 + 0 = 6
   bit 1:  6 × 2 + 1 = 13
   ```

   **Say:** "It's the halving trick backwards. Each time you double, every
   bit you've already read moves one place to the left." Try `11001`.
   *(25.)*

5. **Add it to the machine.** Add this function below `to_binary`, above
   the tests:
   ```python
   def from_binary(bits):
       total = 0
       for bit in bits:
           total = total * 2 + int(bit)
       return total
   ```
   And add tests at the end:
   ```python
   assert from_binary("1101") == 13
   assert from_binary("11111111") == 255
   for n in range(1000):
       assert from_binary(to_binary(n)) == n
   print("All the from_binary checks passed!")
   ```
   **Say:** "The last test is a round trip: turn a number into binary and
   back, and you must get the same number. If both machines are right,
   they undo each other."

6. **The Binary Quiz.** New file, `~/lab/python/binary/quiz.py`. It uses
   the machine's functions by **importing** them:
   ```python
   import random
   from binary_machine import to_binary, from_binary

   score = 0
   for question in range(5):
       n = random.randint(1, 31)
       if random.randint(1, 2) == 1:
           answer = input(f"What is {n} in binary? ")
           right = to_binary(n)
       else:
           answer = input(f"What is {to_binary(n)} as a number? ")
           right = str(n)
       if answer.strip() == right:
           print("Correct!")
           score += 1
       else:
           print(f"Not quite. It was {right}.")
   print(f"You scored {score} out of 5.")
   ```
   **They should see:** the two "checks passed" messages first, and then
   five questions.

   **Say:** "`from binary_machine import ...` borrows the functions from
   the other file, as long as it's in the same folder. When Python
   imports a file, it runs the whole thing, so the tests run too. That's
   why you see the messages: a free check every time!"

   Play it. Then the learner tests the family.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `to_binary(13)` gives `1011` | The bits are added to the end instead of the front | It's `bits = str(n % 2) + bits`, with `bits` last. |
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | `n % 2` without `str(...)`: a number and some text can't be added | Wrap it: `str(n % 2)`. |
| A very long answer full of `0.5`s and dots | `n / 2` instead of `n // 2`, so `n` becomes a decimal | Use `//`, whole-number division. |
| `ModuleNotFoundError: No module named 'binary_machine'` | `quiz.py` isn't in the same folder, or the file has a different name | Both files must be in `~/lab/python/binary/`, and the name must match exactly (no `.py` in the `import` line). |
| `from_binary("12")` gives 4, with no error | 2 isn't a binary digit, but the function doesn't check | That's not binary! The challenge fixes this. |
| `AssertionError` on the `range(1000)` line | One of the functions gives a wrong answer for some number | Print a few: `print(n, to_binary(n), f"{n:b}")` inside the loop, before the `assert`, to find the first one that's different. |

## Talk about it

- Why do the remainders come out backwards?
- What does the round-trip test prove? *(That the two machines undo each
  other, for every number tested.)*
- Our tests checked 1000 numbers. Does that prove the machine works for
  *every* number? *(No, but it makes us very confident. Proving it for
  all numbers needs maths: Stage 7!)*

## Challenge *(if there's time, or for next time)*

- Make `from_binary` refuse anything that isn't binary: if a character
  isn't `"0"` or `"1"`, `return None`. Add a test for it.
- Make the quiz harder as you score: numbers up to 31, then 63, then 255.
- Change the machine to work in **base 3** (digits 0, 1, 2). What do you
  need to change? *(Every 2 becomes a 3.)* What's 100 in base 3? *(10201.)*

## Checkpoint

The learner can, without help:
- [ ] Turn a number into binary by halving, and binary into a number by
      doubling, on paper
- [ ] Explain how `to_binary` uses `%` and `//`
- [ ] Write `assert` tests, including a round-trip test
- [ ] Import a function from their own file

## Lab notebook

Copy both paper methods with one example each. Write the best quiz
score of everyone in the family. Add *convert* and *round trip* to the
dictionary.

## Guide's background *(optional reading)*

These are the two standard algorithms for converting between bases, and
they work for any base, not just 2. Halving with remainders peels off
the lowest digit each time; doubling and adding builds the number from
the highest digit down. (The second one is sometimes called Horner's
method.)

The round-trip test is a very useful habit. When you have two functions
that should undo each other (encode and decode, save and load, encrypt
and decrypt) testing that "decode(encode(x)) == x" for lots of `x`
catches most bugs, without having to work out every answer by hand. The
Caesar cipher from Lesson 3.9 could be tested the same way.

`import` lets one file use another's functions. Python runs the imported
file once, which is why the tests print their messages. Programmers
usually hide tests behind `if __name__ == "__main__":` so they don't run
on import; there's no need to introduce that yet.
