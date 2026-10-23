# Lesson 9.2: Variables and Types

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust` · **New words:** variable, mutable, immutable,
type, integer, float, overflow, panic

## Goal *(read this to the learner)*

> In Python, a variable can change whenever you like, and hold anything.
> In C, you said the type, and C let you change anything. Rust asks you
> to say which variables are *allowed* to change, and it checks every
> type. Today you'll learn Rust's variables and number types, and find
> out what Rust does when a number gets too big, which is different from
> what C did.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Look back at Lesson 6.5 (two's complement) and Lesson 8.1 (C's
      types), if you've forgotten them.

## Warm-up (5 min)

"In Hack, how many bits did a number have?" *(16.)* "What happened when
you added 1 to the biggest one?" *(It wrapped round to the most negative
one.)* "That's called **overflow**. Today we see what Rust does about it."

## Activity

### Session 1: let and mut

1. **A new project.**
   ```
   cd ~/lab/rust
   cargo new variables
   cd variables
   ```
   Replace `src/main.rs` with:
   ```rust
   fn main() {
       let diamonds = 64;
       let mut health = 20;
       println!("I have {diamonds} diamonds and {health} health.");
       health = health - 3;
       println!("A zombie hit me! Now I have {health} health.");
   }
   ```
   `cargo run`. **They should see:**
   ```
   I have 64 diamonds and 20 health.
   A zombie hit me! Now I have 17 health.
   ```
   **Say:** "`let` makes a **variable**. `{health}` inside the quotes
   prints it, like Python's f-strings."

2. **Not allowed to change.** Take out the `mut`: `let health = 20;`.
   `cargo run`. **They should see:**
   ```
   error[E0384]: cannot assign twice to immutable variable `health`
   ```
   and further down, `help: consider making this binding mutable`.
   **Say:** "In Rust, a variable is **immutable** (not allowed to
   change) unless you write `mut`, for **mutable**. Most variables never
   change, and when you read `let mut`, you know to watch that one." Put
   the `mut` back.

   **Ask:** "Why might that be a good rule?" *(You can't change something
   by accident, and you know which values can change when you read the
   program.)*

3. **Types.** Add these lines at the end of `main`:
   ```rust
       let level: u8 = 250;
       let blocks_in_world: i64 = 9_000_000_000;
       let speed: f64 = 4.3;
       let letter: char = 'C';
       let is_night: bool = true;
       println!("level {level}, blocks {blocks_in_world}, speed {speed}, letter {letter}, night {is_night}");
   ```
   **They should see**, after the first two lines:
   ```
   level 250, blocks 9000000000, speed 4.3, letter C, night true
   ```
   **Say:** "After the colon is the **type**. Rust usually works it out
   by itself (`diamonds` is an `i32`), but you can say it." Draw this on
   paper:

   | Type | What it holds | Bits |
   |---|---|---|
   | `u8` | whole numbers 0 to 255 | 8 |
   | `i32` | whole numbers, about −2 billion to 2 billion (the usual one) | 32 |
   | `i64` | whole numbers, much bigger | 64 |
   | `u64` | whole numbers 0 and up, very big | 64 |
   | `f64` | numbers with a decimal point (a **float**) | 64 |
   | `char` | one letter or symbol | 32 |
   | `bool` | `true` or `false` | 8 |

   **Say:** "`u` means *unsigned* (no minus sign), and `i` means
   *integer*, which can be negative. The number is how many bits. The
   underscores in `9_000_000_000` are just for reading: Rust ignores
   them."

4. **Too big to fit.** Change `250` to `300` in the `level` line, and
   `cargo run`. **They should see:**
   ```
   error: literal out of range for `u8`
   ```
   **Ask:** "Why?" *(A `u8` has 8 bits, and the biggest is 255.)* Put it
   back to 250. Commit.

### Session 2: overflow

5. **Overflow while running.** **Say:** "That was a number that was too
   big when the program was *written*. What about one that grows too
   big while it *runs*?"
   ```
   cd ~/lab/rust
   cargo new overflow
   cd overflow
   ```
   ```rust
   fn main() {
       let mut level: u8 = 250;
       for _ in 0..10 {
           level = level + 1;
           println!("level {level}");
       }
   }
   ```
   **Say:** "`0..10` counts from 0 up to 9, like Python's `range(10)`.
   The `_` means we don't need the counter's value." `cargo run`.
   **They should see:**
   ```
   level 251
   level 252
   level 253
   level 254
   level 255

   thread 'main' (92) panicked at src/main.rs:4:17:
   attempt to add with overflow
   ```
   (The number after `'main'` will be different.) **Say:** "The program
   stopped itself. That's called a **panic**: Rust found something
   wrong, and stopped rather than carry on with a wrong number. It even
   says the line and column: line 4, column 17."

6. **Release mode.** Run it again with `cargo run --release`. **They
   should see:** `level 255`, then `level 0`, `level 1`... up to
   `level 4`, and no panic. **Say:** "In a release build, Rust skips the
   check to be faster, and the number wraps round, like Hack and C. So
   test in debug mode, where the checks are on."

   **Ask:** "What did C do in Lesson 8.1 when a number got too big?"
   *(It wrapped round silently, even with no `--release`.)*

7. **Saying what you mean.** **Say:** "If you *want* it to wrap, or to
   stop at the top, Rust has a way to say so." Change the adding line to
   each of these in turn, and run:
   ```rust
           level = level.wrapping_add(1);
   ```
   ```rust
           level = level.saturating_add(1);
   ```
   **They should see:** the first wraps to 0 even in debug mode; the
   second stops at 255 and stays there. **Say:** "Saturating is what a
   Minecraft health bar does: it fills up, and stays full." Commit.

8. **Rustlings.** In `~/lab/rust/rustlings`, run `rustlings` and do the
   `variables` exercises (1 to 6).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0384]: cannot assign twice to immutable variable` | The variable was changed, but it has no `mut` | Add `mut` after `let`. |
