# Lesson 12.4: A Tiny Scheme, in Python

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor;
`~/lab/lang/python`; paper · **New words:** tokenize, read, evaluate,
environment, interpreter loop

## Goal *(read this to the learner)*

> Last lesson, Scheme ran a list as a program with `eval`. Today you'll
> write your own `eval`: a Scheme interpreter in about 70 lines of
> Python. When it's done, it will run `factorial`, the same one you
> typed into MIT Scheme.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once, and type `tiny.py` yourself if you
      can: it's the heart of the stage.
- [ ] Python dictionaries (Stage 3) and recursion (Stage 7) are used
      throughout.

## Warm-up (5 min)

"What does `(car '(+ 1 2))` give?" *(`+`.)* "So what would a program need
to do, to work out `(+ 1 2)`?" *(Look at the first thing, find out it
means add, work out the rest, and add them.)* Write the learner's steps
down: that's today's plan.

## Activity

### Session 1: reading

1. **Three jobs.** Draw three boxes in a row on paper: **tokenize** →
   **read** → **evaluate**. **Say:** "Every interpreter does these.
   Tokenize chops the text into words. Read builds a tree from the words.
   Evaluate works out the tree. Today, all three, for Scheme."

2. **Tokenize.** In `~/lab/lang/python`, make `tiny.py`:
   ```python
   # A tiny Scheme, in Python.
   import operator


   def tokenize(text):
       return text.replace("(", " ( ").replace(")", " ) ").split()


   print(tokenize("(* 6 (+ 3 4))"))
   ```
   `python3 tiny.py`. **They should see:**
   ```
   ['(', '*', '6', '(', '+', '3', '4', ')', ')']
   ```
   **Say:** "Put spaces round every bracket, then split at the spaces.
   That's a whole tokenizer, because Scheme's grammar is so simple."
   *(Compare it with the Jack tokenizer of Lesson 8.13!)*

3. **Read.** Replace the `print` line with:
   ```python
   def read(tokens):
       token = tokens.pop(0)
       if token == "(":
           things = []
           while tokens[0] != ")":
               things.append(read(tokens))
           tokens.pop(0)  # the ")"
           return things
       try:
           return int(token)
       except ValueError:
           return token  # a name, like + or double


   print(read(tokenize("(* 6 (+ 3 4))")))
   ```
   **They should see:**
   ```
   ['*', 6, ['+', 3, 4]]
   ```
   **Say:** "A Scheme list became a Python list, with lists inside lists:
   the tree. `pop(0)` takes the first token off the front. When `read`
   meets `(`, it reads things, each one by calling `read` again, until
   it meets `)`." Act it out: the learner is `read`, and the guide hands
   them tokens one at a time from cards; every `(` means "start a new
   pile", every `)` means "this pile is finished, put it in the one
   before". **Ask:** "Why are `6` and `4` not in quotes any more?"
   *(`int(token)` turned them into numbers. Names like `*` stay as
   strings.)*

### Session 2: evaluating

