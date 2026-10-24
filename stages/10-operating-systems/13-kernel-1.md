# Lesson 10.13: A Kernel of Your Own, Part 1: Hello, Bare Metal

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; QEMU; `~/lab/os/kernel-kit` (from `setup-os.sh`); squared paper
· **New words:** bare metal, `no_std`, entry point, VGA text buffer,
`unsafe`, volatile, code page 437

## Goal *(read this to the learner)*

> In Lesson 10.12, your program ran on top of Linux. Now there won't be
> any Linux: your Rust program will *be* the operating system, running
> straight on the (pretend) computer: **bare metal**. No `println!`, no
> files, no threads, because there's nobody to ask. You'll draw on the
> screen by writing to memory, just as you did on Hack, paint a creeper,
> and make your kernel count and panic in style.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] `setup-os.sh` must have run (the Stage 10 README): check that
      `~/lab/os/kernel-kit` exists, and `bootimage --version` works in
      the learner's account.
- [ ] QEMU must work (Lesson 10.11).

## Warm-up (5 min)

"In Hack, how did a program draw on the screen?" *(By writing to the
memory addresses from 16384: each bit was a pixel.)* "Who drew things in
the Jack OS?" *(The `Screen` class, which *we* wrote.)* "Today, the
screen is memory again, and we write the whole OS."

## Activity

### Session 1: hello from nowhere

1. **Copy the kit.**
   ```
   cd ~/lab/os
   cp -r kernel-kit redstone-os
   cd redstone-os
   ls -a
   ```
   **They should see:** `.cargo`, `Cargo.lock`, `Cargo.toml`,
   `rust-toolchain.toml`, `src`, `target` and `x86_64-redstone.json`.
   Open each file with the learner, and **say**:
   - `Cargo.toml`: "one crate, `bootloader`, which loads our kernel when
     the computer starts. And `panic = "abort"`: when something goes
     wrong, just stop."
   - `rust-toolchain.toml`: "kernels need a few experimental Rust
     features, so this folder uses a **nightly** compiler, pinned to one
     day."
   - `x86_64-redstone.json`: "a description of the computer we're
     building for. Look for `"os": "none"`: there's no operating system.
     We're it."
   - `.cargo/config.toml`: "build Rust's `core` library for our computer
     too, and make `cargo run` start QEMU."

