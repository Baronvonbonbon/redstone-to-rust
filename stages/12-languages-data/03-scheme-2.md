# Lesson 12.3: Lists, Lambdas, and Code That Is Data

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor;
`mit-scheme`; a few small boxes or cups, and slips of paper · **New
words:** list, `car`, `cdr`, `cons`, symbol, quote, `lambda`, `map`,
`filter`, higher-order

## Goal *(read this to the learner)*

> Scheme has just one way to keep many things together: the list. And
> a Scheme program is itself made of lists! Today you'll take lists
> apart and build them, give procedures to other procedures, and see
> Scheme treat a piece of code as ordinary data.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Four small boxes or cups in a row, each with a slip of paper:
      `creeper`, `zombie`, `skeleton`, `spider`.

## Warm-up (5 min)

"How do you leave a Scheme error?" *(`(restart 1)`.)* "Write `double` and
`square` again, from memory." Start `mit-scheme` in `~/lab/lang/scheme`
and type them in.

## Activity

### Session 1: lists

1. **A list of mobs.**
   ```scheme
   (list 1 2 3)
   (define mobs '(creeper zombie skeleton spider))
   mobs
   ```
   **They should see** `;Value: (1 2 3)`, `;Value: mobs`, and
   `;Value: (creeper zombie skeleton spider)`. **Ask:** "What's the `'`
   for?" Try without it: `(creeper zombie)`. *(`;Unbound variable:
   zombie`: Scheme tried to work out `zombie`, to give it to a
   procedure called `creeper`. MIT Scheme happens to look at the last
   ones first.)* `(restart 1)`. **Say:**
   "The `'` is called **quote**. It means 'don't work this out, just
   keep it as it is'. The words inside are **symbols**: names, kept as
   data."

2. **First, and the rest.** Use the boxes. **Say:** "Scheme only has two
   ways to take a list apart: the first thing, and the rest."
   ```scheme
   (car mobs)
   (cdr mobs)
   (car (cdr mobs))
   ```
   **They should see** `;Value: creeper`, `;Value: (zombie skeleton
   spider)`, `;Value: zombie`. Point to the boxes each time: the first
   box; all the boxes except the first. **Say:** "`car` is 'the first',
   `cdr` (say 'could-er') is 'the rest'. Strange names, from a 1950s
   computer." And one way to build:
   ```scheme
   (cons 'pig mobs)
   ```
   **They should see** `;Value: (pig creeper zombie skeleton spider)`.
   Put a new box at the front. **Say:** "`cons` puts one thing on the
   front." Check: `mobs` hasn't changed.

3. **How long is a list?** Scheme has `(length mobs)` *(4)*, but write
   your own, with recursion, and the boxes: **Say:** "The length of an
   empty list is 0. Otherwise, it's 1 more than the length of the
   rest."
   ```scheme
   (null? '())
   (define (my-length things)
     (if (null? things)
         0
         (+ 1 (my-length (cdr things)))))
   (my-length mobs)
   ```
   (Type it on one line, or paste it.) **They should see** `;Value: #t`,
   then `;Value: my-length`, then `;Value: 4`. Act it out with the
   boxes: cover the first box each time you take the `cdr`, and count.
   **Ask:** "What's `(car '())`?" Try it. *(An error: an empty list has
   no first thing.)*

### Session 2: procedures as values

4. **Give a procedure to a procedure.**
   ```scheme
   (map square '(1 2 3 4 5))
   (filter even? '(1 2 3 4 5 6))
   (fold-left + 0 '(1 2 3 4 5))
   ```
   **They should see** `;Value: (1 4 9 16 25)`, `;Value: (2 4 6)` and
   `;Value: 15`. **Say:** "`map` does a procedure to everything in a
   list. `filter` keeps the ones where it says true. `fold-left` combines
   them all, starting from 0. Remember Rust's iterators in Lesson 9.14:
   `.map()`, `.filter()`, `.sum()`? They came from here." **Say:** "A
   procedure that takes a procedure is called **higher-order**."

5. **Procedures with no name.**
   ```scheme
   (lambda (n) (* n 3))
   ((lambda (n) (* n 3)) 14)
   (map (lambda (n) (* n 3)) '(1 2 3))
   ```
   **They should see** `;Value: #[compound-procedure 12]` (the number
   may differ), then `;Value: 42`, then `;Value: (3 6 9)`. **Say:**
   "`lambda` makes a procedure without giving it a name, for when you
   only need it once. Rust's closures, `|n| n * 3`, are the same thing.
   In fact, `(define (double n) ...)` is a short way to write `(define
   double (lambda (n) ...))`."

