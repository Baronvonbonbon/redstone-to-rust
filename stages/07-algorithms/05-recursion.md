# Lesson 7.5: Recursion: Functions That Call Themselves

**Time:** 2–3 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
a set of nesting dolls or nesting cups, or a few boxes that fit inside
each other with a sweet (or a note) in the smallest · **New words:**
recursion, base case, call stack

## Goal *(read this to the learner)*

> What if a function could call *itself*? It sounds like a mirror facing
> a mirror, going on forever. But if each call works on a *smaller*
> problem, and the smallest problem has an easy answer, it stops. This
> trick is called **recursion**, and it's one of the most powerful ideas
> in programming. Today you'll use it to count down, do maths, reverse
> words and grow a tree. Next lesson, it gives you a much faster sort.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Nest the dolls or boxes, with the prize in the smallest.

## Warm-up (5 min)

"Selection sort on a million numbers: how many comparisons, roughly?"
*(About half of a million times a million: way too many.)* "We need a
cleverer idea. Here it is."

## Activity

### Session 1: the idea

1. **Open the dolls.** Hand over the nested dolls. **Say:** "Here are
   the instructions for finding the prize. *To open a doll: if it's the
   smallest one, take the prize. Otherwise, open it, and then **open the
   doll inside**.*" The learner follows the instructions out loud.

   **Ask:** "The instructions for opening a doll say 'open the doll
   inside'. They use themselves! Why don't they go on forever?" *(Each
   doll is smaller, and the smallest one has no doll inside: the
   instructions stop there.)*

   **Say:** "That's **recursion**. It has two parts:
   - the **base case**: the smallest problem, answered straight away (the
     smallest doll);
   - the **recursive case**: do a little work, and use *the same
     instructions* on a smaller problem (the doll inside)."

2. **A countdown.** New file, `~/lab/algo/countdown.py`:
   ```python
   def countdown(n):
       if n == 0:
           print("Blast off!")
           return
       print(n)
       countdown(n - 1)
       print("back in countdown", n)


   countdown(3)
   ```
   **Ask first:** "What will it print?" Then run it. **They should see:**
   ```
   3
   2
   1
   Blast off!
   back in countdown 1
   back in countdown 2
   back in countdown 3
   ```
   **Say:** "Surprise at the end! Each call to `countdown` waits for the
   one inside it to finish, then carries on from where it was. The
   computer keeps a pile of all the calls that are waiting, called the
   **call stack**. `countdown(3)` is at the bottom of the pile, and
   `countdown(0)` is on top. When the top one finishes, it's taken off,
   and the one below carries on."

   Act it out: the learner is `countdown(3)`, and stands up. They call
   the guide, `countdown(2)`, who stands up and calls a toy or a cushion,
   `countdown(1)`... Each sits down when it's done, last one first.

3. **No base case.** New file, `~/lab/algo/forever.py`:
   ```python
   def countdown(n):
       print(n)
       countdown(n - 1)


   countdown(3)
   ```
   Run it. **They should see:** numbers racing past into the minus
   numbers, then a red error ending with something like:
   ```
     [Previous line repeated 996 more times]
   RecursionError: maximum recursion depth exceeded
   ```
   **Say:** "With no base case, it never stops. Each call waits on the
   call stack, and Python only allows about 1000 of them, so it stops
   the program. That's a **RecursionError**: it almost always means a
   missing or wrong base case."

### Session 2: recursive functions

4. **Factorial.** **Say:** "In maths, 5 **factorial**, written 5!, is
   5 × 4 × 3 × 2 × 1. It's the number of ways to line up 5 different
   things." *(Try it with 3 toys: 3! = 6 ways.)* "Notice: 5! is 5 × 4!.
   And 4! is 4 × 3!. The answer uses the same problem, smaller. And 0!
   is 1: that's the base case."

   New file, `~/lab/algo/recursion.py`:
   ```python
   def factorial(n):
       """n × (n - 1) × ... × 1. factorial(0) is 1."""
       if n == 0:
           return 1
       return n * factorial(n - 1)
   ```
   Try it in the shell: `from recursion import factorial`, then
   `factorial(5)` *(120)* and `factorial(20)`
   *(2432902008176640000: there are over two billion billion ways to
   line up 20 mobs!)*

5. **Total of a list.** **Say:** "Lists can be smaller problems too. The
   total of `[3, 4, 5]` is 3 plus the total of `[4, 5]`." In the shell,
   try `[3, 4, 5][1:]`: *(`[4, 5]`: everything but the first.)* Add to
   `recursion.py`:
   ```python
   def total(items):
       """Adds up a list: the first item, plus the total of the rest."""
       if items == []:
           return 0
       return items[0] + total(items[1:])
   ```
   **Ask:** "What's the base case?" *(The empty list, whose total is 0.)*

