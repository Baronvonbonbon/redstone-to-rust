# Lesson 9.1: Hello, Rust

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text
editor; Rust, set up by the guide (below) · **New words:** Rust, Cargo,
crate, project, debug, release, Rustlings

## Goal *(read this to the learner)*

> In Stage 8 you met C: fast, and close to the machine, but it trusted
> you completely, and you broke it in five different ways. **Rust** is
> just as fast, and just as close to the machine, but its compiler checks
> your program before it runs and refuses to build anything that could
> overflow a buffer, leak, or use memory after freeing it. From now on,
> Rust is the main language of this course. Today you'll make your first
> Rust project, and meet the tool that runs everything: **Cargo**.

## Before the lesson *(guide, 30 min, while online)*

- [ ] Read this whole lesson once, and the [stage's README](README.md).
- [ ] From your own account: `./scripts/give-lab.sh LEARNER rust`. It
      puts the Stage 9 setup script, the crate kit and a test script in
      the learner's `~/lab/rust/`.
- [ ] Log in **as the learner** (or open a terminal there), make sure the
      computer is online, and run:
      ```
      bash ~/lab/rust/setup-rust.sh
      ```
      It takes 5 to 15 minutes. It installs Rust in the learner's own
      account (no admin needed), the Rust books for offline reading,
      **Rustlings** (small practice exercises), and the outside libraries
      Stage 9 uses. At the end it switches Cargo to offline mode. Then
      close that terminal.
- [ ] Check, in a new terminal: `cargo --version` prints a version, and
      `ls ~/lab/rust` shows `rustlings` and `crate-kit`.

## Warm-up (5 min)

"In Stage 8, which bugs did C let you write?" *(Buffer overflow, null
pointer crash, memory leak, use after free, double free.)* "Which tools
caught them?" *(The sanitizer, valgrind, gdb: but only when the program
ran.)* **Say:** "Rust catches those before the program ever runs."

## Activity

### Session 1: Cargo

1. **A new project.**
   ```
   cd ~/lab/rust
   cargo new hello
   cd hello
   ls -a
   ```
   **They should see:** `.git`, `.gitignore`, `Cargo.toml` and `src`.
   **Say:** "`cargo new` made a whole **project**: a folder with a git
   repository already in it, a settings file, and a `src` folder for the
   source code. A Rust project is also called a **crate**."

   Look inside both files:
   ```
   cat Cargo.toml
   cat src/main.rs
   ```
   **They should see:** `Cargo.toml` with the project's `name`,
   `version` and `edition`, and an empty `[dependencies]`; `main.rs` with:
   ```rust
   fn main() {
       println!("Hello, world!");
   }
   ```
   **Say:** "`fn` makes a function, and `main` is where every Rust
   program starts, as in C. `println!` prints a line. The `!` means it's
   a **macro**: a shortcut that writes some code for you."

2. **Run it.**
   ```
   cargo run
   ```
   **They should see** something like:
   ```
      Compiling hello v0.1.0 (/home/sam/lab/rust/hello)
       Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.61s
        Running `target/debug/hello`
   Hello, world!
   ```
   **Say:** "One command did three things: compiled the program (like
   `gcc`), put the executable in `target/debug/hello`, and ran it." Run
   `cargo run` again: it's faster, because nothing changed.

3. **Make it yours.** Open `src/main.rs` in the Text Editor (it colours
   Rust code; `nano` is fine too). Change the message to `Hello from
   Rust!`, save, and `cargo run`. **They should see:** `Hello from
   Rust!`. Commit (the repository is already there):
   ```
   git add .
   git commit -m "Hello from Rust"
   ```
   **Ask:** "What does `.gitignore` say?" (`cat .gitignore`.) *(`/target`:
   the compiled files are never committed. They can always be made
   again.)*

4. **A mistake.** Take the `!` out of `println!`, and `cargo run`.
   **They should see:**
   ```
   error[E0423]: cannot find function `println` in this scope
   ```
   followed by a picture of the line, and:
   ```
   help: use `!` to invoke the macro
   ```
   **Say:** "Rust's error messages are famous for being helpful. Every
   error has a code, like `E0423`. `rustc --explain E0423` explains it at
   length, with examples." Try it, then put the `!` back.

### Session 2: debug and release, and the books

5. **Two kinds of build.**
   ```
   cargo build --release
   ls -l target/debug/hello target/release/hello
   ```
   **They should see:** the debug one is several megabytes (about 4.5
   million bytes), and the release one far smaller (about 450,000).
   **Say:** "A **debug** build compiles quickly and keeps extra
   information for finding bugs, and it checks for things like numbers
   overflowing. A **release** build takes longer to compile, and makes
   the fastest program it can. `cargo run --release` runs that one.
   Rust's programs are bigger than C's 16,000 bytes, because each one
   carries its own copy of the parts of the standard library it uses."

