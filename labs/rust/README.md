# The Rust Lab: the Guide's Handbook

Stage 9 (Rust) happens in the learner's `~/lab/rust` folder. This lab
gives them three things:

| File | What it does | Lessons |
|---|---|---|
| `setup-rust.sh` | Installs Rust, the offline books, Rustlings and the crate kit, in the learner's own account; then switches Cargo to offline mode | 9.1 (once, online) |
| `crate-kit/` | A tiny Rust project whose only job is to make Cargo download Stage 9's six crates, at the versions the course was tested with | 9.1, 9.15–9.17 |
| `check-hack FILE.asm` | Compares the learner's Rust assembler's `.hack` file with the official assembler's, and says `SAME`, `DIFFERENT` or `NOT YET` | 9.10–9.12 |

This folder also has `creeper-chase/`, the finished game from Lessons
9.16 and 9.17, for **you** to compare with if the learner's version
won't work. It's the course's own code (MIT), and the lessons show all
of it, so it's not a secret; but `give-lab.sh` doesn't copy it, so that
the learner types and thinks first.

There is **no** answer key for the assembler (Lessons 9.10 and 9.11): it
is Nand to Tetris Project 6, rewritten, and the authors ask that
solutions aren't published. `check-hack` is the judge.

## Setting it up

1. Before Lesson 9.1, from your own account:
   ```
   ./scripts/give-lab.sh LEARNER rust
   ```
   It puts the three things in the learner's `~/lab/rust/`. It never
   deletes anything else in that folder, so it's safe to run again
   later (for example, to get a newer `check-hack`).
2. Log in as the learner (or open a terminal in their account), make
   sure the computer is **online**, and run:
   ```
   bash ~/lab/rust/setup-rust.sh
   ```
   It takes 5 to 15 minutes, and uses about 2 GB of the learner's disk
   space (1.6 GB for Rust and its books in `~/.rustup`, 250 MB for Cargo,
   Rustlings and the crates in `~/.cargo`). It:
   - installs Rust with **rustup**, the official installer, into
     `~/.rustup` and `~/.cargo` (no admin needed, no account);
   - adds the offline books (`rust-docs`) and the standard library's
     source (`rust-src`);
   - installs **Rustlings** and makes `~/lab/rust/rustlings`;
   - downloads and builds the crate kit;
   - writes `[net] offline = true` into `~/.cargo/config.toml`.
3. Close that terminal and open a new one. Check: `cargo --version`,
   `rustlings --help`, and `rustup doc --book` (which opens the Book in
   the browser, with no internet).

Running `setup-rust.sh` a second time is safe: it skips what's already
done.

## The crate kit

| Crate | What for | Lessons |
|---|---|---|
| `rand` 0.10 | Random numbers | 9.15, 9.17 |
| `regex` 1 | Finding patterns in text | 9.15 |
| `lazy_static` 1 | Needed by one Cookbook recipe | 9.15 |
| `serde` 1 (with `derive`) | Turning structs into data and back | 9.15, 9.17 |
| `serde_json` 1 | ... as JSON | 9.15, 9.17 |
| `crossterm` 0.29 | Drawing and reading keys in the terminal | 9.16, 9.17 |

Plus the crates those depend on. In offline mode, `cargo add rand` in
any new project picks the version that's already downloaded.

## Things to know

- **Offline mode.** With `net.offline = true`, Cargo never touches the
  network, and a crate that isn't cached gives `error: the crate
  \`tokio\` could not be found in registry index.` To fetch one more
  crate, in the learner's account and online:
  ```
  cd ~/lab/rust/THE-PROJECT
  CARGO_NET_OFFLINE=false cargo add THE-CRATE
  CARGO_NET_OFFLINE=false cargo build
  ```
  After that it's cached, and works offline. Look at a crate's page on
  crates.io first (no account needed): prefer well-known, widely used
  crates.
- **Updating Rust**, if you ever want to: online, in the learner's
  account, `rustup update`. The lessons were tested with Rust 1.99;
  newer versions word a few messages differently, but behave the same.
- **A broken terminal.** If a terminal game stops in the middle (a panic,
  or Ctrl+C at the wrong moment), the terminal can be left in raw mode:
  nothing shows when typing, or lines go diagonally. Type `reset` and
  press Enter, even if you can't see it.
- **Rustlings** keeps the learner's progress in
  `~/lab/rust/rustlings/.rustlings-state.txt`. `rustlings` with no
  arguments opens watch mode at the current exercise; `rustlings hint
  NAME` shows a hint; `rustlings reset NAME` starts an exercise again.
  Each exercise's solution appears in `solutions/` once it's been
  solved, for comparing.
- **`check-hack`** needs the Nand to Tetris tools from Stage 6
  (`/srv/redstone-library/tools/nand2tetris`) and the learner's assembler
  in `~/lab/rust/hack-asm`. Lesson 9.10 links it into `~/bin`. It runs
  `cargo run --release`, so it always tests the latest code; the first
  run takes a little longer while it compiles.
- **The Rust Cookbook** is in the offline library,
  `/srv/redstone-library/repos/rust-cookbook` (downloaded by
  `mirror-library.sh`). Newer recipes keep their programs in `crates/`,
  older ones on the page; Lesson 9.15 shows both, and which recipes work
  with the kit.

## Licences

Rust, Cargo, rustup and the books are MIT/Apache-2.0; Rustlings is MIT;
the crates in the kit are MIT or MIT/Apache-2.0; the Rust Cookbook is
CC0. This folder's scripts and Creeper Chase are the course's own (MIT).
