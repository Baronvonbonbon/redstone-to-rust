# Lesson 2.12: Ask and Decide

**Time:** 2 sessions of 45 min · **You need:** Thonny; `polygon` from Lesson
2.8 · **New words:** input, if, else, condition, type, integer, string

## Goal *(read this to the learner)*

> Until now, your programs talk but never listen. Today they learn to
> **ask questions** and **make decisions** based on the answer. You'll
> build a shape quiz that draws a mystery shape, asks how many sides it
> has, and keeps your score.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Remind yourself: in Thonny, when a program asks a question, the
      learner types the answer **in the Shell** at the bottom, then
      presses Enter. Arrange the windows so the turtle window doesn't
      cover the Shell.

## Warm-up (5 min)

Play "Simon says" for a minute. "How did you decide whether to do it?"
*(If the instruction started with "Simon says", I did it. Otherwise I
didn't.)* "That's an **if**. Programs make decisions the same way."

## Activity

### Session 1: asking

1. **Ask a question.** New file, `ask.py`:
   ```python
   name = input("What's your name? ")
   print("Hello,", name)
   print("Nice name,", name + "!")
   ```
   Run it. **They should see:** the question in the Shell. They type their
   name, press Enter, and the program greets them.

   **Say:** "`input` shows the question, waits for you to type, and puts
   what you typed into the box. The space before the last quote mark keeps
   your answer from squashing against the question."

2. **The number problem.** Add:
   ```python
   age = input("How old are you? ")
   print("Next year you will be", age + 1)
   ```
   Run it. **They should see:** an error, `TypeError: can only
   concatenate str (not "int") to str`.

   **Say:** "Python is confused. `input` always gives back *words*, even
   when you type a number. And you can't add 1 to words. It's like asking
   'what's "seven" plus 1?'. Let's look." In the Shell:
   ```python
   type("7")
   type(7)
   ```
   **They should see:** `<class 'str'>` and `<class 'int'>`.

   **Say:** "`str` is a **string**: words. `int` is an **integer**: a
   whole number. They look the same to us, but not to Python. `int()`
   turns words into a number." Fix the program:
   ```python
   age = int(input("How old are you? "))
   print("Next year you will be", age + 1)
   ```

3. **What if they type a word?** Run it and type `seven`. **They should
   see:** `ValueError: invalid literal for int() with base 10: 'seven'`.
   **Say:** "`int()` only understands digits. Real programs check for
   this; ours just trust you to type a number."

4. **A shape on request.** New file, `shape-maker.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.shape("turtle")

   def polygon(sides, size):
       for i in range(sides):
           t.forward(size)
           t.left(360 / sides)

   sides = int(input("How many sides? "))
   polygon(sides, 80)

   turtle.done()
   ```
   Run it a few times with different answers.

### Session 2: deciding

5. **The first `if`.** Change the bottom of `shape-maker.py`:
   ```python
   sides = int(input("How many sides? "))

   if sides < 3:
       print("A shape needs at least 3 sides!")
   else:
       polygon(sides, 80)
       print("Here is your shape with", sides, "sides.")
   ```
   Try it with 2, then 5.

   **Say:** "`sides < 3` is a **condition**: a question with a yes or no
   answer. If the answer is yes, Python does the indented lines under
   `if`. Otherwise, it does the lines under `else`. Only one of the two
   ever happens."

6. **More choices with `elif`.**
   ```python
   if sides < 3:
       print("A shape needs at least 3 sides!")
   elif sides > 20:
       print("That's a lot of sides! It'll look like a circle.")
       polygon(sides, 10)
   else:
       polygon(sides, 80)
   ```
   **Say:** "`elif` means 'else, if'. Python checks each condition from
   top to bottom, and does the *first* one that's true. If none are true,
   it does `else`."

7. **The comparison symbols.** Write them on paper, and try each one in
   the Shell, like `5 < 3` (it says `False`):

   | Symbol | Means |
   |---|---|
   | `<` | is less than |
   | `>` | is greater than |
   | `<=` | is less than or equal to |
   | `>=` | is greater than or equal to |
   | `==` | is equal to |
   | `!=` | is not equal to |

   **Say:** "Remember, one `=` means 'put in the box'. Two, `==`, asks
   'are these the same?'. Mixing them up is the most common mistake in
   all of programming."

8. **Odd or even?** In a new file:
   ```python
   n = int(input("Give me a number: "))
   if n % 2 == 0:
       print(n, "is even")
   else:
       print(n, "is odd")
   ```
   **Say:** "Remember `%`, the leftovers? If sharing between 2 leaves
   nothing over, it's even."

9. **The shape quiz.** New file, `quiz.py`:
   ```python
   import turtle
   import random

   t = turtle.Turtle()
   t.speed(0)
   t.hideturtle()

   def polygon(sides, size):
       for i in range(sides):
           t.forward(size)
           t.left(360 / sides)

   score = 0

   for question in range(5):
       t.clear()
       sides = random.randint(3, 10)
       polygon(sides, 60)
       guess = int(input("How many sides? "))
       if guess == sides:
           print("Correct!")
           score = score + 1
       else:
           print("Not quite. It had", sides, "sides.")

   print("You scored", score, "out of 5")

   turtle.done()
   ```
   **Say:** "`t.clear()` rubs out the turtle's drawing, ready for the next
   question. Look at everything this uses: a function with parameters, a
   loop, random numbers, input, a decision, and a score box. That's most
   of what you've learned!"

   Let them play it, then have the guide (or a sibling) play it.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `TypeError: can only concatenate str (not "int") to str` | Doing maths with words from `input` | Wrap the `input` in `int(...)`. |
| `TypeError: '<' not supported between instances of 'str' and 'int'` | Comparing words from `input` with a number | Wrap the `input` in `int(...)`. |
| `ValueError: invalid literal for int() with base 10: 'seven'` | Typed letters, or nothing, where a number was needed | Type digits, then Enter. |
| `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?` | Used `=` in an `if` | Use `==` to compare. |
| `SyntaxError: expected ':'` | Missing colon after `if`, `elif` or `else` | Add `:` at the end of the line. |
| The program seems frozen | It's waiting for an answer | Click in Thonny's Shell, type the answer, press Enter. |
| `IndentationError` or `SyntaxError` on the `else` line | `else` is indented differently from its `if` | `if`, `elif` and `else` line up exactly. |

## Talk about it

- Why does `input` need `int()` around it to do maths?
  *(`input` always gives text, a string.)*
- What's the difference between `=` and `==`?
- In `if ... elif ... else`, how many of the parts can happen at once?
  *(Only one.)*
- Where do games make decisions? *(If health is 0, game over. If you
  touch lava, ouch...)*

## Challenge *(if there's time, or for next time)*

- **Guess my number:** the program picks `random.randint(1, 100)`; you
  guess, and it says "too high" or "too low". (Try 7 guesses with a loop.
  What's the best way to guess? There's a clever answer called *binary
  search*, which comes back in Stage 7.)
- Make the quiz harder as you go: the size gets smaller each question.
- Add a times-table quiz: two random numbers from 1 to 12, ask for the
  answer, and keep score.
- Turtle can ask in a pop-up box instead of the Shell:
  `turtle.numinput("Quiz", "How many sides?")`. Try it.

## Checkpoint

The learner can, without help:
- [ ] Use `input` to ask a question, and `int()` to turn the answer into
      a number
- [ ] Explain the difference between a string and an integer
- [ ] Write `if`, `elif` and `else` with a condition
- [ ] Explain the difference between `=` and `==`

## Lab notebook

Copy the table of comparison symbols. Draw a decision as a flowchart: a
diamond with the question "sides < 3?", and arrows for yes and no. Add
*input*, *condition*, *integer*, *string* and *type* to the dictionary.

## Guide's background *(optional reading)*

This lesson brings in two big ideas. The first is **types**: every value
in Python is a particular kind of thing, and the kind decides what you
can do with it. `7` (an integer) can be added to; `"7"` (a string, which
happens to contain the character 7) can't. Python is strict about this on
purpose, so mistakes show up as clear errors instead of strange answers.
Types become much more important in Rust, at Stage 9.

The second is **conditions**, or branching: a program that takes
different paths depending on what's true. With loops, functions and
variables, conditions complete the basic toolkit. In principle, every
program in the world can be built from these pieces.

Comparisons give back `True` or `False`, called **Booleans** after George
Boole, a mathematician who worked out the algebra of true and false. In
Stage 4, the learner builds those same true/false decisions out of logic
gates and redstone.
