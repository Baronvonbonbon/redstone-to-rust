# Syllabus

This file is the map. Each stage's README in [`stages/`](../stages/)
has its lesson list, resources and checkpoint.

## The arc

The course climbs down the "stack", from what you see on the screen to
the circuits underneath, and then back up again with much more power:

```
  Stage 0–3   USE IT        A computer follows instructions. Talk to it in the
                            terminal and in Python.
  Stage 4–6   OPEN IT UP    Numbers become bits, bits become gates, and gates
                            become a working computer you built yourself.
  Stage 7–8   CLIMB BACK    Algorithms, then C, a virtual machine, a compiler,
                            and an OS for your own computer.
  Stage 9–12  BUILD REAL    Rust, operating systems, networks, security,
              THINGS        interpreters and databases.
  Stage 13    MAKE IT       Pick a field, contribute to open source, teach others.
              YOURS
```

## Stages at a glance

| # | Stage | Needs first | Rough length* | Badge |
|---|---|---|---|---|
| 0 | [Hello, Computer](../stages/00-hello-computer/) | Reading, counting | 11 lessons | Computer Whisperer |
| 1 | [Terminal Explorer](../stages/01-terminal-explorer/) | Stage 0, can type slowly | 15 lessons | Terminal Detective |
| 2 | [Python Turtle](../stages/02-python-turtle/) | Stage 1; adding and subtracting | 14 lessons | Turtle Tamer |
| 3 | [Python Games & Puzzles](../stages/03-python-games/) | Stage 2; multiplication | 16 lessons | Game Maker |
| 4 | [Bits, Gates & Redstone](../stages/04-bits-gates-redstone/) | Stage 3; powers of 2 (taught in the stage) | 14 lessons | Redstone Engineer |
| 5 | [Toolsmith](../stages/05-toolsmith/) | Stage 4 | 16 lessons | Toolsmith |
| 6 | [Build a Computer](../stages/06-build-a-computer/) | Stage 5; negative numbers | 14 lessons | Computer Builder |
| 7 | [Algorithms & Data](../stages/07-algorithms/) | Stage 6; pre-algebra, exponents | 16 lessons | Algorithm Wizard |
| 8 | [The Software Stack](../stages/08-software-stack/) | Stage 7 | 18 lessons | Stack Climber |
| 9 | [Rust](../stages/09-rust/) | Stage 8 | 18 lessons | Rustacean |
| 10 | [Operating Systems](../stages/10-operating-systems/) | Stage 9; algebra | 14 lessons | Kernel Hacker |
| 11 | [Networks & Security](../stages/11-networks-security/) | Stage 10; Hacker's Pledge | 16 lessons | Net Ninja |
| 12 | [Languages & Data](../stages/12-languages-data/) | Stage 11; discrete math begun | 14 lessons | Language Designer |
| 13 | [Specialize & Contribute](../stages/13-specialize/) | Stage 12 | 10 lessons, then an open-ended quest | Open Source Contributor |

\*A "lesson" is one to three 30–45 minute sessions. Later lessons often
take a week or more each, because they contain real projects.

## Threads that run through every stage

Coming back to the same ideas again and again is what makes them stick.
These threads link the stages:

**The Minecraft thread.** Folders are a cave (Stage 1). The Mineshaft
wargame (Stages 1 and 5). Turtle drawings of blocks (Stage 2). Circuits
in Luanti, an open-source Minecraft-like game, using the Mesecons
redstone-style mod (Stage 4). A maze solver for a block world (Stage 7).

**The Mineshaft thread.** Levels 0–9 in Stage 1, levels 10–19 in Stage 5,
and in Stage 8 the learner writes small command-line tools of their own in
C (a ROT13 filter and their own `wc`), like the ones they used down the
Mineshaft. In Stage 11 they design a puzzle trail for someone else.

**The "build it again" thread.** The Nand to Tetris assembler is written
in Python (Stage 6) and rewritten in Rust (Stage 9). The `nc`
conversations of Stage 5 come back as the learner's own servers and
clients in Rust (Stage 11).
Rewriting something you already understand in a new language is the
fastest way to learn that language.

**The secret-code thread.** A Caesar cipher wheel (Stage 0), a secret-code
machine in Python (Stage 3), ASCII as numbers (Stage 4), base64 and ROT13
in the terminal (Stages 1 and 5), a ROT13 filter in C (Stage 8), and
finally real cryptography and why the old codes break (Stage 11).

**The math thread.** Binary dot cards (Stage 0), angles with the turtle
(Stage 2), primes and Collatz (Stage 3), powers of two (Stage 4), two's
complement (Stage 6), Big-O and proof (Stage 7), and discrete math
(Stages 10 to 12). See [MATH-TRACK.md](MATH-TRACK.md).

**The controls thread** (when the guide works with machines or PLCs).
Ladder logic is Boolean logic (Stage 4). A PLC's scan cycle is a
fetch-execute loop (Stage 6). A control loop on a Raspberry Pi Pico in
embedded Rust (Stage 13).

## Languages, and why in this order

1. **Bash** (Stage 1+): talking to the computer directly. Used forever.
2. **Python** (Stage 2+): readable, forgiving, and great for math and
   games. Used for every lab through Stage 7.
3. **Hack assembly and HDL** (Stage 6): see what's really going on in a CPU.
4. **C** (Stage 8, short): feel what memory and pointers really are, and
   how easy they are to get wrong. This is what makes Rust make sense.
5. **Jack** (Stage 8): the small language from Nand to Tetris. You write
   its compiler.
6. **Rust** (Stage 9+): the main language from then on. Its ownership
   rules make sense once you've had memory bugs in C.
7. **Scheme** (Stage 12, a taste): a very different way of thinking, from SICP.
8. **Pickaxe** (Stage 12): the learner's own language, with its
   interpreter written in Rust. In Stage 13 they read clox, a real
   interpreter in C, and compare.

## Checkpoints

Every stage README ends with a **checkpoint**: things the learner must
*do*, not just recall, without help. Pass it, earn the badge, and move on.
If they can't pass it yet, repeat the lessons it points to, then try again.
