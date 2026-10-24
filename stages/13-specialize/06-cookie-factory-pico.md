# Lesson 13.6: The Cookie Factory, for Real

**Time:** 2 sessions of 45 min · **You need:** the Pico, a breadboard,
2 push buttons and 4 jumper wires (or the emulator); `~/lab/pico`;
Lesson 4.13's notebook pages · **New words:** input, output, pull-up,
ground, GPIO, pinout, fail-safe

## Goal *(read this to the learner)*

> In Lesson 4.13 you built the most famous rung in factory programming,
> the seal-in, in Digital and in a pretend Python PLC. Today you'll make
> it real: two real buttons, a real chip running a real scan, a hundred
> times a second. The Pico's LED is the conveyor belt's motor. This is
> exactly what the PLCs in factories do.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once, and look back at Lesson 4.13's seal-in
      rung and the Cookie Factory.
- [ ] Lesson 13.5 is done: `cargo run --release` (or the emulator) works.
- [ ] Unplug the Pico before wiring. Everything is 3.3 volts from USB,
      so it's safe to touch, but wiring with the power off is a good
      habit.
- [ ] Find a **pinout** picture of the Pico (it's printed on the back of
      the board too, and in the [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)).
      This lesson uses physical pins **18** (GND), **19** (GP14) and
      **20** (GP15), the last three on the left-hand side with the USB
      socket at the top.

## Warm-up (5 min)

"Say the seal-in rung's formula." *(motor = (start OR motor) AND NOT
stop.)* "What are the three steps of a scan?" *(Read the inputs, solve
the rungs, write the outputs.)*

## Activity

### Session 1: wiring

1. **Pins.** **Say:** "The Pico's legs are called **GPIO** pins:
   general-purpose input and output. Your program decides, for each one,
   whether it's an **output** (it switches something, like the LED) or
   an **input** (it reads something, like a button)." Look at the
   pinout. Find GP14, GP15, and a **GND** ("ground", 0 volts) pin.

2. **How a button is read.** Draw it:
   ```
     3.3 V ──[ pull-up, inside the chip ]──┬── GP14 ──> the program reads it
                                           │
                                        [button]
                                           │
                                         GND (0 V)
   ```
   **Say:** "Inside the chip, a **pull-up** gently pulls the pin up to
   3.3 volts: that reads as **high**. Press the button, and it connects
   the pin straight to ground: that reads as **low**. So **pressed is
   low**. It's backwards, but it's how nearly every button in the world
   is wired, because it needs only one wire to ground." **Ask:** "What
   does the pin read if the wire falls out?" *(High: not pressed.)*

3. **Wire it** (Pico unplugged). Push the Pico H into one end of the
   breadboard, across the middle gap. Put the two buttons across the
   middle gap further along. Then:
   - Pin 18 (GND) to the breadboard's blue **−** rail.
   - Pin 19 (GP14) to one leg of the **start** button; the leg
     diagonally opposite to the **−** rail.
   - Pin 20 (GP15) to one leg of the **stop** button; its diagonal leg
     to the **−** rail.

   **Say:** "Diagonal legs are always on different sides of the switch,
   so they're the safe pair to use." The guide checks every wire against
   the pinout before plugging in.

   **Emulator:** no wiring: `pico-sim.mjs ... latch` presses GP14 at 0.5
   seconds and GP15 at 1.5 seconds, just like these buttons.

### Session 2: the rung in Rust

4. **A new project.**
   ```
   cp -r ~/lab/pico/kit ~/lab/pico/latch
   cd ~/lab/pico/latch
   ```
   Open `src/main.rs`. It's the blink program. Change three things.

   a. The top `use` line for pins, so we can read inputs too:
   ```rust
   use embedded_hal::digital::{InputPin, OutputPin};
   ```
   b. Replace the line `let mut led = pins.led.into_push_pull_output();`
   with the inputs, the output, and the motor's memory:
   ```rust
       let mut start_button = pins.gpio14.into_pull_up_input();
       let mut stop_button = pins.gpio15.into_pull_up_input();
       let mut motor_light = pins.led.into_push_pull_output();
       let mut motor = false;
   ```
   c. Replace the whole `loop { ... }` with the scan:
   ```rust
       loop {
           // 1. Read the inputs. A pressed button connects the pin to ground: low.
           let start = start_button.is_low().unwrap();
           let stop = stop_button.is_low().unwrap();

           // 2. Solve the rung.
           motor = (start || motor) && !stop;

           // 3. Write the outputs.
           if motor {
               motor_light.set_high().unwrap();
           } else {
               motor_light.set_low().unwrap();
           }

           // One scan every 10 milliseconds: 100 scans a second.
           timer.delay_ms(10);
       }
   ```
   **Ask:** "Find the three steps of the scan. Find the formula from
   Lesson 4.13." **Say:** "It's the same line as the Python Cookie
   Factory, with `||`, `&&` and `!` for OR, AND and NOT."

