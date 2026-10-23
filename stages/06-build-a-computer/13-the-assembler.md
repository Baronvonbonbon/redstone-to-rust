# Lesson 6.13: The Assembler (Project 6)

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the Hack card · **New words:** assembler, translate,
symbol table, two passes

## Goal *(read this to the learner)*

> The CPU you built only understands binary: lines of 16 ones and zeros.
> But you write programs as `@LOOP` and `D=M`. Something has to
> translate one into the other: a program called an **assembler**. So far
> you've used one built into the tools. Now you'll write your own, in
> Python, and use it to turn a whole game, *Pong*, into machine code
> that your computer can play.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once. This is a real program, built in
      stages over several sessions; each stage is tested before the next.
- [ ] The learner should be comfortable with Python from Stage 3:
      lists, dictionaries, functions, `split`, and reading files.

## Warm-up (5 min)

"What's `@21` in binary?" *(`0` then 21 in 15 bits:
`0000000000010101`.)* "What does `format(21, "016b")` give in Python?"
*(The same: 16 binary digits.)* "In `D=M;JGT`, what are dest, comp and
jump?"

## Activity

### Session 1: reading the program

1. **The plan.** **Say:** "The assembler reads a `.asm` file and writes a
   `.hack` file, with one line of binary for every instruction. We'll
   build it in four stages, testing each one:
   1. read the lines, and throw away comments and blank lines;
   2. translate A-instructions and C-instructions;
   3. predefined symbols, like `R0` and `SCREEN`, and variables;
   4. labels, like `(LOOP)`."

2. **A checker first.** Testing means comparing your `.hack` with the
   real assembler's. A script does it. Make `~/bin/check-asm`:
   ```bash
   #!/bin/bash
   # check-asm: compares my assembler's .hack file with the real assembler's.
   asm=$(realpath "$1")
   tmp=$(mktemp -d /tmp/checkasmXXXXXX)   # no dot in the name: the real assembler needs that
   cp "$asm" "$tmp/"
   assembler "$tmp/$(basename "$asm")" > /dev/null
   python3 ~/lab/n2t/projects/6/assembler.py "$asm"
   mine="${asm%.asm}.hack"
   real="$tmp/$(basename "$mine")"
   if diff -q "$mine" "$real" > /dev/null; then
       echo "SAME: all $(wc -l < "$real") instructions match."
   else
       echo "DIFFERENT. Line numbers are instruction numbers + 1. Mine <, real >:"
       diff "$mine" "$real" | head -12
   fi
   ```
   `chmod +x ~/bin/check-asm`. **Say:** "It makes the real `.hack` in a
   scratch folder, runs *your* assembler, and compares them with `diff`.
   You know every piece of this from Stage 5."

3. **Stage 1: clean lines.** New file in Thonny,
   `~/lab/n2t/projects/6/assembler.py`:
   ```python
   import sys

   def clean(line):
       """Takes away the comment and all the spaces. A blank line becomes ''."""
       line = line.split("//")[0]
       return "".join(line.split())

   name = sys.argv[1]
   lines = []
   for line in open(name):
       line = clean(line)
       if line != "":
           lines.append(line)

   for line in lines:
       print(line)
   ```
   Run it from the terminal:
   ```
   cd ~/lab/n2t/projects/6
   python3 assembler.py add/Add.asm
   ```
   **They should see:** six lines, `@2` to `M=D`, with no comments.
   **Say:** "`sys.argv[1]` is the first word after the program's name, like
   `$1` in bash. `split()` with nothing in the brackets splits on any
   spaces, and joining the pieces back together squashes them out."

   Try `python3 assembler.py max/Max.asm` too. Commit.

### Session 2: translating

4. **A-instructions.** Write a function `a_instruction(line)` that turns
   `@21` into `0000000000010101`. Hints:
   - `line[1:]` is everything after the `@`.
   - `int(...)` turns it into a number.
   - `format(n, "016b")` gives 16 binary digits, and the first is 0 for
     any number under 32768.

5. **C-instructions: three pieces.** `D=M;JGT` has three parts. Hints:
   - "How can you tell whether there's a dest?" *(`"=" in line`.)*
   - "`"D=M;JGT".split("=")` gives `['D', 'M;JGT']`. What would you split
     next?" *(The second piece, on `";"`.)*
   - Some instructions have no dest (`0;JMP`), and some no jump (`M=D`).
     Start with `dest = ""` and `jump = ""`, and only fill them in if
     there's a `=` or a `;`.

6. **The tables.** **Say:** "The Hack card has three tables. In Python, a
   table is a dictionary." Type the comp table as a dictionary, with the
   `a` bit in front (0 for the left column, 1 for the right):
   ```python
   COMP = {
       "0": "0101010",
       "1": "0111111",
       "-1": "0111010",
       "D": "0001100",
       "A": "0110000", "M": "1110000",
       # ... type in the rest from the Hack card
   }
   ```
   Then a `JUMP` dictionary the same way, with `""` (no jump) as `"000"`.
   For dest, either type a dictionary too, or work it out: d1 is `"1"` if
   `"A"` is in the dest, d2 for `"D"`, d3 for `"M"`.

   A C-instruction is `"111" + COMP[comp] + dest bits + JUMP[jump]`.

