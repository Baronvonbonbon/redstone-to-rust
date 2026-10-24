# Lesson 12.10: Pickaxe, Part 6: Functions That Call Themselves

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text editor;
`~/lab/lang/pickaxe`; sticky notes; dominoes (or a picture of them) ·
**New words:** function, parameter, argument, return, call, local,
recursion, base case, induction

## Goal *(read this to the learner)*

> The last big piece: functions. After today, Pickaxe programs can
> define their own words, like `fun double(n) { return n * 2; }`, and
> functions can call themselves, so Pickaxe can do recursion, the way
> Scheme does. And you'll see why recursion always works, with a row of
> dominoes.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once. Step 5 replaces a large part of
      `interpreter.rs`; it's worth reading the list of changes before
      the code.
- [ ] `check-pickaxe 12.9` passes.
- [ ] Glance at Lesson 7.9 (dominoes and induction) and Lesson 8.10
      (call and return in the VM).

## Warm-up (5 min)

"In Scheme, how do you make a new procedure?" *(`(define (double n) (*
n 2))`.)* "In Lesson 8.10, what did the VM have to remember when a
function was called?" *(Where to come back to, and the caller's
things, so they could be put back.)* **Say:** "Pickaxe needs the same."

## Activity

### Session 1: designing functions

1. **What they look like.** On paper:
   ```
   fun double(n) {
       return n * 2;
   }
   say double(21);
   ```
   **Say:** "`fun` makes a **function**. `n` is a **parameter**: a name
   for the value that's handed in. In `double(21)`, the 21 is the
   **argument**. `return` hands back the answer, and stops the function
   straight away." The grammar:
   ```
   statement → ...
             | fun NAME ( NAME , NAME ... ) block
             | return expression ;
   primary   → ... | NAME ( expression , expression ... )
   ```

