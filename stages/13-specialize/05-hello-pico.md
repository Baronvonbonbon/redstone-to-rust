# Lesson 13.5: Hello, Pico

**Time:** 2 sessions of 45 min · **You need:** a Raspberry Pi Pico or
Pico H and a micro-USB data cable (or the emulator); a terminal;
`~/lab/pico` · **New words:** microcontroller, embedded, cross-compile,
target, flash, firmware, `no_std`

## Goal *(read this to the learner)*

> Inside a washing machine, a microwave, a car, or a factory's PLC
> there's a tiny computer with no screen, no keyboard and no operating
> system. Today you'll program one: the Raspberry Pi Pico, in Rust.
> Your program will be the only thing running on the chip, and the
> first thing it does is the "Hello, world!" of hardware: blink a light.

## Before the lesson *(guide, 20 min the first time)*

- [ ] Read this lesson and the [Pico lab handbook](../../labs/pico/README.md):
      the parts, the setup, and the honesty note (the course's programs
      were tested in an emulator).
- [ ] The setup is done: `./scripts/install-packages.sh --later`,
      `./scripts/give-lab.sh LEARNER pico`, then, as the learner and
      online, `bash ~/lab/pico/setup-pico.sh`. It ends with `Done. Next,
      Lesson 13.5: cp -r ~/lab/pico/kit ~/lab/pico/blink`.
- [ ] Check the board is an RP2040 **Pico** or **Pico H**: not a Pico W,
      not a Pico 2.
- [ ] No Pico yet? Do the lesson with the emulator: the steps marked
      **Emulator** replace the ones marked **Real Pico**.

## Warm-up (5 min)