6. **Write your own `map`.** **Ask:** "How would `map` work, using only
   `car`, `cdr`, `cons` and recursion?" Work it out together on paper
   first: the map of an empty list is empty; otherwise, do `f` to the
   first, and `cons` it onto the map of the rest.
   ```scheme
   (define (my-map f things)
     (if (null? things)
         '()
         (cons (f (car things)) (my-map f (cdr things)))))
   (my-map square '(1 2 3))
   ```
   **They should see** `;Value: (1 4 9)`. Put `my-length` and `my-map` in
   a file, `lists.scm`, and commit.

7. **Code is data.** **Ask:** "What's `'(+ 1 2)`?"
   ```scheme
   '(+ 1 2)
   (car '(+ 1 2))
   (eval '(+ 1 2) system-global-environment)
   ```
   **They should see** `;Value: (+ 1 2)`, then `;Value: +`, then
   `;Value: 3`. **Say:** "With a quote, `(+ 1 2)` is just a list of three
   things, and `car` gives the first one, the symbol `+`. `eval` takes a
   list and runs it as a program. A Scheme program *is* a list. That's
   why Scheme needs so little grammar, and why it's so easy to write a
   Scheme interpreter. Next lesson, you'll write one, in Python."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `;Unbound variable: zombie` (or another mob) | The quote `'` is missing, so Scheme tried to run the list | Put `'` before the list. |
| `;The object (), passed as the first argument to car, is not the correct type.` | `car` of an empty list | Check `null?` first, as `my-length` does. `(restart 1)`. |
| `;Unbound variable: my-length` | It isn't defined in this session | Type it again, or `(load "lists.scm")`. |
| `;The object (1 2 3), passed as the second argument to integer-add, is not the correct type.` | A list was given where a number was needed | Check which brackets are a list, and which are a call. |
| `my-map` gives `;Value: (1 2 3)` unchanged | `(car things)` was used instead of `(f (car things))` | Apply `f` to each one. |

## Talk about it

- What do `car`, `cdr` and `cons` do? Act them out with the boxes.
- What does `'` do? Why does `(creeper zombie)` give an error?
- What's a higher-order procedure? What's `lambda` for?
- How can a program be data?

## Challenge *(if there's time, or for next time)*

- Write `(my-sum numbers)` and `(my-filter keep? things)` with recursion.
- Write `(count-up n)`, which makes the list `(1 2 ... n)`. *(Hint:
  `append` joins two lists.)*
- Make a list of lists: `'((creeper 20) (zombie 20) (ghast 10))`. Write
  a procedure that finds the mob with the most health.

## Checkpoint

The learner can, without help:
- [ ] Use `car`, `cdr` and `cons`, and explain them with boxes
- [ ] Write a recursive procedure over a list
- [ ] Use `map`, `filter` and `lambda`
- [ ] Explain why `'(+ 1 2)` is data and `(+ 1 2)` is a sum

## Lab notebook

Draw the four mob boxes, with arrows for `car` and `cdr`. Copy `my-map`,
and draw what happens for `(my-map square '(1 2 3))`, one step at a
time. Commit. Add *list*, *symbol*, *quote*, *lambda* and *higher-order*
to `dictionary.md`.

## Guide's background *(optional reading)*

This is SICP Sections 1.3 ("Formulating Abstractions with Higher-Order
Procedures") and 2.2 ("Hierarchical Data"), in the offline library. A
Scheme list is a chain of **pairs**: `cons` makes a pair, `car` and
`cdr` take it apart (the names come from the IBM 704's "contents of the
address/decrement register"), and the chain ends with the empty list.
That's exactly the linked list from Lesson 8.4 in C, with the memory
handled for you.

The idea that code and data are the same kind of thing is called
**homoiconicity**, and it's what makes Lisp macros possible. `eval`
with an environment is the same `eval` that the next lesson's
interpreter, and SICP's famous **metacircular evaluator** (Section
4.1), implement: Scheme written in Scheme. `fold-left` is MIT Scheme's
name; other Schemes call it `foldl` or `reduce`.