7. **Write the file.** Instead of printing, write each translated line to
   the `.hack` file:
   ```python
   out = open(name.replace(".asm", ".hack"), "w")
   for line in lines:
       if line.startswith("@"):
           out.write(a_instruction(line) + "\n")
       else:
           out.write(c_instruction(line) + "\n")
   out.close()
   ```
   Test with the files that have no symbols. Those end with `L`:
   ```
   check-asm add/Add.asm
   check-asm max/MaxL.asm
   check-asm rect/RectL.asm
   check-asm pong/PongL.asm
   ```
   **They should see:** `SAME` four times. PongL is 27,483 instructions!
   Commit.

### Sessions 3 and 4: symbols

8. **Predefined symbols and variables.** Now `max/Max.asm` uses `@R0`,
   and `rect/Rect.asm` uses `@SCREEN` and variables. **Say:** "A symbol is
   a name that stands for a number. We keep them in a dictionary called
   the **symbol table**." Start it with the Hack card's symbols table:
   `SP`, `LCL`, `ARG`, `THIS`, `THAT`, `SCREEN`, `KBD`, and `R0` to
   `R15` (a `for` loop can add those sixteen).

   In `a_instruction`: if what comes after `@` is digits
   (`.isdigit()`), use the number. Otherwise look the name up in the
   table. If it isn't there, it's a new **variable**: give it the next
   free address, starting at 16, and add it to the table.

9. **Labels: two passes.** A label like `(LOOP)` can be used *before* it
   appears in the program, so the assembler has to read the program
   twice. **Say:** "On the first pass, don't translate anything. Just count
   instructions, and when you see `(LOOP)`, write down `LOOP` = the number
   of the next instruction. Labels don't count as instructions. On the
   second pass, translate, skipping the label lines."

   Work through Max on paper first: what number does `(ITSR0)` get?
   *(Count the instructions before it.)* Then write the first pass, and
   check:
   ```
   check-asm max/Max.asm
   check-asm rect/Rect.asm
   check-asm pong/Pong.asm
   ```
   Commit when all are `SAME`.

### Session 5: play Pong

10. **Your machine code, running.** Open `cpu`, Load Program, and choose
    `projects/6/pong/Pong.hack`, the file *your* assembler made. Set
    **Animate** to **No animation**, and Run. Click the keyboard button
    under the screen, and use the **left** and **right** arrow keys to
    move the bat. **They should see:** a ball bouncing, and the score
    going up when they hit it.

    **Say:** "Pong was written in a language called Jack, compiled to
    assembly, and translated to binary by *your* program. In Stage 8,
    you'll write the compiler too."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `IndexError: list index out of range` at `sys.argv[1]` | The program was run without a file name, or with Thonny's Run button | Run it in the terminal: `python3 assembler.py add/Add.asm`. |
| `FileNotFoundError` | Wrong path | Run from `~/lab/n2t/projects/6`, and name the file as `add/Add.asm`. |
| `KeyError: 'D+1'` (or another comp) | That comp isn't in the dictionary, or has a typo | Check the dictionary against the Hack card. |
| `KeyError: ''` | A blank line or a label got through to translation | Skip blank lines in stage 1, and `(` lines in the second pass. |
| `DIFFERENT` with one line wrong | One table entry is wrong | The diff's line number minus 1 is the instruction number. Find it in the `.asm` (without comments), and check its bits against the card. |
| `DIFFERENT` from some point onwards | A label has the wrong number | Labels must not be counted as instructions. Check the first pass. |
| Variables are off by one, or wrong | They don't start at 16, or a name was given two addresses | Check `if name not in table` before adding. |
| `check-asm` says `assembler: command not found` | The link from Lesson 6.1 is missing | `ls -l ~/bin`. |
| `diff: ... No such file or directory` | A dot in a folder name confuses the real assembler | Keep `.asm` files in folders without dots in their names. |

## Talk about it

- What does an assembler do? Why do we need one?
- Why does it need two passes?
- What's in the symbol table, and when is each kind of symbol added?

## Challenge *(if there's time, or for next time)*

- Make the assembler print a friendly error, with the line number, for
  an instruction it doesn't understand, instead of a `KeyError`.
- Write a **disassembler**: read a `.hack` file, and print the
  assembly. (Labels and variable names can't come back: why not?)
- In Stage 9, you'll write this assembler again, in Rust.

## Checkpoint

The learner can, without help:
- [ ] Explain what an assembler does, and the four stages
- [ ] Translate an A-instruction and a C-instruction to binary by hand
- [ ] Explain the symbol table and the two passes
- [ ] Get `SAME` for every program in Project 6, and play Pong

## Lab notebook

Write the assembler's plan in their own words. Hand-translate three
instructions from Max. Commit. Add *assembler*, *translate*, *symbol
table* and *two passes* to `dictionary.md`. Tick
Project 6 on the passport's Nand to Tetris climb.

## Guide's background *(optional reading)*

The assembler is the first piece of real system software the learner
writes: a program whose job is to translate another program. Compilers,
coming in Stage 8, are much bigger translators that follow the same
plan (read, split into pieces, look things up in tables, write the
output). The two-pass approach for labels is a classic technique.

`check-asm` uses the real assembler as a "reference implementation": a
known-good program to compare against. That's how real translators are
tested too. The supplied assembler has one quirk: it works out the
`.hack` file name from the first dot in the *whole path*, so a folder
with a dot in its name (like `mktemp`'s usual `tmp.XXXX`) sends the
output to the wrong place. That's why the script names its own scratch
folder.

This course's "build it again" thread brings the assembler back in Stage
9, rewritten in Rust.