5. **Run it. Real Pico:** BOOTSEL, plug in, `cargo run --release`.
   Press start: the LED comes on, and *stays on* when you let go. Press
   stop: it goes off, and stays off. Hold both: **Ask:** "Who wins?"
   *(Stop, for safety, as in Lesson 4.13.)*

   **Emulator:**
   ```
   cargo build --release
   elf2uf2-rs target/thumbv6m-none-eabi/release/pico latch.uf2
   node ~/lab/pico/sim/pico-sim.mjs latch.uf2 2 latch
   ```
   **They should see:**
   ```
   0.000 s  LED off
   0.500 s  (press start)
   0.510 s  LED on
   0.703 s  (let go of start)
   1.500 s  (press stop)
   1.510 s  LED off
   1.703 s  (let go of stop)
   2.000 s  stopped
   ```
   **Ask:** "Why does the LED come on at 0.510, not 0.500?" *(The scan
   was waiting in its 10 ms delay: the button is only read once per
   scan. A real PLC has this delay too: it's called the **scan time**.)*

6. **Break the seal.** Take `|| motor` out: `motor = start && !stop;`.
   **Ask first:** "What will happen?" Then run it. **They should see** a
   warning (`value assigned to motor is never read`: the compiler
   noticed the memory isn't used!) and, in the emulator:
   ```
   0.510 s  LED on
   0.707 s  (let go of start)
   0.710 s  LED off
   ```
   With a real Pico: the light is only on while you hold start. **Say:**
   "Without the feedback, there's no memory. That's why the motor's own
   contact is in the rung." Put it back.

7. **Fail-safe.** **Ask:** "In a real factory, what if the wire to the
   stop button breaks? With our wiring, what happens?" *(A broken wire
   reads high, 'not pressed', so stop can never be pressed. Dangerous!)*
   **Say:** "That's why real factories use stop buttons that are
   connected *until* you press them, so a broken wire means stop. That's
   called **fail-safe**." Write it in the journal: it's one of the most
   important ideas in all of engineering.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| ``error[E0599]: no method named `is_low` found`` with a `help` suggesting `embedded_hal::digital::v2::InputPin` | `InputPin` isn't in the `use` line (the `help` suggests the old version's; don't use it) | Use `use embedded_hal::digital::{InputPin, OutputPin};` exactly. |
| ``error[E0425]: cannot find value `led` in this scope`` | The old blink `loop` is still there | Replace the whole `loop` (step 4c). |
| The LED comes on as soon as the Pico starts | GP14 is wired straight to GND, not through the button | Unplug, and check the wiring against the pinout. |
| Pressing the button does nothing | The legs used are on the same side of the switch, or the **−** rail isn't connected to GND | Use diagonal legs; check pin 18's wire. |
| The light is on only while start is held | The `\|\| motor` is missing | Step 6: put it back. |

## Talk about it

- What's a GPIO pin? What's the difference between an input and an
  output?
- Why does a pressed button read low?
- How is the Pico's loop like a PLC's scan? What's the scan time?
- What happens without the seal-in contact? Why?
- What does fail-safe mean? Can you think of a fail-safe thing at home?
  *(A kettle that switches off by itself; a lawnmower handle you have to
  hold.)*

## Challenge *(if there's time, or for next time)*

- Add the rest of the Cookie Factory: a third button on GP13 (pin 17) is
  the cookie sensor, and an LED with a 330 Ω resistor on another pin is
  the stamper. *(Ask the guide to check the LED's wiring: long leg
  towards the pin.)*
- Count cookies, and blink the onboard LED that many times when stop is
  pressed.
- Make the scan time 500 ms. Can you press start and let go without the
  Pico noticing? Why does that matter in a real factory?

## Checkpoint

The learner can, without help:
- [ ] Wire a button to a GPIO pin and ground, using the pinout
- [ ] Explain pull-up, and why pressed is low
- [ ] Write the seal-in rung as a Pico scan loop, and run it
- [ ] Explain what the seal-in contact does, by breaking it
- [ ] Explain fail-safe, with the stop-button example

## Lab notebook

Draw the wiring, with pin numbers, and the button-and-pull-up picture.
Put the Lesson 4.13 rung, the Python line and the Rust line side by
side. Commit the project. Add *GPIO*, *pull-up*, *ground*, *pinout*,
*scan time* and *fail-safe* to `dictionary.md`.

## Guide's background *(optional reading)*

The RP2040's internal pull-ups are roughly 50 kΩ, enough for a button on
short wires. Mechanical buttons **bounce** (they make and break contact
a few times in the first millisecond or so); a 10 ms scan reads them
too slowly to see it, which is one reason PLC scans and many
microcontroller loops don't need explicit debouncing for simple logic.
For counting presses, though, bounce does matter (see the Challenge).

On a real machine, stop circuits use normally-closed contacts and are
hard-wired, not just programmed: an emergency stop cuts power through
safety relays rated for the job, and the PLC's own stop logic is only a
convenience. This lesson's normally-open stop button is fine for a
learning board and wrong for a machine, which is exactly why it's
worth talking about. For the Challenge's LED, the RP2040's pins can
supply a few milliamps safely; 330 Ω at 3.3 V gives a comfortable
3–5 mA.
