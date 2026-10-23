# Lesson 9.18: Project: My Own Rust Program

**Time:** 5–6 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust`; squared paper · **New words:** specification,
milestone, smart pointer, thread

## Goal *(read this to the learner)*

> You've learned the whole of Rust's core: ownership and borrowing,
> structs and enums, `Option` and `Result`, traits, iterators, crates
> and tests. Now you'll plan and build a program of your own choice,
> and finish the last of the Rustlings, which show a few more of Rust's
> tools. At the end, you'll show it off, and earn the **Rustacean**
> badge.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once.
- [ ] Read the project ideas in step 1 with the learner a day early, so
      they can think about it.
- [ ] Plan a demo day for the last session.

## Warm-up (5 min)

"Which Rust idea was hardest? Which was most surprising?" Write both
down; come back to them on demo day.

## Activity

### Session 1: choosing and planning

1. **Choose.** Some ideas (or the learner's own):
   - **A Python game, again.** Rewrite one of the Stage 3 games in Rust,
     in the terminal: rock, paper, scissors (Lesson 3.4), or the text
     adventure (Lessons 3.11 and 3.12) with rooms as structs and
     directions as an enum.
   - **Creeper Chase 2.** Walls, several creepers, levels loaded from
     text files, a creeper that finds its way round walls with
     breadth-first search (Lesson 7.14).
   - **The Game of Life**, in the terminal with `crossterm`: a grid of
     cells that live or die by their neighbours.
   - **A Hack disassembler**: `.hack` back to assembly, with tests.
   - **A maze maker and solver**: the maze project from Lesson 7.16, in
     Rust.
   - **A Mineshaft helper tool**: a command-line tool in the style of
     Lesson 8.5 (a word counter, a ROT13 filter, a `grep` of your own)
     that reads files and standard input, with good error messages.

   **Say:** "Choose something you'd *use* or *play*. It should take about
   four sessions: big enough to be proud of, small enough to finish."

2. **A specification.** **Say:** "A **specification** says what the
   program will do, before you write it." On paper, the learner writes:
   - What it does, in three sentences.
   - What the user types or presses, and what they see. Draw the screen.
   - The structs and enums it needs, with their fields.
   - Three **milestones**: small versions that work, each a bit more
     than the last. The first should be finished by the end of Session 2.

   Check the plan together. **Ask:** "What's the smallest version that
   does something?" Make that milestone 1.

### Sessions 2 to 4: building

3. **Build in milestones.** For each one:
   - `cargo new` (for the first), or carry on.
   - Write a little, `cargo run`, repeat.
   - Put the rules in methods, and write at least one test for each
     milestone.
   - Before each commit: `cargo fmt`, `cargo clippy`, `cargo test`.
   - Commit at the end of every session, even if it's not finished.

   **Say:** "When the compiler complains, read the whole message aloud,
   then do what it says. It's usually right."

4. **When stuck.** In this order:
   - Read the error again, and `rustc --explain` its code.
   - Look up the type or method in `rustup doc --std` (search box at the
     top).
   - Find the matching chapter of the Book, or a recipe in the Cookbook.
   - Make a tiny new project that tries *only* the thing that's not
     working.
   - Then ask the guide.

### Alongside: the last Rustlings

5. **The rest of Rustlings.** These show tools that the project might
   need. Spread them over the sessions:
   - `box1`, `rc1`, `arc1`, `cow1`: **smart pointers**, which own
     something on the heap in different ways. `Box` you've met. `Rc` lets
     several owners share one value; `Arc` does the same across threads.
   - `threads1` to `threads3`: **threads** let a program do several
     things at once. **Say:** "Remember the borrowing rule: many readers
     or one writer? That's what stops threads trampling on each other's
     data."
   - `macros1` to `macros4`: how to write things like `vec!`.
   - `clippy1` to `clippy3`.
   - The `conversions` exercises.

   When every exercise is done, Rustlings shows a message of
   congratulations. Tick it on the passport.

### Sessions 5 and 6: demo day, and the checkpoint

6. **Demo day.** The learner shows the program to someone: they explain
   what it does, run it, show one test, and show one piece of code
   they're proud of, explaining why it's written that way.

7. **The Stage 9 checkpoint.** Without notes, the learner explains,
   with drawings if they like:
   - The three rules of ownership, and a move versus a clone (Lesson
     9.4).
   - The borrowing rule, with the book (9.5).
   - What `Option` and `Result` are, and why Rust has no null (9.7, 9.9).
   - What `?` does (9.9).
   - What a trait is, and what `<T: PartialOrd>` means (9.13).
   - An iterator chain, with the conveyor belt (9.14).
   - Which C bugs from Stage 8 Rust prevents, and how.

   If any is shaky, go back to that lesson's checkpoint.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The project is too big to finish | The plan was too ambitious | Finish the current milestone, and save the rest as "next time". |
| The same borrow-checker error keeps coming back | The design fights ownership: often two things want to change the same data | Give the data one owner (often a `Game` struct), and change it through that owner's `&mut self` methods. |
| `cannot borrow ... as mutable more than once` inside a loop over a Vec | Changing the Vec while going through it | Loop over the indexes, or collect the changes first and apply them after the loop. |
| A crate that isn't in the kit | The kit has six crates | Use what's there, or ask the guide (see the Rust lab handbook). |
| Rustlings says an exercise is still wrong after the fix | The file isn't saved, or a test in the exercise still fails | Save, and read the whole Rustlings message. |

## Talk about it

- What's in your specification? What changed while you built it?
- Which part of your program are you proudest of? Why?
- What did Rust stop you from doing wrong?
- What would you add next?

## Challenge *(if there's time, or for next time)*

- Read the first chapters of *Comprehensive Rust* in the offline library
  (`/srv/redstone-library/repos/comprehensive-rust`): Google's course
  for its own engineers.
- Put the project in its own git repository and write a `README.md` for
  it: what it is, how to run it, and how to play.
- Rewrite the Stage 8 VM translator in Rust. (Keep it private: it's a
  Nand to Tetris project.)

## Checkpoint

The learner can, without help:
- [ ] Plan a program with a specification and milestones
- [ ] Build it in Rust, with tests, `fmt` and Clippy
- [ ] Finish every Rustlings exercise
- [ ] Answer the Stage 9 checkpoint questions (step 7)

## Lab notebook

Stick in the specification, and the drawing of the screen. Write what
was hardest and what was most surprising, then and now. Commit. Add
*specification*, *milestone*, *smart pointer* and *thread* to
`dictionary.md`. Stamp the Stage 9 badge, **Rustacean**, on the
passport.

## Guide's background *(optional reading)*

Rust programmers call themselves **Rustaceans**; the unofficial mascot
is Ferris the crab. A learner who has finished this stage has covered
the core of the Book (Chapters 1 to 13, plus traits and smart pointers),
all of Rustlings, and a real project, which is roughly what a working
programmer needs before starting on Rust at their job.

The commonest trouble in a first Rust project is structure, not syntax:
designs with many objects pointing at each other, natural in Python,
fight the borrow checker. The fix that the error table suggests (one
owner, changes through methods) is the standard one; the second is to
refer to things by index into a Vec rather than by reference.

Stage 10 uses Rust to look inside the operating system: processes,
memory, files and system calls.
