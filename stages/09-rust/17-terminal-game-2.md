# Lesson 9.17: Creeper Chase, Part 2: The Creeper Comes

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust/creeper-chase` from Lesson 9.16 · **New words:**
tick, game state, `Default`, `#[cfg(test)]` (again)

## Goal *(read this to the learner)*

> Your `@` can walk round the field. Now give it a reason to: diamonds to
> collect, and a creeper that hunts you, getting faster with every
> diamond. You'll keep the best score in a file, so it's still there
> tomorrow, and you'll write tests for the game's rules, so you can
> change the game without breaking them.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] The finished program is in the course repository, in
      `labs/rust/creeper-chase/src/main.rs`, for you to compare with if
      something won't work. It's the course's own code, so it's fine to
      look; but let the learner type and think first.

## Warm-up (5 min)

"In Creeper Chase, what happens when you press an arrow? And when you
press nothing?" *(The `@` moves; nothing moves.)* "Now the creeper must
move even when you press nothing. How?" *(`read_key` only waits 50
milliseconds, so the loop keeps going round.)*

## Activity

### Session 1: the creeper

1. **More game state.** **Say:** "Everything the game needs to remember
   is its **game state**. It's all in the `Game` struct." Change the
   struct, and `new`:
   ```rust
   struct Game {
       player: Spot,
       creeper: Spot,
       diamond: Spot,
       score: u32,
       ticks: u32,
       speed: u32,
   }
   ```
   ```rust
       fn new() -> Game {
           Game {
               player: Spot { x: 2, y: 2 },
               creeper: Spot { x: WIDTH - 3, y: HEIGHT - 3 },
               diamond: Spot { x: 10, y: 5 },
               score: 0,
               ticks: 0,
               speed: 12,
           }
       }
   ```
   **Say:** "The creeper starts in the far corner. Each time round the
   loop is a **tick**, about 50 milliseconds. The creeper moves once
   every `speed` ticks: 12 ticks to start with, so a bit more than once
   every half second."

2. **How a creeper walks.** **Ask:** "On squared paper, the creeper is at
   (5, 7) and you're at (2, 2). Which way should it step?" Agree a simple
   rule: *if it's not in your column yet, step one square towards your
   column; otherwise, step one square towards your row.* Act it out on
   paper until it reaches the `@`.

   Now write `fn move_creeper(&mut self)` in `impl Game`, using that rule:
   an `if`, then `else if` three times, comparing `self.creeper.x` with
   `self.player.x`, and then the `y`s. Try it first, then compare:
   ```rust
       fn move_creeper(&mut self) {
           let c = &mut self.creeper;
           if c.x < self.player.x {
               c.x += 1;
           } else if c.x > self.player.x {
               c.x -= 1;
           } else if c.y < self.player.y {
               c.y += 1;
           } else if c.y > self.player.y {
               c.y -= 1;
           }
       }
   ```
   **Say:** "`let c = &mut self.creeper;` is a short name for the
   creeper, borrowed to change it."

3. **The tick.** Add:
   ```rust
       /// One tick of the game. Gives back true if the creeper caught the player.
       fn tick(&mut self) -> bool {
           self.ticks += 1;
           if self.ticks >= self.speed {
               self.ticks = 0;
               self.move_creeper();
           }
           self.creeper == self.player
       }
   ```
   And in `draw`, after the `@`, draw the creeper in green:
   ```rust
           let c = self.creeper;
           queue!(out, cursor::MoveTo((c.x + 1) as u16, (c.y + 1) as u16), style::PrintStyledContent("C".green()))?;
   ```

4. **Caught!** In `play`, after the `match`, add:
   ```rust
           if game.tick() {
               return Ok(());
           }
   ```
   `cargo run`. **They should see:** a green `C` in the bottom right that
   walks towards the `@`, across first and then up or down. When it
   reaches the `@`, the game ends with `Bye!`. Commit.

### Session 2: diamonds and speed

