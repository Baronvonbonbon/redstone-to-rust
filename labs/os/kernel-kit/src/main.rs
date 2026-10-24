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
