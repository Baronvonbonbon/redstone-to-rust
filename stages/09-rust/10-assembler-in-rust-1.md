# Lesson 9.10: The Assembler Again, in Rust: Part 1

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/n2t/projects/6`; `~/lab/rust`; the Hack card; the
learner's Python assembler from Lesson 6.13, for comparing ·
**New words:** rewrite, `if let`, `split_once`, `format!`

## Goal *(read this to the learner)*

> In Lesson 6.13 you wrote an assembler in Python, and used it to turn
> Pong into machine code. Now you'll write it again, in Rust. You already
> know *what* it has to do, so all your attention can go on *how* Rust
> does it. That's the fastest way to learn a new language: rewrite
> something you understand. This lesson does everything except symbols.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once, and skim Lesson 6.13 again.
- [ ] Check `ls ~/lab/rust/check-hack` and
      `ls ~/lab/n2t/projects/6/add/Add.asm` both work, in the learner's
      account. (`check-hack` came with the `rust` lab, Lesson 9.1.)
- [ ] There's no answer key, as in Lesson 6.13: `check-hack` is the
      judge.

## Warm-up (5 min)

"What are the four stages of the assembler from Lesson 6.13?" *(Clean
the lines; translate A- and C-instructions; predefined symbols and
variables; labels.)* "What's `@21` in binary? And `D=M`?"
*(`0000000000010101`; `1111110000010000`, using the card.)*

## Activity

### Session 1: the starting program

1. **The project, and the checker.**
   ```
   cd ~/lab/rust
   cargo new hack-asm
   ln -s ~/lab/rust/check-hack ~/bin/check-hack
   ```
   **Say:** "`check-hack` works like your `check-asm` from Lesson 6.13: it
   makes the real `.hack` file in a scratch folder, runs *your* Rust
   assembler on the same file, and compares them."

2. **The starting program.** Replace `hack-asm/src/main.rs` with this.
   Type it in: everything in it is from Lessons 9.7 to 9.9.
   ```rust
   use std::env;
   use std::fs;
   use std::process;

   /// Takes away the comment and all the spaces. A blank line becomes "".
   fn clean(line: &str) -> String {
       let without_comment = match line.find("//") {
           Some(start) => &line[..start],
           None => line,
       };
       without_comment.split_whitespace().collect()
   }

   fn main() {
       let args: Vec<String> = env::args().collect();
       if args.len() != 2 {
           eprintln!("Usage: hack-asm FILE.asm");
           process::exit(1);
       }
       let name = &args[1];
       let text = match fs::read_to_string(name) {
           Ok(text) => text,
           Err(error) => {
               eprintln!("{name}: {error}");
               process::exit(1);
           }
       };

       let mut lines = Vec::new();
       for line in text.lines() {
           let line = clean(line);
           if !line.is_empty() {
               lines.push(line);
           }
       }

       let mut output = String::new();
       for line in &lines {
           output.push_str(line);
           output.push('\n');
       }

       let out_name = name.replace(".asm", ".hack");
       if let Err(error) = fs::write(&out_name, output) {
           eprintln!("{out_name}: {error}");
           process::exit(1);
       }
   }
   ```
   Go through it together, comparing with the Python version:
   - `clean` is the same idea as Python's `clean`. `split_whitespace()`
     splits on the spaces, and `.collect()` into a `String` joins the
     pieces back together with nothing between them.
   - `!line.is_empty()`: `!` means *not*.
   - `fs::write` writes the whole output in one go. `if let Err(error) =
     ...` is a short `match` with only one arm: "if it's an error, do
     this; otherwise do nothing."

3. **Check it.**
   ```
   cd ~/lab/n2t/projects/6
   check-hack add/Add.asm
   ```
   The first time takes a while, while Cargo compiles. **They should
   see:**
   ```
   DIFFERENT. Line numbers are instruction numbers + 1. Mine <, real >:
   1,6c1,6
   < @2
   < D=A
   ```
   and then the real binary. **Say:** "Right: we cleaned the lines, but
   didn't translate them yet. Same plan as Python, one stage at a time."
   Commit, in `~/lab/rust/hack-asm` (Cargo made a repository there).

### Session 2: A-instructions, and the plan for each line

4. **One line at a time.** Replace the `let mut output` loop with this,
   which calls a `translate` function for every line, and stops with a
   message if it gives back an error:
   ```rust
       let mut output = String::new();
       for line in &lines {
           match translate(line) {
               Ok(binary) => {
                   output.push_str(&binary);
                   output.push('\n');
               }
               Err(error) => {
                   eprintln!("{name}: {line}: {error}");
                   process::exit(1);
               }
           }
       }
   ```
   and add `translate` above `main`:
   ```rust
   fn translate(line: &str) -> Result<String, String> {
       if let Some(value) = line.strip_prefix('@') {
           match value.parse::<u16>() {
               Ok(number) => Ok(a_instruction(number)),
               Err(_) => Err(format!("I don't know the symbol {value}")),
           }
       } else {
           c_instruction(line)
       }
   }
   ```
   **Say:** "`strip_prefix('@')` gives `Some` with the rest of the line if
   it starts with `@`, and `None` if not. `if let Some(value) = ...` runs
   the first block only when it's `Some`. `parse::<u16>()` turns the text
   into a 16-bit number. `format!` is like `println!`, but makes a
   `String` instead of printing it."

5. **`a_instruction`.** Write `fn a_instruction(value: u16) -> String`.
   Hint: in Python it was `format(n, "016b")`. In Rust,
   `format!("{value:016b}")` does the same: `b` for binary, 16 digits,
   with 0s in front.

   For now, to make it compile, add a `c_instruction` that always gives
   an error:
   ```rust
   fn c_instruction(line: &str) -> Result<String, String> {
       Err(format!("I can't do C-instructions yet"))
   }
   ```
   `cargo build` in `~/lab/rust/hack-asm`, then `check-hack add/Add.asm`
   in `~/lab/n2t/projects/6`. **They should see:**
   ```
   .../add/Add.asm: D=A: I can't do C-instructions yet
   NOT YET: the assembler stopped (above).
   ```
   **Say:** "The first line, `@2`, worked. The second is a C-instruction."

### Session 3: C-instructions

6. **The tables.** **Say:** "In Python, the tables were dictionaries. In
   Rust, a `match` that gives back an `Option` is a neat way to write a
   fixed table: `Some(bits)` if the comp is in it, `None` if not."
   ```rust
   fn comp_bits(comp: &str) -> Option<&str> {
       match comp {
           "0" => Some("0101010"),
           "1" => Some("0111111"),
           "-1" => Some("0111010"),
           "D" => Some("0001100"),
           "A" => Some("0110000"),
           "M" => Some("1110000"),
           // ... type in the rest from the Hack card, with the a bit in front
           _ => None,
       }
   }
   ```
   There are 28 comps in all. Then `jump_bits` the same way, with `""` (no
   jump) giving `"000"`. For dest, write `fn dest_bits(dest: &str) ->
   String`: for each of `'A'`, `'D'` and `'M'` in turn, push `'1'` if
   `dest.contains(...)` that letter, and `'0'` if not.

7. **Splitting.** Replace `c_instruction`. Hints:
   - `line.split_once('=')` gives `Some((before, after))` if there's an
     `=`, and `None` if not. The dest part:
     ```rust
     let (dest, rest) = match line.split_once('=') {
         Some((dest, rest)) => (dest, rest),
         None => ("", line),
     };
     ```
   - Do the same to `rest` with `';'`, to get `comp` and `jump`.
   - Look up `comp_bits(comp)`. If it's `None`, give back
     `Err(format!("I don't know the comp {comp}"))`. Do the same for the
     jump.
   - The answer is `"111"`, then the comp bits, the dest bits and the jump
     bits, all in one `format!`, wrapped in `Ok(...)`.

8. **Test.** In `~/lab/n2t/projects/6`:
   ```
   check-hack add/Add.asm
   check-hack max/MaxL.asm
   check-hack rect/RectL.asm
   check-hack pong/PongL.asm
   ```
   **They should see:** `SAME` four times, the last `SAME: all 27483
   instructions match.` Then try one with symbols:
   ```
   check-hack max/Max.asm
   ```
   **They should see:** `.../max/Max.asm: @R0: I don't know the symbol R0`
   and `NOT YET`. **Say:** "That's next lesson." Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `...: D=D-M: I don't know the comp D-M` (or another comp) | That comp is missing from `comp_bits`, or has a typo | Check the table against the Hack card. |
