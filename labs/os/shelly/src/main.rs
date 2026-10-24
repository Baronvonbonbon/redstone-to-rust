use std::env;
use std::fs::File;
use std::io::{self, Write};
use std::process::{Child, Command, Stdio};

/// Runs a line like `ls -l | grep txt > list.txt`.
fn run_line(line: &str) -> io::Result<()> {
    let stages: Vec<&str> = line.split('|').collect();
    let mut children: Vec<Child> = Vec::new();
    for (i, stage) in stages.iter().enumerate() {
        let (stage, out_file) = match stage.split_once('>') {
            Some((command, file)) => (command, Some(file.trim())),
            None => (*stage, None),
        };
        let words: Vec<&str> = stage.split_whitespace().collect();
        let Some((&program, args)) = words.split_first() else {
            return Err(io::Error::other("a | with nothing next to it"));
        };

        let mut command = Command::new(program);
        command.args(args);
        if let Some(previous) = children.last_mut() {
            command.stdin(previous.stdout.take().unwrap());
        }
        if let Some(name) = out_file {
            match File::create(name) {
                Ok(file) => command.stdout(file),
                Err(error) => return Err(io::Error::other(format!("{name}: {error}"))),
            };
        } else if i < stages.len() - 1 {
            command.stdout(Stdio::piped());
        }
        match command.spawn() {
            Ok(child) => children.push(child),
            Err(error) if error.kind() == io::ErrorKind::NotFound => {
                return Err(io::Error::other(format!("{program}: command not found")));
            }
            Err(error) => return Err(error),
        }
    }
    for mut child in children {
        child.wait()?;
    }
    Ok(())
}

fn main() {
    loop {
        let here = env::current_dir().unwrap();
        print!("shelly:{}> ", here.display());
        io::stdout().flush().unwrap();

        let mut line = String::new();
        if io::stdin().read_line(&mut line).unwrap() == 0 {
            println!();
            return;
        }
        let words: Vec<&str> = line.split_whitespace().collect();
        let Some((&program, args)) = words.split_first() else {
            continue;
        };

        match program {
            "exit" => return,
            "cd" => {
                let home = env::var("HOME").unwrap();
                let place = args.first().copied().unwrap_or(&home);
                if let Err(error) = env::set_current_dir(place) {
                    eprintln!("shelly: cd: {place}: {error}");
                }
            }
            _ => {
                if let Err(error) = run_line(&line) {
                    eprintln!("shelly: {error}");
                }
            }
        }
    }
}
