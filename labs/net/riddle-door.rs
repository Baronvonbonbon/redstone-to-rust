use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

const RIDDLE: &str = "What has keys but can't open locks?";
const ANSWER: &str = "piano";
const NEXT_CLUE: &str = "Well done! The next clue is inside the biggest book on the shelf.";

fn visit(mut stream: TcpStream) -> std::io::Result<()> {
    writeln!(stream, "{RIDDLE}")?;
    let reader = BufReader::new(stream.try_clone()?);
    for line in reader.lines() {
        let Ok(line) = line else { break };
        if line.trim().eq_ignore_ascii_case(ANSWER) {
            writeln!(stream, "{NEXT_CLUE}")?;
            return Ok(());
        }
        writeln!(stream, "Not quite. Try again!")?;
    }
    Ok(())
}

fn main() {
    let listener = TcpListener::bind("127.0.0.1:4242").unwrap();
    println!("The riddle door is on port 4242");
    for stream in listener.incoming() {
        let Ok(stream) = stream else { continue };
        thread::spawn(move || {
            let _ = visit(stream);
        });
    }
}