2. **Run it.**
   ```
   cargo run
   ```
   **They should see**, after a minute of `Compiling` the first time,
   `Building bootloader`, `Created bootimage`, and then a QEMU window
   with, at the top left in light cyan (a light blue-green):
   ```
   Hello from Redstone OS!
   ```
   (There may be a little blinking line at the top left too: that's the
   cursor, which our kernel doesn't use.) **Say:** "That's a whole operating
   system. It just doesn't do much yet." Close the QEMU window to stop
   it.

3. **Read the kernel.** Open `src/main.rs`:
   ```rust
   #![no_std]
   #![no_main]

   use bootloader as _;
   use core::panic::PanicInfo;

   static HELLO: &[u8] = b"Hello from Redstone OS!";

   #[unsafe(no_mangle)]
   pub extern "C" fn _start() -> ! {
       let screen = 0xb8000 as *mut u8;
       for (i, &letter) in HELLO.iter().enumerate() {
           unsafe {
               *screen.add(i * 2) = letter;
               *screen.add(i * 2 + 1) = 0x0b;
           }
       }
       loop {}
   }

   #[panic_handler]
   fn panic(_info: &PanicInfo) -> ! {
       loop {}
   }
   ```
   Go through it together:
   - "`#![no_std]`: don't use the standard library. Everything in `std`
     (printing, files, threads) asks an OS, and there isn't one. We still
     have `core`: numbers, `Option`, iterators, `match`."
   - "`#![no_main]`: there's no `main`, because nothing calls it."
   - "`use bootloader as _;` means 'include the bootloader crate', even
     though we don't call it."
   - "`_start` is the **entry point**: the bootloader jumps here when it
     has loaded us. `-> !` means it never returns. Where would it return
     *to*?"
   - "`0xb8000` is where the screen is in memory: the **VGA text
     buffer**. Each character on the screen is two bytes: the letter,
     then its colour. That's why it's `i * 2` and `i * 2 + 1`."
   - "`*mut u8` is a raw pointer, like in C, and writing through one is
     `unsafe`: Rust can't check it, so we promise it's right."
   - "`loop {}` at the end: a kernel never stops."
   - "And Rust needs a `panic_handler`, because there's no OS to print
     the panic."

4. **Colours.** **Say:** "The colour byte is two hex digits: the first is
   the background, the second the letter." Draw the colour table:

   | Digit | Colour | Digit | Colour |
   |---|---|---|---|
   | 0 | black | 8 | dark grey |
   | 1 | blue | 9 | light blue |
   | 2 | green | a | light green |
   | 3 | cyan | b | light cyan |
   | 4 | red | c | light red |
   | 5 | magenta | d | pink |
   | 6 | brown | e | yellow |
   | 7 | light grey | f | white |

   **Ask:** "What's `0x0b`?" *(Light cyan on black.)* Change it to `0x4e`
   and `cargo run`. *(Yellow on red.)* Then try their own favourite.

5. **What `no_std` means.** Try these one at a time, putting each back
   afterwards:
   - Delete the `#![no_std]` line, and `cargo build`. **They should
     see:** ``error[E0463]: can't find crate for `std` ``, and a note that
     the `x86_64-redstone` target may not support the standard library.
   - Add `println!("Hi");` before `loop {}`. **They should see:** ``error:
     cannot find macro `println` in this scope``.
   - Delete the whole `panic` function. **They should see:**
     ``error: `#[panic_handler]` function required, but not found``.

   **Say:** "No standard library, no printing. We'll build our own." Put
   everything back, and commit.

### Session 2: a screen module and a creeper

6. **The screen as a grid.** **Say:** "The screen is 80 columns and 25
   rows. Row 0 is the top. So where in memory is the character at column
   x, row y?" Work it out together on squared paper: each row is 80
   characters, each character 2 bytes. *(place = (y × 80 + x) × 2, from
   `0xb8000`.)* **Ask:** "Where's the bottom-right character?" *((24 × 80
   + 79) × 2 = 3998.)*

7. **`src/screen.rs`.** Make a new file:
   ```rust
   //! The VGA text screen: 80 columns and 25 rows of coloured characters.

   #![allow(dead_code)]

   use core::ptr::write_volatile;

   pub const WIDTH: usize = 80;
   pub const HEIGHT: usize = 25;

   pub const BLACK: u8 = 0;
   pub const BLUE: u8 = 1;
   pub const GREEN: u8 = 2;
   pub const CYAN: u8 = 3;
   pub const RED: u8 = 4;
   pub const BROWN: u8 = 6;
   pub const GRAY: u8 = 7;
   pub const LIGHT_GREEN: u8 = 10;
   pub const LIGHT_CYAN: u8 = 11;
   pub const YELLOW: u8 = 14;
   pub const WHITE: u8 = 15;

   /// A full block, in the screen's own alphabet.
   pub const BLOCK: u8 = 0xdb;

   /// Where the screen starts in memory.
   const SCREEN: *mut u8 = 0xb8000 as *mut u8;

   /// Makes a colour byte: the background in the top four bits,
   /// the letter's colour in the bottom four.
   pub fn colour(letter: u8, background: u8) -> u8 {
       background << 4 | letter
   }

   /// Puts one character at column x, row y.
   pub fn put(x: usize, y: usize, character: u8, colour: u8) {
       if x >= WIDTH || y >= HEIGHT {
           return;
       }
       let place = (y * WIDTH + x) * 2;
       unsafe {
           write_volatile(SCREEN.add(place), character);
           write_volatile(SCREEN.add(place + 1), colour);
       }
   }

   /// Fills the whole screen with spaces of one colour.
   pub fn clear(colour: u8) {
       for y in 0..HEIGHT {
           for x in 0..WIDTH {
               put(x, y, b' ', colour);
           }
       }
   }

   /// Writes text, starting at column x, row y.
   pub fn text(x: usize, y: usize, words: &str, colour: u8) {
       for (i, character) in words.bytes().enumerate() {
           put(x + i, y, character, colour);
       }
   }
   ```
   **Say:**
   - "`#![allow(dead_code)]`: we won't use every colour, and that's
     fine."
   - "`background << 4 | letter` shifts the background up four bits:
     the same as times 16. **Ask:** what's `colour(14, 4)`? *(4 × 16 + 14
     = 78 = `0x4e`: yellow on red, from step 4.)*"
   - "`put` checks it's on the screen first: writing past the end would
     scribble on other memory, and nothing would stop us."
   - "`write_volatile` means 'really write this, now'. The compiler
     likes to skip writes to memory that nobody reads back, but the
     screen hardware *is* reading it."
   - "`0xdb` is a full block: the screen has its own alphabet, called
     **code page 437**, with letters, lines and shapes."