"How many computers are in this house?" Count together: laptops and
phones, then keep going: the microwave, the washing machine, the TV
remote, the car, the thermostat, the Minecraft controller... *(Dozens!
Most computers aren't PCs.)*

## Activity

### Session 1: a computer the size of a stick of gum

1. **Meet the Pico.** Look at it closely (a magnifying glass helps).
   **Ask:** "Where's the computer?" *(The black square in the middle:
   the RP2040 chip.)* **Say:** "That one chip has two processors, a bit
   of memory, and pins that can read buttons and switch lights. The
   small square chip is the **flash** memory, where your program is
   kept, even with the power off. A computer like this, built into a
   thing, is a **microcontroller**, and programming it is **embedded**
   programming." Compare with the Stage 6 Hack computer: a CPU, memory,
   and input and output, all on one chip.

2. **Compare the numbers.** Write them side by side:

   | | The PC | The Pico |
   |---|---|---|
   | Processor speed | about 3 000 MHz, many cores | 125 MHz, 2 cores |
   | Memory (RAM) | about 16 000 000 KB | 264 KB |
   | Storage | about 500 GB | 2 MB of flash |
   | Operating system | Linux | none! |

   **Ask:** "Pico memory is about how many Minecraft screenshots?"
   *(Less than one.)* **Say:** "With no operating system, there's no
   `println!`, no files, no processes. Your program has the whole chip
   to itself, like Redstone OS in Stage 10."

3. **The kit.** Make a project from the kit, and look inside:
   ```
   cp -r ~/lab/pico/kit ~/lab/pico/blink
   cd ~/lab/pico/blink
   ls -a
   cat .cargo/config.toml
   ```
   **They should see** `Cargo.toml`, `memory.x`, `src`, and a `.cargo`
   folder, whose file starts:
   ```
   [build]
   target = "thumbv6m-none-eabi"
   ```
   **Say:** "The PC's processor is x86. The Pico's is an ARM Cortex-M0+,
   which speaks a different machine language: **thumbv6m**. So the
   compiler on the PC makes a program for a *different* computer. That's
   called **cross-compiling**. The **target** says which computer."
   `cat memory.x`: **Say:** "And this tells the linker where the Pico's
   flash and memory are, like the Hack computer's memory map in Lesson
   6.11."

4. **Read the program.** Open `src/main.rs` together. Go through it:
   - `#![no_std]`: "no standard library": no operating system to ask
     for files or printing. Only `core`, the bits of Rust that need
     nothing.
   - `#![no_main]` and `#[entry]`: there's no Linux to call `main`, so
     we mark where the chip starts.
   - `fn main() -> !`: the `!` means "never returns". **Ask:** "Why?"
     *(Where would it return to? There's nothing else running.)*
   - `pac::Peripherals::take()`: "take charge of the chip's hardware".
     There's only one of each, so Rust lets only one part of the
     program have it. Ownership, from Lesson 9.4, for real hardware!
   - The clocks set the speed; the `Timer` counts microseconds; `pins`
     are the legs. `pins.led.into_push_pull_output()` makes the LED's
     pin (GP25) an output.
   - The `loop`: on, wait 500 ms, off, wait 500 ms, for ever.

5. **Build it.**
   ```
   cargo build --release
   ```
   **They should see**, after a minute the first time:
   ```
      Compiling rp-pico v0.9.0
      Compiling pico v0.1.0 (/home/sam/lab/pico/blink)
       Finished `release` profile [optimized] target(s) in 26.00s
   ```
   `ls -l target/thumbv6m-none-eabi/release/pico`: about 16 750 bytes.
   **Say:** "That's a whole program, with everything it needs to start a
   computer from nothing. Your Rust programs on Linux are bigger, and
   they lean on Linux for everything."

### Session 2: blink!

6. **Load it. Real Pico:** **Say:** "To put a program on the Pico, it
   pretends to be a USB stick." Hold down the white **BOOTSEL** button,
   plug in the USB cable, and let go. A drive called **RPI-RP2** appears
   in the file manager (open it once, so it's mounted). Then:
   ```
   cargo run --release
   ```
   The runner (`elf2uf2-rs -d`) turns the program into a `.uf2` file,
   says it found the Pico's drive and is transferring the program, and
   copies it. The drive disappears, and **the LED blinks**, once a
   second. That's it: you've written **firmware**, the program that
   lives inside a device.

   **Emulator:** without a Pico, `cargo run --release` ends with
   `Error: "Unable to find mounted pico"`. Make the `.uf2` file
   yourself, and run it in the emulator for 1.2 seconds:
   ```
   elf2uf2-rs target/thumbv6m-none-eabi/release/pico blink.uf2
   node ~/lab/pico/sim/pico-sim.mjs blink.uf2 1.2
   ```
   **They should see:**
   ```
   0.000 s  LED off
   0.000 s  LED on
   0.500 s  LED off
   1.000 s  LED on
   1.213 s  stopped
   ```
   (The last time is a little different each run.) **Say:** "The
   emulator is a program that pretends to be the RP2040, instruction by
   instruction. It runs your real `.uf2` file."

7. **Change it.** Make it blink five times faster: change both
   `delay_ms(500)` to `delay_ms(100)`. Load it again (BOOTSEL and `cargo
   run --release`, or the two emulator lines with `0.5` seconds).
   **They should see** the LED flicker; in the emulator, `LED on` and
   `LED off` every `0.100 s`. **Ask:** "What's the fastest blink your
   eyes can see? Try 20, 10, 5." *(Somewhere around 20 ms, the blinking
   becomes a glow.)*

8. **Unplug it, plug it in again** (without BOOTSEL). **Ask:** "Does it
   still blink? Why?" *(The program is in the flash, so the Pico runs it
   whenever it gets power, like a microwave remembering how to be a
   microwave.)* Commit the project: `git init`, then add and commit, as
   in Stage 5. (The kit's `.gitignore` leaves out `target` and `.uf2`
   files.)

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| No RPI-RP2 drive appears | BOOTSEL wasn't held while plugging in, or the cable only charges | Unplug, hold BOOTSEL, plug in, then let go. Try another cable. |
| `Error: "Unable to find mounted pico"` | No Pico in BOOTSEL mode, or its drive isn't mounted | BOOTSEL again, and open the drive in the file manager. Or use the emulator. |
| The program loaded but nothing blinks | A Pico W or Pico 2 | Check the board (see the lab handbook). Use the emulator meanwhile. |
| ``error[E0463]: can't find crate for `core` `` | The Pico target isn't installed | Run `bash ~/lab/pico/setup-pico.sh` (online). |
| ``error: could not execute process `elf2uf2-rs -d ...` (never executed)`` or `elf2uf2-rs: command not found` | `elf2uf2-rs` isn't installed | Run `setup-pico.sh`. |
| `Cannot find module 'rp2040js'` | The emulator isn't installed | The guide installs Node.js (`install-packages.sh --later`); rerun `setup-pico.sh`. |

## Talk about it

- What's a microcontroller? Name five things with one inside.
- Why does the Pico need `no_std`?
- What's cross-compiling? What's the target?
- Why does `main` return `!`?
- Why does the program survive unplugging?

## Challenge *(if there's time, or for next time)*

- Blink SOS in Morse code: three short, three long, three short, then a
  pause.
- Blink a heartbeat: two quick blinks, a long pause.
- Make the blink speed up, a little faster each time round, then start
  slow again. *(A variable for the delay, outside the `loop`.)*

## Checkpoint

The learner can, without help:
- [ ] Make a new Pico project from the kit
- [ ] Explain `no_std`, `#[entry]` and `-> !`
- [ ] Build a program, and load it onto the Pico (or run it in the
      emulator)
- [ ] Change the blink speed
- [ ] Explain cross-compiling and the target

## Lab notebook

Draw the Pico and label the chip, the flash, the LED, the BOOTSEL
button and the USB socket. Copy the PC-and-Pico table. Add
*microcontroller*, *embedded*, *cross-compile*, *target*, *flash* and
*firmware* to `dictionary.md`.

## Guide's background *(optional reading)*

The RP2040 has two ARM Cortex-M0+ cores at 125 MHz (it's often run
faster), 264 KB of SRAM and no built-in flash: the Pico board adds 2 MB
of external QSPI flash. Its mask ROM holds a bootloader that appears as
a USB mass-storage device in BOOTSEL mode and accepts **UF2** files, a
format of 512-byte blocks, each carrying its own flash address, designed
by Microsoft for MakeCode boards. `elf2uf2-rs` converts Rust's ELF
output to UF2 and copies it to the drive.

The kit follows the `rp-pico` board crate's template (from the
rp-rs project): `memory.x` includes the 256-byte **second-stage
bootloader** (`BOOT2`) that sets up the flash chip, `cortex-m-rt`
provides the vector table and the `#[entry]` start-up code, and
`panic-halt` makes a panic stop the chip in an endless loop. The
*Embedded Rust Book* (in the offline library, `repos/embedded-rust-book`)
explains all of this in depth, and is the next book for a learner who
loves this path.
