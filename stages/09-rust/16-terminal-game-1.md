# Lesson 9.16: Creeper Chase, Part 1: Drawing and Moving

**Time:** 2–3 sessions of 45 min · **You need:** a terminal (full
screen is best); a text editor; `~/lab/rust`; squared paper ·
**New words:** raw mode, alternate screen, game loop, constant, `const`,
poll

## Goal *(read this to the learner)*

> Over two lessons you'll build a real terminal game in Rust: **Creeper
> Chase**. You're the `@`. Collect diamonds, and don't let the creeper
> catch you. This lesson draws the field and moves you round it with the
> arrow keys; the next adds the creeper, the diamonds, the score and the
> tests. Everything you've learned in this stage goes into it.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once.
- [ ] Know the rescue: if the terminal ever acts strangely after the
      game stops (nothing appears when typing, or lines go diagonally),
      type `reset` and press Enter, even if you can't see it.
- [ ] The game uses the `crossterm` crate from the kit (Lesson 9.1).

## Warm-up (5 min)

"In Lesson 8.12, Diamond Dash had a game loop. What did it do each time
round?" *(Read a key, move things, draw, wait.)* "Today we write that
loop in Rust, for the terminal."

## Activity

### Session 1: the plan, and the field

1. **Design on paper.** On squared paper, draw a field 30 squares wide
   and 12 high, with a wall of `#` round it. Number the columns from 0 at
   the left and the rows from 0 at the top. Put `@` at (2, 2). **Say:**
   "Like the screen in Hack, y goes *down*. The wall is just outside the
   field, at x = −1 and x = 30, and y = −1 and y = 12."

2. **The project.**
   ```
   cd ~/lab/rust
   cargo new creeper-chase
   cd creeper-chase
   cargo add crossterm
   ```

3. **The start of the program.** Type this into `src/main.rs`, above the
   `fn main` that Cargo made (keep that for now):
   ```rust
   use std::io::{self, Write};
   use std::time::Duration;

   use crossterm::event::{self, Event, KeyCode, KeyEventKind};
   use crossterm::style::Stylize;
   use crossterm::{cursor, execute, queue, style, terminal};

   const WIDTH: i32 = 30;
   const HEIGHT: i32 = 12;

   #[derive(Clone, Copy, Debug, PartialEq)]
   struct Spot {
       x: i32,
       y: i32,
   }

   struct Game {
       player: Spot,
   }

   impl Game {
       fn new() -> Game {
           Game {
               player: Spot { x: 2, y: 2 },
           }
       }

       fn move_player(&mut self, dx: i32, dy: i32) {
           let x = self.player.x + dx;
           let y = self.player.y + dy;
           if (0..WIDTH).contains(&x) && (0..HEIGHT).contains(&y) {
               self.player = Spot { x, y };
           }
       }
   }
   ```
   Go through it:
   - `const` makes a **constant**: a value that never changes, written in
     capitals by habit.
   - `Spot` is a place on the field. It derives `Clone` and `Copy` so it's
     copied like a number (Lesson 9.4), and `PartialEq` so two spots can
     be compared with `==`.
   - `move_player` works out where the player would go, and only moves if
     that's inside the field. **Ask:** "What's `(0..WIDTH).contains(&x)`
     in words?" *(x is from 0 up to 29.)*

   `cargo run`. **They should see:** some warnings that things are never
   used, and `Hello, world!`. **Say:** "That's fine: we'll use them all."

### Session 2: drawing

4. **The `draw` method.** Add it inside `impl Game`, after `move_player`:
   ```rust
       fn draw(&self, out: &mut impl Write) -> io::Result<()> {
           queue!(out, terminal::Clear(terminal::ClearType::All))?;
           for y in -1..=HEIGHT {
               for x in -1..=WIDTH {
                   if x == -1 || x == WIDTH || y == -1 || y == HEIGHT {
                       queue!(out, cursor::MoveTo((x + 1) as u16, (y + 1) as u16), style::Print("#"))?;
                   }
               }
           }
           let p = self.player;
           queue!(out, cursor::MoveTo((p.x + 1) as u16, (p.y + 1) as u16), style::PrintStyledContent("@".yellow()))?;
           queue!(out, cursor::MoveTo(0, (HEIGHT + 3) as u16), style::Print(format!("You are at {}, {}. Arrows to move, q to quit.", p.x, p.y)))?;
           out.flush()
       }
   ```
   **Say:**
   - "`queue!` lines up drawing commands, and `out.flush()` sends them all
     to the terminal at once, so the picture doesn't flicker."
   - "`cursor::MoveTo(column, row)` moves the terminal's cursor. Its
     corner is (0, 0), so the field is drawn one square in, to leave room
     for the wall: that's the `+ 1`s. `as u16` turns our `i32` into the
     type `MoveTo` wants."
   - "`"@".yellow()` is a yellow `@`. That's what `Stylize` is for."
   - "`out: &mut impl Write` means 'anything you can write to', borrowed
     to change. It's usually the screen."

