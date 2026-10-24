# Lesson 10.14: A Kernel of Your Own, Part 2: Creeper Chase OS

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; a text
editor; QEMU; `~/lab/os/redstone-os` from Lesson 10.13; your Creeper
Chase from Lesson 9.17 (`~/lab/rust/creeper-chase`) · **New words:**
port, scancode, polling, interrupt, time-stamp counter, pseudo-random
number

## Goal *(read this to the learner)*

> Your kernel can draw. Now it'll listen: you'll read the keyboard
> straight from its chip, with no driver but your own. Then you'll put
> Creeper Chase *inside your kernel*: the same game rules you wrote in
> Stage 9, running with no Linux, no `std`, and no `rand` crate. Your
> own operating system, whose only job is a game.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Check `~/lab/os/redstone-os` builds and runs (`cargo run`).
- [ ] In the QEMU window, the keyboard only works after a click on the
      window. To get the mouse back, press **Ctrl+Alt+G**.

## Warm-up (5 min)

"In Hack, how did a program read the keyboard?" *(It read memory
address 24576, `KBD`, which held the key being pressed.)* "What did the
Jack OS's `Keyboard.readChar` do?" *(It kept checking `KBD` until a key
appeared.)*

## Activity

### Session 1: the keyboard

1. **Ports.** **Say:** "On a PC, the keyboard isn't in memory. It's on a
   **port**: a separate set of numbered doors, used with two special
   instructions, `in` to read and `out` to write. The keyboard chip has
   two: port `0x64` says whether a key is waiting, and port `0x60` gives
   it." Make `src/keyboard.rs`:
   ```rust
   //! The keyboard, read from the PS/2 controller's ports.

   use core::arch::asm;

   /// Reads one byte from a port.
   fn read_port(port: u16) -> u8 {
       let value: u8;
       unsafe {
           asm!("in al, dx", out("al") value, in("dx") port);
       }
       value
   }

   /// Gives back the next scancode, if a key has been pressed or let go.
   pub fn scancode() -> Option<u8> {
       let status = read_port(0x64);
       if status & 1 == 1 {
           Some(read_port(0x60))
       } else {
           None
       }
   }
   ```
   **Say:** "`asm!` puts one assembly instruction right into Rust, like
   Hack assembly in Stage 6. `in al, dx` reads the port whose number is
   in `dx` into `al`. `status & 1` checks the lowest bit: 1 means a key
   is waiting."

2. **See the codes.** Replace `_start` in `src/main.rs` (keep the panic
   handler from Lesson 10.13), add `mod keyboard;` next to `mod screen;`,
   and change the `use screen::...` line to `use screen::{BLACK, GRAY,
   Pen, RED, WHITE, YELLOW, colour};`:
   ```rust
   #[unsafe(no_mangle)]
   pub extern "C" fn _start() -> ! {
       screen::clear(colour(WHITE, BLACK));
       screen::text(0, 0, "Scancodes:", colour(YELLOW, BLACK));
       let mut codes = Pen::new(0, 1, colour(GRAY, BLACK));
       loop {
           if let Some(code) = keyboard::scancode() {
               write!(codes, "{code:02x} ").unwrap();
           }
       }
   }
   ```
   `cargo run`, click in the window, and press `a`, `b`, `c`, Space and
   Enter. **They should see:**
   ```
   Scancodes:
   1e 9e 30 b0 2e ae 39 b9 1c 9c
   ```
   **Say:** "Each key gives a **scancode** when it's pressed, and another
   when it's let go: the same number plus `0x80`. `a` is `1e` down and
   `9e` up." Press an arrow key. *(Two bytes each time: `e0 48` for up,
   then `e0 c8`. `e0` means "an extra key": the arrows came later than
   the letters.)* **Ask:** "Hold a key down. What happens?" *(The press
   code repeats.)*

3. **Polling.** **Say:** "Our loop asks the keyboard 'anything yet?'
   millions of times a second. That's **polling**, like a child in the
   back of the car: 'are we there yet?' Real kernels use **interrupts**
   instead: the keyboard rings a bell (an interrupt), and the CPU stops
   what it's doing to deal with it. Linux does that. Polling is simpler,
   and fine for a kernel with one job."

