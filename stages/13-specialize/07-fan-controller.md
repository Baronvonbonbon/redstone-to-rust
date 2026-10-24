# Lesson 13.7: The Fan Controller

**Time:** 2 sessions of 45 min · **You need:** the Pico (or the
emulator); `~/lab/pico`; a calculator; the learner in the `dialout`
group (see the [lab handbook](../../labs/pico/README.md)) · **New
words:** sensor, setpoint, deadband, ADC, control loop, serial

## Goal *(read this to the learner)*

> Factories, fridges, fish tanks and your house's heating all do the
> same job: measure something, compare it with what it *should* be, and
> switch something on or off. Today you'll build one: a fan controller.
> The Pico's own thermometer is the sensor, its LED is the fan, and it
> reports what it's doing to the PC over USB, twice a second.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] For a real Pico: the learner is in the `dialout` group (`sudo
      usermod -aG dialout LEARNER`, then they log out and in), so they
      can read the Pico's USB messages.
- [ ] The program is long. If typing it all is too much, the learner can
      copy `~/lab/pico/reference/fan.rs` and read it instead, part by
      part, with you. Understanding it matters more than typing it.

## Warm-up (5 min)

"Our house's heating: how does it know when to switch on?" *(A
thermostat measures the temperature and compares it with the number
you set.)* "When does it switch off?"

## Activity

### Session 1: measuring and deciding

1. **The control loop.** Draw it as a circle with four stops: **measure**
   (a **sensor**) → **compare** with the **setpoint** (what it should
   be) → **act** (switch the fan) → the world changes → measure again.
   **Say:** "That's a **control loop**. A PLC's scan is one; so is a
   thermostat. Today's: if it's too hot, fan on; if it's cool enough,
   fan off."

2. **The thermometer inside the chip.** **Say:** "The RP2040 has a
   thermometer built in. It gives a voltage, which an **ADC**, an
   analogue-to-digital converter, turns into a number from 0 to 4095.
   The chip's datasheet says: 0.706 volts at 27 degrees, and 1.721
   millivolts *less* for each degree warmer." Work one out together,
   with a calculator, for the number **876**:
   - volts = 876 × 3.3 ÷ 4096 = 0.7058
   - degrees = 27 − (0.7058 − 0.706) ÷ 0.001721 = 27.1

   **Say:** "That's what the `celsius` function will do, thousands of
   times."

3. **The deadband.** **Ask:** "The setpoint is 24 degrees. Fan on above
   24, off below 24. The temperature is 24.0, then 24.1, then 23.9, then
   24.1... What does the fan do?" *(On, off, on, off: it chatters, and
   wears out.)* Draw a number line:
   ```
       fan goes OFF here           fan goes ON here
            |                           |
   ---------+-------------+-------------+---------
          23.5          24.0          24.5
                     (setpoint)
            <-------- deadband -------->
   ```
   **Say:** "Between 23.5 and 24.5 the fan *keeps doing what it was
   doing*. That gap is the **deadband**. It's memory again: like the
   seal-in, the fan's own state is part of the rule."

4. **Start the program.**
   ```
   cp -r ~/lab/pico/kit ~/lab/pico/fan
   cd ~/lab/pico/fan
   ```
   The kit already has the extra crates this needs (look in
   `Cargo.toml`: `usb-device`, `usbd-serial`, `heapless`). Replace
   `src/main.rs` with this first part (the start is like Lesson 13.6's):
   ```rust
   // A fan controller: the Pico's own thermometer, a setpoint and a deadband.
   // The "fan" is the Pico's LED. It reports over USB, for `cat /dev/ttyACM0`.
   #![no_std]
   #![no_main]

   use core::fmt::Write;
   use embedded_hal::delay::DelayNs;
   use embedded_hal::digital::OutputPin;
   use embedded_hal_0_2::adc::OneShot;
   use heapless::String;
   use panic_halt as _;
   use rp_pico::entry;
   use rp_pico::hal::{self, pac};
   use usb_device::class_prelude::UsbBusAllocator;
   use usb_device::prelude::*;
   use usbd_serial::SerialPort;

   // How far from the setpoint before the fan changes: half a degree each way.
   const BAND: f32 = 0.5;

   // The chip's thermometer gives a number from 0 to 4095. Turn it into degrees.
   fn celsius(raw: u16) -> f32 {
       let volts = raw as f32 * 3.3 / 4096.0;
       27.0 - (volts - 0.706) / 0.001721
   }
   ```
   Then `main`, from `#[entry]` down to `let pins = ...;`, exactly as in
   `~/lab/pico/latch/src/main.rs`, and after it:
   ```rust
       let mut fan = pins.led.into_push_pull_output();
   ```
   **Say:** "`f32` is a decimal number, like clox's `double` but smaller.
   `heapless::String` is a string with a fixed size, because with no
   operating system there's no heap to grow into." Stop here for today;
   the rest is next session.

