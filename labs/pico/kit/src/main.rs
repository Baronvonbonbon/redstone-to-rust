// Blink the Pico's own LED, for ever.
#![no_std]
#![no_main]

use embedded_hal::delay::DelayNs;
use embedded_hal::digital::OutputPin;
use panic_halt as _;
use rp_pico::entry;
use rp_pico::hal::{self, pac};

#[entry]
fn main() -> ! {
    // Take charge of the chip's hardware. There's only one of each!
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
    let mut led = pins.led.into_push_pull_output();

    loop {
        led.set_high().unwrap();
        timer.delay_ms(500);
        led.set_low().unwrap();
        timer.delay_ms(500);
    }
}