4. **A typewriter.** Add to `keyboard.rs`:
   ```rust
   /// Turns a scancode into a letter, if it's a letter key being pressed.
   pub fn letter(scancode: u8) -> Option<u8> {
       let rows: [(u8, &[u8]); 3] = [
           (0x10, b"qwertyuiop"),
           (0x1e, b"asdfghjkl"),
           (0x2c, b"zxcvbnm"),
       ];
       for (first, letters) in rows {
           if scancode >= first && scancode < first + letters.len() as u8 {
               return Some(letters[(scancode - first) as usize]);
           }
       }
       if scancode == 0x39 { Some(b' ') } else { None }
   }
   ```
   **Say:** "The scancodes follow the rows of the keyboard: `q` is `10`,
   `w` is `11`, and so on along the top row; `a` is `1e`; `z` is `2c`.
   Each row is a list of letters, and the scancode minus the row's first
   one says which letter." In `_start`, add before the `loop`:
   ```rust
       screen::text(0, 12, "You typed:", colour(YELLOW, BLACK));
       let mut typed = Pen::new(0, 13, colour(WHITE, BLACK));
   ```
   and inside the `if let`, after the `write!`:
   ```rust
               if let Some(letter) = keyboard::letter(code) {
                   write!(typed, "{}", letter as char).unwrap();
               }
   ```
   `cargo run`, and type their name. **They should see** the codes at
   the top, and their name under `You typed:`, in small letters. Commit.

### Session 2: the game's rules, again

5. **Make room.** **Say:** "In Lesson 9.17, Creeper Chase's rules were in
   methods of their own, separate from the drawing and the keys. That
   was so we could test them. Now it pays off again: the rules don't use
   `std` at all, so they can move into a kernel."

   Open `~/lab/rust/creeper-chase/src/main.rs` beside your kernel's
   `main.rs`. Copy into the kernel's `main.rs`, after the `use` lines:
   - the `WIDTH` and `HEIGHT` constants;
   - the `Spot` struct, with its `#[derive(...)]`;
   - the `Game` struct;
   - the whole `impl Game` block, *except* `draw`.

   Don't copy anything else (not `read_key`, `play`, `main` or the
   scores). Then `cargo build`. **They should see** an error about
   `rand`:
   ```
   error[E0433]: cannot find module or crate `rand` in this scope
   ```
   **Say:** "There's no `rand` crate here: it needs the OS to get random
   numbers. We'll make our own."

