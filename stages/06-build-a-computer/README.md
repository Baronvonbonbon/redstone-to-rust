# Stage 6: Build a Computer

**Badge:** Computer Builder · **Needs first:** Stage 5; negative numbers
(adding and subtracting them on a number line) · **Lessons:** 14

The learner builds a working computer, starting from nothing but NAND
gates. This is the first half of **Nand to Tetris**, the famous course by
Noam Nisan and Shimon Schocken: Projects 1 to 6. In a hardware
description language (HDL), they build the gates from Stage 4 again, then
multiplexors, 16-bit buses, adders, an ALU, memory, a program counter, a
CPU, and finally the Hack computer itself, with a screen and keyboard.
Then they learn its machine language, write programs that multiply and
draw, and write an **assembler** in Python that translates a whole game
of Pong into machine code. The stage ends with a program that writes
programs: it turns pixel art into Hack assembly.

Every lesson is fully scripted. Every chip design, program and Python
script in this stage was built and run against the official Nand to
Tetris tests, the course's own practice tests, and the real assembler.
The main steps in the simulator windows (loading chips and programs,
running tests, the clock, the keyboard and screen tests, and Pong) were
checked on screen, and the error messages in the lessons are the real
ones.

## Tools

- **The Nand to Tetris software suite**, desktop version 2.7: the
  Hardware Simulator, CPU Emulator and Assembler. `mirror-library.sh`
  downloads it into the offline library
  (`/srv/redstone-library/tools/nand2tetris/`); the
  [Nand to Tetris handbook](../../labs/n2t/README.md) has the details.
  It needs Java, which setup installed for Digital in Stage 4.
- **The project files and practice chips**, from your own account:
  `./scripts/give-lab.sh LEARNER n2t`. They go in `~/lab/n2t/`.
  Lesson 6.1 makes the short commands `hardware`, `cpu` and `assembler`.
- **The [HDL card](../../labs/n2t/HDL-CARD.md)** and **the
  [Hack card](../../labs/n2t/HACK-CARD.md)**: one-page references, written
  for this course. Print them.
- Thonny and Python, as before, for Lessons 6.4, 6.5, 6.7, 6.13 and 6.14.
- **(Optional purchase)** *The Elements of Computing Systems* (2nd
  edition, MIT Press), the course's book. Not needed: the lessons and
  cards cover everything.
- **(Online, optional, no account):** the *Nand to Tetris web IDE*
  (nand2tetris.github.io/web-ide), the newer browser version of the same
  tools. Work there is saved in the browser, not in `~/lab`, so this
  course uses the desktop tools. **nandgame.com** is a puzzle game that
  covers the same ground, for extra practice.

## A note on solutions

The Nand to Tetris authors ask that project solutions aren't published.
This course respects that: lessons give designs, truth tables, drawings
and hints, one at a time, but never the finished HDL or assembly for a
project. The official tests check every chip and program, so the guide
never needs an answer key. A test that says `End of script - Comparison
ended successfully` is all the proof needed. Please keep the learner's
solutions private too (their `~/lab/n2t` git repository stays on your
computer).

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 6.1 | [The Big Climb](01-the-big-climb.md) | The plan; tools and git; HDL; the CreeperAlarm and Vote practice chips; the Hardware Simulator | HDL, chips, pins, tests |
| 6.2 | [First Gates](02-first-gates.md) | Not, And, Or and Xor from NAND; building in order; internal pins | Project 1 begins |
| 6.3 | [Choosing Machines: Mux and DMux](03-mux-and-dmux.md) | Selectors and their truth tables; DMux into Mux | multiplexors |
| 6.4 | [Sixteen Wires at Once](04-sixteen-wires.md) | Buses, Python writing HDL, Or8Way, four- and eight-way trees | buses, Project 1 done |
| 6.5 | [Negative Numbers in Binary](05-negative-numbers.md) | The odometer, the binary clock, flip and add 1, Python, overflow | two's complement |
| 6.6 | [Adders in HDL](06-adders.md) | Half and full adders, a 16-bit ripple adder, Inc16 | Project 2 begins |
| 6.7 | [The ALU](07-the-alu.md) | Six control bits, a paper ALU in Python, building it in stages, flags | the ALU, Project 2 done |
| 6.8 | [Remembering: Bits and Registers](08-remembering.md) | The clock, the DFF, Bit with its loop, Register | sequential logic |
| 6.9 | [Memory and the Program Counter](09-memory-and-the-counter.md) | RAM8 up to RAM16K, address splitting, the PC | RAM, Project 3 done |
| 6.10 | [Speaking Machine Language](10-machine-language.md) | A, D and M; A- and C-instructions; jumps and labels; the CPU Emulator; Sum | machine language |
| 6.11 | [Pixels and Keys](11-pixels-and-keys.md) | The screen and keyboard as memory, pointers, Block; Mult and Fill | memory-mapped I/O, Project 4 |
| 6.12 | [The CPU and the Computer](12-the-computer.md) | Memory, decoding instructions, the CPU, the Computer runs programs | the CPU, Project 5 |
| 6.13 | [The Assembler](13-the-assembler.md) | A Python assembler in four stages, `check-asm`, symbols, labels; play Pong | translation, Project 6 |
| 6.14 | [Project: Pixel Art on My Computer](14-pixel-art-project.md) | A program that writes Hack assembly from pixel art; demo day; Stage 6 checkpoint | code generation |

## Setup notes

- The tools and project files come from the offline library, so run
  `mirror-library.sh` (while online) before the stage. If its automatic
  download fails, the handbook explains the hand download.
- The learner's work lives in `~/lab/n2t`, in its own git repository
  (Lesson 6.1), with a commit for every chip that passes.
- Don't put dots in folder names under `~/lab/n2t`: the supplied
  assembler gets confused by them (Lesson 6.13 explains).

## Free play for this stage

- More practice chips in `~/lab/n2t/practice`, with hand-written tests.
- Hack programs: a bouncing pixel, a drawing program that follows the
  arrow keys, a counter shown in binary on the screen.
- More pixel art through `hackart.py`, from Stage 3's Sprite Maker
  pictures.
- nandgame.com, online, for the same ideas as puzzles.

## Habits to build now

- **Draw it first.** Every chip starts as a drawing with every wire
  named; every program as Python-ish words.
- **Build in order, test each piece.** A chip is only as good as the
  chips inside it.
- **Commit every chip that passes.**
- **Read the failing row.** `diff` the `.out` and `.cmp` files, and
  trace that row by hand.

## Checkpoint

The learner can, without help:
- [ ] Build chips in HDL from a formula or a drawing, and test them
- [ ] Explain two's complement, and why the ALU needs no subtractor
- [ ] Explain how a Bit remembers, and how RAM finds an address
- [ ] Read and write Hack assembly with loops, jumps, labels and pointers
- [ ] Explain the fetch-execute cycle, and how the CPU decodes an instruction
- [ ] Translate Hack assembly to binary by hand and with their own assembler

They can also:
- [ ] Pass every test in Projects 1 to 6, and play Pong on code their
      assembler made
- [ ] Write a program that writes programs (Lesson 6.14)
