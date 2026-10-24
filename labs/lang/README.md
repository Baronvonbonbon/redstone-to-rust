# The Language Lab: the Guide's Handbook

Stage 12 (Languages & Data) happens in the learner's `~/lab/lang` folder.
This lab gives them one thing:

| File | What it does | Lessons |
|---|---|---|
| `check-pickaxe` | Builds the learner's Pickaxe interpreter (`~/lab/lang/pickaxe`) and runs it on test programs, comparing what it prints with what it should | 12.5–12.10, 12.14 |
| `tests/12.N/` | The test programs for each lesson: `.pick` files are run as programs, `.in` files are typed into the prompt, and `.out` files are the right answers | |

This folder also has, for **you**, the finished interpreter, in
`pickaxe/` (the course's own code, MIT), to compare with if the
learner's version won't build. The lessons show all of its code, so it
isn't a secret, but `give-lab.sh` doesn't copy it, so that the learner
types and thinks first. `cd labs/lang/pickaxe && cargo run` runs it.

## Setting it up

From your own account, before Lesson 12.5:
```
./scripts/give-lab.sh LEARNER lang
```
It puts `check-pickaxe` and `tests/` in the learner's `~/lab/lang/`. It
never touches anything else there (the learner's projects live there
too), so it's safe to run again.

Stage 12 also needs:

- **MIT Scheme** (Lessons 12.2 and 12.3): `./scripts/install-packages.sh
  --later`, from your account, online.
- Rust from Stage 9, Python 3, and `sqlite3` with the Stage 5 SQL lab
  (`give-lab.sh LEARNER sql`) for Lessons 12.11 and 12.12.

## Using `check-pickaxe`

Run it at the end of each Pickaxe lesson, with that lesson's number:
```
~/lab/lang/check-pickaxe 12.7
```
It prints `PASS` or `FAIL` for each test, then a total. For a `FAIL`, it
shows the difference: lines starting `<` are what *should* have
appeared, and lines starting `>` are what the learner's Pickaxe printed.
Most failures are a message worded slightly differently, or a missing
`;` in a test the learner typed.

Lessons 12.5, 12.6 and 12.7 each change what Pickaxe does when it runs
(tokens, then trees, then values), so their tests only make sense in
that lesson. From Lesson 12.8 on, the program keeps its shape, so
`check-pickaxe 12.9` runs 12.8's tests as well, and `12.10` runs all
three. In Lesson 12.14, `check-pickaxe 12.10` is the safety net that
catches anything the learner's new feature breaks.

If the learner changed Pickaxe's words in Lesson 12.5 (`print` instead
of `say`, say), the tests won't match. That's fine: compare the outputs
by eye instead, or copy `tests/` and change the words in the `.pick`,
`.in` and `.out` files.

## Where things live

| Folder | What's in it | Lessons |
|---|---|---|
| `~/lab/lang/python` | `grammar.py`, `tiny.py` (the tiny Scheme), `sets.py`, `truth.py` | 12.1, 12.4, 12.11 |
| `~/lab/lang/scheme` | `boom.scm`, `lists.scm` | 12.2, 12.3 |
| `~/lab/lang/pickaxe` | The Pickaxe interpreter, and `.pick` programs | 12.5–12.10, 12.14 |
| `~/lab/lang/data` | `club.sql`, `world.py` (and the `.db` files they make) | 12.12 |
| `~/lab/lang/chest` | The Chest database | 12.13 |

Each is its own git repository (the Rust ones from `cargo new`).
