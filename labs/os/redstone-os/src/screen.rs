//! The VGA text screen: 80 columns and 25 rows of coloured characters.

#![allow(dead_code)]

use core::fmt;
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
