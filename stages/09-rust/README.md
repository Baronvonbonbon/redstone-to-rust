# Stage 9: Rust

**Badge:** Rustacean · **Needs first:** Stage 8 · **Lessons:** 18

In Stage 8 the learner wrote C, and broke it in every classic way: a
buffer overflow, a null pointer, a leak, use after free. Rust is a
language as fast and as close to the machine as C, whose compiler
refuses to build those bugs. From this stage on, it's the course's main
language.

The stage has four parts:

- **The core of the language** (Lessons 9.1–9.9): Cargo, types and
  overflow, functions, **ownership** and **borrowing** (acted out with
  toys and a book before they're typed), structs, enums with `Option`,
  collections, and errors with `Result`. Each idea is set against the C
  bug it prevents, and each lesson ends with a batch of **Rustlings**
  exercises.
- **The assembler again** (9.10–9.12): the learner's Nand to Tetris
  assembler from Lesson 6.13, rewritten in Rust and checked against the
  official one, then tidied with a module, unit tests, `cargo fmt` and
  Clippy.
- **Bigger ideas** (9.13–9.15): traits and generics; iterators and
  closures; and **crates**, with the offline **Rust Cookbook**.
- **Building things** (9.16–9.18): **Creeper Chase**, a terminal game
  with a creeper that hunts the player, diamonds, a saved high score and
  tests; then a project of the learner's own, and the rest of Rustlings.

Every program in the lessons was compiled and run with Rust 1.99, and
every error message is a real one, from a deliberately broken version.
The game was played on a real terminal by a test script.

## Tools

- **Rust**, **Rustlings** and the **crate kit**, installed into the
  learner's account by one script, once, while online. From your own
  account, before Lesson 9.1: `./scripts/give-lab.sh LEARNER rust`; then
  as the learner: `bash ~/lab/rust/setup-rust.sh`. Lesson 9.1 and the
  [Rust lab handbook](../../labs/rust/README.md) have the details. After
  that, everything in this stage works offline.
- **The books, offline:** `rustup doc --book` opens *The Rust Programming
  Language* ("the Book"), `rustup doc --rust-by-example` opens *Rust by
  Example*, and `rustup doc --std` the standard library's documentation.
- **The Rust Cookbook**, in the offline library
  (`/srv/redstone-library/repos/rust-cookbook`), for Lesson 9.15.
- **The Nand to Tetris tools** from Stage 6, for `check-hack` (Lessons
  9.10–9.12).
- **A text editor.** The system's Text Editor colours Rust code; `nano`
  works too. (An editor with Rust support, such as one with
  `rust-analyzer`, is a nice extra, but not needed.)
- **(Free, in the offline library)** *Comprehensive Rust*, Google's
  course for its own engineers, for the guide or an older learner.

## A note on solutions

The Rust programs in Lessons 9.1–9.9 and 9.13–9.17 are the course's own,
and appear in full. **The assembler (9.10–9.12) is Nand to Tetris
Project 6**, so, as in Stages 6 and 8, the lessons give the plan, the
parts that aren't the project itself, and hints; `check-hack` is the
judge. Please keep the learner's assembler private.

Rustlings has its own `solutions` folder, which fills in as each
exercise is solved: it's fine for the learner to compare afterwards.

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 9.1 | [Hello, Rust](01-hello-cargo.md) | `cargo new`, `cargo run`, debug and release, the Book offline, Rustlings | Cargo, crates |
| 9.2 | [Variables and Types](02-variables-and-types.md) | `let` and `mut`, number types, overflow that panics instead of wrapping | immutability, types |
| 9.3 | [Functions, Ifs and Loops](03-functions-and-control-flow.md) | Hailstone numbers again; the last expression is the answer | expressions |
| 9.4 | [Ownership](04-ownership.md) | Acting out moves with toys; clones and copies; torches that burn out | ownership, drop |
| 9.5 | [Borrowing](05-borrowing.md) | Lending a book; `&` and `&mut`; slices; no dangling pointers | the borrow checker |
| 9.6 | [Structs and Methods](06-structs.md) | A `Mob` that can be hit, die, and measure distances | structs, `impl` |
| 9.7 | [Enums, Match and Option](07-enums-and-option.md) | Blocks as an enum; exhaustive `match`; no null | enums, `Option` |
| 9.8 | [Vecs, Strings and HashMaps](08-collections.md) | A chest, a loot counter, a bounds check that C didn't have | collections |
| 9.9 | [When Things Go Wrong: Result](09-errors.md) | Parsing levels; `?`; `wc` again, in Rust | `Result`, errors |
| 9.10 | [The Assembler Again, in Rust: Part 1](10-assembler-in-rust-1.md) | A- and C-instructions; `SAME` for the files without symbols | rewriting |
| 9.11 | [The Assembler Again, in Rust: Part 2](11-assembler-in-rust-2.md) | A symbol table struct, two passes, Pong, a race with Python | symbol tables |
| 9.12 | [Tidy Code: Modules, Tests and Clippy](12-modules-tests-clippy.md) | `mod`, `pub`, `cargo test`, `cargo fmt`, Clippy on old projects | testing, linting |
| 9.13 | [Traits and Generics](13-traits-and-generics.md) | A `Mob` trait, a Vec of different mobs, a generic `largest` | traits, generics |
| 9.14 | [Iterators and Closures](14-iterators-and-closures.md) | A conveyor belt; squares, primes, words, Collatz in one line | iterators, closures |
| 9.15 | [Crates and the Rust Cookbook](15-crates-and-the-cookbook.md) | Dice, treasure coordinates, saving a player; recipes offline | crates, JSON |
| 9.16 | [Creeper Chase, Part 1](16-terminal-game-1.md) | A field, a player and a game loop in the terminal | raw mode, game loop |
| 9.17 | [Creeper Chase, Part 2](17-terminal-game-2.md) | The creeper, diamonds, a high score file, tests for the rules | game state, testing |
| 9.18 | [Project: My Own Rust Program](18-rust-project.md) | A specification, milestones, the last Rustlings; Stage 9 checkpoint | putting it together |

### Rustlings, lesson by lesson

| After lesson | Exercises |
|---|---|
| 9.1 | `intro` |
| 9.2 | `variables` |
| 9.3 | `functions`, `if`, `primitive_types`, `quiz1` |
| 9.4 | `vecs`, `move_semantics1`–`3` |
| 9.5 | `move_semantics4`–`5` |
| 9.6 | `structs` |
| 9.7 | `enums` |
| 9.8 | `strings`, `modules`, `hashmaps`, `quiz2` |
| 9.9 | `options`, `errors` |
| 9.13 | `generics`, `traits`, `quiz3`, `lifetimes`, `tests` |
| 9.14 | `iterators` |
| 9.18 | `box1`, `rc1`, `arc1`, `cow1`, `threads`, `macros`, `clippy`, `conversions` |

## Setup notes

- Give the `rust` lab and run `setup-rust.sh` before Lesson 9.1, while
  online (see Tools). After that, the stage needs no internet.
- The learner's projects live in `~/lab/rust`, one folder each. `cargo
  new` makes each one a git repository by itself.
- The first `cargo run` of each project takes a while (it compiles), and
  later ones are quick. Projects that use crates take longer the first
  time.
- Each project's `target` folder holds compiled files, and can be large
  (about 170 MB for the game). `cargo clean` deletes it safely; it's
  made again by the next build.

## Free play for this stage

- More Rustlings, again: `rustlings reset NAME` and do favourites twice.
- *Rust by Example* (`rustup doc --rust-by-example`): short, runnable
  pages on everything in this stage.
- More Cookbook recipes that use the kit's crates.
- Rewriting earlier Python programs (the mob book, the secret code
  machine, rock, paper, scissors) in Rust.
- Making Creeper Chase harder: walls, more creepers, levels.

## Habits to build now

- **Read the whole error.** Rust's compiler explains itself, and usually
  suggests the fix. `rustc --explain` for more.
- **`cargo fmt`, `cargo clippy`, `cargo test` before every commit.**
- **Model the data first.** Structs and enums on paper, then code.
- **Handle every error.** `match` or `?`, and `unwrap` only when an
  error would mean a bug.
- **Small milestones.** A tiny version that works, then grow it.

## Checkpoint

The learner can, without help:
- [ ] Explain ownership, moves, clones and copies, and when values are
      dropped
- [ ] Explain the borrowing rule, and fix the borrow checker's common
      errors
- [ ] Use structs, enums, `match`, `Option` and `Result`, with `?`
- [ ] Use Vecs, HashMaps, iterators and closures
- [ ] Write a trait, and a generic function with a trait bound
- [ ] Add a crate, and use a Cookbook recipe offline
- [ ] Organise a program into modules, with unit tests

They can also:
- [ ] Get `SAME` for every Project 6 program with their Rust assembler
- [ ] Play Creeper Chase, with its tests passing
- [ ] Finish every Rustlings exercise
- [ ] Build a program of their own (Lesson 9.18)