8. **Paint a scene.** Replace `src/main.rs` with:
   ```rust
   #![no_std]
   #![no_main]

   mod screen;

   use bootloader as _;
   use core::panic::PanicInfo;
   use screen::{BLACK, BLOCK, BLUE, BROWN, GREEN, LIGHT_GREEN, WHITE, YELLOW, colour};

   #[rustfmt::skip]
   const CREEPER: [&str; 8] = [
       "GGGGGGGG",
       "GGGGGGGG",
       "GBBGGBBG",
       "GBBGGBBG",
       "GGGBBGGG",
       "GGBBBBGG",
       "GGBBBBGG",
       "GGBGGBGG",
   ];

   #[unsafe(no_mangle)]
   pub extern "C" fn _start() -> ! {
       screen::clear(colour(WHITE, BLUE));
       for x in 0..screen::WIDTH {
           screen::put(x, 20, BLOCK, colour(GREEN, BLUE));
           for y in 21..screen::HEIGHT {
               screen::put(x, y, BLOCK, colour(BROWN, BLUE));
           }
       }
       screen::text(34, 2, "REDSTONE OS", colour(YELLOW, BLUE));

       for (row, line) in CREEPER.iter().enumerate() {
           for (column, pixel) in line.bytes().enumerate() {
               let paint = if pixel == b'G' { LIGHT_GREEN } else { BLACK };
               screen::put(10 + column * 2, 12 + row, BLOCK, colour(paint, BLUE));
               screen::put(11 + column * 2, 12 + row, BLOCK, colour(paint, BLUE));
           }
       }
       loop {}
   }

   #[panic_handler]
   fn panic(_info: &PanicInfo) -> ! {
       loop {}
   }
   ```
   **Say:** "The creeper is a picture made of letters: G for green, B for
   black. Each picture pixel is two characters wide, because characters
   are twice as tall as they are wide. `#[rustfmt::skip]` tells `cargo
   fmt` to leave our picture alone, instead of squashing it onto one
   line." `cargo run`. **They should see:**
   a blue sky, `REDSTONE OS` in yellow, a creeper face standing on a row
   of green grass, and brown dirt below. Commit.

### Session 3: write!, and a red screen of panic

9. **A pen.** **Say:** "Without `std` there's no `println!`. But `core`
   still knows how to *format* numbers and text; it just needs somewhere
   to write them. If we make something that can write a string, Rust's
   `write!` will do the rest." Add at the top of `screen.rs`, after the
   `#![allow...]` line: `use core::fmt;`. Then add at the bottom:
   ```rust
   /// A place on the screen to write to with `write!`, like a pen.
   pub struct Pen {
       x: usize,
       y: usize,
       colour: u8,
   }

   impl Pen {
       /// A new pen, at column x, row y, writing in a colour.
       pub fn new(x: usize, y: usize, colour: u8) -> Pen {
           Pen { x, y, colour }
       }
   }

   impl fmt::Write for Pen {
       fn write_str(&mut self, words: &str) -> fmt::Result {
           for character in words.bytes() {
               if character == b'\n' || self.x >= WIDTH {
                   self.x = 0;
                   self.y += 1;
               }
               if character != b'\n' {
                   put(self.x, self.y, character, self.colour);
                   self.x += 1;
               }
           }
           Ok(())
       }
   }
   ```
   **Say:** "`Pen::new` makes a pen. `fmt::Write` is a trait (Lesson
   9.13): anything that has a
   `write_str` method can be used by `write!`. A new line, or reaching the
   right-hand edge, moves the pen to the start of the next row."

