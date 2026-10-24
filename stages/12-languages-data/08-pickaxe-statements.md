# Lesson 12.8: Pickaxe, Part 4: Statements, Variables and Scope

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/lang/pickaxe`; paper; a few boxes or envelopes, and
sticky notes · **New words:** statement, variable, declare, assign,
scope, block, global, shadowing

## Goal *(read this to the learner)*

> So far Pickaxe answers one sum at a time and forgets everything. A
> real language remembers things. Today Pickaxe learns statements:
> `say` to print, `let` to make a variable, `=` to change it, and
> `{ }` blocks with their own private variables. Then it can run whole
> programs from files.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] `check-pickaxe 12.7` passes.
- [ ] Two boxes for step 2: a big one labelled **globals**, and a smaller
      one labelled **block**. Sticky notes for variables.

## Warm-up (5 min)

"What's the difference between an expression and a statement?" Guess.
**Say:** "An expression works out a value, like `1 + 2`. A statement
*does* something, like printing or remembering. In Rust, `let x = 5;`
is a statement, and `x + 1` is an expression."

## Activity

### Session 1: boxes of variables

1. **New grammar.** On paper, add statements to the grammar:
   ```
   program   → statement*
   statement → say expression ;
             | let NAME = expression ;
             | NAME = expression ;
             | { statement* }
             | expression ;
   ```
   **Say:** "A program is a list of statements. A block is a list of
   statements in curly brackets."

2. **Act out scope.** The **globals** box is on the table. Act out this
   program, line by line, with sticky notes for variables:
   ```
   let diamonds = 3;              # a sticky note "diamonds 3" in globals
   diamonds = diamonds + 5;       # find it, change it to 8
   {                              # put the block box on top
       let diamonds = 100;        # a NEW note in the block box
       say diamonds;              # look in the top box first: 100
   }                              # take the block box away, notes and all
   say diamonds;                  # 8: the global one was never touched
   ```
   **Say:** "`let` always puts a new note in the *top* box. `=` and
   looking up a name search from the top box down, and use the first
   one found. Where a variable can be seen is called its **scope**. A
   block's variable with the same name as an outer one hides it: that's
   called **shadowing**. When the block ends, its box is thrown away."
   **Ask:** "What if the block said `diamonds = 100;` with no `let`?"
   *(It would find the global one and change it to 100.)*

### Session 2: statements in the parser

3. **The statement tree.** In `src/parser.rs`, change the comment at the
   top to `// The parser turns tokens into a tree: expressions and
   statements.` and add, below `Expr`:
   ```rust
   #[derive(Debug, Clone)]
   pub enum Stmt {
       Say(Expr),
       Let(String, Expr),
       Set(String, Expr),
       Block(Vec<Stmt>),
       Run(Expr),
   }
   ```
   **Say:** "`Run` is an expression on its own, like `1 + 2;`. It's
   worked out and the answer thrown away. Later, it will run functions."

4. **The statement functions.** In `impl Parser`, after `describe`, add:
   ```rust
       fn name(&mut self) -> Result<String, String> {
           match self.next() {
               Some(Token::Word(w)) => Ok(w),
               _ => {
                   self.pos -= 1;
                   Err(format!("I expected a name but found {}", self.describe()))
               }
           }
       }
   ```
   and, after `at_end`, add:
   ```rust
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
   ```
   Finally, change `pub fn expression` to just `fn expression` (only the
   parser uses it now). Read `statement` with the grammar from step 1:
   **Say:** "The first word decides which kind of statement it is. If it
   isn't `say`, `let` or `{`, it must start with an expression. If an `=`
   comes next, the expression had better be a plain name, like
   `diamonds`: you can't do `3 = 4`."

### Session 3: the interpreter remembers

5. **A struct with boxes.** In `src/interpreter.rs`, change the top to:
   ```rust
   // The interpreter walks the tree and does what it says.
   use crate::parser::{Expr, Stmt};
   use std::collections::HashMap;
   use std::fmt;
   ```
   Keep `Value`, `Display` and `binary` as they are. **Replace** the
   `eval` function with this whole struct:
   ```rust
   pub struct Interpreter {
       // The first box holds the globals; each block adds a box on top.
       scopes: Vec<HashMap<String, Value>>,
   }

   impl Interpreter {
       pub fn new() -> Interpreter {
           Interpreter {
               scopes: vec![HashMap::new()],
           }
       }

       pub fn run(&mut self, program: &[Stmt]) -> Result<(), String> {
           for statement in program {
               self.exec(statement)?;
           }
           Ok(())
       }

       fn exec(&mut self, statement: &Stmt) -> Result<(), String> {
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
                           return Ok(());
                       }
                   }
                   return Err(format!("there's no {name} yet: use let first"));
               }
               Stmt::Block(body) => return self.block(body),
               Stmt::Run(value) => {
                   self.eval(value)?;
               }
           }
           Ok(())
       }

       fn block(&mut self, body: &[Stmt]) -> Result<(), String> {
           self.scopes.push(HashMap::new());
           let mut result = Ok(());
           for statement in body {
               result = self.exec(statement);
               if result.is_err() {
                   break;
               }
           }
           self.scopes.pop();
           result
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
                   let left = self.eval(left)?;
                   let right = self.eval(right)?;
                   binary(left, op, right)
               }
           }
       }
   }
   ```
   Match the code to the boxes:
   - "`scopes` is the pile of boxes: a `Vec` of `HashMap`s. The first is
     the globals."
   - "`Let` puts a note in the top box: `last_mut()`."
   - "`Set` and looking up a `Name` search from the top down: `.rev()`."
   - "`block` puts a new box on top, runs the statements, then takes the
     box away, even if there was an error. That's why it doesn't use `?`
     inside the loop: the box must always come off."
   - "`eval` is the same as before, but it's a method now, because it
     needs the boxes to look up names."

6. **Programs and the prompt.** Replace `src/main.rs`:
   ```rust
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
   ```
   **Say:** "With a file name, Pickaxe runs the file. Without one, it's a
   prompt, and the *same* interpreter is kept for every line, so it
   remembers your variables."

7. **Run programs.** `cargo run -- hello.pick` (from Lesson 12.5). **They
   should see:** `I have 3 diamonds!` Make `diamonds.pick`:
   ```
   # Diamonds and a chest
   let diamonds = 3;
   say "Start: " + diamonds;
   diamonds = diamonds + 5;
   say "After mining: " + diamonds;
   {
       let diamonds = 100;
       say "Inside the chest: " + diamonds;
   }
   say "Back outside: " + diamonds;
   ```
   **Ask:** "What will it print?" Write the guess, then `cargo run --
   diamonds.pick`. **They should see:**
   ```
   Start: 3
   After mining: 8
   Inside the chest: 100
   Back outside: 8
   ```
   That's step 2's act-out, run by the learner's own language.

8. **The prompt remembers.** `cargo run`:
   ```
   pickaxe> let x = 4;
   pickaxe> say x * x;
   16
   pickaxe> say y;
   Oops: I don't know what y is
   pickaxe> z = 1;
   Oops: there's no z yet: use let first
   pickaxe> say 1
   Oops: I expected ; but found the end
   pickaxe> { let inside = 1; }
   pickaxe> say inside;
   Oops: I don't know what inside is
   ```
   **Ask:** "Why doesn't Pickaxe know `inside`?" *(Its box was thrown away
   at the `}`.)* Then `~/lab/lang/check-pickaxe 12.8`: **they should
   see** four `PASS` lines and `4 passed, 0 failed.` `cargo fmt`, `cargo
   clippy`, commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| ``error[E0004]: non-exhaustive patterns: `&Stmt::Run(_)` not covered`` | `exec` is missing a kind of statement | Add its arm to the `match` in `exec`. |
| ``error[E0425]: cannot find function `eval` in module `interpreter` `` | `main.rs` is still the old one from Lesson 12.7 | Replace `main.rs` with step 6's. |
| ``error[E0624]: method `expression` is private`` | `main.rs` still calls `parser.expression()` | Use step 6's `main.rs`, which calls `program()`. |
| `Back outside: 100` | The block's `let` is going into the globals | `Let` must use `self.scopes.last_mut()`, and `block` must `push` a new box. |
| Every variable is forgotten at the prompt | A new `Interpreter` is made for each line | Make it once, before the loop, as step 6 does. |
| `Oops: I expected ; but found say` | The line before is missing its `;` | Add the `;`. |

## Talk about it

- What's the difference between a statement and an expression?
- What's the difference between `let` and `=`?
- What's a scope? What happens to a block's variables at its `}`?
- Why does `block` take its box away even when there's an error?

## Challenge *(if there's time, or for next time)*

- Add a `forget NAME;` statement that removes a variable.
- Make `let` complain if the variable already exists in the *same* box.
  *(Is that a good rule? Rust allows it.)*
- Add `ask NAME;`, which reads a line from the keyboard into a text
  variable.

## Checkpoint

The learner can, without help:
- [ ] Explain statements, and the new grammar
- [ ] Act out scope with boxes, and predict what `diamonds.pick` prints
- [ ] Explain how `scopes` works, with `last_mut` and `.rev()`
- [ ] Run a Pickaxe program from a file, and use the prompt

## Lab notebook

Draw the boxes for `diamonds.pick` at the moment it prints `Inside the
chest: 100`. Copy the grammar for statements. Commit. Add *statement*,
*variable*, *scope*, *block*, *global* and *shadowing* to
`dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows *Crafting Interpreters*, Chapter 8 ("Statements and
State"). Lox keeps each scope as an environment object pointing to its
enclosing one; Pickaxe's `Vec` of `HashMap`s is the same idea as a
stack, which is simpler in Rust because it avoids shared, mutable
pointers. Searching from the top of the stack gives **lexical (block)
scope** for programs without functions; Lesson 12.10 handles functions
by hiding the caller's boxes.

`Let` declares, `Set` assigns, and assigning to a name that was never
declared is an error, which catches spelling mistakes (`diamnods =
4;`). Python makes a new variable instead, which is friendlier but hides
those mistakes. `Stmt::Run` is Lox's "expression statement". In file
mode, errors go to standard error and the exit code is 1, as Stage 8's
tools did.
