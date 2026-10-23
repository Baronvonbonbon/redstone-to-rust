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

## Licences

The software suite is free, open-source software (GPL). The project
files belong to the book *The Elements of Computing Systems* and are
used here as the course intends: downloaded from nand2tetris.org, not
copied into this repository. This folder's cards and practice material
are the course's own (CC BY-SA for the text, MIT for code).
