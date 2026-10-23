use std::fs;
use std::io::{self, Write};
use std::time::Duration;

use crossterm::event::{self, Event, KeyCode, KeyEventKind};
use crossterm::style::Stylize;
use crossterm::{cursor, execute, queue, style, terminal};
use rand::RngExt;
use serde::{Deserialize, Serialize};

const WIDTH: i32 = 30;
const HEIGHT: i32 = 12;

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
}

impl Game {
    fn new() -> Game {
        let mut game = Game {
            player: Spot { x: 2, y: 2 },
            creeper: Spot { x: WIDTH - 3, y: HEIGHT - 3 },
            diamond: Spot { x: 0, y: 0 },
            score: 0,
            ticks: 0,
            speed: 12,
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

    fn new_diamond(&mut self) {
        let mut rng = rand::rng();
        loop {
            let spot = Spot {
                x: rng.random_range(0..WIDTH),
                y: rng.random_range(0..HEIGHT),
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

    fn draw(&self, out: &mut impl Write) -> io::Result<()> {
        queue!(out, terminal::Clear(terminal::ClearType::All))?;
        for y in -1..=HEIGHT {
            for x in -1..=WIDTH {
                if x == -1 || x == WIDTH || y == -1 || y == HEIGHT {
                    queue!(out, cursor::MoveTo((x + 1) as u16, (y + 1) as u16), style::Print("#"))?;
                }
            }
        }
        let d = self.diamond;
        queue!(out, cursor::MoveTo((d.x + 1) as u16, (d.y + 1) as u16), style::PrintStyledContent("*".cyan()))?;
        let p = self.player;
        queue!(out, cursor::MoveTo((p.x + 1) as u16, (p.y + 1) as u16), style::PrintStyledContent("@".yellow()))?;
        let c = self.creeper;
        queue!(out, cursor::MoveTo((c.x + 1) as u16, (c.y + 1) as u16), style::PrintStyledContent("C".green()))?;
        queue!(out, cursor::MoveTo(0, (HEIGHT + 3) as u16), style::Print(format!("Diamonds: {}   Arrows to move, q to quit.", self.score)))?;
        out.flush()
    }
}

/// Waits up to 50 milliseconds for a key. Gives back the key, or None.
fn read_key() -> io::Result<Option<KeyCode>> {
    if !event::poll(Duration::from_millis(50))? {
        return Ok(None);
    }
    match event::read()? {
        Event::Key(key) if key.kind == KeyEventKind::Press => Ok(Some(key.code)),
        _ => Ok(None),
    }
}

fn play(out: &mut impl Write) -> io::Result<u32> {
    let mut game = Game::new();
    loop {
        game.draw(out)?;
        match read_key()? {
            Some(KeyCode::Left) => game.move_player(-1, 0),
            Some(KeyCode::Right) => game.move_player(1, 0),
            Some(KeyCode::Up) => game.move_player(0, -1),
            Some(KeyCode::Down) => game.move_player(0, 1),
            Some(KeyCode::Char('q')) => return Ok(game.score),
            _ => {}
        }
        if game.tick() {
            return Ok(game.score);
        }
    }
}

#[derive(Serialize, Deserialize, Default)]
struct Scores {
    best: u32,
    games: u32,
}

fn load_scores() -> Scores {
    match fs::read_to_string("scores.json") {
        Ok(text) => serde_json::from_str(&text).unwrap_or_default(),
        Err(_) => Scores::default(),
    }
}

fn save_scores(scores: &Scores) -> io::Result<()> {
    let text = serde_json::to_string_pretty(scores)?;
    fs::write("scores.json", text)
}

fn main() -> io::Result<()> {
    let mut out = io::stdout();
    terminal::enable_raw_mode()?;
    execute!(out, terminal::EnterAlternateScreen, cursor::Hide)?;
    let result = play(&mut out);
    execute!(out, cursor::Show, terminal::LeaveAlternateScreen)?;
    terminal::disable_raw_mode()?;
    let score = result?;

    let mut scores = load_scores();
    scores.games += 1;
    println!("BOOM! You collected {score} diamonds.");
    if score > scores.best {
        scores.best = score;
        println!("That's a new best!");
    }
    println!("Best: {}. Games played: {}.", scores.best, scores.games);
    save_scores(&scores)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn creeper_walks_across_first() {
        let mut game = Game::new();
        game.player = Spot { x: 2, y: 2 };
        game.creeper = Spot { x: 5, y: 7 };
        game.move_creeper();
        assert_eq!(game.creeper, Spot { x: 4, y: 7 });
    }

    #[test]
    fn player_stays_in_the_field() {
        let mut game = Game::new();
        game.player = Spot { x: 0, y: 0 };
        game.move_player(-1, 0);
        assert_eq!(game.player, Spot { x: 0, y: 0 });
    }

    #[test]
    fn a_diamond_scores_a_point() {
        let mut game = Game::new();
        game.diamond = game.player;
        let caught = game.tick();
        assert_eq!(game.score, 1);
        assert!(!caught);
        assert_ne!(game.diamond, game.player);
    }
}