### Session 2: talking to the PC

5. **USB serial.** **Say:** "The Pico can pretend, over USB, to be an old
   **serial** cable: a wire that carries text one letter at a time, the
   way computers talked before networks. Linux shows it as a file:
   `/dev/ttyACM0`. Everything is a file!" Add, after the `fan` line:
   ```rust
       // The USB connection, pretending to be a serial cable.
       let usb_bus = UsbBusAllocator::new(hal::usb::UsbBus::new(
           pac.USBCTRL_REGS,
           pac.USBCTRL_DPRAM,
           clocks.usb_clock,
           true,
           &mut pac.RESETS,
       ));
       let mut serial = SerialPort::new(&usb_bus);
       let mut usb = UsbDeviceBuilder::new(&usb_bus, UsbVidPid(0x16c0, 0x27dd))
           .strings(&[StringDescriptors::default()
               .manufacturer("Redstone to Rust")
               .product("Pico fan")
               .serial_number("1")])
           .unwrap()
           .device_class(2)
           .build();
   ```

6. **The sensor, the setpoint, and the loop.** Add the rest:
   ```rust
       // The thermometer inside the chip.
       let mut adc = hal::Adc::new(pac.ADC, &mut pac.RESETS);
       let mut thermometer = adc.take_temp_sensor().unwrap();

       // Start 2 degrees above the room's temperature, so a warm finger can reach it.
       let room = celsius(adc.read(&mut thermometer).unwrap());
       let setpoint = room + 2.0;
       let mut fan_on = false;
       let mut ticks: u32 = 0;

       loop {
           // USB needs looking after often, so this loop goes round every millisecond.
           usb.poll(&mut [&mut serial]);

           // Twice a second: read, solve, write, report.
           if ticks.is_multiple_of(500) {
               let temp = celsius(adc.read(&mut thermometer).unwrap());
               if temp > setpoint + BAND {
                   fan_on = true;
               }
               if temp < setpoint - BAND {
                   fan_on = false;
               }
               if fan_on {
                   fan.set_high().unwrap();
               } else {
                   fan.set_low().unwrap();
               }
               let mut line: String<64> = String::new();
               let state = if fan_on { "ON" } else { "off" };
               let _ = write!(line, "{temp:.1} C  setpoint {setpoint:.1}  fan {state}\r\n");
               let _ = serial.write(line.as_bytes());
           }
           ticks = ticks.wrapping_add(1);
           timer.delay_ms(1);
       }
   }
   ```
   **Ask:** "Find the deadband. What happens between the two `if`s?"
   *(Neither is true, so `fan_on` stays as it was.)* Check it against
   the reference: `diff src/main.rs ~/lab/pico/reference/fan.rs`
   (nothing printed means identical).

7. **Run it. Real Pico:** BOOTSEL, plug in, `cargo run --release`. Then,
   in the terminal:
   ```
   cat /dev/ttyACM0
   ```
   A line every half second, like `22.0 C  setpoint 24.0  fan off`.
   Put a warm finger on the black RP2040 chip (it's safe: 3.3 volts),
   and watch the temperature creep up, past the setpoint, until the
   fan turns ON. Take the finger away, and wait for it to cool, past
   the bottom of the deadband, to `off`. Ctrl+C stops `cat`. (The chip's
   thermometer isn't very accurate, so the room temperature it shows
   may be a few degrees out. That's fine: the setpoint is measured from
   it.)

   **Emulator:** the `fan` scenario does the finger for you: 23.5 °C at
   3 seconds, 25 at 6, 24 at 9, and 23 at 12.
   ```
   cargo build --release
   elf2uf2-rs target/thumbv6m-none-eabi/release/pico fan.uf2
   node ~/lab/pico/sim/pico-sim.mjs fan.uf2 13 fan
   ```
   **They should see**, among the lines (it takes a while):
   ```
   0.501 s  USB: 22.0 C  setpoint 24.0  fan off
   3.006 s  (finger on the chip: 23.5 degrees)
   3.504 s  USB: 23.4 C  setpoint 24.0  fan off
   6.011 s  (warmer: 25 degrees)
   6.507 s  LED on
   6.507 s  USB: 24.8 C  setpoint 24.0  fan ON
   9.002 s  (cooling: 24 degrees)
   9.010 s  USB: 23.9 C  setpoint 24.0  fan ON
   12.008 s  (cooler: 23 degrees)
   12.013 s  LED off
   12.014 s  USB: 22.9 C  setpoint 24.0  fan off
   ```
   **Ask:** "At 9 seconds it's 23.9, below the setpoint. Why is the fan
   still ON?" *(23.9 is inside the deadband: above 23.5. It stays as it
   was.)* "And why 23.4, not 23.5?" *(The ADC only counts in whole
   steps, so the number is rounded: about 0.4 degrees a step.)*

