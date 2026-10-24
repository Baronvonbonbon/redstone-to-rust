# Lesson 12.2: Brackets First: Scheme

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor;
MIT Scheme (`mit-scheme`, from `install-packages.sh --later`) · **New
words:** Scheme, Lisp, prefix, expression, REPL, `define`, procedure

## Goal *(read this to the learner)*

> Scheme is one of the oldest and strangest-looking languages there is:
> everything is in brackets, and the `+` comes first. But it has almost
> no rules at all, which makes it one of the most powerful. Today
> you'll talk to Scheme, teach it new words, and make it count down to
> an explosion.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check `mit-scheme --version` in the learner's account prints
      `MIT/GNU Scheme 12.1` (or similar). If it says `command not
      found`, run `./scripts/install-packages.sh --later` from your
      account, online.
- [ ] Make the folder: as the learner, `mkdir -p ~/lab/lang/scheme`.

## Warm-up (5 min)

"In the sum grammar from last lesson, what was the tree for `1 + 2 * 3`?"
Draw it. **Say:** "What if we wrote the tree down, exactly as it is,
with brackets? The thing at the top first, then what's under it:
`(+ 1 (* 2 3))`. That's Scheme. You write the tree."

## Activity

### Session 1: talking to Scheme

1. **Start it.**
   ```
   cd ~/lab/lang/scheme
   mit-scheme
   ```
   **They should see** a few lines about MIT/GNU Scheme and copyright,
   then the prompt:
   ```
   1 ]=>
   ```
   **Say:** "This is a **REPL**: read, evaluate, print, loop. It reads
   what you type, works it out, prints the answer, and waits again. Just
   like `python3` with no file, or Shelly."

2. **Sums with the operator first.** Type each, and press Enter:
   ```scheme
   (+ 2 3)
   (* 6 7)
   (+ 1 2 3 4 5)
   (- 10 (* 2 3))
   ```
   **They should see:**
   ```
   ;Value: 5
   ;Value: 42
   ;Value: 15
   ;Value: 4
   ```
   **Say:** "In Scheme, every bracket is 'do this, to these'. The first
   thing is what to do, and the rest are what to do it to. `+` can take
   as many numbers as you like." **Ask:** "How would you write `1 + 2 *
   3`?" *(`(+ 1 (* 2 3))`. Try it: 7.)* "Does Scheme need to know that
   `*` comes before `+`?" *(No! The brackets say exactly what's inside
   what. There's nothing to remember.)* That's called **prefix** (the
   operator goes first).

