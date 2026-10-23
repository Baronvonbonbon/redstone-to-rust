# Stage 8: The Software Stack

**Badge:** Stack Climber · **Needs first:** Stage 7 · **Lessons:** 18

The learner climbs back up from the computer they built in Stage 6. It
starts with a short unit of **C**, the language most of Linux is written
in. Compiling turns out to be just a bigger version of their assembler.
Pointers turn out to be the A register from Hack. Then they overflow a
buffer on purpose, leak memory and use it after freeing it, and catch
each bug with the sanitizer, valgrind and gdb. This is the set of
problems that Rust, in Stage 9, was built to stop. They finish the unit
with command-line tools of their own: a ROT13 filter, their own `wc`, and
a Makefile.

Then comes the second half of **Nand to Tetris**, Projects 7 to 12:

- **A VM translator** in Python, which turns stack-machine code into
  Hack assembly: arithmetic, memory segments, loops, and function calls
  with frames.
- **Programs in Jack**, Nand to Tetris's own language, ending with a
  game: Diamond Dash, written for the course, and then one of the
  learner's own.
- **A Jack compiler**: a tokenizer, a recursive-descent parser, and code
  generation for expressions, statements, objects and arrays.
- **The operating system's core**: multiplying with only adding, dividing
  by doubling, a heap with a free list, and drawing pixels and lines.

The final project sends the learner's own game down the whole ladder
using only their own tools. First they make the translator smart enough
to fit the result into Hack's 32K of ROM. Then they play it on the CPU
Emulator.

Every lesson is fully scripted. Every C program was compiled and run,
and every error message in the lessons is a real one. The Nand to Tetris
parts were checked against working solutions, kept out of the repository:
every hint, every test result, the bug messages in the error tables, and
the whole-stack build of Diamond Dash.

## Tools

- **The C tools:** `gcc`, `gdb`, `valgrind` and the C manual pages.
  From your own account, while online:
  `./scripts/install-packages.sh --later` (before Lesson 8.1). The
  learner's C programs live in `~/lab/c`, in a git repository.
- **The Nand to Tetris suite** from Stage 6: now also the **VM
  Emulator** (`vme`) and the **Jack compiler** (`jackc`). Lesson 8.6
  makes the links.
