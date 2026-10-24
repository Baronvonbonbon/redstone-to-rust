// The parser turns tokens into a tree: expressions and statements.
use crate::scanner::Token;

#[derive(Debug, Clone)]
pub enum Expr {
    Number(i64),
    Text(String),
    Bool(bool),
    Name(String),
    Unary(String, Box<Expr>),
    Binary(Box<Expr>, String, Box<Expr>),
    Call(String, Vec<Expr>),
}

#[derive(Debug, Clone)]
pub enum Stmt {
    Say(Expr),
    Let(String, Expr),
    Set(String, Expr),
    Block(Vec<Stmt>),
    If(Expr, Vec<Stmt>, Vec<Stmt>),
    While(Expr, Vec<Stmt>),
    Fun(String, Vec<String>, Vec<Stmt>),
    Return(Expr),
    Run(Expr),
}

pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Parser {
        Parser { tokens, pos: 0 }
    }

    fn peek(&self) -> Option<&Token> {
        self.tokens.get(self.pos)
    }

    fn next(&mut self) -> Option<Token> {
        let token = self.tokens.get(self.pos).cloned();
        self.pos += 1;
        token
    }

    // Is the next token this symbol or word?
    fn looking_at(&self, wanted: &str) -> bool {
        match self.peek() {
            Some(Token::Symbol(s)) | Some(Token::Word(s)) => s == wanted,
            _ => false,
        }
    }

    // If the next token is this symbol or word, use it up.
    fn is(&mut self, wanted: &str) -> bool {
        let found = self.looking_at(wanted);
        if found {
            self.pos += 1;
        }
        found
    }

    // If the next token is one of these, use it up and say which.
    fn either(&mut self, choices: &[&str]) -> Option<String> {
        for choice in choices {
            if self.is(choice) {
                return Some(choice.to_string());
            }
        }
        None
    }

    fn expect(&mut self, wanted: &str) -> Result<(), String> {
        if self.is(wanted) {
            Ok(())
        } else {
            Err(format!("I expected {wanted} but found {}", self.describe()))
        }
    }

    fn describe(&self) -> String {
        match self.peek() {
            Some(Token::Number(n)) => n.to_string(),
            Some(Token::Text(t)) => format!("\"{t}\""),
            Some(Token::Word(w)) | Some(Token::Symbol(w)) => w.clone(),
            None => "the end".to_string(),
        }
    }

    fn name(&mut self) -> Result<String, String> {
        match self.next() {
            Some(Token::Word(w)) => Ok(w),
            _ => {
                self.pos -= 1;
                Err(format!("I expected a name but found {}", self.describe()))
            }
        }
    }

    pub fn at_end(&self) -> bool {
        self.pos >= self.tokens.len()
    }

    // program = statement*
    pub fn program(&mut self) -> Result<Vec<Stmt>, String> {
        let mut statements = Vec::new();
        while !self.at_end() {
            statements.push(self.statement()?);
        }
        Ok(statements)
    }

    fn block(&mut self) -> Result<Vec<Stmt>, String> {
        self.expect("{")?;
        let mut statements = Vec::new();
        while !self.is("}") {
            if self.at_end() {
                return Err("a block is missing its }".to_string());
            }
            statements.push(self.statement()?);
        }
        Ok(statements)
    }

    fn statement(&mut self) -> Result<Stmt, String> {
        if self.is("say") {
            let value = self.expression()?;
            self.expect(";")?;
            Ok(Stmt::Say(value))
        } else if self.is("let") {
            let name = self.name()?;
            self.expect("=")?;
            let value = self.expression()?;
            self.expect(";")?;
            Ok(Stmt::Let(name, value))
        } else if self.is("if") {
            let test = self.expression()?;
            let yes = self.block()?;
            let no = if self.is("else") {
                if self.looking_at("if") {
                    vec![self.statement()?]
                } else {
                    self.block()?
                }
            } else {
                Vec::new()
            };
            Ok(Stmt::If(test, yes, no))
        } else if self.is("while") {
            let test = self.expression()?;
            let body = self.block()?;
            Ok(Stmt::While(test, body))
        } else if self.is("fun") {
            let name = self.name()?;
            self.expect("(")?;
            let mut params = Vec::new();
            if !self.is(")") {
                loop {
                    params.push(self.name()?);
                    if self.is(")") {
                        break;
                    }
                    self.expect(",")?;
                }
            }
            let body = self.block()?;
            Ok(Stmt::Fun(name, params, body))
        } else if self.is("return") {
            let value = self.expression()?;
            self.expect(";")?;
            Ok(Stmt::Return(value))
        } else if self.looking_at("{") {
            Ok(Stmt::Block(self.block()?))
        } else {
            let value = self.expression()?;
            if self.is("=") {
                let Expr::Name(name) = value else {
                    return Err("only a name can go before =".to_string());
                };
                let new_value = self.expression()?;
                self.expect(";")?;
                return Ok(Stmt::Set(name, new_value));
            }
            self.expect(";")?;
            Ok(Stmt::Run(value))
        }
    }

    // expression = or
    fn expression(&mut self) -> Result<Expr, String> {
        self.or()
    }

    fn or(&mut self) -> Result<Expr, String> {
        let mut left = self.and()?;
        while let Some(op) = self.either(&["or"]) {
            let right = self.and()?;
            left = Expr::Binary(Box::new(left), op, Box::new(right));
        }
        Ok(left)
    }

    fn and(&mut self) -> Result<Expr, String> {
        let mut left = self.equality()?;
        while let Some(op) = self.either(&["and"]) {
            let right = self.equality()?;
            left = Expr::Binary(Box::new(left), op, Box::new(right));
        }
        Ok(left)
    }

    fn equality(&mut self) -> Result<Expr, String> {
        let mut left = self.comparison()?;
        while let Some(op) = self.either(&["==", "!="]) {
            let right = self.comparison()?;
            left = Expr::Binary(Box::new(left), op, Box::new(right));
        }
        Ok(left)
    }

    fn comparison(&mut self) -> Result<Expr, String> {
        let mut left = self.term()?;
        while let Some(op) = self.either(&["<", "<=", ">", ">="]) {
            let right = self.term()?;
            left = Expr::Binary(Box::new(left), op, Box::new(right));
        }
        Ok(left)
    }

    fn term(&mut self) -> Result<Expr, String> {
        let mut left = self.factor()?;
        while let Some(op) = self.either(&["+", "-"]) {
            let right = self.factor()?;
            left = Expr::Binary(Box::new(left), op, Box::new(right));
        }
        Ok(left)
    }

    fn factor(&mut self) -> Result<Expr, String> {
        let mut left = self.unary()?;
        while let Some(op) = self.either(&["*", "/", "%"]) {
            let right = self.unary()?;
            left = Expr::Binary(Box::new(left), op, Box::new(right));
        }
        Ok(left)
    }

    fn unary(&mut self) -> Result<Expr, String> {
        if let Some(op) = self.either(&["-", "!"]) {
            let inside = self.unary()?;
            return Ok(Expr::Unary(op, Box::new(inside)));
        }
        self.primary()
    }

    fn primary(&mut self) -> Result<Expr, String> {
        match self.next() {
            Some(Token::Number(n)) => Ok(Expr::Number(n)),
            Some(Token::Text(t)) => Ok(Expr::Text(t)),
            Some(Token::Word(w)) if w == "true" => Ok(Expr::Bool(true)),
            Some(Token::Word(w)) if w == "false" => Ok(Expr::Bool(false)),
            Some(Token::Word(w)) => {
                if self.is("(") {
                    let mut args = Vec::new();
                    if !self.is(")") {
                        loop {
                            args.push(self.expression()?);
                            if self.is(")") {
                                break;
                            }
                            self.expect(",")?;
                        }
                    }
                    Ok(Expr::Call(w, args))
                } else {
                    Ok(Expr::Name(w))
                }
            }
            Some(Token::Symbol(s)) if s == "(" => {
                let inside = self.expression()?;
                self.expect(")")?;
                Ok(inside)
            }
            _ => {
                self.pos -= 1;
                Err(format!("I expected a value but found {}", self.describe()))
            }
        }
    }
}
