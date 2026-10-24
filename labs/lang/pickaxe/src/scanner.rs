// The scanner turns the program's letters into tokens: the "words" of Pickaxe.

#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    Number(i64),
    Text(String),
    Word(String),
    Symbol(String),
}

pub fn scan(source: &str) -> Result<Vec<Token>, String> {
    let mut tokens = Vec::new();
    let mut chars = source.chars().peekable();
    while let Some(&c) = chars.peek() {
        if c.is_whitespace() {
            chars.next();
        } else if c == '#' {
            // A comment: skip to the end of the line.
            for c in chars.by_ref() {
                if c == '\n' {
                    break;
                }
            }
        } else if c.is_ascii_digit() {
            let mut digits = String::new();
            while let Some(&d) = chars.peek() {
                if !d.is_ascii_digit() {
                    break;
                }
                digits.push(d);
                chars.next();
            }
            let Ok(number) = digits.parse() else {
                return Err(format!("{digits} is too big for Pickaxe"));
            };
            tokens.push(Token::Number(number));
        } else if c.is_alphabetic() || c == '_' {
            let mut word = String::new();
            while let Some(&d) = chars.peek() {
                if !d.is_alphanumeric() && d != '_' {
                    break;
                }
                word.push(d);
                chars.next();
            }
            tokens.push(Token::Word(word));
        } else if c == '"' {
            chars.next();
            let mut text = String::new();
            loop {
                match chars.next() {
                    Some('"') => break,
                    Some(d) => text.push(d),
                    None => return Err("a text is missing its closing \"".to_string()),
                }
            }
            tokens.push(Token::Text(text));
        } else if "+-*/%(){};,".contains(c) {
            chars.next();
            tokens.push(Token::Symbol(c.to_string()));
        } else if "=!<>".contains(c) {
            chars.next();
            if chars.peek() == Some(&'=') {
                chars.next();
                tokens.push(Token::Symbol(format!("{c}=")));
            } else {
                tokens.push(Token::Symbol(c.to_string()));
            }
        } else {
            return Err(format!("I don't know what {c} means"));
        }
    }
    Ok(tokens)
}