8. **Take the deadband away.** Change `BAND` to `0.0`, and run it again
   (in the emulator, add `| grep -v USB` to see only the LED). **They
   should see** the LED go off at `9.010 s`, as soon as it's 23.9.
   **Say:** "With a real thermometer, which wobbles up and down by a
   little all the time, a fan with no deadband would click on and off,
   on and off, around the setpoint. Every thermostat in the world has a
   deadband." Put `0.5` back. Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| ``error[E0599]: cannot write into `String<64>` `` | The `use core::fmt::Write;` line is missing | Add it at the top. |
| ``error[E0599]: no method named `read` found for struct `Adc` `` with a `help` suggesting `embedded_hal::adc::OneShot` | The `use embedded_hal_0_2::adc::OneShot;` line is missing (the ADC uses the older embedded-hal, renamed in `Cargo.toml`) | Add exactly `use embedded_hal_0_2::adc::OneShot;`. The `help` line's suggestion won't work. |
| ``error[E0425]: cannot find value `led` in this scope`` | Leftover lines from blink | Use `fan`, not `led`. |
| `cat: /dev/ttyACM0: Permission denied` | Not in the `dialout` group yet | The guide runs `sudo usermod -aG dialout LEARNER`; log out and in. |
| `cat: /dev/ttyACM0: No such file or directory` | The program isn't running yet, or the port has another number | Wait a few seconds; `ls /dev/ttyACM*`. |
| The LED works, but no lines ever arrive | The text doesn't fit in the `String` (if its size was changed), or the `usb.poll` line is missing | Keep `String<64>` and the `usb.poll` line. |
| The fan changes at the wrong temperatures | The `>` and `<`, or the `+` and `-`, are swapped | Check against the number line in step 3. |

## Talk about it

- What are the four stops of a control loop? Which line of code is
  each?
- What's a deadband for? What happens without one?
- How is the deadband like the seal-in?
- Why does the loop run every millisecond but report only twice a
  second?
- What's an ADC?

## Challenge *(if there's time, or for next time)*

- Make the LED blink fast when the temperature is more than 2 degrees
  over the setpoint: an **alarm**.
- Add the start and stop buttons from Lesson 13.6: the controller only
  runs after start, and stop turns the fan off.
- Instead of on and off, make the fan's speed depend on how hot it is
  with **PWM**, which switches the LED on and off so fast it looks dim.
  The `rp-pico` crate comes with an example, already on the computer:
  `less ~/.cargo/registry/src/*/rp-pico-0.9.0/examples/pico_pwm_blink.rs`.
- Use the `-s` option of `elf2uf2-rs` (change `runner` in
  `.cargo/config.toml` to `elf2uf2-rs -d -s`) so `cargo run` shows the
  serial lines by itself.

## Checkpoint

The learner can, without help:
- [ ] Draw and explain a control loop, with this program's lines
- [ ] Turn an ADC number into degrees with a calculator
- [ ] Explain the deadband, with the number line
- [ ] Run the fan controller and read its USB messages (or the
      emulator's)
- [ ] Show what happens with no deadband

## Lab notebook

Draw the control loop and the deadband number line. Copy the emulator's
lines from 6 to 12 seconds, and explain each. Add *sensor*, *setpoint*,
*deadband*, *ADC*, *control loop* and *serial* to `dictionary.md`.

## Guide's background *(optional reading)*

This is **on/off control with hysteresis**, the simplest closed-loop
control, used in thermostats, fridges, sump pumps and level switches.
The next step is **PID** control (proportional, integral, derivative),
which varies the output smoothly, usually with PWM to a fan or heater.
A PLC's PID block and this loop share the same structure: a fixed
sample rate, a measured variable, a setpoint, and an output. A 500 ms
sample period is slow for a motor but fine for temperature, which
changes slowly.

The RP2040's sensor formula (27 − (V − 0.706)/0.001721) comes from its
datasheet; Raspberry Pi notes the sensor is very sensitive to the
reference voltage, so expect an offset of a few degrees on a real board.
The ADC's resolution is 3.3 V / 4096 ≈ 0.8 mV, about 0.47 °C per count,
which is why the emulator shows 23.4 for 23.5. The USB VID:PID
16c0:27dd is the shared "CDC-ACM serial" test ID used by the rp-rs
examples; it's fine for hobby use but not for a product. The ADC in
`rp2040-hal` 0.10 still implements embedded-hal 0.2's `OneShot`, which
is why the kit's `Cargo.toml` pulls in both versions of `embedded-hal`.
