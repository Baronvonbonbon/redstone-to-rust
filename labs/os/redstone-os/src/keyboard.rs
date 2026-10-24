//! The keyboard, read from the PS/2 controller's ports.

#![allow(dead_code)]

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
