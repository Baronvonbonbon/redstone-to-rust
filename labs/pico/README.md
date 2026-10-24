# The Pico lab (Stage 13, Lessons 13.5 to 13.7)

For the guide. The Pico path programs a Raspberry Pi Pico, a $4–$5
microcontroller board, in Rust, with no operating system at all: the
learner's program is the only thing running on the chip. It ends with
the Cookie Factory's PLC rung on real buttons and a fan controller with
a deadband, reporting over USB.

**Honesty note.** Every program here was built with the pinned crates
and checked in the **rp2040js emulator** (below), which runs the real
`.uf2` files, LED, buttons, thermometer and USB included. They have not
yet been tested on a physical board by the course's authors. The
outputs in the lessons that come from the emulator are marked; the few
that only a real board shows (the `RPI-RP2` drive, `elf2uf2-rs`'s copy
messages) are described from the tools' documentation. If you run it on
a real Pico, a patch with what you saw is very welcome (Lesson 13.4).

## What's here

| Path | What it is |
|---|---|
| `kit/` | A Cargo project ready for the Pico: the target, the linker script (`memory.x`), the runner, pinned crates (`Cargo.lock`), and a blink program. Copied for each new program. |
| `reference/` | The guide's finished versions of the three lesson programs: `blink.rs`, `latch.rs`, `fan.rs`. The learner types them in the lessons; these are for checking. |
| `sim/` | `pico-sim.mjs`, a small script around rp2040js that runs a `.uf2` and prints the LED, button and USB events. |
| `setup-pico.sh` | The one online step, run once in the learner's account. |

## Hardware

| Part | Notes | Rough price |
|---|---|---|
| **Raspberry Pi Pico H** (or a plain Pico) | Must be an **RP2040** Pico. **Not** a Pico W (its LED is wired to the wireless chip, so `blink` does nothing) and **not** a Pico 2 (a different chip, RP2350). The **H** has its pins already soldered on, so no soldering is needed. | $5 |
| Micro-USB cable | It must be a **data** cable. Many cheap phone-charging cables only carry power, and the Pico never appears. | $3 |
| Half-size breadboard | For the buttons in Lesson 13.6. | $3 |
| 2 tactile push buttons (6 mm, 4 legs) | Start and stop. | $1 |
| 4 male-to-male jumper wires | | $1 |

Lesson 13.7 needs no more parts: the "fan" is the Pico's LED, and the
thermometer is inside the chip. A real fan needs a transistor or a relay
board and a separate supply: a good project with an adult who knows
electronics, not part of the lesson.

**Safety.** Everything runs at 3.3 volts from the USB port, so it's
safe to touch. Never connect anything to the mains, and never connect a
motor straight to a Pico pin.

## Setting up (guide, once)

1. Stage 9's `setup-rust.sh` has run in the learner's account.
2. Install the system packages (`libudev-dev` and `pkg-config` are for
   building `elf2uf2-rs`; Node.js is only for the emulator):
   ```
   ./scripts/install-packages.sh --later
   ```
3. Give the lab: `./scripts/give-lab.sh LEARNER pico`. It copies this
   folder to `~/lab/pico`, without touching the learner's own Pico
   projects if they're already there.
4. As the learner, online: `bash ~/lab/pico/setup-pico.sh`. It adds
   Rust's `thumbv6m-none-eabi` target, installs `elf2uf2-rs` 2.2.0,
   builds the kit (downloading its crates), and installs the emulator.
   About 5 minutes. It ends with `Done. Next, Lesson 13.5: cp -r
   ~/lab/pico/kit ~/lab/pico/blink`. After that, everything works
   offline.
5. For Lesson 13.7's USB serial, let the learner's account use serial
   ports, then they log out and in again:
   ```
   sudo usermod -aG dialout LEARNER
   ```

## Putting a program on the Pico

The Pico has a tiny built-in program for receiving new ones. Hold down
its white **BOOTSEL** button while plugging in the USB cable, then let
go. A drive called **RPI-RP2** appears in the file manager, like a USB
stick. Then, in the program's folder:

```
cargo run --release
```

builds the program, and the runner (`elf2uf2-rs -d`, set in
`.cargo/config.toml`) turns it into a `.uf2` file and copies it onto the
drive. The Pico restarts and runs it, and the drive disappears. To load
a new program, do BOOTSEL again. Without a Pico in BOOTSEL mode, `cargo
run` ends with `Error: "Unable to find mounted pico"`.

## The emulator

For learners without a board, or to check a program before loading it:

```
elf2uf2-rs target/thumbv6m-none-eabi/release/pico blink.uf2
node ~/lab/pico/sim/pico-sim.mjs blink.uf2 1.2
```

The number is how many seconds of Pico time to run. The emulator is
slower than a real Pico, so a few simulated seconds take a few real
seconds. Add `latch` to press the buttons (start at 0.5 s, stop at
1.5 s) or `fan` to warm the thermometer (23.5 °C at 3 s, 25 at 6, 24 at
9, 23 at 12).

The emulator is [rp2040js](https://github.com/wokwi/rp2040js) 1.4.1
(MIT), pinned in `sim/package.json`. The RP2040's own start-up code
(its bootrom, BSD-3-Clause, from Raspberry Pi) is downloaded by
`setup-pico.sh` from the rp2040js repository rather than stored here.

## Troubleshooting

| What you see | What it means | What to do |
|---|---|---|
| No RPI-RP2 drive | BOOTSEL wasn't held while plugging in, or a charge-only cable | Unplug, hold BOOTSEL, plug in, let go. Try another cable. |
| `Error: "Unable to find mounted pico"` | No Pico in BOOTSEL mode, or the drive isn't mounted | BOOTSEL again; open the drive in the file manager once so Pop!_OS mounts it. |
| The program loaded but the LED never blinks | A Pico W, or a Pico 2 | Check the board: it must say "Pico" (or "Pico H") with an RP2040 chip. |
| ``error[E0463]: can't find crate for `core` `` | The Pico target isn't installed | Run `setup-pico.sh`. |
| `failed to run custom build command for libudev-sys` | `libudev-dev` missing when installing `elf2uf2-rs` | `./scripts/install-packages.sh --later`, then rerun `setup-pico.sh`. |
| `cat: /dev/ttyACM0: Permission denied` | The learner isn't in the `dialout` group yet | `sudo usermod -aG dialout LEARNER`, then log out and in. |
| `cat: /dev/ttyACM0: No such file or directory` | The fan program isn't running, or it's on `ttyACM1` | Check the LED, unplug and replug, then `ls /dev/ttyACM*`. |
| A few seconds of nothing, then lines | Pop!_OS's ModemManager checks every new serial device | Wait 5–10 seconds. |
| `npm ERR!` or `Cannot find module 'rp2040js'` | The emulator wasn't installed (needs Node.js and the internet once) | Install Node.js with `install-packages.sh --later` and rerun `setup-pico.sh`. |
