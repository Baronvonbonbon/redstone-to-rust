# Redstone to Rust

A free, open, **offline-first** computer science course for a young,
advanced learner. It starts with "a computer only does exactly what you
tell it" and works up through the terminal, Python, logic gates, building
a computer from NAND gates (Nand to Tetris), algorithms, C, Rust,
operating systems, networks and security, and compilers.

It was written for homeschooling. **Every lesson is scripted, so a guide
with no computer experience can lead it.** The guide reads the lesson,
follows the steps, and uses the "If something goes wrong" table when the
learner gets stuck.

```
 Stage 0  Hello, Computer          unplugged activities, typing, files & folders
 Stage 1  Terminal Explorer        the shell, bashcrawl, a detective mystery, Mineshaft wargame
 Stage 2  Python Turtle            first programs, drawing with code
 Stage 3  Python Games & Puzzles   text adventures, math explorers, Pygame Zero
 Stage 4  Bits, Gates & Redstone   binary, logic, circuits in Luanti (an open-source Minecraft-like game) and a simulator
 Stage 5  Toolsmith                a breakable computer, permissions, scripting, git, vim, SQL
 Stage 6  Build a Computer         Nand to Tetris, Part 1 (hardware)
 Stage 7  Algorithms & Data        Big-O, sorting, trees, graphs, proofs
 Stage 8  The Software Stack       C, then Nand to Tetris, Part 2 (VM, compiler, OS)
 Stage 9  Rust                     the Rust Book, Rustlings, Rust Cookbook
 Stage 10 Operating Systems        OSTEP, Arch in a VM, writing an OS in Rust
 Stage 11 Networks & Security      packets, sockets, crypto, ethical hacking
 Stage 12 Languages & Data         Crafting Interpreters, SICP, building a database
 Stage 13 Specialize & Contribute  embedded Rust, Linux From Scratch, open source
```

The name comes from Minecraft. Redstone is how you build logic circuits
in Minecraft, and Rust is the systems language the course ends up in.

## Principles

- **No accounts, logins, or email addresses.** Everything runs on your own
  computer. A few optional online extras (such as OverTheWire) are clearly
  marked; none of them needs a personal account.
- **Offline first.** Install everything once while online
  (`scripts/install-packages.sh`, `scripts/mirror-library.sh`); after that,
  nearly every lesson works with the network unplugged.
- **Open resources.** Books and tools are free and open. Where a great
  resource isn't free (for example the Nand to Tetris textbook), it's
  marked as an optional purchase and the course still works without it.
- **Each stage mixes three kinds of work:** a book or course to learn
  from, a game or wargame to practice with, and a project to build.
- **Stage gates, not ages.** Move on when the learner passes a stage's
  checkpoint, not when the calendar says so. Some stages also need a
  math level first; see [docs/MATH-TRACK.md](docs/MATH-TRACK.md).

## Start here

1. **Guide:** read [docs/GUIDE.md](docs/GUIDE.md) (about 15 minutes). It covers how
   to run a session, what to do when stuck, and how to pace things.
2. Set up the computer: [docs/SETUP.md](docs/SETUP.md).
3. Look over the whole map: [docs/SYLLABUS.md](docs/SYLLABUS.md).
4. Open [stages/00-hello-computer/](stages/00-hello-computer/) and start Lesson 0.1.
5. Print [PASSPORT.md](PASSPORT.md) for the learner to stamp as they go.

## What's in this repo

| Path | What it is |
|---|---|
| `docs/` | Guide handbook, syllabus, math track, resource catalog, setup |
| `stages/` | One folder per stage: an overview, then one file per lesson |
| `labs/mineshaft/` | **Mineshaft:** a 20-level offline wargame (like OverTheWire Bandit) in Docker |
| `labs/underpants-heist/` | **The Great Underpants Heist:** a command-line detective mystery |
| `labs/treasure-cave/` | **Treasure Cave:** a folder maze for practicing `find` and wildcards |
| `labs/sprite-maker/` | **Sprite Maker:** turns text pixel art into pictures for Pygame Zero games |
| `labs/sandbox/` | **The Sandbox:** a breakable Linux computer in Docker where the learner is the admin (Stage 5) |
| `labs/sql/` | A Minecraft mob database for learning SQL (Stage 5) |
| `labs/n2t/` | Nand to Tetris extras: HDL, Hack, VM and Jack reference cards, practice chips (Stage 6), and Stage 8's check scripts, compiler tests and the Diamond Dash game |
| `labs/algo/` | The Stage 7 checker, practice mazes, and answers for the guide |
| `scripts/` | Install packages, create the learner's account, download the offline library |
| `PASSPORT.md` | The learner's printable progress passport |

## Status

| Stages | State |
|---|---|
| 0–8 | Fully scripted lessons, with tested labs and programs |
| 9–13 | Outlined in [docs/SYLLABUS.md](docs/SYLLABUS.md); stage folders not written yet |

Contributions are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

- Course text: [CC BY-SA 4.0](LICENSE-CONTENT.txt).
- Code (labs, scripts): [MIT](LICENSE-CODE.txt).
- Linked third-party resources keep their own licenses; see
  [docs/RESOURCES.md](docs/RESOURCES.md). This repo links to them and downloads them;
  it doesn't copy them.
