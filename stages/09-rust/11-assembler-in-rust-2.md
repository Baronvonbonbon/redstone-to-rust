# Lesson 9.11: The Assembler Again, in Rust: Part 2

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/n2t/projects/6`; `~/lab/rust/hack-asm` from Lesson 9.10;
the Hack card · **New words:** symbol table (again), `continue`,
benchmark

## Goal *(read this to the learner)*

> Your Rust assembler can translate numbers, but not names like `R0`,
> `SCREEN`, `i` or `(LOOP)`. Today you'll add the **symbol table**, as a
> struct with a HashMap inside, and the two passes. Then you'll assemble
> Pong again, play it, and race your Rust assembler against your Python
> one.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Check that `check-hack pong/PongL.asm` says `SAME` (Lesson 9.10).

## Warm-up (5 min)

"What three kinds of symbol does Hack have?" *(Predefined ones like
`R0` and `SCREEN`; labels like `(LOOP)`; variables, from 16 up.)* "Why
two passes?" *(A label can be used before the line where it's
defined.)*

## Activity

### Session 1: the symbol table

1. **The plan.** **Say:** "In Python, the symbol table was a dictionary,
   and the next variable's address was a number beside it. In Rust,
   we'll put both together in a **struct**, with methods, like the `Mob`
   in Lesson 9.6." Write the plan on paper:
   ```
   struct SymbolTable
       symbols: a HashMap from names (String) to addresses (u16)
       next_variable: the address for the next new variable (starts at 16)

   SymbolTable::new()          the predefined symbols, ready to use
   add_label(name, address)    puts a label in the table
   address_of(name)            the name's address; a new name becomes a
                               variable, at next_variable
   ```

2. **Write it.** Add `use std::collections::HashMap;` at the top, then
   the struct:
   ```rust
   struct SymbolTable {
       symbols: HashMap<String, u16>,
       next_variable: u16,
   }
   ```
   and an `impl SymbolTable` block with the three. Hints:
   - In `new`, make a `HashMap::new()`, and `insert` the predefined
     symbols from the Hack card. A loop does the seven named ones:
     ```rust
     for (name, value) in [("SP", 0), ("LCL", 1), ("ARG", 2), ("THIS", 3), ("THAT", 4), ("SCREEN", 16384), ("KBD", 24576)] {
         symbols.insert(name.to_string(), value);
     }
     ```
     and a `for r in 0..16` loop does `R0` to `R15`: `format!("R{r}")`
     makes the name.
   - `add_label` takes `&mut self`, and inserts.
   - `address_of` takes `&mut self` too, because it might add a
     variable. `match self.symbols.get(name)`: if it's `Some(address)`,
     give back `*address` (the `*` reads the number the reference points
     to). If it's `None`, remember `self.next_variable`, insert the name
     with that address, add 1 to `next_variable`, and give back the
     address you remembered.

3. **Use it in `translate`.** `translate` now needs the table, and it
   might change it (new variables), so it borrows it with `&mut`:
   ```rust
   fn translate(line: &str, table: &mut SymbolTable) -> Result<String, String> {
   ```
   **Ask:** "When `parse::<u16>()` fails, what should happen now?"
   *(Look the name up with `table.address_of(value)`, and make an
   A-instruction with that.)* Make that change.

   `cargo build`. **They should see:** an error in `main`, because the
   call to `translate` doesn't pass a table yet. **Say:** "Good: the
   compiler's showing us the next job."

### Session 2: two passes

4. **The first pass.** In `main`, after the lines are cleaned, make the
   table and do the first pass:
   ```rust
       let mut table = SymbolTable::new();
       let mut address = 0;
       for line in &lines {
           if line.starts_with('(') {
               // a label: work out the name, and add it
           } else {
               address += 1;
           }
       }
   ```
   Hints for the label: `&line[1..line.len() - 1]` is the line without
   its first and last characters, the `(` and `)`. **Ask:** "Why does
   `address` only go up in the `else`?" *(Labels aren't instructions:
   they don't take up a place in the ROM.)*

5. **The second pass.** In the translating loop:
   - Skip label lines: `if line.starts_with('(') { continue; }`.
     **Say:** "`continue` jumps straight to the next time round the
     loop."
   - Call `translate(line, &mut table)`.

6. **Test everything.** In `~/lab/n2t/projects/6`:
   ```
   check-hack add/Add.asm
   check-hack max/MaxL.asm
   check-hack rect/RectL.asm
   check-hack pong/PongL.asm
   check-hack max/Max.asm
   check-hack rect/Rect.asm
   check-hack pong/Pong.asm
   ```
   **They should see:** seven `SAME` lines, the last `SAME: all 27483
   instructions match.` **Say:** "The old ones still pass, so adding
   symbols didn't break anything." Commit.

### Session 3: play it, and the race

7. **Play.** `check-hack` left your `pong/Pong.hack` in place. Open `cpu`,
   Load Program, choose `projects/6/pong/Pong.hack`, **No animation**,
   Run, click the keyboard button, and play with the left and right
   arrows. **They should see:** Pong, as in Lesson 6.13, from machine
   code made by their Rust program.

8. **The race.** A test of how fast something runs is a **benchmark**.
   ```
   cd ~/lab/n2t/projects/6
   time python3 assembler.py pong/Pong.asm
   time ~/lab/rust/hack-asm/target/release/hack-asm pong/Pong.asm
   time ~/lab/rust/hack-asm/target/debug/hack-asm pong/Pong.asm
   ```
   **They should see** three `real` times. On the course's test computer
   they were about 0.085 seconds for Python, 0.018 for Rust's release
   build, and 0.06 for the debug build. **Ask:** "Rust was about five
   times faster. Why isn't it a hundred times faster, like C against
   Python in Lesson 8.1?" *(Both are so quick that most of the time is
   starting the program and reading and writing the files. The race in
   8.1 was a hundred million sums.)*

   **Say:** "Speed wasn't the main thing we got from Rust here. What
   was?" *(Every possible error has to be handled; the compiler checked
   the types and every `match`; there can't be a crash from a `KeyError`
   we forgot.)* Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `DIFFERENT` from some point onwards, with jump addresses one or more too big | Labels are being counted as instructions | `address += 1` only for lines that aren't labels. |
| `DIFFERENT`, with variables at 0, 1, 2... instead of 16, 17, 18... | `next_variable` doesn't start at 16 | `next_variable: 16` in `new`. |
| `DIFFERENT`, with every variable at the same address | `next_variable` isn't going up | Add 1 to it each time a new variable is made. |
| `error[E0061]: this function takes 2 arguments but 1 argument was supplied` | `translate` is called without the table | `translate(line, &mut table)`. |
| `error[E0596]: cannot borrow \`table\` as mutable, as it is not declared as mutable` | The table isn't `let mut` | `let mut table`. |
| `error[E0596]: cannot borrow \`self.symbols\` as mutable, as it is behind a \`&\` reference` | `address_of` or `add_label` takes `&self` | `&mut self`. |
| `error[E0308]: mismatched types` ... `expected \`u16\`, found \`&u16\`` | `get` gives a reference | `*address`. |
| `.../Max.asm: (ITSR0): I don't know the comp (ITSR0)` | Label lines are being translated | `continue` on lines that start with `(`. |
| Pong doesn't move | The keyboard isn't active | Click the keyboard button under the screen. |

## Talk about it

- Why is the symbol table a struct? What does each method do?
- Why does `translate` need `&mut SymbolTable`, not `&SymbolTable`?
- What did the benchmark show? Why weren't the times further apart?
- Which assembler would you rather change in a year's time? Why?

## Challenge *(if there's time, or for next time)*

- Make the assembler give an error for a label that's defined twice.
- Write a disassembler in Rust: `.hack` back to assembly.
- Make a much bigger test file: `cat pong/Pong.asm pong/Pong.asm ...`
  (ten times; labels will clash, so use `PongL.asm`), and race again.

## Checkpoint

The learner can, without help:
- [ ] Explain the symbol table struct and its three methods
- [ ] Explain the two passes, and why labels don't count
- [ ] Get `SAME` for all seven Project 6 programs, and play Pong
- [ ] Run a benchmark with `time`, and explain the result

## Lab notebook

Draw the `SymbolTable` struct, with a few entries from Max. Write the
three benchmark times. Commit. Add *benchmark* and *continue* to
`dictionary.md`. Tick "...and again, in Rust" on the passport's Nand to
Tetris climb.

## Guide's background *(optional reading)*

The design here (a struct holding the map and the next free address,
with a method that adds variables on first use) is a small example of
**encapsulation**: the rest of the program can't get the variable
numbering wrong, because only `address_of` changes it. The Python
version kept these as loose variables.

The times in step 8 came from the course's own reference assemblers on
one computer; the learner's will differ. A program this size is
dominated by start-up and file I/O. Rust's real speed advantage shows on
heavy computation, and its bigger advantage for an assembler is
correctness: no exceptions to forget to catch, and every case handled.

Lesson 9.12 tidies this program into modules, adds tests, and runs
Clippy over it.