6. **Reverse a word.** Now the learner writes it, with hints:
   - "What's the smallest word, and what's its reverse?" *(The empty
     word `""`, and its reverse is `""`.)*
   - "`'creeper'[1:]` is `'reeper'`. If you had the reverse of
     `'reeper'`, how would you make the reverse of `'creeper'`?" *(Put
     the `c` on the end: `reverse(text[1:]) + text[0]`.)*

   Call it `reverse(text)`, in `recursion.py`. Then:
   ```
   python3 check.py recursion
   ```
   **They should see:** `factorial, total and reverse: right every
   time.` and `ALL GOOD!` Commit.

### Session 3: a recursive tree

7. **A fractal tree.** **Say:** "A tree is a trunk with two smaller trees
   on top. That's recursion!" New file, `~/lab/algo/tree.py`:
   ```python
   import turtle

   turtle.setup(800, 600)
   t = turtle.Turtle()
   t.speed(0)
   t.left(90)
   t.penup()
   t.goto(0, -250)
   t.pendown()


   def tree(length):
       if length < 10:
           return
       t.forward(length)
       t.left(30)
       tree(length * 0.7)
       t.right(60)
       tree(length * 0.7)
       t.left(30)
       t.backward(length)


   tree(150)
   turtle.done()
   ```
   **Say:** "The base case: a branch shorter than 10 is too small to
   draw. Otherwise, draw the trunk, turn left and draw a smaller tree,
   turn right and draw another, then turn back and walk back down. Each
   tree must leave the turtle where it started, or the next one goes
   wrong."

   Run it. **They should see:** a trunk from the bottom of the window,
   splitting in two again and again, into a round tree with tiny
   twigs. The turtle ends back at the bottom, pointing up.

   Play: change `30` and `60` to `20` and `40` (thinner), or `0.7` to
   `0.6` (smaller), or `10` to `3` (more twigs, and slower).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `RecursionError: maximum recursion depth exceeded` | The base case is missing, or never reached | Check the `if` at the top. Does every call get closer to it? |
| `NOT YET: RecursionError. A function called itself too many times...` | A base case is wrong: for example `if n == 1` in `factorial`, so `factorial(0)` never stops | `factorial(0)` is 1: the base case is `n == 0`. |
| `NOT YET: total([]) gave 1, but it should be 0.` | The base case gives back the wrong thing | Adding up nothing gives 0. |
| `NOT YET: factorial doesn't call itself...` | It was written with a loop | Today it must be recursive: `n * factorial(n - 1)`. |
| The tree is lopsided or wanders off | The turns don't add up to zero, or `backward` is missing | Left 30, right 60, left 30: back to where it started. And walk back down the trunk. |
| `TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'` | A path through the function doesn't `return` anything | Every `if` and the end of the function need a `return`. |

## Talk about it

- What are the two parts of every recursive function?
- What's the call stack? What happens to it when a call finishes?
- Why does `countdown` print "back in countdown" in reverse order?

## Challenge *(if there's time, or for next time)*

- Write `power(base, exp)`, with recursion: `power(2, 10)` is 1024.
  *(Base case: `exp` is 0, answer 1.)*
- Write `count_up(n)`, which prints 1 to `n` with recursion, and no
  loop. *(Hint: call `count_up(n - 1)` first, then print.)*
- In the tree, make the branches thinner as they get shorter:
  `t.pensize(length / 10)` before `forward`.
- Thonny's debugger can show the call stack: click the bug button (or
  Debug current script), then press F7 (Step into) again and again. Each
  call opens in its own box.

## Checkpoint

The learner can, without help:
- [ ] Explain recursion, the base case and the recursive case, with
      nesting dolls
- [ ] Write `factorial`, `total` and `reverse` recursively, and pass
      `python3 check.py recursion`
- [ ] Explain the call stack, and what a `RecursionError` means
- [ ] Draw a recursive picture with the turtle

## Lab notebook

Draw the call stack for `countdown(3)`, as a pile of boxes, at the
moment "Blast off!" is printed. Draw the tree. Commit. Add *recursion*,
*base case*, *call stack* and *factorial* to `dictionary.md`.

## Guide's background *(optional reading)*

**Recursion** solves a problem by solving smaller copies of the same
problem. Every loop can be written as recursion and the other way round,
but some problems (trees, mazes, divide and conquer) are much more
natural recursively. It's the central idea of Lessons 7.6, 7.7 and 7.13.

The **call stack** is real: it's a region of memory where each function
call keeps its local variables and where to return to. Python limits
its depth to about 1000 to catch runaway recursion. In Stage 8, the
learner builds a call stack for their own Hack computer, and sees
exactly how it works.

`items[1:]` makes a new list each time, so `total` and `reverse` are
actually O(n²). That's fine here, because the point is the idea; Python
programmers would use `sum()` and `text[::-1]` in real programs.
*Algorithms* by Jeff Erickson (free, open) has a famous first chapter
on recursion, for guides who want to go deeper.