5. **A random diamond.** `cargo add rand`, add `use rand::RngExt;` at the
   top, and this method:
   ```rust
       fn new_diamond(&mut self) {
           let mut rng = rand::rng();
           loop {
               let spot = Spot {
                   x: rng.random_range(0..WIDTH),
                   y: rng.random_range(0..HEIGHT),
               };
               if spot != self.player && spot != self.creeper {
                   self.diamond = spot;
                   return;
               }
           }
       }
   ```
   **Ask:** "Why the loop?" *(If the random spot is where the player or
   the creeper is, try again.)*

   Change `new` so the first diamond is random too:
   ```rust
       fn new() -> Game {
           let mut game = Game {
               player: Spot { x: 2, y: 2 },
               creeper: Spot { x: WIDTH - 3, y: HEIGHT - 3 },
               diamond: Spot { x: 0, y: 0 },
               score: 0,
               ticks: 0,
               speed: 12,
           };
           game.new_diamond();
           game
       }
   ```

6. **Scoring.** At the start of `tick`, add:
   ```rust
           if self.player == self.diamond {
               self.score += 1;
               if self.speed > 3 {
                   self.speed -= 1;
               }
               self.new_diamond();
           }
   ```
   **Ask:** "What does `speed` going down do?" *(The creeper moves more
   often: it gets faster. Never faster than every 3 ticks.)*

   In `draw`, draw the diamond as a cyan `*` *before* the `@` (so the
   `@` is on top when they're in the same place), and change the bottom
   line to show the score:
   ```rust
           let d = self.diamond;
           queue!(out, cursor::MoveTo((d.x + 1) as u16, (d.y + 1) as u16), style::PrintStyledContent("*".cyan()))?;
   ```
   ```rust
           queue!(out, cursor::MoveTo(0, (HEIGHT + 3) as u16), style::Print(format!("Diamonds: {}   Arrows to move, q to quit.", self.score)))?;
   ```
   `cargo run`, and play. **They should see:** a cyan `*`; walking onto it
   adds one to `Diamonds:`, and a new one appears. The creeper speeds up.
   Commit.

### Session 3: scores, and tests

7. **Return the score.** Change `play` to give back the score: its first
   line becomes `fn play(out: &mut impl Write) -> io::Result<u32> {`, and
   both places that say `return Ok(())` (for `q`, and for being caught)
   say `return Ok(game.score)` instead. In
   `main`, change `result?;` to `let score = result?;`.

8. **A scores file.** `cargo add serde --features derive` and `cargo add
   serde_json`. At the top, add `use std::fs;` and `use
   serde::{Deserialize, Serialize};`. Then, after `play`:
   ```rust
   #[derive(Serialize, Deserialize, Default)]
   struct Scores {
       best: u32,
       games: u32,
   }

   fn load_scores() -> Scores {
       match fs::read_to_string("scores.json") {
           Ok(text) => serde_json::from_str(&text).unwrap_or_default(),
           Err(_) => Scores::default(),
       }
   }

   fn save_scores(scores: &Scores) -> io::Result<()> {
       let text = serde_json::to_string_pretty(scores)?;
       fs::write("scores.json", text)
   }
   ```
   **Say:** "`Default` gives a struct a starting value: here, 0 and 0.
   If there's no file yet, or it's broken, we start from the default
   instead of crashing: that's `unwrap_or_default`."

   And the end of `main`, replacing `println!("Bye!"); Ok(())`:
   ```rust
       let mut scores = load_scores();
       scores.games += 1;
       println!("BOOM! You collected {score} diamonds.");
       if score > scores.best {
           scores.best = score;
           println!("That's a new best!");
       }
       println!("Best: {}. Games played: {}.", scores.best, scores.games);
       save_scores(&scores)
   ```
   Play twice. **They should see** after each game something like:
   ```
   BOOM! You collected 4 diamonds.
   That's a new best!
   Best: 4. Games played: 1.
   ```
   and `cat scores.json` shows the best and the number of games.

9. **Tests for the rules.** At the bottom of `main.rs`:
   ```rust
   #[cfg(test)]
   mod tests {
       use super::*;

       #[test]
       fn creeper_walks_across_first() {
           let mut game = Game::new();
           game.player = Spot { x: 2, y: 2 };
           game.creeper = Spot { x: 5, y: 7 };
           game.move_creeper();
           assert_eq!(game.creeper, Spot { x: 4, y: 7 });
       }

       #[test]
       fn player_stays_in_the_field() {
           let mut game = Game::new();
           game.player = Spot { x: 0, y: 0 };
           game.move_player(-1, 0);
           assert_eq!(game.player, Spot { x: 0, y: 0 });
       }

       #[test]
       fn a_diamond_scores_a_point() {
           let mut game = Game::new();
           game.diamond = game.player;
           let caught = game.tick();
           assert_eq!(game.score, 1);
           assert!(!caught);
           assert_ne!(game.diamond, game.player);
       }
   }
   ```
   `cargo test`. **They should see:** `running 3 tests`, three `ok`s, and
   `test result: ok. 3 passed`. **Say:** "The tests check the game's
   rules without drawing anything or pressing any keys. That's why the
   rules are in methods of their own." Then `cargo fmt`, `cargo clippy`,
   and commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0063]: missing fields \`creeper\`, \`diamond\`, \`score\` and 2 other fields in initializer of \`Game\`` | `new` doesn't set the new fields | Set every field in `new` (step 1). |