6. **Pseudo-random numbers.** **Say:** "A computer can't really pick a
   number by chance. It does maths that *looks* random: a
   **pseudo-random number** generator. Here's a famous recipe: take a
   number, the **seed**, multiply it by a huge number, add another, and
   that's the next seed. The new seed's top bits look random." Add a
   field `seed: u64,` at the end of `Game`, change `new` to take it
   (`fn new(seed: u64) -> Game`), and add `seed,` at the end of the
   struct in `new`. Then add this method to `impl Game`:
   ```rust
       /// A random number from 0 up to (but not including) `top`.
       fn random(&mut self, top: i32) -> i32 {
           self.seed = self
               .seed
               .wrapping_mul(6364136223846793005)
               .wrapping_add(1442695040888963407);
           ((self.seed >> 33) % top as u64) as i32
       }
   ```
   and change `new_diamond` to use it:
   ```rust
       fn new_diamond(&mut self) {
           loop {
               let spot = Spot {
                   x: self.random(WIDTH),
                   y: self.random(HEIGHT),
               };
               if spot != self.player && spot != self.creeper {
                   self.diamond = spot;
                   return;
               }
           }
       }
   ```
   **Say:** "`wrapping_mul` lets the number overflow and wrap round, on
   purpose (Lesson 9.2: normally that's a panic). `>> 33` keeps the top
   bits, which are the most random, and `% top` makes it smaller than
   `top`." **Ask:** "If the seed is the same every time, what happens?"
   *(The same diamonds every game. We'll fix that with the clock.)*
   `cargo build`: it should build, with warnings that things are never
   used. Commit.

### Session 3: time, and the game loop

7. **A clock.** **Say:** "The game needs ticks, like `read_key`'s 50
   milliseconds in Lesson 9.16. The CPU counts its own clock cycles in a
   **time-stamp counter**, billions a second, and one instruction,
   `rdtsc`, reads it." Add, after `impl Game`:
   ```rust
   /// How many clock cycles since the computer started.
   fn now() -> u64 {
       unsafe { core::arch::x86_64::_rdtsc() }
   }
   ```
   and a constant under `HEIGHT`:
   ```rust
   /// How many clock cycles one tick lasts: about a twentieth of a second.
   const TICK: u64 = 150_000_000;
   ```
   **Ask:** "If the CPU does 3 billion cycles a second, how long is
   150 million cycles?" *(150,000,000 ÷ 3,000,000,000 = 1/20 of a
   second.)* **Say:** "Every computer's CPU is a different speed, so you
   might need to change `TICK` later."

8. **Drawing.** Add a function to put things inside the wall, after
   `now`:
   ```rust
   /// Puts a character in the field, inside the wall.
   fn put(x: i32, y: i32, character: u8, paint: u8) {
       screen::put((x + 1) as usize, (y + 1) as usize, character, paint);
   }
   ```
   and this method in `impl Game`:
   ```rust
       fn draw(&self) {
           let wall = colour(GRAY, BLACK);
           for y in -1..=HEIGHT {
               for x in -1..=WIDTH {
                   if x == -1 || x == WIDTH || y == -1 || y == HEIGHT {
                       put(x, y, b'#', wall);
                   } else {
                       put(x, y, b' ', wall);
                   }
               }
           }
           let d = self.diamond;
           put(d.x, d.y, 4, colour(LIGHT_CYAN, BLACK));
           let p = self.player;
           put(p.x, p.y, 2, colour(YELLOW, BLACK));
           let c = self.creeper;
           put(c.x, c.y, b'C', colour(LIGHT_GREEN, BLACK));
           let mut pen = Pen::new(0, 15, colour(WHITE, BLACK));
           write!(pen, "Diamonds: {}   Arrows to move.", self.score).unwrap();
       }
   ```
   **Say:** "Character 4 in code page 437 is a diamond shape, and 2 is a
   smiley face: our player." Change the `use screen::...` line to:
   ```rust
   use screen::{BLACK, GRAY, LIGHT_CYAN, LIGHT_GREEN, Pen, RED, WHITE, YELLOW, colour};
   ```

9. **Play.** Add `play`, and replace `_start`:
   ```rust
   /// Plays one game. Gives back the score.
   fn play() -> u32 {
       let mut game = Game::new(now());
       let mut last_tick = now();
       let mut arrow = false;
       loop {
           if let Some(code) = keyboard::scancode() {
               if code == 0xe0 {
                   arrow = true;
                   continue;
               }
               if arrow {
                   match code {
                       0x4b => game.move_player(-1, 0),
                       0x4d => game.move_player(1, 0),
                       0x48 => game.move_player(0, -1),
                       0x50 => game.move_player(0, 1),
                       _ => {}
                   }
               }
               arrow = false;
           }
           if now() - last_tick >= TICK {
               last_tick = now();
               game.draw();
               if game.tick() {
                   return game.score;
               }
           }
       }
   }

   #[unsafe(no_mangle)]
   pub extern "C" fn _start() -> ! {
       let mut best = 0;
       loop {
           screen::clear(colour(WHITE, BLACK));
           let score = play();
           if score > best {
               best = score;
           }
           let mut pen = Pen::new(0, 17, colour(WHITE, RED));
           writeln!(pen, "BOOM! You collected {score} diamonds.").unwrap();
           write!(pen, "Best: {best}. Press space to play again.").unwrap();
           while keyboard::scancode() != Some(0x39) {}
       }
   }
   ```
   Go through `play` together. **Say:**
   - "`Game::new(now())`: the seed is the clock, so every game is
     different."
   - "An arrow key is `e0` and then its code, so when we see `e0` we
     remember it in `arrow`, and look at the next byte. The let-go codes
     (`c8` and so on) match nothing, so they're ignored."
   - "Each time round, we check the keyboard. Only when a whole tick has
     passed do we draw and move the creeper: the same `tick` as Stage 9."
   - "`_start` plays game after game, remembering the best score, and
     waits for Space (scancode `39`) in between."

   `cargo run`. Click in the window, and play! **They should see:** the
   field in `#`s, the yellow smiley, a cyan diamond and a green `C`
   coming for them; `Diamonds:` going up; and when caught, on a red
   stripe:
   ```
   BOOM! You collected 3 diamonds.
   Best: 3. Press space to play again.
   ```

10. **Tidy up.** `cargo build` warns that `letter` is never used: the
    game doesn't type. Put `#![allow(dead_code)]` at the top of
    `keyboard.rs`, under its `//!` line, to keep it for later. Then
    `cargo fmt` and `cargo clippy`, and commit.

### Sessions 4 and 5: make it yours, and the Stage 10 checkpoint

11. **Make it yours.** Ideas (choose one or two):
    - If the creeper is too fast or too slow, change `TICK`.
    - A title screen: `REDSTONE OS`, the creeper face from Lesson 10.13,
      and "Press space to play".
    - Walls inside the field, as in the Lesson 9.17 challenge.
    - Two creepers.
    - Type your name on the title screen, with `keyboard::letter`, and
      show it in the `BOOM!` line. (Keep the letters in an array, `[u8;
      16]`, with a count: there's no `String` without `std`!)

12. **The Stage 10 checkpoint.** Without notes, the learner explains,
    with drawings if they like:
    - What the kernel does: the referee game (10.1), system calls (10.2).
    - `fork`, `exec` and `wait`, and a zombie (10.3).
    - FIFO, shortest job first and round robin, with averages (10.4).
    - Translating an address with a page table (10.5).
    - A race condition and two fixes (10.6), and a deadlock (10.7).
    - Inodes and links, and why deleting isn't wiping (10.8).
    - How Shelly runs a pipeline (10.9, 10.10).
    - The boot relay, and PID 1 (10.11, 10.12).
    - How their kernel draws, reads keys and keeps time (10.13, 10.14).

    If any is shaky, go back to that lesson's checkpoint.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Keys do nothing in QEMU | The window doesn't have the keyboard | Click inside the QEMU window first. |
| The mouse is stuck inside QEMU | QEMU grabbed it | Press Ctrl+Alt+G. |
| `error[E0433]: cannot find module or crate \`rand\` in this scope` | `new_diamond` still uses `rand` | Change it to use `self.random` (step 6). |
| `error[E0061]: this function takes 0 arguments but 1 argument was supplied` | `Game::new` doesn't take the seed yet | `fn new(seed: u64) -> Game`, and `seed,` in the struct. |
| `error[E0063]: missing field \`seed\` in initializer of \`Game\`` | `seed,` is missing at the end of the struct in `new` | Add it. |
| `error[E0599]: no method named \`draw\` found` | `draw` isn't in `impl Game` | Put it inside the `impl Game { }` block. |
| The creeper moves very fast or very slowly | This computer's clock is faster or slower than 3 GHz | Change `TICK`: bigger is slower. |
| The arrows move the player, but sometimes twice | The keyboard repeats a held key | Tap the arrows; that's how the real game behaves too. |
| The diamonds are always in the same places | The seed is a fixed number | Use `Game::new(now())`. |

## Talk about it

- How does your kernel read the keyboard? What's a port?
- What's the difference between polling and interrupts? Which does
  Linux use?
- How does `random` work? Why isn't it *really* random?
- Why could the game's rules move from Stage 9 into the kernel without
  changing?

## Challenge *(if there's time, or for next time)*

- **Interrupts, for real.** Chapters 5 to 7 of *Writing an OS in Rust*,
  in the offline library (`repos/writing-an-os-in-rust/blog/content/
  edition-2/posts`), add CPU exceptions, a double fault handler, and
  hardware interrupts from the timer and the keyboard. They need two
  more crates (`x86_64` and `pic8259`), which the guide can fetch (see
  the OS lab handbook). Try it in a copy of your kernel.
- Show the time since boot on the screen, in seconds, using `now()` and
  your `TICK` (or your measured cycles per second).
- Use the speaker! Port `0x61` and the timer chip on ports `0x42` and
  `0x43` can beep. (Search the OSDev wiki's "PC Speaker" page for how,
  if you're online with the guide.)

## Checkpoint

The learner can, without help:
- [ ] Read scancodes from the keyboard's ports, and explain them
- [ ] Explain polling and interrupts
- [ ] Explain the pseudo-random number generator and the time-stamp
      counter
- [ ] Play Creeper Chase on their own kernel, and change something
- [ ] Answer the Stage 10 checkpoint questions (step 12)

## Lab notebook

Copy the scancodes for your name. Draw `play`'s loop: check keys, is it
time?, draw, tick, caught? Write how the seed and `random` work, with
the first three numbers worked out by hand (just the idea: the real
numbers are huge!). Commit. Add *port*, *scancode*, *polling*,
*interrupt*, *time-stamp counter* and *pseudo-random number* to
`dictionary.md`. Stamp the Stage 10 badge, **Kernel Hacker**, on the
passport.

## Guide's background *(optional reading)*

The keyboard here is the PS/2 controller (an Intel 8042 and its
successors), which every PC and QEMU still emulates; USB keyboards are
presented through it by the firmware's "legacy" support. Its default
scancodes are "set 1", from the IBM PC of 1981. Reading ports with `in`
needs kernel mode, which is exactly what a normal Linux program doesn't
have (Lesson 10.2).

The random number generator is a **linear congruential generator**:
seed = seed × a + c, with the wrap-around at 2⁶⁴ making it modular
arithmetic. The constants are Donald Knuth's choice for 64-bit numbers
(from his MMIX computer). It's a linear function, which ties to the
stage's algebra gate, and good enough for a game, but not for secrets:
Stage 11 shows why. `rdtsc` reads the time-stamp counter, which on
modern CPUs ticks at a constant rate (often the CPU's base frequency),
so `TICK` may need adjusting on very fast or slow computers. In QEMU
without KVM it still follows real time, roughly.

The finished kernel is in the course repository, in
`labs/os/redstone-os/`, for you to compare with. It's the course's own
code (MIT), and this lesson shows all of it, so it isn't a secret.