5. **Keys.** Add this function after the `impl Game` block (not inside
   it):
   ```rust
   /// Waits up to 50 milliseconds for a key. Gives back the key, or None.
   fn read_key() -> io::Result<Option<KeyCode>> {
       if !event::poll(Duration::from_millis(50))? {
           return Ok(None);
       }
       match event::read()? {
           Event::Key(key) if key.kind == KeyEventKind::Press => Ok(Some(key.code)),
           _ => Ok(None),
       }
   }
   ```
   **Say:** "`poll` waits up to 50 milliseconds for something to happen. If
   nothing does, `None`: the game carries on without waiting for you.
   That matters next lesson, when the creeper moves by itself. The `if`
   inside the match arm is a *guard*: only key *presses* count, not
   releases."

### Session 3: the game loop

6. **Play, and main.** Replace Cargo's `fn main` with these two:
   ```rust
   fn play(out: &mut impl Write) -> io::Result<()> {
       let mut game = Game::new();
       loop {
           game.draw(out)?;
           match read_key()? {
               Some(KeyCode::Left) => game.move_player(-1, 0),
               Some(KeyCode::Right) => game.move_player(1, 0),
               Some(KeyCode::Up) => game.move_player(0, -1),
               Some(KeyCode::Down) => game.move_player(0, 1),
               Some(KeyCode::Char('q')) => return Ok(()),
               _ => {}
           }
       }
   }

   fn main() -> io::Result<()> {
       let mut out = io::stdout();
       terminal::enable_raw_mode()?;
       execute!(out, terminal::EnterAlternateScreen, cursor::Hide)?;
       let result = play(&mut out);
       execute!(out, cursor::Show, terminal::LeaveAlternateScreen)?;
       terminal::disable_raw_mode()?;
       result?;
       println!("Bye!");
       Ok(())
   }
   ```
   **Say:**
   - "`play` is the **game loop**: draw, read a key, move, for ever,
     until `q`. `_ => {}` means 'any other key, or none: do nothing'."
   - "**Raw mode** sends each key to the program the moment it's pressed,
     without waiting for Enter, and stops the terminal printing it."
   - "The **alternate screen** is a second, blank screen. When the game
     ends, the terminal switches back, and everything you'd typed
     before is still there."
   - "Look at `main`: whatever `play` gives back, even an error, we put
     the terminal back to normal *before* passing the error on with `?`.
     Otherwise a crash would leave the terminal in raw mode."

7. **Play it.** `cargo run`. **They should see:** a wall of `#`, a
   yellow `@` near the top left, and `You are at 2, 2. Arrows to move, q
   to quit.` underneath. The arrows move the `@`, and the numbers change;
   it can't go through the wall. `q` quits, and **they should see:**
   `Bye!` and the old terminal. Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The terminal acts strangely after the game stops (typing is invisible, lines go diagonally) | The program stopped while in raw mode | Type `reset` and press Enter, even if you can't see it. |
| `error[E0432]: unresolved import \`crossterm\`` | The crate isn't in this project | `cargo add crossterm`. |
| `error[E0599]: no method named \`yellow\` found for reference \`&'static str\`` | `Stylize` isn't brought in | `use crossterm::style::Stylize;`. |
| `error[E0599]: no method named \`flush\` found` | `Write` isn't brought in | `use std::io::{self, Write};`. |
| The `@` walks into the wall, or the picture is shifted | A `+ 1` is missing in `draw`, or `move_player`'s check is wrong | Compare with step 4 and the drawing on paper. |
| Nothing moves when arrows are pressed | The terminal window isn't selected | Click the terminal window. |
| The picture is torn or wraps strangely | The terminal window is too small | Make it bigger: at least 40 columns and 16 rows. |

## Talk about it

- What does the game loop do each time round?
- What's raw mode? Why must the program always switch it off?
- Why does `read_key` wait only 50 milliseconds?
- Why does `draw` take `&self`, but `move_player` take `&mut self`?

## Challenge *(if there's time, or for next time)*

- Make the wall a different colour: `"#".dark_grey()`.
- Let `w`, `a`, `s` and `d` move too (`KeyCode::Char('w')`).
- Leave a trail: keep a `Vec<Spot>` of everywhere the player has been,
  and draw a `.` on each.

## Checkpoint

The learner can, without help:
- [ ] Explain the game loop, and raw mode
- [ ] Explain how `draw` works out where to put each character
- [ ] Move the `@` round the field, and quit cleanly
- [ ] Rescue a broken terminal with `reset`

## Lab notebook

Stick in the squared-paper field, with the coordinates. Draw the game
loop as a circle: draw, key, move. Commit. Add *raw mode*, *alternate
screen*, *game loop* and *constant* to `dictionary.md`.

## Guide's background *(optional reading)*

**crossterm** (MIT) talks to the terminal using the escape codes that
`clear` and `tput` use (Stage 1), and works on Linux, macOS and Windows.
Raw mode turns off the terminal driver's line editing and echo (`stty
raw -echo`); the alternate screen is what `less`, `nano` and `top` use,
which is why your old commands reappear when they quit.

`main` restores the terminal before propagating any error, but a *panic*
inside `play` would skip that. A production program would also install
a panic hook to restore the terminal; for a learner, `reset` is the
simple rescue. The game was tested on a real pseudo-terminal: the field
draws, the arrows move the `@`, and `q` quits with `Bye!`.