| `error: literal out of range for \`u8\`` | The number doesn't fit in the type | Use a bigger type, or a smaller number. |
| `attempt to add with overflow` (a panic) | The number grew too big while running | Use a bigger type, or `wrapping_add` / `saturating_add` if that's what's wanted. |
| `warning: unused variable` | A variable is never used | Fine for now: it's only a warning. A name starting with `_` hides it. |
| `error[E0308]: mismatched types` and `error[E0277]: cannot add \`i32\` to \`u8\`` | A number of one type is mixed with another, such as `u8` and `i32` | Make them the same type, for example with `as`: `level as i32`. |

## Talk about it

- Why are Rust's variables immutable unless you say `mut`?
- What's the difference between `u8` and `i8`? Between `i32` and `f64`?
- What does Rust do on overflow, in debug and in release? What does C do?
- Is a panic good or bad?

## Challenge *(if there's time, or for next time)*

- What's the biggest `u64`? Print `u64::MAX`. And `i32::MIN`?
- Try `let x = 7 / 2;` and `let y = 7.0 / 2.0;`. Why are they different?
- Rust lets you **shadow** a variable: `let health = health + 5;` makes a
  *new* `health`. Try it with no `mut` anywhere.

## Checkpoint

The learner can, without help:
- [ ] Make variables with `let` and `let mut`, and explain the difference
- [ ] Pick a type for a number, and say how many bits it has
- [ ] Explain what Rust does on overflow in debug and release builds
- [ ] Finish the `variables` Rustlings

## Lab notebook

Copy the type table. Write what happens to a `u8` at 255 in Hack, C,
Rust debug and Rust release. Commit. Add *mutable*, *immutable*, *type*,
*integer*, *float*, *overflow* and *panic* to `dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows Chapter 3.1 and 3.2 of the Book. Integer overflow is
checked in debug builds and wraps in release builds by default (the
`overflow-checks` setting in `Cargo.toml` can change that). Either way it
is never *undefined behaviour*, which is what signed overflow is in C:
a C compiler may assume it never happens, and optimise accordingly,
which is a famous source of security bugs.

A panic stops the program with a message. It's not a crash in the C
sense: Rust unwinds the stack, calling `Drop` for everything (Lesson
9.4), and prints where it happened. `RUST_BACKTRACE=1 cargo run` shows
the chain of function calls.