2. **Act it out.** The learner is the interpreter. Act out:
   ```
   let x = 10;
   fun add_one(n) {
       let answer = n + 1;
       return answer;
   }
   say add_one(x * 2);
   ```
   - `let x`: a sticky note `x 10` in the globals box.
   - `fun add_one`: write the whole function on a card, and put it in a
     **functions** pile. Nothing runs yet!
   - `say add_one(x * 2)`: work out the argument first: 20. Now **call**:
     put the caller's boxes aside (there are none here, just the
     globals), get a new box with `n 20` in it (the **locals**), and run
     the card's block. `answer` goes in a box on top. `return answer`:
     the answer, 21, travels back out, through the blocks, to the call.
     Throw away the function's boxes, and put the caller's back.
   - `say` prints 21.

   **Ask:** "Could the function see `x`?" *(Yes: it's a global.)* "If
   `say` had been inside a block with its own variables, could the
   function see those?" *(No: they were put aside. A function only sees
   the globals and its own locals. That way, a function always works
   the same, wherever it's called from.)*

3. **The problem with return.** **Ask:** "`return` can be inside an
   `if`, inside a `while`, inside the function's block. How does the
   answer get all the way out?" **Say:** "Each `exec` will now say one of
   two things: 'carry on' or 'I'm returning, with this value'. Every
   block and loop that gets 'returning' stops and passes it outwards,
   until it reaches the call. In Rust: `exec` gives back
   `Option<Value>`: `None` means carry on, `Some(value)` means return."

### Session 2: the parser

4. **Parsing functions.** In `src/parser.rs`, add to `Expr`, after
   `Binary`:
   ```rust
       Call(String, Vec<Expr>),
   ```
   and to `Stmt`, after `While`:
   ```rust
       Fun(String, Vec<String>, Vec<Stmt>),
       Return(Expr),
   ```
   In `statement`, after the `while` part (before `} else if
   self.looking_at("{") {`):
   ```rust
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
   ```
   In `primary`, replace the line `Some(Token::Word(w)) =>
   Ok(Expr::Name(w)),` with:
   ```rust
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
   ```
   **Say:** "A name followed by `(` is a call. The loop collects things
   separated by commas until the `)`: names for the parameters, and
   whole expressions for the arguments, so `double(x * 2)` works."

### Session 3: the interpreter

5. **Calling.** The changes to `src/interpreter.rs`, in a list first:
   - A new kind of value, `Nothing`, for functions that don't `return`
     anything.
   - The `Interpreter` keeps a `functions` table, and counts how
     `depth` its calls are.
   - `exec` and `block` give back `Option<Value>`, and pass a `Some`
     outwards (step 3).
   - New arms for `Fun` (remember the function) and `Return`, and for
     `Call` in `eval`.
   - A new `call` method, which does step 2's act-out.

   Replace everything in `src/interpreter.rs` *above* `fn binary` with:
   ```rust
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
   ```
   Read `call` with the act-out from step 2:
   - "Find the function's card, and check the number of arguments."
   - "Work out each argument, in the *caller's* boxes, into `locals`.
     `zip` pairs each parameter with its argument."
   - "`split_off(1)` puts aside every box except the globals. Push the
     locals box, and run the body."
   - "Afterwards, cut back to the globals, and put the caller's boxes
     back with `extend`."
   - "`unwrap_or(Value::Nothing)`: if the body never returned, the answer
     is `nothing`."

   **Ask:** "Why is there a `LIMIT`?" *(A function that calls itself for
   ever would use up Rust's own memory for calls, and crash. Pickaxe
   stops first, with a friendly message.)*

6. **Functions!** Make `funs.pick`:
   ```
   # Funs
   fun double(n) {
       return n * 2;
   }
   say double(21);

   fun greet(name) {
       say "Hello, " + name + "!";
   }
   greet("Steve");
   greet("Alex");

   fun factorial(n) {
       if n <= 1 {
           return 1;
       }
       return n * factorial(n - 1);
   }
   say factorial(5);
   say factorial(20);
   ```
   `cargo run -- funs.pick`. **They should see:**
   ```
   42
   Hello, Steve!
   Hello, Alex!
   120
   2432902008176640000
   ```
   **Say:** "`factorial` calls itself. Recursion, in your own language!"
   Try `say factorial(21);` *(`Oops: that number is too big for
   Pickaxe`: Scheme wouldn't mind, but `i64` does.)*

7. **Why recursion works: dominoes.** Line up the dominoes. **Say:**
   "Two things make every domino fall: the first one falls, and each one
   knocks over the next. In Lesson 7.9, that was **induction**." Connect
   it to `factorial`:
   - "The first domino: `factorial(1)` is right: it returns 1. That's
     the **base case**."
   - "Each knocks the next: *if* `factorial(n - 1)` is right, then `n *
     factorial(n - 1)` is right for `n`."
   - "So every `factorial` is right, however big. And `n - 1` gets
     smaller every time, so it always reaches the base case."

   **Ask:** "What happens without the base case?" Try it at the prompt:
   ```
   pickaxe> fun forever(n) { return forever(n + 1); }
   pickaxe> say forever(1);
   Oops: forever went more than 200 calls deep
   ```

8. **More mistakes, and the checker.** At the prompt:
   ```
   pickaxe> say double(2);
   Oops: there's no fun called double
   pickaxe> fun add(a, b) { return a + b; }
   pickaxe> say add(1);
   Oops: add needs 2 values, but got 1
   pickaxe> return 5;
   Oops: return can only be used inside a fun
   pickaxe> fun quiet() { say "hi"; }
   pickaxe> say quiet();
   hi
   nothing
   ```
   Then `~/lab/lang/check-pickaxe 12.10`. **They should see** ten `PASS`
   lines and `10 passed, 0 failed.` **Say:** "Pickaxe is finished: a real
   language, with your own interpreter. Everything in it, you built."
   `cargo fmt`, `cargo clippy`, commit, and tick the passport.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| ``error[E0004]: non-exhaustive patterns: `&Stmt::Fun(_, _, _)` and `&Stmt::Return(_)` not covered`` (and the same for `&Expr::Call(_, _)`) | The parser has the new statements, but the interpreter doesn't | Do step 5. |
| ``error[E0308]: mismatched types`` ... ``expected `Option<Value>`, found `()` `` | One `Ok(())` was left from Lesson 12.9 | Every `Ok(())` in `exec` and `block` becomes `Ok(None)`. |
| `factorial(5)` gives `nothing` | `return` isn't passed out of the `if` block | Check `block` stops on anything that isn't `Ok(None)`, and `If` uses `return self.block(...)`. |
| `Oops: I don't know what n is` inside a function | The locals box wasn't pushed, or was pushed before `split_off` | Follow the order in `call` exactly. |
| After calling a function, the caller's variables are gone | The caller's boxes weren't put back | Check `self.scopes.extend(callers);`. |
| ``thread 'main' has overflowed its stack`` | The `depth` check is missing, so endless recursion crashed Rust | Check the `LIMIT` lines in `call`. |

## Talk about it

- What's the difference between a parameter and an argument?
- How does `return` get out of an `if` inside a `while` inside a
  function?
- Why does a function put the caller's boxes aside?
- How do the dominoes show that `factorial` is right for every number?

## Challenge *(if there's time, or for next time)*

- Write `fib(n)` in Pickaxe, and print `fib(20)`. *(6765.)* Then
  `power(base, n)`, and `gcd(a, b)` (Euclid's algorithm, with `%`).
- Write `is_prime(n)` with a `while` loop, and print the primes below 50.
- Add built-in functions: make `call` check for `"len"` or `"ask"` before
  looking in `functions`.

## Checkpoint

The learner can, without help:
- [ ] Write Pickaxe functions with parameters and `return`
- [ ] Act out a call with boxes, and explain `call`
- [ ] Explain how `Option<Value>` carries `return` outwards
- [ ] Explain why `factorial` works for every number, with dominoes
- [ ] Pass `check-pickaxe 12.10`

## Lab notebook

Draw the boxes during `add_one(x * 2)`. Draw the dominoes for
`factorial`, labelled with the base case and the step. Copy your
favourite Pickaxe program. Commit. Add *function*, *parameter*,
*argument*, *return*, *base case* and *induction* to `dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows *Crafting Interpreters*, Chapter 10 ("Functions").
Lox implements `return` by throwing an exception and catching it at the
call; Pickaxe uses `Option<Value>` to carry it out instead, which is
the usual Rust way and makes the control flow visible. Lox functions
are values (they can be stored in variables) and are **closures**
(Chapter 11) that capture their surrounding scope; Pickaxe keeps
functions in a separate table and gives them only the globals, which
is simpler and still supports recursion. Closures are a good extension
for an older learner, following Chapter 11.

`LIMIT` protects against Rust's own stack overflowing: each Pickaxe call
uses several Rust stack frames, and a debug build has an 8 MB main
stack; 200 levels is comfortably safe. Proof by induction appears in
*Book of Proof* (Chapter 10) and Levin's *Discrete Mathematics*
(Section 2.5), both in the math track.
