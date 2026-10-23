# Lesson 9.12: Tidy Code: Modules, Tests and Clippy

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust/hack-asm` from Lesson 9.11; the earlier Rust
projects · **New words:** module, `pub`, private, unit test, assertion,
`cargo test`, `cargo fmt`, Clippy, lint

## Goal *(read this to the learner)*

> Your assembler works. Now make it *tidy*: split it into two files, add
> tests that check its pieces every time you change it, and let two of
> Rust's helpers loose on it: `cargo fmt`, which lays code out neatly,
> and **Clippy**, which reads your code and suggests better ways to
> write it. Real Rust programmers use all four every day.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Check `check-hack pong/Pong.asm` says `SAME` (Lesson 9.11).

## Warm-up (5 min)

"In Lesson 8.18, how did you know a change to your translator hadn't
broken anything?" *(We ran all eleven tests again.)* "Today Rust runs
the tests for us, with one command."

## Activity

### Session 1: a module

1. **Two files.** **Say:** "`main.rs` does two jobs: reading files and
   symbols, and turning one instruction into bits. The bits part never
   changes and doesn't need the rest, so it can have its own file: a
   **module**."

   In `~/lab/rust/hack-asm/src`, make a new file `code.rs`. *Move* (cut
   and paste) these functions from `main.rs` into it: `a_instruction`,
   `comp_bits`, `jump_bits`, `dest_bits` and `c_instruction`.

2. **Joining them up.** At the very top of `main.rs`, add:
   ```rust
   mod code;
   ```
   **Say:** "That line says: there's a module called `code`, in
   `code.rs`." Now `cargo build`. **They should see:**
   ```
   error[E0425]: cannot find function `a_instruction` in this scope
   ```
   and the same for `c_instruction`. **Say:** "Things in a module are
   called by the module's name first: `code::a_instruction`." Change the
   calls in `translate` to `code::a_instruction(...)` and
   `code::c_instruction(...)`, and build again. **They should see:**
   ```
   error[E0603]: function `a_instruction` is private
   ```
   **Say:** "Everything in a module is **private** unless you say
   otherwise: only the module itself can use it. That keeps the inside
   of a module from being tangled up with everything else." Put `pub`
   (for *public*) in front of each `fn` in `code.rs`: `pub fn
   a_instruction(...)`. Build again: no errors.

3. **Still the same?**
   ```
   cd ~/lab/n2t/projects/6
   check-hack max/Max.asm
   check-hack pong/Pong.asm
   ```
   **They should see:** `SAME` twice. Commit.

### Session 2: tests

4. **A test module.** At the bottom of `code.rs`, add:
   ```rust
   #[cfg(test)]
   mod tests {
       use super::*;

       #[test]
       fn a_instructions() {
           assert_eq!(a_instruction(21), "0000000000010101");
           assert_eq!(a_instruction(0), "0000000000000000");
       }

       #[test]
       fn c_instructions() {
           assert_eq!(c_instruction("D=M"), Ok(String::from("1111110000010000")));
           assert_eq!(c_instruction("0;JMP"), Ok(String::from("1110101010000111")));
           assert!(c_instruction("D=Q").is_err());
       }
   }
   ```
   **Say:** "Each `#[test]` function is a **unit test**: a small check of
   one piece. `assert_eq!(a, b)` is an **assertion**: it says 'a must
   equal b', and fails the test if not. `assert!` checks something is
   true. `#[cfg(test)]` means this module is only built for testing, and
   `use super::*` lets the tests see everything in `code.rs`."

   **Ask:** "Check the second one with the Hack card: is `0;JMP` really
   `1110101010000111`?" *(111, then a=0 and comp `0` is 101010, dest
   000, jump JMP 111.)*

5. **Run them.** In `~/lab/rust/hack-asm`:
   ```
   cargo test
   ```
   **They should see**, after the compiling lines:
   ```
   running 2 tests
   test code::tests::a_instructions ... ok
   test code::tests::c_instructions ... ok

   test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
   ```

6. **Make one fail.** Change `"0000000000010101"` to
   `"0000000000010100"` in the test, and `cargo test`. **They should
   see:**
   ```
   test code::tests::a_instructions ... FAILED
   ```
   and further down:
   ```
   assertion `left == right` failed
     left: "0000000000010101"
    right: "0000000000010100"
   ```
   **Say:** "`left` is what the function gave, and `right` is what the
   test expected. Here the test was wrong, not the function. Usually it's
   the other way round, and the test has caught a bug." Put it back, and
   check it passes. Add a test of your own for a dest with all three
   registers, `AMD=D+1`. Commit.

### Session 3: fmt and Clippy

