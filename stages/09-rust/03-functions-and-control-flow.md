# Lesson 9.3: Functions, Ifs and Loops

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust`; paper · **New words:** expression, statement,
return type, range

## Goal *(read this to the learner)*

> You've written functions, ifs and loops in Python, Jack and C. Rust's
> look familiar, with one twist: almost everything in Rust is an
> **expression**, which means it has a value. You'll use that to bring
> back the hailstone numbers from Lesson 3.7, and hunt for the longest
> chain under 10,000.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Look back at Lesson 3.7, Hailstone Numbers.

## Warm-up (10 min)

"Do you remember the hailstone rule from Lesson 3.7?" *(If it's even,
halve it; if it's odd, times it by 3 and add 1; stop at 1.)* Do it on
paper from 6: *6, 3, 10, 5, 16, 8, 4, 2, 1*. "How many steps?" *(8.)*
"And what's the puzzle called?" *(The **Collatz conjecture**: nobody
has proved that every number gets to 1.) **Say:** "Today we write it in
Rust, and make the computer search thousands of numbers."

## Activity

### Session 1: a function

1. **The project.**
   ```
   cd ~/lab/rust
   cargo new collatz
   cd collatz
   ```
   ```rust
   fn collatz_steps(start: u64) -> u32 {
       let mut n = start;
       let mut steps = 0;
       while n != 1 {
           if n % 2 == 0 {
               n = n / 2;
           } else {
               n = 3 * n + 1;
           }
           steps += 1;
       }
       steps
   }

   fn main() {
       for n in 1..=10 {
           println!("{n} takes {} steps", collatz_steps(n));
       }
   }
   ```
   **They should see:** `1 takes 0 steps`, `2 takes 1 steps`, and so on,
   with `6 takes 8 steps` and `7 takes 16 steps`, matching the paper.

2. **Reading it.** Go through it together:
   - `fn collatz_steps(start: u64) -> u32`: the function takes a `u64`
     called `start`, and gives back a `u32`. **Say:** "Every function
     argument has its type written down. The `->` says the **return
     type**."
   - `%` is the remainder, as in Python: `n % 2 == 0` means even.
   - `if` and `while` have no brackets round the condition, but always
     have `{ }` round the body.
   - `steps += 1` is short for `steps = steps + 1`.
   - `1..=10` is a **range** from 1 to 10, *including* 10 (the `=`).
     `1..10` would stop at 9.

3. **The last line.** **Ask:** "Where's the `return`?" **Say:** "The last
   line, `steps`, has no semicolon. In Rust, the last **expression** in a
   block, with no semicolon, is its value. So the function gives back
   `steps`." Add a semicolon: `steps;`. `cargo run`. **They should see:**
   ```
   error[E0308]: mismatched types
   ```
   with a picture that says `expected \`u32\`, found \`()\``, and at the
   bottom, `help: remove this semicolon to return this value`.
   **Say:** "A semicolon turns an expression into a **statement**, which
   has no value. `()` is Rust's word for 'no value'. The compiler even
   says how to fix it." Take the semicolon out. (`return steps;` works
   too, but Rust programmers keep `return` for leaving a function
   early.)

### Session 2: if is an expression

4. **If with a value.** Change the loop in `main`:
   ```rust
       for n in 1..=10 {
           let kind = if n % 2 == 0 { "even" } else { "odd" };
           println!("{n} ({kind}) takes {} steps", collatz_steps(n));
       }
   ```
   **They should see:** `1 (odd) takes 0 steps`, `2 (even) takes 1
   steps`, and so on. **Say:** "The `if` *has a value*: `"even"` or
   `"odd"`. In Python you'd write `"even" if n % 2 == 0 else "odd"`. In
   C, `n % 2 == 0 ? "even" : "odd"`."

5. **The hunt.** Add to the end of `main`:
   ```rust
       let mut best = 1;
       for n in 1..10000 {
           if collatz_steps(n) > collatz_steps(best) {
               best = n;
           }
       }
       println!("Under 10000, {best} takes the most: {} steps", collatz_steps(best));
   ```
   **Ask:** "Guess first: which number under 10,000 takes the most
   steps?" Write the guess down, then `cargo run`. **They should see:**
   ```
   Under 10000, 6171 takes the most: 261 steps
   ```
   **Say:** "6171 climbs up and down 261 times before it reaches 1." Try
   `cargo run --release` and notice how fast it is. Commit.

6. **Rustlings.** Do the `functions`, `if` and `primitive_types`
   exercises, and `quiz1`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0308]: mismatched types` ... `expected \`u32\`, found \`()\`` | The last line of the function has a semicolon | Remove it, so the value is returned. |
| `` `if` and `else` have incompatible types `` | The two branches of an `if` give different kinds of value | Make both give the same type. |
| `expected one of ... found \`{\`` near an `if` | Brackets or `then` from another language | Rust's `if` is `if condition { ... }`. |
| `error[E0308]: mismatched types` at a function call | An argument of the wrong type, such as a `u32` for a `u64` | Match the type in the function's first line. |
| The program runs for ages | The `while` never ends: check `n` really changes each time round | Ctrl+C, and check the loop. |

## Talk about it

- What's the difference between an expression and a statement?
- Why does a semicolon on the last line cause an error?
- What does `1..=10` mean? And `1..10`?
- What's the Collatz conjecture? Why do mathematicians still not know if
  it's true?

## Challenge *(if there's time, or for next time)*

- Which number under a million takes the most steps? Use `cargo run
  --release`, and time it with `time`. *(837,799, with 524 steps.)*
- Write `fn is_even(n: u64) -> bool` and use it in both places.
- Rust has a `loop` that goes for ever, and `break` can give a value:
  `let x = loop { ... break 42; };`. Rewrite the hunt to stop at the
  first number that takes more than 100 steps.

## Checkpoint

The learner can, without help:
- [ ] Write a function with typed arguments and a return type
- [ ] Explain why the last line has no semicolon
- [ ] Use `if` as an expression, and `while` and `for` with ranges
- [ ] Finish `functions`, `if`, `primitive_types` and `quiz1` in Rustlings

## Lab notebook

Write the Collatz chain for 6 or 7 as a zigzag graph (up for ×3+1, down
for halving). Write the hunt's answer and your guess. Commit. Add
*expression*, *statement*, *return type* and *range* to `dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows Chapters 3.3 and 3.5 of the Book. "Everything is an
expression" comes from functional languages (Stage 12 shows more). Blocks
`{ ... }`, `if`, `match` and `loop` all have values, which is why Rust
has no `?:` operator.

The Collatz conjecture (Lothar Collatz, 1937) has been checked by
computer for every number up to about 2^68, and Terence Tao proved in
2019 that "almost all" numbers reach small values. It remains unproved.
The counts in this lesson come from the course's own tested program.
