# Lesson 3.5: Functions That Answer Back

**Time:** 45 min · **You need:** Thonny · **New words:** return, test,
assert

## Goal *(read this to the learner)*

> In Stage 2, your functions *did* things: drew a house, drew a polygon.
> Today your functions will *answer* things: "is this number even?",
> "what's double this?". And you'll learn how programmers check that their
> functions give the right answers, automatically.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min): FizzBuzz, out loud

Take turns counting from 1. But if a number can be divided by 3, say
"Fizz" instead; if it can be divided by 5, say "Buzz"; and if both, say
"FizzBuzz". (1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14,
FizzBuzz...) Whoever gets it wrong starts again from 1. Later in the
lesson, Python plays it perfectly.

## Activity

1. **A function that gives back an answer.** New file,
   `~/lab/python/stage3/answers.py`:
   ```python
   def double(n):
       return n * 2

   print(double(5))
   print(double(21))
   big = double(double(double(1)))
   print(big)
   ```
   **They should see:** `10`, `42`, `8`.

   **Say:** "`return` means 'here's the answer, take it back to whoever
   asked'. The call `double(5)` turns into the answer, 10, right there in
   the line. So you can print it, store it in a box, or even feed it into
   another `double`."

2. **Printing isn't returning.** Add:
   ```python
   def say_double(n):
       print(n * 2)

   answer = say_double(5)
   print("The answer box holds:", answer)
   ```
   **They should see:** `10`, then `The answer box holds: None`.

   **Say:** "`say_double` *shows* the answer on the screen, but doesn't
   *give it back*. So `answer` gets `None`, Python's word for 'nothing'.
   Showing is for people. Returning is for the rest of the program."

3. **Functions that answer yes or no.**
   ```python
   def is_even(n):
       return n % 2 == 0

   print(is_even(4))
   print(is_even(7))
   ```
   **Say:** "`n % 2 == 0` is a question with a `True` or `False` answer,
   so we can return it directly. Functions that answer yes or no usually
   have names starting with `is_`."

4. **Checking with `assert`.** Add:
   ```python
   assert double(5) == 10
   assert is_even(4)
   assert not is_even(7)
   print("All the checks passed!")
   ```
   Run it: nothing new happens except the message. Now add a wrong check:
   ```python
   assert double(5) == 11
   ```
   **They should see:** `AssertionError`, pointing at that line.

   **Say:** "`assert` means 'I'm sure this is true. If it isn't, stop and
   tell me!' Programmers write lots of these, called **tests**, so the
   computer checks their functions every time. If you change a function
   later and break it, a test catches it." Delete the wrong check.

5. **FizzBuzz.** New file, `fizzbuzz.py`. First, the tests: what *should*
   the answers be?
   ```python
   def fizzbuzz(n):
       if n % 3 == 0:
           return "Fizz"
       elif n % 5 == 0:
           return "Buzz"
       elif n % 15 == 0:
           return "FizzBuzz"
       else:
           return str(n)

   assert fizzbuzz(1) == "1"
   assert fizzbuzz(3) == "Fizz"
   assert fizzbuzz(5) == "Buzz"
   assert fizzbuzz(15) == "FizzBuzz"
   print("All tests passed!")

   for n in range(1, 101):
       print(fizzbuzz(n))
   ```
   Run it. **They should see:** an `AssertionError` on the `fizzbuzz(15)`
   line.

   **Say:** "There's a bug, on purpose, and the test caught it! What does
   `fizzbuzz(15)` give back? Use the Shell to find out." *(It gives
   `"Fizz"`.)* "Why?" Let them work it out. *(15 can be divided by 3, so
   the first `if` is true and it returns `"Fizz"` straight away. The
   `n % 15` check never gets a chance.)*

   The fix: move the `n % 15` check to the top. Run it again: all tests
   pass, then 100 lines of perfect FizzBuzz.

   **Say:** "`return` leaves the function immediately. That's why the
   order of the checks matters."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| A function call gives `None` | The function has no `return` (or it prints instead of returning) | Add `return` with the answer. |
| `AssertionError` | A test failed: the function gave a different answer from the one you expected | Call the function in the Shell to see what it really returns. Then decide: is the function wrong, or the test? |
| Lines after `return` never run | `return` leaves the function straight away | Put `return` last, or move the lines above it. |
| `SyntaxError: 'return' outside function` | `return` isn't indented inside a `def` | Indent it. |
| `assert fizzbuzz(1) == 1` fails | The function returns the string `"1"`, not the number `1` | Compare with `"1"`. |

## Talk about it

- What's the difference between `print` and `return`?
  *(Print shows something to a person; return gives an answer back to the
  program.)*
- Why do programmers write tests? *(So the computer can check their code
  for them, every time, and catch mistakes when something changes.)*
- Why did the order of the `if`s matter in FizzBuzz?

## Challenge *(if there's time, or for next time)*

- Write `is_multiple(n, of)` that returns `True` if `n` can be divided by
  `of`. Rewrite `fizzbuzz` to use it.
- Write `biggest(a, b)` without using `max`, and test it, including
  when `a` and `b` are the same.
- Write `area(width, height)` and `perimeter(width, height)` for
  rectangles, with tests. What rectangle has an area of 24 and the smallest
  perimeter?

## Checkpoint

The learner can, without help:
- [ ] Write a function that returns an answer, and use the answer
- [ ] Explain the difference between printing and returning
- [ ] Write `assert` tests for a function, and use a failing test to find
      a bug

## Lab notebook

Write FizzBuzz's rules, and the bug: why 15 came out as "Fizz". Add
*return*, *None*, *test* and *assert* to the dictionary.

## Guide's background *(optional reading)*

Functions that **return values** are the building blocks of nearly all
programs, and they're easy to test: give them an input, check the output.
Functions that only print are much harder to reuse or check.

**Automated testing** is a core professional habit. Real projects have
thousands of tests that run every time someone changes the code. `assert`
is the simplest form; later, Python's `pytest` and Rust's built-in
`cargo test` do the same thing on a bigger scale. Writing the test *before*
fixing the bug, as in the FizzBuzz step, is called **test-driven
development**.

FizzBuzz is famous for another reason: it's a classic simple test given to
people applying for programming jobs, and the ordering bug in this lesson
is the most common mistake people make.