- **The Stage 8 lab**, from your own account, before Lesson 8.6:
  `./scripts/give-lab.sh LEARNER stack`. It holds four check scripts,
  the course's compiler tests and Diamond Dash. The
  [Nand to Tetris handbook](../../labs/n2t/README.md#stage-8-the-software-stack)
  explains each one.
- **The [VM card](../../labs/n2t/VM-CARD.md)** and **the
  [Jack card](../../labs/n2t/JACK-CARD.md)**: one-page references,
  written for this course. Print them, and keep the Hack card from
  Stage 6 handy.
- Thonny and Python, for the translator and the compiler.
- **(Optional purchase)** *The Elements of Computing Systems* (2nd
  edition), Chapters 7 to 12. The lessons cover what's needed.
- **(Free, in the offline library)** *Think Python 2e*, Chapters 15 to
  18, on classes, which the compiler uses; and OpenStax *Introduction to
  Computer Science* (a hand download, see `mirror-library.sh`), whose
  chapters on low-level and high-level programming languages cover C,
  compilers and interpreters, for the guide.

## A note on solutions

Projects 7 to 12 are Nand to Tetris projects, and the authors ask that
their solutions aren't published, so this course gives none:

- The lessons give the book's plans, in words and as VM code templates.
- They give starting programs for the parts that aren't the project
  itself, such as reading files and printing XML.
- Hints come one at a time.

The test scripts are the judge, and the guide never needs an answer key.
The C programs, the compiler tests and Diamond Dash are the course's own,
and appear in full. Please keep the learner's translator, compiler and
OS private.

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 8.1 | [Hello, C](01-hello-c.md) | Compiling, types, `printf`, loops; racing C against Python | compilers, types |
| 8.2 | [Addresses and Pointers](02-pointers.md) | `&` and `*`, a swap that needs pointers, arrays as boxes in a row | pointers |
| 8.3 | [Strings, Overflows and Crashes](03-strings-and-overflows.md) | Null-terminated strings, a buffer overflow, the sanitizer, gdb | memory safety |
| 8.4 | [The Heap: Asking for Memory](04-the-heap.md) | `malloc` and `free`, structs, a linked list in C, leaks and use after free | the heap |
| 8.5 | [Your Own Tools in C](05-tools-in-c.md) | `argv`, a ROT13 filter, a `wc` of their own, exit codes, a Makefile | Unix tools, `make` |
| 8.6 | [The Stack Machine](06-the-stack-machine.md) | The ladder of languages; a stack of cards; the VM Emulator | virtual machines |
| 8.7 | [The VM Translator, Part 1](07-vm-arithmetic.md) | Push, add, and true or false in Hack | Project 7 begins |
| 8.8 | [The VM Translator, Part 2](08-vm-memory.md) | Segments, base addresses, R13, statics | Project 7 done |
| 8.9 | [Loops and Jumps in the VM](09-program-flow.md) | A VM loop by hand; label, goto, if-goto | Project 8 begins |
| 8.10 | [Functions: Call and Return](10-functions.md) | The frame with sticky notes; call, return, the bootstrap | Project 8 done |
| 8.11 | [Programming in Jack](11-programming-in-jack.md) | Hello, loops, guessing, Numberblocks towers | Project 9 begins |
| 8.12 | [A Jack Game](12-a-jack-game.md) | Diamond Dash; classes and the game loop; their own game | Project 9 done |
| 8.13 | [The Tokenizer](13-the-tokenizer.md) | Five kinds of token; a tokenizer; XML | Project 10 begins |
| 8.14 | [The Parser](14-the-parser.md) | Grammar, parse trees, recursive descent | Project 10 done |
| 8.15 | [Writing VM Code: Expressions and Statements](15-code-generation.md) | Code generation, symbol tables, while and if | Project 11 begins |
| 8.16 | [Writing VM Code: Objects and Arrays](16-objects-and-arrays.md) | Objects on the heap, methods, `a[i]`, strings; Pong with their compiler | Project 11 done |
| 8.17 | [The Operating System](17-the-operating-system.md) | Shift-and-add, dividing, square roots, a free list, pixels and lines | Project 12 |
| 8.18 | [Project: My Whole Stack](18-whole-stack-project.md) | A build script, shrinking the translator, their game on their own toolchain; Stage 8 checkpoint | putting it all together |

## Setup notes

- Install the C tools before Lesson 8.1, and give the `stack` lab before
  Lesson 8.6 (see Tools).
- The Nand to Tetris projects for this stage are already in
  `~/lab/n2t/projects/7` to `12`, from Lesson 6.1, and the learner's
  work goes there, in the same git repository as Stage 6.
- The check scripts take a few seconds each, because they run the
  emulators.
- Lessons 8.13 to 8.16 are a long, real program. Expect them to take
  several weeks. That's normal.

## Free play for this stage

- More Jack games, and showing them off in `vme`.
- The other Nand to Tetris example programs in `~/lab/n2t/projects/9`.
- More C tools: `upper`, `mycat`, a word-frequency counter.
- `man 3 printf`, `man 3 strcpy` (look for the warnings!) and other C
  manual pages.
- nandgame.com (online, no account) has software levels after the
  hardware ones.

## Habits to build now

- **Test after every change.** Every shrink, every new rule.
- **Use the tools that find bugs.** `-Wall`, `-fsanitize=address`,
  valgrind, gdb, and the check scripts.
- **Draw the memory.** Stacks, frames, heaps and pointers make sense on
  paper first.
- **Read the grammar.** One rule, one function.
- **Keep the old version.** Commit before every big change, so `git diff`
  can show what broke.

## Checkpoint

The learner can, without help:
- [ ] Explain pointers, the stack and the heap, and find memory bugs with
      the sanitizer, valgrind or gdb
- [ ] Write a small C command-line tool with a Makefile
- [ ] Translate VM commands, including `call` and `return`, into Hack on
      paper
- [ ] Explain the three jobs of a compiler, and recursive descent
- [ ] Explain how objects, methods and arrays are compiled
- [ ] Explain shift-and-add multiplication and a free-list heap

They can also:
- [ ] Pass every Project 7 and 8 test with their own translator
- [ ] Pass `check-xml` and `check-jack` with their own compiler
- [ ] Pass `check-os` for Math, Memory and Array
- [ ] Play their own game, built with their own toolchain, on the CPU
      Emulator (Lesson 8.18)
