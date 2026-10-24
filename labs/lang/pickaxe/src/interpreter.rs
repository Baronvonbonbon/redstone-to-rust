// The interpreter walks the tree and does what it says.
use crate::parser::{Expr, Stmt};
use std::collections::HashMap;
use std::fmt;

// How deep functions may call each other, before Pickaxe gives up.
const LIMIT: usize = 200;

#[derive(Debug, Clone, PartialEq)]
pub enum Value {
    Number(i64),
    Text(String),
    Bool(bool),
    Nothing,
}

impl fmt::Display for Value {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Value::Number(n) => write!(f, "{n}"),
            Value::Text(t) => write!(f, "{t}"),
            Value::Bool(b) => write!(f, "{b}"),
            Value::Nothing => write!(f, "nothing"),
        }
    }
}

pub struct Interpreter {
    // The first box holds the globals; each block adds a box on top.
    scopes: Vec<HashMap<String, Value>>,
    functions: HashMap<String, (Vec<String>, Vec<Stmt>)>,
    depth: usize,
}

impl Interpreter {
    pub fn new() -> Interpreter {
        Interpreter {
            scopes: vec![HashMap::new()],
            functions: HashMap::new(),
            depth: 0,
        }
    }

    pub fn run(&mut self, program: &[Stmt]) -> Result<(), String> {
        for statement in program {
            if self.exec(statement)?.is_some() {
                return Err("return can only be used inside a fun".to_string());
            }
        }
        Ok(())
    }

    // Some(value) means "return this value from the function now".
    fn exec(&mut self, statement: &Stmt) -> Result<Option<Value>, String> {
        match statement {
            Stmt::Say(value) => {
                println!("{}", self.eval(value)?);
            }
            Stmt::Let(name, value) => {
                let value = self.eval(value)?;
                self.scopes.last_mut().unwrap().insert(name.clone(), value);
            }
            Stmt::Set(name, value) => {
                let value = self.eval(value)?;
                for scope in self.scopes.iter_mut().rev() {
                    if let Some(old) = scope.get_mut(name) {
                        *old = value;
                        return Ok(None);
                    }
                }
                return Err(format!("there's no {name} yet: use let first"));
            }
            Stmt::Block(body) => return self.block(body),
            Stmt::If(test, yes, no) => {
                if self.test(test)? {
                    return self.block(yes);
                } else {
                    return self.block(no);
                }
            }
            Stmt::While(test, body) => {
                while self.test(test)? {
                    if let Some(value) = self.block(body)? {
                        return Ok(Some(value));
                    }
                }
            }
            Stmt::Fun(name, params, body) => {
                self.functions
                    .insert(name.clone(), (params.clone(), body.clone()));
            }
            Stmt::Return(value) => return Ok(Some(self.eval(value)?)),
            Stmt::Run(value) => {
                self.eval(value)?;
            }
        }
        Ok(None)
    }

    fn block(&mut self, body: &[Stmt]) -> Result<Option<Value>, String> {
        self.scopes.push(HashMap::new());
        let mut result = Ok(None);
        for statement in body {
            result = self.exec(statement);
            if !matches!(result, Ok(None)) {
                break;
            }
        }
        self.scopes.pop();
        result
    }

    fn test(&mut self, test: &Expr) -> Result<bool, String> {
        match self.eval(test)? {
            Value::Bool(b) => Ok(b),
            other => Err(format!("if and while need true or false, not {other}")),
        }
    }

    fn eval(&mut self, expr: &Expr) -> Result<Value, String> {
        match expr {
            Expr::Number(n) => Ok(Value::Number(*n)),
            Expr::Text(t) => Ok(Value::Text(t.clone())),
            Expr::Bool(b) => Ok(Value::Bool(*b)),
            Expr::Name(name) => {
                for scope in self.scopes.iter().rev() {
                    if let Some(value) = scope.get(name) {
                        return Ok(value.clone());
                    }
                }
                Err(format!("I don't know what {name} is"))
            }
            Expr::Unary(op, inside) => match (op.as_str(), self.eval(inside)?) {
                ("-", Value::Number(n)) => Ok(Value::Number(-n)),
                ("!", Value::Bool(b)) => Ok(Value::Bool(!b)),
                (op, value) => Err(format!("I can't do {op} to {value}")),
            },
            Expr::Binary(left, op, right) => {
                if op == "and" || op == "or" {
                    return self.logic(left, op, right);
                }
                let left = self.eval(left)?;
                let right = self.eval(right)?;
                binary(left, op, right)
            }
            Expr::Call(name, args) => self.call(name, args),
        }
    }

    // and, or: only look at the right side if we need to.
    fn logic(&mut self, left: &Expr, op: &str, right: &Expr) -> Result<Value, String> {
        let left = self.test(left)?;
        if op == "and" && !left {
            return Ok(Value::Bool(false));
        }
        if op == "or" && left {
            return Ok(Value::Bool(true));
        }
        Ok(Value::Bool(self.test(right)?))
    }

    fn call(&mut self, name: &str, args: &[Expr]) -> Result<Value, String> {
        let Some((params, body)) = self.functions.get(name).cloned() else {
            return Err(format!("there's no fun called {name}"));
        };
        if args.len() != params.len() {
            return Err(format!(
                "{name} needs {} values, but got {}",
                params.len(),
                args.len()
            ));
        }
        let mut locals = HashMap::new();
        for (param, arg) in params.iter().zip(args) {
            locals.insert(param.clone(), self.eval(arg)?);
        }
        if self.depth == LIMIT {
            return Err(format!("{name} went more than {LIMIT} calls deep"));
        }
        // The function sees the globals and its own locals, not the caller's.
        let callers = self.scopes.split_off(1);
        self.scopes.push(locals);
        self.depth += 1;
        let result = self.block(&body);
        self.depth -= 1;
        self.scopes.truncate(1);
        self.scopes.extend(callers);
        Ok(result?.unwrap_or(Value::Nothing))
    }
}

fn binary(left: Value, op: &str, right: Value) -> Result<Value, String> {
    use Value::{Bool, Number, Text};
    let too_big = || "that number is too big for Pickaxe".to_string();
    match (left, op, right) {
        (Number(a), "+", Number(b)) => a.checked_add(b).map(Number).ok_or_else(too_big),
        (Number(a), "-", Number(b)) => a.checked_sub(b).map(Number).ok_or_else(too_big),
        (Number(a), "*", Number(b)) => a.checked_mul(b).map(Number).ok_or_else(too_big),
        (Number(_), "/" | "%", Number(0)) => Err("you can't divide by zero".to_string()),
        (Number(a), "/", Number(b)) => Ok(Number(a / b)),
        (Number(a), "%", Number(b)) => Ok(Number(a % b)),
        (Number(a), "<", Number(b)) => Ok(Bool(a < b)),
        (Number(a), "<=", Number(b)) => Ok(Bool(a <= b)),
        (Number(a), ">", Number(b)) => Ok(Bool(a > b)),
        (Number(a), ">=", Number(b)) => Ok(Bool(a >= b)),
        (Text(a), "+", b) => Ok(Text(format!("{a}{b}"))),
        (a, "+", Text(b)) => Ok(Text(format!("{a}{b}"))),
        (a, "==", b) => Ok(Bool(a == b)),
        (a, "!=", b) => Ok(Bool(a != b)),
        (a, op, b) => Err(format!("I can't do {a} {op} {b}")),
    }
}
