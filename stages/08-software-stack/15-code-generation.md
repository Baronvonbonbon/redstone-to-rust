# Lesson 8.15: Writing VM Code: Expressions and Statements (Project 11)

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the Jack card and the VM card; squared paper · **New
words:** code generation, symbol table, kind, scope

## Goal *(read this to the learner)*

> Your parser understands Jack. Now it's time for it to *translate*:
> instead of writing XML, each grammar function will write VM code. A
> sum becomes pushes and an `add`; a `while` becomes labels and jumps;
> a variable becomes `local 2` or `argument 0`, looked up in a
> **symbol table**. By the end of this lesson, your compiler will
> compile programs with functions, loops and choices, and they'll run.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] All seven `check-xml parse` checks should pass (Lesson 8.14).
- [ ] The compiler tests are in `~/lab/n2t/stack/tests/`. Each test is
      a Jack program that puts its answers in the RAM, from 8000 on, and
      `check-jack` compares them. You don't need to read them.

## Warm-up (5 min)

"What VM code does `2 + 3` need?" *(push constant 2, push constant 3,
add.)* "And `x + 1`, if `x` is `local 0`?" *(push local 0, push constant
1, add.)*

## Activity

### Session 1: from XML to VM code

1. **A new copy.** Project 11 starts from Project 10:
   ```
   cd ~/lab/n2t/projects/11
   cp ../10/tokenizer.py .
   cp ../10/parser.py compiler.py
   ```
   **Say:** "`compiler.py` keeps the parser's shape: every function stays.
   But they'll write VM code into a list, instead of XML."

2. **Change the tools.** In `compiler.py`:
   - In `__init__`, replace `self.lines` and `self.depth` with
     `self.vm = []`.
   - Add a method `emit(self, line)` that appends one line of VM code to
     `self.vm`.
   - Change `eat` so it writes nothing, and *gives back* the token's word
     (`return word`), so `name = self.eat()` keeps a name.
   - Take out `open` and `close`, and every call to them.
   - The main part: compile one `.jack` file into a `.vm` file with the
     same name, or every `.jack` file in a folder (like the VM translator
     in Lesson 8.10). Write `"\n".join(self.vm)` into the file.

   **Say:** "`check-jack` gives your compiler a folder, so it must handle
   folders."

