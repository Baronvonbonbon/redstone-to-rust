#![no_std]
#![no_main]

mod keyboard;
mod screen;

use bootloader as _;
use core::fmt::Write;
use core::panic::PanicInfo;
use screen::{BLACK, GRAY, LIGHT_CYAN, LIGHT_GREEN, Pen, RED, WHITE, YELLOW, colour};

const WIDTH: i32 = 30;
const HEIGHT: i32 = 12;
/// How many clock cycles one tick lasts: about a twentieth of a second.
const TICK: u64 = 150_000_000;

#[derive(Clone, Copy, Debug, PartialEq)]
struct Spot {
    x: i32,
    y: i32,
}

struct Game {
    player: Spot,
    creeper: Spot,
    diamond: Spot,
    score: u32,
    ticks: u32,
    speed: u32,
    seed: u64,
}

impl Game {
    fn new(seed: u64) -> Game {
        let mut game = Game {
            player: Spot { x: 2, y: 2 },
            creeper: Spot {
                x: WIDTH - 3,
                y: HEIGHT - 3,
            },
            diamond: Spot { x: 0, y: 0 },
            score: 0,
            ticks: 0,
            speed: 12,
            seed,
        };
        game.new_diamond();
        game
    }

    fn move_player(&mut self, dx: i32, dy: i32) {
        let x = self.player.x + dx;
        let y = self.player.y + dy;
        if (0..WIDTH).contains(&x) && (0..HEIGHT).contains(&y) {
            self.player = Spot { x, y };
        }
    }

    fn move_creeper(&mut self) {
        let c = &mut self.creeper;
        if c.x < self.player.x {
            c.x += 1;
        } else if c.x > self.player.x {
            c.x -= 1;
        } else if c.y < self.player.y {
            c.y += 1;
        } else if c.y > self.player.y {
            c.y -= 1;
        }
    }

    /// A random number from 0 up to (but not including) `top`.
    fn random(&mut self, top: i32) -> i32 {
        self.seed = self
            .seed
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        ((self.seed >> 33) % top as u64) as i32
    }

    fn new_diamond(&mut self) {
        loop {
            let spot = Spot {
                x: self.random(WIDTH),
                y: self.random(HEIGHT),
            };
            if spot != self.player && spot != self.creeper {
                self.diamond = spot;
                return;
            }
        }
    }

    /// One tick of the game. Gives back true if the creeper caught the player.
    fn tick(&mut self) -> bool {
        if self.player == self.diamond {
            self.score += 1;
            if self.speed > 3 {
                self.speed -= 1;
            }
            self.new_diamond();
        }
        self.ticks += 1;
        if self.ticks >= self.speed {
            self.ticks = 0;
            self.move_creeper();
        }
        self.creeper == self.player
    }

    fn draw(&self) {
        let wall = colour(GRAY, BLACK);
        for y in -1..=HEIGHT {
            for x in -1..=WIDTH {
                if x == -1 || x == WIDTH || y == -1 || y == HEIGHT {
                    put(x, y, b'#', wall);
                } else {
                    put(x, y, b' ', wall);
                }
            }
        }
        let d = self.diamond;
        put(d.x, d.y, 4, colour(LIGHT_CYAN, BLACK));
        let p = self.player;
        put(p.x, p.y, 2, colour(YELLOW, BLACK));
        let c = self.creeper;
        put(c.x, c.y, b'C', colour(LIGHT_GREEN, BLACK));
        let mut pen = Pen::new(0, 15, colour(WHITE, BLACK));
        write!(pen, "Diamonds: {}   Arrows to move.", self.score).unwrap();
    }
}

/// How many clock cycles since the computer started.
fn now() -> u64 {
    unsafe { core::arch::x86_64::_rdtsc() }
}

/// Puts a character in the field, inside the wall.
fn put(x: i32, y: i32, character: u8, paint: u8) {
    screen::put((x + 1) as usize, (y + 1) as usize, character, paint);
}

/// Plays one game. Gives back the score.
fn play() -> u32 {
    let mut game = Game::new(now());
    let mut last_tick = now();
    let mut arrow = false;
    loop {
        if let Some(code) = keyboard::scancode() {
            if code == 0xe0 {
                arrow = true;
                continue;
            }
            if arrow {
                match code {
                    0x4b => game.move_player(-1, 0),
                    0x4d => game.move_player(1, 0),
                    0x48 => game.move_player(0, -1),
                    0x50 => game.move_player(0, 1),
                    _ => {}
                }
            }
            arrow = false;
        }
        if now() - last_tick >= TICK {
            last_tick = now();
            game.draw();
            if game.tick() {
                return game.score;
            }
        }
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn _start() -> ! {
    let mut best = 0;
    loop {
        screen::clear(colour(WHITE, BLACK));
        let score = play();
        if score > best {
            best = score;
        }
        let mut pen = Pen::new(0, 17, colour(WHITE, RED));
        writeln!(pen, "BOOM! You collected {score} diamonds.").unwrap();
        write!(pen, "Best: {best}. Press space to play again.").unwrap();
        while keyboard::scancode() != Some(0x39) {}
    }
}

#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    let red = colour(WHITE, RED);
    screen::clear(red);
    let mut pen = Pen::new(0, 0, red);
    let _ = write!(pen, "KERNEL PANIC! {info}");
    loop {
        unsafe { core::arch::asm!("hlt") };
    }
}
