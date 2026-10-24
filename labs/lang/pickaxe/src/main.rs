mod interpreter;
mod parser;
mod scanner;

use interpreter::Interpreter;
use parser::Parser;
use std::io::{self, BufRead, Write};
use std::{env, fs, process};

fn run(source: &str, interpreter: &mut Interpreter) -> Result<(), String> {
    let tokens = scanner::scan(source)?;
    let program = Parser::new(tokens).program()?;
    interpreter.run(&program)
}

fn main() {
    let mut interpreter = Interpreter::new();
    let args: Vec<String> = env::args().collect();
    if let Some(file) = args.get(1) {
        let Ok(source) = fs::read_to_string(file) else {
            eprintln!("I can't read {file}");
            process::exit(1);
        };
        if let Err(problem) = run(&source, &mut interpreter) {
            eprintln!("Oops: {problem}");
            process::exit(1);
        }
        return;
    }
    // No file: a prompt, one line at a time.
    print!("pickaxe> ");
    io::stdout().flush().unwrap();
    for line in io::stdin().lock().lines() {
        let Ok(line) = line else { break };
        if let Err(problem) = run(&line, &mut interpreter) {
            println!("Oops: {problem}");
        }
        print!("pickaxe> ");
        io::stdout().flush().unwrap();
    }
    println!();
}