| `error[E0308]: mismatched types` at `return Ok(())` | `play` now gives back a `u32` | `return Ok(game.score);` |
| The creeper never moves | `tick` isn't called, or `speed` is 0 | Check step 4, and that `speed` starts at 12. |
| The creeper moves diagonally, or jumps | More than one `if` runs each time | Use `else if`, so only one step happens. |
| The diamond is never drawn | It's drawn after the `@` and the creeper, or not at all | Draw it before them (step 6). |
| `scores.json` isn't where expected | It's saved in the folder the game was run from | Run with `cargo run` from `~/lab/rust/creeper-chase`. |
| The terminal acts strangely after the game | It stopped in raw mode | Type `reset` and Enter. |
| A test fails with `left: Spot { x: 5, y: 6 }` | The creeper moves up or down before across | Check the order of the `if`s in `move_creeper`. |

## Talk about it

- What's in the game state? Which methods change it?
- Why does the creeper move only every `speed` ticks?
- Why does `load_scores` use a default instead of crashing?
- Why are the rules easy to test, but drawing isn't?

## Challenge *(if there's time, or for next time)*

- Add a second creeper that starts in another corner. (A `Vec<Spot>` of
  creepers?)
- Put some stone blocks (`#`) inside the field that nobody can walk
  through. The creeper's simple rule will get stuck: what could it do
  instead?
- Show the best score on the bottom line during the game.
- Write a test that the speed never goes below 3.

## Checkpoint

The learner can, without help:
- [ ] Explain the tick, and how the creeper's speed works
- [ ] Explain `move_creeper`'s rule, on paper
- [ ] Save and load the scores file, and explain `unwrap_or_default`
- [ ] Run the tests, and add one of their own

## Lab notebook

Draw the creeper's path from (5, 7) to (2, 2) on squared paper. Write
the game's rules in words, and which test checks which rule. Write your
best score. Commit. Add *tick*, *game state* and *Default* to
`dictionary.md`.

## Guide's background *(optional reading)*

The game uses three crates from the kit: `crossterm` for the terminal,
`rand` for the diamonds, and `serde`/`serde_json` for the scores file.
The course's tested version is in `labs/rust/creeper-chase/`: it was run
on a real pseudo-terminal, where the arrows moved the player, the
creeper chased and caught it, `BOOM!` was printed with the score, and
`scores.json` counted the games; `cargo test` passed all three tests and
Clippy was clean.

Separating the rules (`move_player`, `move_creeper`, `tick`) from the
input and output (`read_key`, `draw`) is the most important design idea
in game programming, and in much other software: the core is easy to
test, and the input and output can change (a window instead of a
terminal) without touching it.

The creeper's "across, then up or down" rule is greedy and never takes
a detour, so it gets stuck behind walls. The second challenge leads
naturally to breadth-first search from Stage 7.
