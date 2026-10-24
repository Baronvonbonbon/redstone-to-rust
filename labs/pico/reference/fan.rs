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
    let mut fan = pins.led.into_push_pull_output();

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
