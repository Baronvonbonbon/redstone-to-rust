# Nand to Tetris: the Guide's Handbook

Stage 6 (and later Stage 8) uses the **Nand to Tetris** software suite
and project files, from nand2tetris.org, by Noam Nisan and Shimon
Schocken. This folder holds the course's own extra material:

- [HDL-CARD.md](HDL-CARD.md) and [HACK-CARD.md](HACK-CARD.md): one-page
  references for the learner. Print them.
- `practice/`: practice chips and programs with their own tests, which
  aren't part of the Nand to Tetris projects: CreeperAlarm and Vote
  (Lesson 6.1), Sum (6.10), Block (6.11), Same and Squares (the Stage 6
  checkpoint), and `creeper16.txt` (6.14).
- [VM-CARD.md](VM-CARD.md) and [JACK-CARD.md](JACK-CARD.md): one-page
  references for Stage 8. Print them too.
- `stack/`: Stage 8's test scripts, compiler tests and an example game
  (see [Stage 8](#stage-8-the-software-stack) below).

The Nand to Tetris tools and project files themselves are **not** in
this repository: they're downloaded into the offline library.

## Setting it up

1. While online, run `./scripts/mirror-library.sh`. It downloads the
   desktop suite (version 2.7, about 1 MB) from the Google Drive link on
   nand2tetris.org/software, unpacks it to
   `/srv/redstone-library/tools/nand2tetris/`, and marks the tool
   scripts as programs (they aren't, in the zip).
2. Check: `ls /srv/redstone-library/tools/nand2tetris/tools` shows
   `HardwareSimulator.sh`, `CPUEmulator.sh`, `Assembler.sh` and others.
3. Before Lesson 6.1, from your own account:
   `./scripts/give-lab.sh LEARNER n2t`. It copies the project files and
   this folder's practice files into the learner's `~/lab/n2t/`.

**If the download fails** (the link may change): open
nand2tetris.org/software, choose the "Software package" (desktop
version), and download the zip it leads to. Unzip it in
`/srv/redstone-library/tools/` so that
`/srv/redstone-library/tools/nand2tetris/tools/` exists, then run
`chmod +x /srv/redstone-library/tools/nand2tetris/tools/*.sh`.

The suite needs Java (`default-jre`, installed by setup for Stage 4).

## Using the tools

The learner makes three links in Lesson 6.1:

| Command | Tool | In the terminal | Window |
|---|---|---|---|
| `hardware` | Hardware Simulator | `hardware Chip.tst` runs a test | `hardware` |
| `cpu` | CPU Emulator | `cpu Program.tst` runs a test | `cpu` |
| `assembler` | Assembler | `assembler Program.asm` makes `Program.hack` | `assembler` |

A test prints `End of script - Comparison ended successfully` when
everything matches, or `Comparison failure at line N` at the first wrong
row. The `.out` file stops at that row, so
`diff Chip.out Chip.cmp` shows the wrong line next to the right one.

## Things to know

- **No answer key.** The authors ask that project solutions aren't
  published, and this course follows that. You don't need solutions:
  the tests are the judge. Lessons give designs and hints one at a time.
  Please keep the learner's work private too.
- **Build in order.** In a project folder, the simulator uses the
  learner's own chip if there's an `.hdl` file for it, and its built-in
  one otherwise. The folders come with empty files for every project
  chip, so an unfinished chip makes everything that uses it fail (an
  empty chip always outputs 0). In the next project's folder, the
  earlier chips aren't there, so the reliable built-in ones are used.
- **`Memory.tst` (Project 5) only works in the window**: it waits for
  someone to hold K and then Y on the simulator's keyboard. In the
  terminal, it waits forever; Ctrl+C stops it. Lesson 6.12 has the steps.
- **`Fill.tst` (Project 4)** expects a `Fill.hack` file. Lesson 6.11
  loads `Fill.asm` in the window instead, and uses `FillAutomatic.tst`
  in the terminal.
- **The CPU Emulator counts lines from 0** in its error messages, so
  "In line 4" is the fifth line.
- **Dots in folder names** confuse the supplied assembler: it works out
  the `.hack` name from the first dot in the whole path, so
  `/tmp/a.b/Add.asm` becomes `/tmp/a.hack`. Keep `~/lab/n2t` free of
  dotted folder names. (A dot in the learner's account name would cause
  the same problem; use the CPU Emulator, which assembles by itself.)
- **`MD` and `AMD`, not `DM` and `ADM`.** The book's second edition
  writes some destinations the new way, but these tools only understand
  the old spelling. The Hack card uses the old one.
- **Window speed.** In both simulators, set **Animate** to **No
  animation** (or move the speed slider to Fast) for long programs. If
  the Hardware Simulator's window freezes during a long run, close it and
  run the same test in the terminal.
- **The web IDE.** nand2tetris.github.io/web-ide is the newer, browser
  version of the same tools, with no account. It's recommended by the
  authors, and the desktop tools may be retired one day. It has the same
  projects and tests (the course's checks didn't test it), but the
  learner's files live in the browser's storage rather than in
  `~/lab/n2t`, so download them often if you switch.

## Stage 8: the software stack

Stage 8 uses the same download, plus three more of its tools, and a
second lab with the course's own test scripts. Before Lesson 8.6, from
your own account:

```
./scripts/give-lab.sh LEARNER stack
```

It makes `~/lab/n2t/stack/`, with:

| File | What it does | Lessons |
|---|---|---|
| `check-vm FOLDER` | runs the learner's `vm.py` on an official Project 7 or 8 test, then the test on the CPU Emulator | 8.7–8.10, 8.18 |
| `check-xml tokens\|parse FILE.jack` | compares the learner's tokenizer or parser output with the official XML | 8.13, 8.14 |
| `check-jack FOLDER` | compiles a test with the learner's compiler, runs it on the VM Emulator, and compares the answers it leaves in `RAM[8000]` onwards | 8.15, 8.16 |
| `check-os Math\|Memory\|Array` | runs the official Project 12 test on the learner's OS class | 8.17 |
| `tests/1-Sums` to `tests/4-Arrays` | the course's own compiler tests, each a Jack program with known answers | 8.15, 8.16 |
| `diamond-dash/` | Diamond Dash, an example Jack game written for the course | 8.12, 8.18 |

Lesson 8.6 links the four scripts into `~/bin`, with two more tools:
`vme` (the VM Emulator) and `jackc` (the official Jack compiler). Every
script prints `ALL GOOD!` or `NOT YET.` with the wrong row or the error.

### Things to know for Stage 8

- **Still no answer key.** Projects 7 to 12 are the authors' projects
  too. The lessons give the book's plans in words and VM templates, and
  starting programs for the parts that aren't the project itself
  (reading files, printing XML); the learner writes the translator, the
  compiler and the OS. Please keep their work private.
- **Loading a folder in the VM Emulator** asks whether to use the
  built-in OS: answer **Yes**. A program that ends shows `Program
  Halted: Main.main finished execution`.
- **On the command line, the VM Emulator has no built-in OS.** That's
  why `check-jack` and `check-os` copy the OS, as VM code, from
  `tools/OS/`, and give the tests more steps than the official `.tst`
  files ask for (5,000,000): the OS as VM code takes a while to start.
  Each check takes a few seconds.
- **The CPU Emulator starts with `RAM[0]` at 0.** The official tests set
  `SP` themselves. For a hand-made test before Lesson 8.10 (which adds
  the bootstrap), set `RAM[0]` to 256 in the window first.
- **The Hack card's spellings.** The CPU Emulator accepts `M+D`, but the
  learner's own assembler only knows `D+M` (the card's). Lesson 8.7 warns
  about this, because Lesson 8.18 feeds the translator's output to that
  assembler.
- **The 32K ROM.** A straightforward translator turns a game plus the OS
  into about 40,000–50,000 instructions, too many for Hack's ROM
  (`Program too large`). Lesson 8.18 shrinks it with shared routines, as
  the book suggests.
- **Speed.** The CPU Emulator runs everything as Hack instructions, so
  a game built with the learner's whole toolchain runs slowly there.
  `build-all` (Lesson 8.18) uses the official `Screen.vm` and removes
  `Sys.wait` for that reason.

## Licences

The software suite is free, open-source software (GPL). The project
files belong to the book *The Elements of Computing Systems* and are
used here as the course intends: downloaded from nand2tetris.org, not
copied into this repository. This folder's cards and practice material
are the course's own (CC BY-SA for the text, MIT for code).
