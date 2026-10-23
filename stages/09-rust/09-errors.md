# Lesson 9.9: When Things Go Wrong: Result

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust`; `count_words.c` from Lesson 8.5, for comparing ·
**New words:** `Result`, `Ok`, `Err`, `?`, error message, standard error

## Goal *(read this to the learner)*

> Files go missing. People type "abc" when you ask for a number. In C,
> a function said "something went wrong" with a special number, and it
> was easy to forget to check. In Rust, a function that can fail gives
> back a **Result**: either `Ok` with the answer, or `Err` with what went
> wrong, and you can't get the answer out without deciding what to do
> about the error. You'll finish by rewriting your `wc` tool from Lesson
> 8.5 in Rust.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Check `~/lab/c` still has `count_words.c` from Lesson 8.5.

## Warm-up (5 min)

"What does `Option` hold?" *(`Some(value)` or `None`.)* "What did your C
`wc` do when the file didn't exist?" *(It printed a message and exited
with 1, because we remembered to check what `fopen` gave back.)*

## Activity

### Session 1: Result and ?

1. **Reading a level.**
   ```
   cd ~/lab/rust
   cargo new levels
   cd levels
   ```
   ```rust
   use std::num::ParseIntError;

   fn read_level(text: &str) -> Result<u8, ParseIntError> {
       let level: u8 = text.trim().parse()?;
       Ok(level)
   }

   fn main() {
       for text in ["12", " 7 ", "300", "abc", ""] {
           match read_level(text) {
               Ok(level) => println!("{text:?} is level {level}"),
               Err(error) => println!("{text:?} isn't a level: {error}"),
           }
       }
   }
   ```
   **They should see:**
   ```
   "12" is level 12
   " 7 " is level 7
   "300" isn't a level: number too large to fit in target type
   "abc" isn't a level: invalid digit found in string
   "" isn't a level: cannot parse integer from empty string
   ```

2. **Reading it.** **Say:** "A `Result` is an enum, like `Option`, with
   two variants":
   ```rust
   enum Result<T, E> {
       Ok(T),
       Err(E),
   }
   ```
   - `read_level` gives back `Result<u8, ParseIntError>`: either `Ok`
     with a `u8`, or `Err` with a `ParseIntError`, which explains what
     was wrong.
   - `.trim()` takes the spaces off each end, and `.parse()` turns text
     into a number. Parsing can fail, so it gives a `Result`.
   - **The `?`** at the end means: "if this is an `Err`, stop the
     function here and give back the error; if it's `Ok`, take the value
     out." **Say:** "That one character does what four lines of C did:
     check, and pass the error up."
   - `Ok(level)` wraps the answer.
   - `{text:?}` prints the text with quotes round it, so we can see the
     spaces and the empty one.

3. **`?` needs a Result.** Change the first line of `read_level` to
   `fn read_level(text: &str) -> u8 {`. `cargo run`. **They should see**
   several errors, the first being:
   ```
   error[E0277]: the `?` operator can only be used in a function that returns `Result` or `Option` (or another type that implements `FromResidual`)
   ```
   **Say:** "`?` passes the error up, so the function has to be able to
   give one back." Put it back. Commit.

### Session 2: wc in Rust

4. **The tool.**
   ```
   cd ~/lab/rust
   cargo new count_words
   cd count_words
   ```
   ```rust
   use std::env;
   use std::fs;
   use std::process;

   fn count(text: &str) -> (usize, usize, usize) {
       let lines = text.matches('\n').count();
       let words = text.split_whitespace().count();
       let chars = text.len();
       (lines, words, chars)
   }

   fn main() {
       let args: Vec<String> = env::args().collect();
       if args.len() != 2 {
           eprintln!("Usage: {} FILE", args[0]);
           process::exit(1);
       }
       let text = match fs::read_to_string(&args[1]) {
           Ok(text) => text,
           Err(error) => {
               eprintln!("{}: {error}", args[1]);
               process::exit(1);
           }
       };
       let (lines, words, chars) = count(&text);
       println!("{lines} {words} {chars} {}", args[1]);
   }
   ```

5. **Reading it.**
   - `env::args()` gives the command-line arguments, like C's `argv`.
     `.collect()` puts them in a Vec. As in C, `args[0]` is the program's
     own name.
   - `eprintln!` prints to **standard error**, like `fprintf(stderr, ...)` in Lesson 8.5, so error
     messages don't get mixed up with real output in a pipe.
   - `process::exit(1)` stops with exit code 1, like C's `exit(1)`.
   - `fs::read_to_string` reads a whole file into a `String`. It gives a
     `Result`, because the file might not be there. The `match` handles
     both.
   - `count` gives back three numbers at once, in a **tuple**: `(lines,
     words, chars)`. `let (lines, words, chars) = ...` unpacks them.

6. **Try it.** Make a test file, and compare with the real `wc`:
   ```
   printf 'Creepers are green.\nThey go  BOOM\n\nand ruin your house.\n' > poem.txt
   cargo run -q -- poem.txt
   wc poem.txt
   ```
   **They should see:** `4 10 56 poem.txt` from ours, and the same three
   numbers from `wc`. **Say:** "`-q` makes Cargo quiet, and everything
   after `--` is given to our program, not to Cargo."

   Now the errors:
   ```
   cargo run -q
   echo $?
   cargo run -q -- nothing.txt
   echo $?
   ```
   **They should see:**
   ```
   Usage: target/debug/count_words FILE
   1
   nothing.txt: No such file or directory (os error 2)
   1
   ```
   **Say:** "The error message came from the operating system, through
   the `Result`, like `perror` in C. But in Rust, we couldn't forget to
   check." Try
   it on `src/main.rs` too, and compare with `wc src/main.rs`.

7. **Compare with C.** Open `~/lab/c/count_words.c` side by side. **Ask:**
   "Which is shorter? Which one could forget to check whether the file
   opened?" Commit.

### Session 3: Rustlings

8. Do the `options` exercises (1 to 3) and the `errors` exercises (1 to
   6). These are harder: use `h` for hints, and take two sittings if
   needed.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0277]: the \`?\` operator can only be used in a function that returns \`Result\`` | `?` in a function that can't return an error | Make the function return a `Result`, or use `match`. |
| `error[E0282]: type annotations needed` | Rust can't tell what `collect` or `parse` should make | Say the type: `let args: Vec<String> = ...`. |
| `error[E0308]: mismatched types` ... `expected \`Result<u8, ParseIntError>\`, found \`u8\`` | Returning the plain value from a function that returns a `Result` | Wrap it: `Ok(level)`. |
| `Usage: target/debug/count_words FILE` | No file was given | `cargo run -q -- poem.txt`. The `--` matters. |
| `thread 'main' panicked at ... called \`Result::unwrap()\` on an \`Err\` value` | `.unwrap()` was used, and the result was an error | Handle the error with `match` or `?`. |

## Talk about it

- What's the difference between `Option` and `Result`?
- What does `?` do? What would it take in C?
- Why do error messages go to standard error?
- How did Rust find out the file was missing?

## Challenge *(if there's time, or for next time)*

- Make `count_words` take any number of files, like the real `wc`, and
  carry on after a missing one.
- `.unwrap()` takes the value out of a `Result`, and panics on an error.
  `.expect("message")` does the same with your own message. When is that
  acceptable? *(When an error would mean the program itself is wrong.)*
- Ask the user for a level with `std::io::stdin().read_line(...)`, and
  keep asking until it's a good one.

## Checkpoint

The learner can, without help:
- [ ] Explain `Result`, `Ok` and `Err`
- [ ] Use `?` in a function that returns a `Result`
- [ ] Read command-line arguments and a file, handling every error
- [ ] Finish the `options` and `errors` Rustlings

## Lab notebook

Draw a function with a `?`: an arrow down for `Ok`, and an arrow out of
the function for `Err`. Write the three numbers for `poem.txt` from both
tools. Commit. Add *Result*, *Ok*, *Err*, *?* and *tuple* to
`dictionary.md`.

## Guide's background *(optional reading)*

This follows Chapter 9 of the Book. Rust separates **recoverable**
errors (`Result`, which the caller must handle) from **unrecoverable**
ones (`panic!`, for bugs). The `#[must_use]` attribute on `Result` makes
the compiler warn if one is ignored.

`?` also converts the error type when a `From` conversion exists, which
is how Lesson 9.15 returns `Box<dyn Error>` from `main` and uses `?` on
several kinds of error. The exit code and messages in step 6 were
checked on Rust 1.99; `count_words` counts bytes for its third number,
as `wc` does without `-m`.
