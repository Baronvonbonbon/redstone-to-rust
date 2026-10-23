# Lesson 9.15: Crates and the Rust Cookbook

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust`; the offline library's Rust Cookbook ·
**New words:** crate, dependency, `cargo add`, regular expression,
serialise, JSON, recipe

## Goal *(read this to the learner)*

> Nobody writes everything themselves. Rust programmers share libraries,
> called **crates**, and Cargo can add one to your project with one
> command. Today you'll roll thousands of dice, find treasure
> coordinates hidden in a message, and save a player to a file and load
> it back. Then you'll learn to use the **Rust Cookbook**: a book of
> short programs ("recipes") for common jobs, which lives in your
> offline library.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once, including the Guide's background
      about offline crates.
- [ ] Check the Cookbook is there:
      `ls /srv/redstone-library/repos/rust-cookbook/src`. (It's
      downloaded by `mirror-library.sh`.)
- [ ] The crates for this lesson were downloaded in Lesson 9.1 by
      `setup-rust.sh`. Nothing here needs the internet.

## Warm-up (5 min)

"In Python, how did you use a random number?" *(`import random`.)*
**Say:** "Python came with `random` built in. Rust's standard library is
smaller on purpose, and things like random numbers come as crates."

## Activity

### Session 1: dice

1. **Adding a crate.**
   ```
   cd ~/lab/rust
   cargo new dice
   cd dice
   cargo add rand
   cat Cargo.toml
   ```
   **They should see:** `Adding rand v0.10.3 to dependencies` (perhaps
   with more lines about its *features*), and in `Cargo.toml`, under
   `[dependencies]`, a new line: `rand = "0.10.3"`. **Say:** "A crate your
   project uses is a **dependency**. `cargo add` wrote it into
   `Cargo.toml`. Cargo found it in the kit we downloaded in Lesson 9.1:
   no internet needed."

2. **Rolling.**
   ```rust
   use rand::RngExt;

   fn main() {
       let mut rng = rand::rng();
       let mut counts = [0; 7];
       for _ in 0..6000 {
           let roll = rng.random_range(1..=6);
           counts[roll] += 1;
       }
       for (face, count) in counts.iter().enumerate().skip(1) {
           println!("{face}: {count}");
       }

       let mobs = ["zombie", "skeleton", "creeper", "spider"];
       let pick = mobs[rng.random_range(0..mobs.len())];
       println!("A wild {pick} appears!");
   }
   ```
   `cargo run`. The first time, Cargo compiles `rand` and the crates it
   needs. **They should see** something like:
   ```
   1: 1034
   2: 973
   3: 1005
   4: 965
   5: 1017
   6: 1006
   A wild skeleton appears!
   ```
   Different every time. **Say:** "`rand::rng()` makes a random number
   generator, and `random_range(1..=6)` rolls a die. `[0; 7]` is an
   array of seven 0s; we don't use slot 0, so `skip(1)` leaves it out.
   `enumerate` numbers each item, as in Python."

   **Ask:** "6000 rolls: how many of each would you expect?" *(About
   1000.)* "Are they exactly 1000?" *(No: randomness wobbles. Try 600,000
   rolls: the wobble gets smaller compared to the total.)* Commit.

3. **A crate that isn't in the kit.** Try:
   ```
   cargo add tokio
   ```
   **They should see:** an error that the crate `tokio` could not be found
   in the registry index. **Say:** "Cargo is in offline mode, and that
   crate wasn't in the kit. If you ever need one, the guide can go online
   and fetch it (the [handbook](../../labs/rust/README.md) says how)."

### Session 2: treasure and saving

4. **Regular expressions.** `cargo new treasure`, `cd treasure`,
   `cargo add regex`:
   ```rust
   use regex::Regex;

   fn main() {
       let notes = "Diamonds at (12, -40). Lava at (3, 7)! Village at (-100, 250).";
       let coords = Regex::new(r"\((-?\d+), (-?\d+)\)").unwrap();
       for found in coords.captures_iter(notes) {
           let x: i32 = found[1].parse().unwrap();
           let z: i32 = found[2].parse().unwrap();
           println!("x = {x}, z = {z}, {} blocks from home", x.abs() + z.abs());
       }
   }
   ```
   **They should see:**
   ```
   x = 12, z = -40, 52 blocks from home
   x = 3, z = 7, 10 blocks from home
   x = -100, z = 250, 350 blocks from home
   ```
   **Say:** "A **regular expression** is a pattern for finding text, like
   `grep` used in Stage 1. Read this one piece by piece: `\(` is a real
   bracket; `-?` is an optional minus; `\d+` is one or more digits; the
   plain `( )` round them *capture* what matched, as `found[1]` and
   `found[2]`. The `r` before the string means the backslashes are
   kept as they are." Commit.

5. **Saving a player.** `cargo new save`, `cd save`, then:
   ```
   cargo add serde --features derive
   cargo add serde_json
   ```
   ```rust
   use std::error::Error;
   use std::fs;

   use serde::{Deserialize, Serialize};

   #[derive(Serialize, Deserialize, Debug)]
   struct Item {
       name: String,
       count: u32,
   }

   #[derive(Serialize, Deserialize, Debug)]
   struct Player {
       name: String,
       health: u32,
       items: Vec<Item>,
   }

   fn main() -> Result<(), Box<dyn Error>> {
       let steve = Player {
           name: String::from("Steve"),
           health: 20,
           items: vec![
               Item { name: String::from("dirt"), count: 64 },
               Item { name: String::from("diamond"), count: 3 },
           ],
       };
       let text = serde_json::to_string_pretty(&steve)?;
       fs::write("steve.json", &text)?;
       println!("{text}");

       let loaded: Player = serde_json::from_str(&fs::read_to_string("steve.json")?)?;
       println!("Loaded {} with {} kinds of item.", loaded.name, loaded.items.len());
       Ok(())
   }
   ```
   **They should see:** the player written out as **JSON**:
   ```
   {
     "name": "Steve",
     "health": 20,
     "items": [
       {
         "name": "dirt",
         "count": 64
   ```
   and so on, then `Loaded Steve with 2 kinds of item.` `cat steve.json`
   shows the same file. **Say:** "Turning a struct into text that can be
   saved is called **serialising**. JSON is a text format that almost
   every language can read. `serde` derives the code for it, like
   `Debug`. And `main` can return a `Result` too: `Box<dyn Error>` means
   'any kind of error', so `?` works on file errors and JSON errors
   alike."

   **Ask:** "Change `"health": 20` to `"health": "lots"` in `steve.json`,
   and make the program only load (comment out the saving lines with
   `//`). What happens?" *(An error: `invalid type: string "lots",
   expected u32`, with the line and column.)* Commit.

### Session 3: the Cookbook

6. **Finding a recipe.** **Say:** "The Rust Cookbook is a book of
   recipes: short, complete programs for one job each. Ours is in the
   offline library."
   ```
   cd /srv/redstone-library/repos/rust-cookbook
   less src/SUMMARY.md
   ```
   **They should see:** the table of contents: Algorithms, Command Line,
   Compression, Concurrency... **Say:** "Each line points to a `.md` page."
   Press `/`, search for `range`, and find "Generate random numbers within
   a range". Press `q`.

7. **Reading one.**
   ```
   less src/algorithms/randomness/rand-range.md
   ```
   **They should see:** a short explanation, and instead of code, a line
   `{{#include ../../../crates/algorithms/randomness/src/bin/random_range.rs }}`.
   **Say:** "On the website, that line is replaced by the program. Here,
   we follow it ourselves." Look at the program:
   ```
   cat crates/algorithms/randomness/src/bin/random_range.rs
   ```

8. **Cooking it.**
   ```
   cd ~/lab/rust
   cargo new recipes
   cd recipes
   cargo add rand
   cp /srv/redstone-library/repos/rust-cookbook/crates/algorithms/randomness/src/bin/random_range.rs src/main.rs
   cargo run
   ```
   **They should see:** `Integer:` and `Float:` with two random numbers.

9. **A recipe with the code on the page.** Some pages have the program
   right there.
   ```
   less /srv/redstone-library/repos/rust-cookbook/src/text/regex/hashtags.md
   ```
   It needs two crates, shown as badges at the top: `regex` and
   `lazy_static`. `cargo add regex lazy_static`, then copy the program
   (from `use lazy_static` to the last `}`) into `src/main.rs` with the
   editor, and `cargo run`. **They should see:** nothing at all!
   **Say:** "The recipe checks its answers with `assert!`, and an assert
   that passes prints nothing. No news is good news." Add
   `println!("{tags:?}");` at the end of `main` to see the hashtags.

   Other recipes that work with the kit: `src/encoding/complex/json.md`
   (needs `serde_json`), and the other programs in
   `crates/algorithms/randomness/src/bin/` (need `rand`). Try one more.
   Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error: the crate \`tokio\` could not be found in registry index` (or another crate) | Cargo is offline, and that crate isn't in the kit | Use a crate from the kit, or ask the guide (see the handbook). |
| `error[E0432]: unresolved import \`rand\`` | The crate isn't in this project's `Cargo.toml` | `cargo add rand` in the project folder. |
| `error[E0599]: no method named \`random_range\` found` | `use rand::RngExt;` is missing | Add it at the top. |
| `cannot find derive macro \`Serialize\`` | `serde` was added without its derive feature | `cargo add serde --features derive`. |
| `invalid type: string "lots", expected u32` | The JSON file doesn't match the struct | Fix the file, or delete it and run again. |
| A recipe prints nothing | Its `assert!`s passed | Add a `println!` to see the values. |
| A Cookbook recipe's crate isn't in the kit | The Cookbook covers hundreds of crates | Pick one whose badges show `rand`, `regex`, `lazy_static`, `serde` or `serde_json`. |

## Talk about it

- What's a crate? What's a dependency?
- Why does the course download crates once, and then work offline?
- What does `serde` do? Why is JSON useful?
- How do you use a Cookbook recipe here, without the website?

## Challenge *(if there's time, or for next time)*

- Roll two dice 36,000 times, and count each total from 2 to 12. Which
  total is most common? Why?
- Find every email-like word, or every number, in a paragraph with a
  regex.
- Save the inventory HashMap from Lesson 9.8 to JSON, and load it back.

## Checkpoint

The learner can, without help:
- [ ] Add a crate with `cargo add`, and use it
- [ ] Explain why some crates aren't available offline
- [ ] Save a struct to JSON and load it back
- [ ] Find a recipe in the offline Cookbook, and run it

## Lab notebook

List the six crates in the kit, and what each is for (`cat
~/lab/rust/crate-kit/src/main.rs` lists them). Write the regex for the
coordinates, with what each part means. Commit. Add *crate*,
*dependency*, *regular expression*, *serialise*, *JSON* and *recipe* to
`dictionary.md`.

## Guide's background *(optional reading)*

Crates come from **crates.io**, Rust's public registry; downloading them
needs no account. To keep the course offline-first and free of
surprises, `setup-rust.sh` fetches a small kit once (`rand`, `regex`,
`lazy_static`, `serde`, `serde_json` and `crossterm`, plus the crates
they depend on) into Cargo's cache in `~/.cargo/registry`, and then sets
`net.offline = true` in `~/.cargo/config.toml`. In offline mode, `cargo
add` picks the cached version, and a crate that isn't cached gives the
error in step 3. To fetch another crate, see the
[Rust lab handbook](../../labs/rust/README.md).

Every crate you add is someone else's code running on your computer.
For a learner this is a good moment for a habit: prefer well-known
crates, and look at a crate's page (downloads, maintainers) before
adding it. Supply-chain attacks through package registries are real.

The *Rust Cookbook* is CC0 (public domain). Its newer recipes keep their
code in `crates/` and pull it into the pages with `{{#include}}` when
the book is built; older recipes have the code inline. The recipes named
here were tested with the kit's crate versions (rand 0.10, regex 1,
serde_json 1).