3. **The code generation rules.** These come from the Nand to Tetris
   book. Copy the table onto paper, and keep it by the keyboard:

   | Jack | VM code |
   |---|---|
   | a number `n` | `push constant n` |
   | a variable | `push` its segment and index (step 5) |
   | `a + b` (and `- & \| < > =`) | code for a, code for b, then `add` (`sub`, `and`, `or`, `lt`, `gt`, `eq`) |
   | `a * b`, `a / b` | code for a, code for b, then `call Math.multiply 2` or `call Math.divide 2` |
   | `-x`, `~x` | code for x, then `neg` or `not` |
   | `true` | `push constant 1`, then `neg` (that's −1) |
   | `false`, `null` | `push constant 0` |
   | `f(a, b)` in class `Main` | code for a, code for b, then `call Main.f 2` |
   | `Math.max(a, b)` | code for a, code for b, then `call Math.max 2` |
   | `do f(...)` | the call's code, then `pop temp 0` (throw the answer away) |
   | `return x` | code for x, then `return` |
   | `return;` | `push constant 0`, then `return` (every function gives back something) |

   **Ask:** "Why does `a + b * c` come out as `(a + b) * c` with these
   rules?" *(Each op is done as soon as its term is read, left to right.
   That's why Jack has no precedence: it makes the compiler simple.)*

### Session 2: expressions and functions

4. **Write expressions.** Follow the table in `compile_expression` and
   `compile_term`. Hints:
   - In `compile_expression`, remember the op, compile the next term,
     and only *then* emit the op's command. A dictionary from op to
     command (`{"+": "add", ...}`) saves many `if`s.
   - In `compile_call`, count the expressions in the list as you compile
     them: that's the number for `call`.
   - A call without a dot, like `double(21)`, is in the same class:
     `Main.double`. (In Lesson 8.16 that changes a little, for methods.)

5. **Functions.** **Say:** "`function Main.double 1` needs the number of
   locals, but we only know it after reading the `var` lines. So write
   the `function` line *after* the `var` lines, just before the
   statements." Write `compile_do` and `compile_return` too. The first
   test needs arguments (`double(n)` uses `n`), which need the symbol
   table, so it comes after the next step. Commit.

### Session 3: the symbol table

6. **Where do variables live?** **Say:** "Every variable has a **kind**
   (static, field, argument or local), a type, and a number. The
   compiler keeps a **symbol table**: a dictionary from each name to
   those three things." On paper, for:
   ```
   class Main {
       static int calls;
       function int add3(int a, int b, int c) {
           var int sum, i;
           ...
   ```
   fill in two tables:

   | Class table | kind | type | number |
   |---|---|---|---|
   | calls | static | int | 0 |

   | Subroutine table | kind | type | number |
   |---|---|---|---|
   | a | argument | int | 0 |
   | b | argument | int | 1 |
   | c | argument | int | 2 |
   | sum | local | int | 0 |
   | i | local | int | 1 |

   **Say:** "Each kind counts from 0 separately. The subroutine table is
   emptied at the start of every subroutine: that's the variable's
   **scope**, where its name means something. Look in the subroutine
   table first, then the class table." The kinds map onto VM segments:
   static → `static`, field → `this`, argument → `argument`, local →
   `local`.

7. **Build it.** Hints:
   - Two dictionaries: `self.class_table` (made in `__init__`) and
     `self.sub_table` (made new in `compile_subroutine`), each from a name
     to `(type, kind, number)`.
   - A helper `define(table, name, type, kind)` that works out the next
     number for that kind by counting how many of that kind are already
     in the table.
   - Fill `class_table` in `compile_class_var_dec`, and `sub_table` from
     the parameter list and the `var` lines.
   - Helpers `push_var(name)` and `pop_var(name)` that look the name up
     and emit `push local 1` or whatever it is.

   Now the first test:
   ```
   check-jack ~/lab/n2t/stack/tests/1-Sums
   ```
   1-Sums uses `do`, `return`, calls, arguments and expressions.
   **They should see:** `ALL GOOD! Every answer matches.` If not, the two
   rows show the answers: the first number is `RAM[8000]`, which is
   `1 + 2 * 3` (9), and so on. Compare with the comments in
   `tests/1-Sums/Main.jack`. Commit.

### Sessions 4 and 5: statements

8. **`let`, `while` and `if`.** `let x = e` is the code for e, then
   `pop_var("x")` (leave out the `[`...`]` kind for now: Lesson 8.16).
   For `while` and `if`, these are also from the book:
   ```
   while (cond) { body }        if (cond) { yes } else { no }

   label L1                     code for cond
   code for cond                not
   not                          if-goto L1
   if-goto L2                   code for yes
   code for body                goto L2
   goto L1                      label L1
   label L2                     code for no (if there's an else)
                                label L2
   ```
   **Ask:** "Why the `not`?" *(`if-goto` jumps when the condition is
   true, but we want to jump *past* the body when it's false.)* Every
   label must be different: use a counter, as in the VM translator.

   ```
   check-jack ~/lab/n2t/stack/tests/2-Loops
   ```
   **They should see:** `ALL GOOD!` 2-Loops has loops, `if`s inside `if`s,
   a static variable and recursion (`fib` calls itself). Commit.

9. **An official program.** Compile the Nand to Tetris `Seven` program
   with *your* compiler and run it:
   ```
   python3 compiler.py Seven
   ```
   Load the folder `Seven` in `vme` (Yes to the built-in OS, No
   animation, Run). **They should see:** `7` at the top left of the
   screen. **Say:** "That 7 was worked out by `1 + (2 * 3)`, compiled by
   your compiler, run by the VM." Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The last answer in 1-Sums is `1` where it should be `-1` | `true` is pushed as 1 | `push constant 1`, then `neg`. |
| `NOT YET: your compiler crashed (above).` with a `KeyError` | A name isn't in either symbol table | Check that parameters and `var`s are defined, and the class table is searched second. |
| `Out of segment space in Main.main.2` (or another function) | The `function` line has the wrong number of locals, or locals are numbered wrongly | Count only the `var`s, and number each kind from 0. |
| 2-Loops' first answer is `0` where it should be `55`, and others are wrong | The `while` has no `not`, so it jumps out when the condition is true | `not` before `if-goto` in `while`. |
| 2-Loops' second and third answers are `2` and `3` where they should be `9` and `8` | The `if` has no `not` | `not` before `if-goto` in `if` too. |
| `SyntaxError` from your compiler | The parser part disagrees with the file | Run `check-xml parse` on a Project 10 file to check the parser still works. |
| `vme` says a function isn't found | The `call` name is wrong: missing the class name or the dot | `call Main.double 1`, `call Output.printInt 1`. |

## Talk about it

- What does code generation mean?
- What's in a symbol table? Why are there two?
- Why does `while` need two labels? Why the `not`?
- Why must the `function` line wait until after the `var` lines?

## Challenge *(if there's time, or for next time)*

- Compile `ConvertToBin` with your compiler and run it in `vme`: before
  running, put a number in `RAM[8000]` (in the RAM box), and afterwards
  look at `RAM[8001]` to `RAM[8016]`. They should hold its bits.
- Make the compiler print the `.jack` line number when it finds a name
  that isn't defined.
- Compare your compiler's VM code for `2-Loops` with `jackc`'s (copy the
  folder, compile it with each, and `diff`). They're different, but both
  right. Why?

## Checkpoint

The learner can, without help:
- [ ] Turn a Jack expression into VM code on paper
- [ ] Fill in symbol tables for a subroutine
- [ ] Turn `while` and `if` into VM code with labels on paper
- [ ] Pass `check-jack` for 1-Sums and 2-Loops

## Lab notebook

Copy the code generation table and the `while`/`if` patterns. Draw the
two symbol tables from step 6. Commit. Add *code generation*, *symbol
table*, *kind* and *scope* to `dictionary.md`.

## Guide's background *(optional reading)*

This is the first half of Nand to Tetris Project 11. The compiler is a
**syntax-directed translator**: code is generated as the parser
recognises each construct, with no separate tree. Expressions come out
in postfix order naturally, because each operator is emitted after both
operands' code: exactly what a stack machine needs. The patterns in this
lesson are the book's, described in words and as VM templates, and the
learner writes the Python.

`check-jack` copies a test folder to a scratch folder, compiles it with
the learner's `projects/11/compiler.py`, adds the Jack OS as VM code
from the tools folder, and runs a test script on the VM Emulator that
compares `RAM[8000]` onwards with answers made by the official compiler.
The tests are the course's own (`~/lab/n2t/stack/tests`). Running the
OS as VM code is slower than the built-in one, so each check takes a few
seconds.

The learner's VM code won't be the same as `jackc`'s line for line (the
official compiler names its labels differently, for one thing), and it
doesn't need to be: what matters is that it does the same thing.