3. **Mistakes.** Type `(+ 2 "creeper")`. **They should see:**
   ```
   ;The object "creeper", passed as the second argument to integer-add, is not the correct type.
   ;To continue, call RESTART with an option number:
   ; (RESTART 2) => Specify an argument to use in its place.
   ; (RESTART 1) => Return to read-eval-print level 1.

   2 error>
   ```
   **Say:** "The prompt changed to `2 error>`. Scheme kept the mistake
   open, in case you want to look at it. To go back to normal, type
   `(restart 1)`." Do that. **They should see** `;Abort!` and the `1 ]=>`
   prompt again. Try `creepers` on its own: **they should see** `;Unbound
   variable: creepers` (it doesn't know that word). `(restart 1)` again.

4. **Teach it words.** **Say:** "`define` gives something a name."
   ```scheme
   (define diamonds 12)
   diamonds
   (* diamonds 2)
   ```
   **They should see** `;Value: diamonds`, then `;Value: 12`, then
   `;Value: 24`. Now teach it a new verb:
   ```scheme
   (define (double n) (* n 2))
   (double 21)
   (double diamonds)
   (define (square n) (* n n))
   (square (double 3))
   ```
   **They should see** `;Value: double`, `42`, `24`, `;Value: square`,
   `36`. **Say:** "`(define (double n) ...)` means 'to double `n`, work
   out `(* n 2)`'. Scheme calls a function a **procedure**. Notice:
   using `double` looks exactly like using `*`. Your words are as good
   as Scheme's own."

5. **Choosing.** `if` has three parts: a test, the answer if it's true,
   and the answer if it's not.
   ```scheme
   (if (> diamonds 10) "rich" "dig more")
   (> 3 2)
   (and (> 3 2) (< 1 0))
   ```
   **They should see** `;Value: "rich"`, `;Value: #t`, `;Value: #f`.
   **Say:** "`#t` and `#f` are Scheme's true and false." Leave with
   `(exit)`. *(It says goodbye with a random message, sometimes in
   Latin. If it asks `Kill Scheme (y or n)?`, type `y`.)*

### Session 2: recursion, Scheme's favourite thing

6. **Factorial.** Scheme has no `while` loop in this lesson: everything
   repeats by **recursion** (Stage 7). Start `mit-scheme` again:
   ```scheme
   (define (factorial n) (if (= n 0) 1 (* n (factorial (- n 1)))))
   (factorial 5)
   (factorial 30)
   ```
   **They should see** `;Value: 120` and then:
   ```
   ;Value: 265252859812191058636308480000000
   ```
   **Ask:** "In Rust, what happened when a number got too big?" *(It
   panicked: `attempt to multiply with overflow`.)* **Say:** "Scheme's
   numbers grow as big as they need to. Try `(expt 2 100)`."

7. **A program in a file.** Typing long procedures on one line is hard,
   so put them in a file. Leave Scheme with `(exit)`, and make
   `~/lab/lang/scheme/boom.scm` in the editor:
   ```scheme
   ; Count down, then explode.
   (define (countdown n)
     (if (= n 0)
         (display "BOOM!")
         (begin
           (display n)
           (newline)
           (countdown (- n 1)))))

   ; How many steps does a hailstone number take to reach 1? (Stage 3)
   (define (hail n)
     (cond ((= n 1) 0)
           ((even? n) (+ 1 (hail (/ n 2))))
           (else (+ 1 (hail (+ (* 3 n) 1))))))
   ```
   **Say:** "`;` starts a comment. `display` prints, `newline` starts a
   new line, and `begin` does several things in order. `cond` is like
   `if`, `else if`, `else`." Start `mit-scheme` in that folder, and:
   ```scheme
   (load "boom.scm")
   (countdown 3)
   (hail 27)
   ```
   **They should see:**
   ```
   ;Loading "boom.scm"... done
   ;Value: hail
   ```
   then
   ```
   3
   2
   1
   BOOM!
   ;Unspecified return value
   ```
   and `;Value: 111`. **Say:** "111 steps: the same as your Python
   program in Stage 3. `Unspecified return value` means `countdown`
   printed things, but didn't work out an answer."

8. **Fractions.** Try `(/ 7 2)`. **They should see** `;Value: 7/2`.
   **Say:** "Scheme keeps it as an exact fraction! `(quotient 7 2)` gives
   3, like Rust's `/`, and `(remainder 7 2)` gives 1, like `%`." Commit
   `boom.scm` (`git init` in `~/lab/lang/scheme` first).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `mit-scheme: command not found` | It isn't installed | The guide runs `./scripts/install-packages.sh --later`. |
| Nothing happens after pressing Enter | A bracket isn't closed, so Scheme is waiting for more | Type the missing `)`, then Enter. |
| `2 error>` (or 3, 4...) | A mistake is open | `(restart 1)`. |
| `;Unbound variable: dubble` | A spelling mistake, or it wasn't `define`d yet | Check the spelling; `define` it first. |
| `;The object 5 is not applicable.` | Brackets round a number, like `(5)`, which means "do 5" | Remove the extra brackets. |
| `;Aborting!: maximum recursion depth exceeded` | A recursive procedure that never stops | Check the stopping case, like `(= n 0)`. |
| `;Unable to find file ...boom.scm` | Scheme was started in a different folder | `(exit)`, `cd ~/lab/lang/scheme`, start it again. |

## Talk about it

- Why doesn't Scheme need to know that `*` comes before `+`?
- What does `define` do? What's a procedure?
- How does Scheme repeat things without a loop?
- What happens to big numbers in Scheme, and in Rust?

## Challenge *(if there's time, or for next time)*

- Write `(cube n)`, using `square`.
- Write `(stack-count n)`, which works out how many blocks are in a
  Numberblocks staircase of height `n` (1 + 2 + ... + n), with
  recursion. Check: `(stack-count 10)` is 55.
- `(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))`. Try
  `(fib 20)` *(6765)*. Why is `(fib 30)` so slow? (Stage 7!)

## Checkpoint

The learner can, without help:
- [ ] Use the Scheme REPL, and get out of an error with `(restart 1)`
- [ ] Write sums in prefix, with brackets inside brackets
- [ ] `define` a value and a procedure, and use them
- [ ] Write a recursive procedure, and `load` it from a file

## Lab notebook

Write `1 + 2 * 3` and `(1 + 2) * 3` in Scheme. Draw the tree for
each, and circle each bracket's part of the tree. Copy `countdown`.
Commit. Add *Scheme*, *prefix*, *REPL* and *procedure* to
`dictionary.md`.

## Guide's background *(optional reading)*

Scheme (1975) is a dialect of **Lisp** (1958), the second-oldest
programming language still in use. Its writing style, with every
expression in brackets and the operator first, is called
**s-expressions**; because the code *is* a tree, Lisps need almost no
grammar, and programs can easily read and write other programs (Lesson
12.3). This lesson follows Section 1.1 of *Structure and Interpretation
of Computer Programs* (SICP), by Harold Abelson and Gerald Jay Sussman
with Julie Sussman, the famous MIT textbook, which is in the offline
library (`repos/sicp/html/index.xhtml`; CC BY-SA). It's written for
university students, so it's for the guide, or for reading together; its
first section is very approachable.

MIT Scheme's error levels (`2 error>`) are a **debugger** waiting for
instructions; `(restart 1)` abandons the error. Ctrl+C then `Q` also
gets out of a runaway computation. The `Unspecified return value` line
appears because `display` is done for its effect, not its answer;
SICP calls such procedures "commands". Scheme's numbers are
**arbitrary-precision** integers and exact rationals, which is why
`(/ 7 2)` is `7/2`.
