// The Cookie Factory's seal-in rung, on a real chip.
// Start button: GP14 to ground. Stop button: GP15 to ground. The motor is the Pico's LED.
#![no_std]
#![no_main]

use embedded_hal::delay::DelayNs;
use embedded_hal::digital::{InputPin, OutputPin};
use panic_halt as _;
use rp_pico::entry;
use rp_pico::hal::{self, pac};

#[entry]
fn main() -> ! {
    let mut pac = pac::Peripherals::take().unwrap();
    let mut watchdog = hal::Watchdog::new(pac.WATCHDOG);
    let clocks = hal::clocks::init_clocks_and_plls(
        rp_pico::XOSC_CRYSTAL_FREQ,
        pac.XOSC,
        pac.CLOCKS,
        pac.PLL_SYS,
        pac.PLL_USB,
        &mut pac.RESETS,
        &mut watchdog,
    )
    .unwrap();
    let mut timer = hal::Timer::new(pac.TIMER, &mut pac.RESETS, &clocks);
    let sio = hal::Sio::new(pac.SIO);
    let pins = rp_pico::Pins::new(
        pac.IO_BANK0,
        pac.PADS_BANK0,
        sio.gpio_bank0,
        &mut pac.RESETS,
    );
    let mut start_button = pins.gpio14.into_pull_up_input();
    let mut stop_button = pins.gpio15.into_pull_up_input();
    let mut motor_light = pins.led.into_push_pull_output();
    let mut motor = false;

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
}