| `DIFFERENT`, with one line wrong | One table entry has a wrong bit | The diff's line number minus 1 is the instruction number. Check that instruction's bits against the card. |
| `error[E0425]: cannot find function \`c_instruction\`` | `translate` calls a function that isn't written yet | Add the "can't do it yet" `c_instruction` from step 5. |
| `NOT YET: the assembler stopped (above).` with a Rust compile error above it | The program doesn't compile | `cargo build` in `~/lab/rust/hack-asm`, and fix the first error. |
| `check-hack: there's no file called ...` | Wrong path, or the wrong folder | Run it from `~/lab/n2t/projects/6`, as `check-hack add/Add.asm`. |
| `check-hack: command not found` | The link from step 1 is missing | `ln -s ~/lab/rust/check-hack ~/bin/check-hack`. |
| `warning: unused variable: \`line\`` | The "can't do it yet" `c_instruction` doesn't use `line` | Fine: step 7 replaces it. |

## Talk about it

- What's the same in the Python and Rust assemblers? What's different?
- What does `if let` do? How is it different from `match`?
- Why does `translate` give back a `Result`?
- How long did the Rust assembler take for PongL? Try `time check-hack
  pong/PongL.asm`. (Most of the time is the *real* assembler, in Java!)

## Challenge *(if there's time, or for next time)*

- `dest_bits` could also be a `match`, with all eight dests. Which is
  easier to read?
- Make the error say which line of the file it was on. *(Hint: count
  lines while cleaning, and keep the number with each line in a
  tuple.)*

## Checkpoint

The learner can, without help:
- [ ] Explain the starting program, comparing it with the Python one
- [ ] Explain `if let`, `strip_prefix`, `split_once` and `format!`
- [ ] Get `SAME` for Add, MaxL, RectL and PongL with their Rust assembler

## Lab notebook

Write the Python line and the Rust line side by side for: reading a file,
splitting on `=`, a table, and binary formatting. Commit. Add *rewrite*,
*if let* and *format!* to `dictionary.md`.

## Guide's background *(optional reading)*

This is the course's "build it again" thread: the learner's own
assembler from Project 6, rewritten in a new language. It is still a
Nand to Tetris project, so this lesson gives the plan and the parts that
aren't the project itself (reading the file, writing the output, the
error handling), and hints for the rest. Please keep the learner's code
private, as with Stage 6 and Stage 8.

`check-hack` uses the official assembler as the reference, like
`check-asm`, but runs the learner's Rust assembler with `cargo run
--release`, so it always uses the latest code. The functions-as-tables
style (`match` returning `Option<&str>`) compiles to a fast lookup and
needs no setting up. A HashMap works too, and the next lesson needs one
for the symbol table.

`comp_bits` takes a `&str` and returns an `Option<&str>`. Rust's
*lifetime elision* rules connect the two, and returning a string written
in the program (which lives for ever, `'static`) is always allowed, so
no lifetime has to be written. The course's version passed every Project
6 file with this design.