6. **The books, offline.**
   ```
   rustup doc --book
   ```
   **They should see:** *The Rust Programming Language* ("the Book") opens
   in the web browser, from files on this computer, with no internet.
   **Say:** "This book is how most people learn Rust. Each lesson in this
   stage says which chapter goes with it. `rustup doc --std` opens the
   standard library's documentation, and `rustup doc --rust-by-example`
   opens a book of small examples." Read Chapter 1.2 ("Hello, World!")
   together.

7. **Rustlings.** **Say:** "Rustlings is a set of small broken programs.
   You fix each one, and it tells you when you've got it."
   ```
   cd ~/lab/rust/rustlings
   rustlings
   ```
   The very first time, **they should see** a welcome message ending in
   `Press ENTER to continue`: read it together, and press Enter. Then
   **they should see:** a progress bar, and a message about the first
   exercise, `exercises/00_intro/intro1.rs`. Open that file in the editor,
   read it, and follow what it says. Each time the file is saved,
   Rustlings checks it again. When an exercise passes, press `n` for the
   next one. `h` shows a hint, `l` lists all the exercises, and `q`
   quits (the keys are listed at the bottom). Do `intro1` and
   `intro2`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `cargo: command not found` | Rust isn't set up, or the terminal was opened before setup | Open a new terminal. If it still fails, the guide runs `setup-rust.sh` again, online. |
| `error[E0423]: cannot find function \`println\`` | The `!` is missing | `println!`. |
| `error: could not find \`Cargo.toml\`` | `cargo run` was typed outside the project folder | `cd` into the project first. |
| `rustlings: command not found`, or Rustlings says the folder is wrong | Not in the Rustlings folder, or setup didn't finish | `cd ~/lab/rust/rustlings`, then `rustlings`. |
| The Rustlings screen looks stuck | It's waiting for the file to be saved | Save the exercise file in the editor. |
| `rustup doc` shows an empty page | The docs weren't installed | Online, in the learner's account: `rustup component add rust-docs`. |

## Talk about it

- What does Cargo do? What's in a Rust project?
- Why does every Rust error have a code?
- What's the difference between a debug build and a release build?
- How is Rust like C, and how is it different?

## Challenge *(if there's time, or for next time)*

- Make `cargo run` print a Creeper face with several `println!` lines.
- Time the C and Rust versions of the 100-million race from Lesson 8.1.
  *(Write the loop in Rust with `let mut total: u64 = 0;` and
  `for i in 0..100_000_000 { total += i; }`, and use `--release`.)*
- Read Chapter 1.3 of the Book, "Hello, Cargo!".

## Checkpoint

The learner can, without help:
- [ ] Make a project with `cargo new`, and run it with `cargo run`
- [ ] Explain what's in `Cargo.toml` and `src/main.rs`
- [ ] Read a Rust error, and find its explanation with `rustc --explain`
- [ ] Open the Book offline, and use Rustlings

## Lab notebook

Draw a Rust project's folders, with what each one is for. Commit. Add
*Rust*, *Cargo*, *crate*, *debug*, *release* and *Rustlings* to
`dictionary.md`.

## Guide's background *(optional reading)*

Rust was started by Graydon Hoare in 2006 and reached version 1.0 in
2015. It's now used in Linux, Windows, Android, Firefox and many other
places, mostly to replace C and C++ where memory bugs are dangerous. Its
**borrow checker** (Lessons 9.4 and 9.5) proves at compile time that a
program has no use-after-free, double free, dangling pointer or data
race, without the run-time cost of a garbage collector.

**rustup** installs and updates the Rust toolchain in
`~/.rustup` and `~/.cargo`, inside the learner's own account. **Cargo**
builds projects, runs tests and manages **crates** (libraries). Because
this course is offline-first, `setup-rust.sh` downloads a small kit of
crates once and then sets `net.offline = true` in `~/.cargo/config.toml`.
Lesson 9.15 explains what that means, and the
[Rust lab handbook](../../labs/rust/README.md) says how to go online
again if you ever need a crate that isn't in the kit.

The sizes and times in this lesson came from Rust 1.99 on one computer.
Yours will differ a little.

Rustlings keeps a `solutions` folder next to `exercises`; each solution
appears there only after the learner solves that exercise, for
comparing. It's fine for them to look at those.