7. **`cargo fmt`.** **Say:** "Every Rust project in the world can be laid
   out the same way, by one tool."
   ```
   cargo fmt --check
   ```
   **They should see:** either nothing (already neat), or `Diff in ...`
   with lines marked `-` (how it is) and `+` (how `fmt` would lay it
   out). Then:
   ```
   cargo fmt
   git diff
   ```
   **Say:** "It changed the layout, never what the code does. Run the
   tests again to be sure." `cargo test`, and commit.

8. **Clippy.** **Say:** "Clippy is a **linter**: it reads your code and
   warns about things that work, but could be written better. Each
   warning is a **lint**." Try it on some of the first projects from this
   stage:
   ```
   cd ~/lab/rust/variables
   cargo clippy
   ```
   **They should see:**
   ```
   warning: manual implementation of an assign operation
    --> src/main.rs:5:5
     |
   5 |     health = health - 3;
     |     ^^^^^^^^^^^^^^^^^^^ help: replace it with: `health -= 3`
   ```
   Then `~/lab/rust/collatz` and `~/lab/rust/borrowing`. **They should
   see:** for Collatz, `manual implementation of \`.is_multiple_of()\``
   (suggesting `n.is_multiple_of(2)`) and the same assign one for
   `n = n / 2`. For borrowing, `writing \`&String\` instead of \`&str\``,
   which Lesson 9.5 promised. Fix each one the way Clippy suggests, check
   the program still prints the same, and commit.

9. **Clippy on the assembler.** `cd ~/lab/rust/hack-asm` and `cargo
   clippy`. Fix anything it finds, run `cargo test` and a `check-hack`,
   and commit. **Say:** "From now on: `cargo fmt`, `cargo clippy` and
   `cargo test` before every commit."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0425]: cannot find function \`a_instruction\` in this scope` | The function moved to `code.rs`, but is called without its module | `code::a_instruction`. |
| `error[E0603]: function \`c_instruction\` is private` | It's in the module, but not `pub` | `pub fn`. |
| `error[E0433]: cannot find module or crate \`code\` in this scope` | `mod code;` is missing from `main.rs` | Add it at the top. |
| `error[E0583]: file not found for module \`code\`` | `code.rs` is missing, misspelt, or not in `src` | It must be `src/code.rs`. |
| `assertion \`left == right\` failed` | A test failed: `left` is what the code gave | Check which is wrong, the code or the test. |
| `error[E0425]: cannot find function` inside the tests | `use super::*;` is missing | Add it at the top of `mod tests`. |
| `cargo clippy` says nothing at all | No suggestions: well done! | Nothing. |

## Talk about it

- Why split a program into modules? What does `pub` do?
- What does a unit test check? Why keep tests next to the code?
- What's the difference between `cargo fmt` and `cargo clippy`?
- Clippy suggested `health -= 3`. Was the old code wrong?

## Challenge *(if there's time, or for next time)*

- Move `SymbolTable` into its own module, `symbols.rs`, with tests:
  `R5` is 5, `SCREEN` is 16384, and the first two new variables get 16
  and 17.
- Run `cargo clippy` on every project in `~/lab/rust`, and fix them all.
- `cargo test` runs tests in `main.rs` too. What would a good test of
  `clean` be?

## Checkpoint

The learner can, without help:
- [ ] Move code into a module, with `mod` and `pub`
- [ ] Write a unit test with `assert_eq!`, run `cargo test`, and read a
      failure
- [ ] Use `cargo fmt` and `cargo clippy`, and explain what each does
- [ ] Keep `check-hack` saying `SAME` after every change

## Lab notebook

Draw the assembler as two boxes, `main.rs` and `code.rs`, with arrows
for the calls between them, and mark the `pub` functions. Write the
before-commit routine: fmt, clippy, test. Commit. Add *module*, *pub*,
*private*, *unit test*, *assertion*, *Clippy* and *lint* to
`dictionary.md`.

## Guide's background *(optional reading)*

This follows Chapters 7 and 11 of the Book. Rust modules form a tree
rooted at `main.rs` (or `lib.rs`); `mod code;` tells the compiler to
look for `code.rs` next to it. Privacy is per module, so `tests`, a
child module of `code`, can use private items with `use super::*`.

Unit tests in Rust conventionally live in the same file as the code, in
a `#[cfg(test)] mod tests` block; integration tests go in a `tests/`
folder. `cargo test` builds a special test binary and runs every
`#[test]` function, in parallel.

Clippy has hundreds of lints, grouped by how sure it is; the default
set is warnings that are nearly always worth taking. Lessons 9.2, 9.3
and 9.5 deliberately wrote code in the simplest way so that this lesson
has something to find. The messages shown came from Rust 1.99; newer
versions may word them differently or find more.