4. **The world of names.** Replace the `print` line with:
   ```python
   world = {
       "+": operator.add,
       "-": operator.sub,
       "*": operator.mul,
       "<": operator.lt,
       "=": operator.eq,
   }
   ```
   **Say:** "An **environment** is a dictionary from names to what they
   mean. `operator.add` is Python's own adding procedure:
   `operator.add(2, 3)` is 5." *(Try it in `python3`, with `import
   operator`.)*

5. **Evaluate.** Below `world`:
   ```python
   def evaluate(x, names):
       if isinstance(x, int):
           return x
       if isinstance(x, str):
           return names[x]
       first = x[0]
       if first == "define":
           _, name, value = x
           names[name] = evaluate(value, names)
           return name
       if first == "if":
           _, test, yes, no = x
           if evaluate(test, names):
               return evaluate(yes, names)
           return evaluate(no, names)
       if first == "lambda":
           _, params, body = x

           def function(*args):
               inside = dict(names)
               inside.update(zip(params, args))
               return evaluate(body, inside)

           return function
       function = evaluate(first, names)
       args = [evaluate(arg, names) for arg in x[1:]]
       return function(*args)
   ```
   Read it together, one `if` at a time:
   - "A number means itself. A name means whatever the environment says."
   - "`define` works out the value and puts it in the environment.
     `_, name, value = x` takes the list apart: `_` means 'I don't need
     this one' (it's the word `define`)."
   - "`if` works out the test, then only *one* of the other two."
   - "`lambda` makes a real Python function. When it's called, it makes
     a new environment, `inside`: a copy of the names, plus each
     parameter set to its value."
   - "Anything else is a call: work out the first thing (the procedure)
     and all the others (the arguments), then call it. `*args` means 'all
     of these, as separate arguments'."

6. **The loop.** At the bottom:
   ```python
   while True:
       try:
           line = input("tiny> ")
       except EOFError:
           break
       if line.strip():
           try:
               print(evaluate(read(tokenize(line)), world))
           except Exception as problem:
               print("Oops:", repr(problem))
   ```
   `python3 tiny.py`, and type each line:
   ```scheme
   (+ 1 2)
   (* 6 (+ 3 4))
   (define diamonds 12)
   (* diamonds 2)
   (define double (lambda (n) (* n 2)))
   (double 21)
   (if (< 2 3) 100 200)
   (define fact (lambda (n) (if (< n 2) 1 (* n (fact (- n 1))))))
   (fact 5)
   (fact 20)
   ```
   **They should see**, one per line: `3`, `42`, `diamonds`, `24`,
   `double`, `42`, `100`, `fact`, `120`, `2432902008176640000`. **Say:**
   "Your own Scheme, running recursion! It's about 70 lines." Ctrl+D
   leaves it. Commit.

7. **Mistakes.** Try `(creeper 1)`, `(+ 1 2` and `(1 2)`. **They should
   see:**
   ```
   Oops: KeyError('creeper')
   Oops: IndexError('list index out of range')
   Oops: TypeError("'int' object is not callable")
   ```
   **Ask:** "Which job found each mistake: tokenize, read or
   evaluate?" *(`creeper`: evaluate, looking up a name. `(+ 1 2`: read,
   running out of tokens before the `)`. `(1 2)`: evaluate, trying to
   call 1.)* **Say:** "These messages are Python's, not friendly ones.
   In your own language, you'll write friendly messages for each kind of
   mistake."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NameError: name 'operator' is not defined` | `import operator` is missing | Add it at the top. |
| `Oops: KeyError('-')` | `-` isn't in `world` | Add `"-": operator.sub`. |
| `Oops: ValueError('not enough values to unpack (expected 4, got 3)')` | An `if` with no "no" part, like `(if (< 1 2) 5)` | Tiny Scheme's `if` needs all three parts. |
| `(fact 5)` gives `Oops: KeyError('<')` | `inside = dict(names)` was written as `inside = {}`, so the function can't see `<`, `*` or `fact` | Copy `names`, so the function can see the world. |
| The `tiny>` prompt never appears | The `print(...)` test lines from steps 2 and 3 are still there, and one has an error | Remove the test lines. |

## Talk about it

- What are the three jobs of an interpreter?
- What does an environment do? Why does a `lambda` get its own?
- Why is Scheme so easy to tokenize and read?
- Which part of `evaluate` is recursive, and why?

## Challenge *(if there's time, or for next time)*

- Add `/`, `>` and `%` to `world` (`operator.floordiv`, `operator.gt`,
  `operator.mod`).
- Add `"print": print`, and try `(print (fact 10))`.
- Add `quote`: `(quote (1 2 3))` gives back `[1, 2, 3]` without working
  it out. *(One more `if` in `evaluate`.)*
- Add lists: `"list": lambda *things: list(things)`, `"car": lambda x:
  x[0]`, `"cdr": lambda x: x[1:]`.

## Checkpoint

The learner can, without help:
- [ ] Explain tokenize, read and evaluate, with `(* 6 (+ 3 4))`
- [ ] Explain an environment, and how `define` and `lambda` use it
- [ ] Run `fact` in their own tiny Scheme
- [ ] Say which job found each mistake in step 7

## Lab notebook

Draw the three boxes with `(* 6 (+ 3 4))` going through them: the text,
the tokens, the tree, and `42`. Commit. Add *tokenize*, *evaluate* and
*environment* to `dictionary.md`.

## Guide's background *(optional reading)*

This interpreter is in the style of Peter Norvig's famous `lis.py`
("(How to Write a (Lisp) Interpreter (in Python))"), cut down and
written for this course. It's the same shape as SICP's metacircular
evaluator (Section 4.1): `eval` dispatches on the kind of expression,
and **apply** (here, Python's own call, `function(*args)`) runs a
procedure on its arguments.

Its environments are simplified: a `lambda` copies the environment at
the moment it's *called*, so recursion works, and a function sees
names defined after it. Real Scheme uses **lexical scope** with a chain
of environments, each pointing to the one it was made in, which is
what *Crafting Interpreters* builds in Chapters 8 and 11, and what
Lesson 12.8 starts with blocks. Python's own `eval` and `exec` are not
used anywhere: everything here is the learner's code.