10. **Counting, and panicking.** Replace `src/main.rs` with:
    ```rust
    #![no_std]
    #![no_main]

    mod screen;

    use bootloader as _;
    use core::fmt::Write;
    use core::panic::PanicInfo;
    use screen::{BLACK, Pen, RED, WHITE, YELLOW, colour};

    #[unsafe(no_mangle)]
    pub extern "C" fn _start() -> ! {
        screen::clear(colour(WHITE, BLACK));
        let mut pen = Pen::new(0, 0, colour(YELLOW, BLACK));
        writeln!(pen, "Redstone OS can count!").unwrap();
        for number in 1..=10 {
            writeln!(pen, "{number} squared is {}", number * number).unwrap();
        }
        panic!("The creeper got in!");
    }

    #[panic_handler]
    fn panic(info: &PanicInfo) -> ! {
        let red = colour(WHITE, RED);
        screen::clear(red);
        let mut pen = Pen::new(0, 0, red);
        let _ = write!(pen, "KERNEL PANIC! {info}");
        loop {
            unsafe { core::arch::asm!("hlt") };
        }
    }
    ```
    **Say:** "When it panics, the whole screen goes red, and we write
    what happened. `hlt` is a CPU instruction that means 'rest until
    something happens': better than spinning round `loop {}` as fast as
    possible." `cargo run`. **They should see** the squares flash by,
    and then a red screen:
    ```
    KERNEL PANIC! panicked at src/main.rs:19:5:
    The creeper got in!
    ```
    **Ask:** "Why did the squares disappear?" *(The panic handler cleared
    the screen.)* To see them, put `//` in front of the `panic!` line
    (and add `loop {}` after it, because `_start` must never return).
    Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| ``error[E0463]: can't find crate for `std` `` | `#![no_std]` is missing | Put it back as the first line. |
| ``error: `#[panic_handler]` function required, but not found`` | The panic function is missing | Put it back (step 3). |
| ``error[E0133]: dereference of raw pointer is unsafe and requires unsafe block`` | A raw-pointer write outside `unsafe { }` | Wrap it in `unsafe { }`. |
| `error[E0308]: mismatched types` at `_start`, ``expected `!`, found `()` `` | `_start` can come to an end | End it with `loop {}` (or a `panic!`). |
| ``error: could not execute process `bootimage runner ...` (never executed)`` | `bootimage` isn't installed | Run `setup-os.sh` (the Stage 10 README). |
| `error: the crate ... could not be found in registry index` | A crate isn't in the offline cache | Use only the kit's crate; see the OS lab handbook. |
| The QEMU window stays black | The kernel wrote nothing, or wrote it off the screen | Check the address `0xb8000`, and that `put` gets x below 80 and y below 25. |
| The squares are written over each other | `writeln!` was typed as `write!` | Use `writeln!` for a new line after each. |

## Talk about it

- What's missing when there's no standard library? Why?
- Where's the screen? How do you work out where a character goes?
- Why is writing to the screen `unsafe`? Why `volatile`?
- How did we get `write!` to work with no `std`?

## Challenge *(if there's time, or for next time)*

- Draw a diamond sword, or your own Minecraft mob, in the scene.
- Code page 437 has hearts (`3`), diamonds (`4`), smiley faces (`1` and
  `2`) and lines for boxes (`0xc9`, `0xcd`, `0xbb`, `0xba`, `0xc8`,
  `0xbc`). Draw a box round `REDSTONE OS`.
- Write `fn number(x, y, n: u32)` that writes a number *without*
  `write!`, by dividing by 10 again and again (Stage 4's place value!).
- Make the kernel print a times table, in colour.

## Checkpoint

The learner can, without help:
- [ ] Explain `no_std`, `no_main` and `_start`
- [ ] Work out where a character goes in the VGA text buffer
- [ ] Draw on the screen with the `screen` module
- [ ] Explain how `Pen` lets `write!` work, and what the panic handler
      does

## Lab notebook

Draw the screen grid with the formula for a character's place. Copy
the colour table. Draw your creeper on squared paper first, then
compare. Commit. Add *bare metal*, *no_std*, *entry point*, *VGA text
buffer*, *unsafe*, *volatile* and *code page 437* to `dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows the first three chapters of Philipp Oppermann's
*Writing an OS in Rust* (in the offline library, in
`repos/writing-an-os-in-rust/blog/content/edition-2/posts`): "A
Freestanding Rust Binary", "A Minimal Rust Kernel" and "VGA Text Mode".
The kit is its setup, and `main.rs` in the kit is its first kernel,
lightly changed; the `screen` module and `Pen` are the course's own,
simpler versions of its `vga_buffer` module (which adds a global writer
behind a lock, and `print!` macros).

The `bootloader` crate (version 0.9) and `bootimage` tool make a disk
image with a small bootloader that switches the CPU into 64-bit mode,
sets up paging, and jumps to `_start`. `cargo run` uses `bootimage
runner`, which starts `qemu-system-x86_64` with the image as a disk.
The nightly compiler is needed for `build-std` (compiling `core` for a
new target) and for custom target files.

The VGA text buffer at physical address `0xb8000` has existed since the
IBM PC of 1981; every PC graphics card still pretends to have one when
it starts. In the colour byte, the top bit of the background can mean
"blink" on real hardware, which is why the course only uses the first
eight colours for backgrounds.
