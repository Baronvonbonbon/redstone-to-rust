# Lesson 12.9: Pickaxe, Part 5: Choosing and Repeating

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor;
`~/lab/lang/pickaxe` · **New words:** control flow, condition,
`else if`, short-circuit, Turing complete

## Goal *(read this to the learner)*

> Pickaxe can remember things, but it always does every line, once, in
> order. Today it learns to choose (`if`, `else`) and repeat (`while`),
> and to combine true-or-false questions with `and` and `or`. Then it
> can run Creeper Boom and the hailstone numbers. With those, it can
> work out anything a computer can.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] `check-pickaxe 12.8` passes.

## Warm-up (5 min)

"In Lesson 12.8, what did `block` do with its box when the `}` came?"
*(Threw it away.)* "What's the smallest change that would let a block
run *twice*?" *(Call `block` twice! A loop just calls it again and
again.)*

## Activity

### Session 1: if and while

1. **Grammar.** Add to the statement rule on paper:
   ```
   statement → ...
             | if expression block ( else ( if-statement | block ) )?
             | while expression block
   expression → or
   or         → and ( or and )*
   and        → equality ( and equality )*
   ```
   **Say:** "`( ... )?` means 'maybe'. The `else` part is optional, and
   after `else` can come another `if`: that's how `else if` works. `or`
   is the least sticky of all, then `and`, so `a > 1 and b > 1 or c` is
   `(a > 1 and b > 1) or c`."

2. **The parser.** In `src/parser.rs`, add two kinds of statement to
   `Stmt`, after `Block`:
   ```rust
       If(Expr, Vec<Stmt>, Vec<Stmt>),
       While(Expr, Vec<Stmt>),
   ```
   In `statement`, after the `let` part (before `} else if
   self.looking_at("{") {`), add:
   ```rust
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
   ```
   **Say:** "An `If` keeps the test, the 'yes' statements, and the 'no'
   statements. With no `else`, 'no' is empty. With `else if`, 'no' is a
   list with one statement in it: another `If`." Then change
   `expression`, and add two levels above `equality`:
   ```rust
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
   ```

3. **The interpreter.** In `src/interpreter.rs`, in `exec`, after the
   `Stmt::Block` line, add:
   ```rust
               Stmt::If(test, yes, no) => {
                   if self.test(test)? {
                       return self.block(yes);
                   } else {
                       return self.block(no);
                   }
               }
               Stmt::While(test, body) => {
                   while self.test(test)? {
                       self.block(body)?;
                   }
               }
   ```
   and, after the `block` method, a helper:
   ```rust
       fn test(&mut self, test: &Expr) -> Result<bool, String> {
           match self.eval(test)? {
               Value::Bool(b) => Ok(b),
               other => Err(format!("if and while need true or false, not {other}")),
           }
       }
   ```
   **Say:** "Pickaxe's `if` uses Rust's `if`, and Pickaxe's `while` uses
   Rust's `while`! The interpreter borrows the power of the language it's
   written in. `test` makes sure the condition is really true or false:
   `if 5 { ... }` is a mistake in Pickaxe, as in Rust."

4. **Creeper Boom.** Make `fizz.pick`:
   ```
   # Creeper Boom: count to 15
   let n = 1;
   while n <= 15 {
       if n % 15 == 0 {
           say "CREEPER BOOM";
       } else if n % 3 == 0 {
           say "Creeper";
       } else if n % 5 == 0 {
           say "Boom";
       } else {
           say n;
       }
       n = n + 1;
   }
   ```
   `cargo run -- fizz.pick`. **They should see** (down the screen):
   `1`, `2`, `Creeper`, `4`, `Boom`, `Creeper`, `7`, `8`, `Creeper`,
   `Boom`, `11`, `Creeper`, `13`, `14`, `CREEPER BOOM`. *(It's FizzBuzz
   from Lesson 3.5, in creeper clothes.)* **Ask:** "Why
   must the 15 test come first?" *(15 is also divisible by 3, so it
   would say `Creeper` and stop checking.)*

### Session 2: and, or, and a real program

5. **`and` and `or`, the lazy way.** **Ask:** "In `false and
   anything`, do you need to look at `anything`?" *(No: it's false
   whatever.)* In `src/interpreter.rs`, in `eval`, change the start of
   the `Expr::Binary` arm to:
   ```rust
               Expr::Binary(left, op, right) => {
                   if op == "and" || op == "or" {
                       return self.logic(left, op, right);
                   }
   ```
   and add, after `eval`, inside `impl Interpreter`:
   ```rust
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
   ```
   `cargo run`, and:
   ```
   pickaxe> say 3 > 2 and 2 > 1;
   true
   pickaxe> say 1 > 2 or 2 > 1;
   true
   pickaxe> say false and 1 / 0 == 0;
   false
   pickaxe> say true and 1 / 0 == 0;
   Oops: you can't divide by zero
   ```
   **Ask:** "Why no divide-by-zero error the first time?" *(`and` saw
   `false` and never looked at the right side.)* **Say:** "That's called
   **short-circuit**: stopping as soon as the answer is known. Rust,
   Python and Scheme all do it. It's useful: `n != 0 and 10 / n > 2` is
   safe."

6. **Hailstones.** Make `hail.pick`:
   ```
   # Hailstone numbers, from Stage 3
   let n = 27;
   let steps = 0;
   while n != 1 {
       if n % 2 == 0 {
           n = n / 2;
       } else {
           n = 3 * n + 1;
       }
       steps = steps + 1;
   }
   say "27 took " + steps + " steps";
   ```
   **They should see:** `27 took 111 steps`. **Say:** "The same answer as
   Python in Stage 3, and Scheme in Lesson 12.2. Three languages, one of
   them yours."

7. **Is Pickaxe a real language?** **Say:** "With variables, `if` and
   `while`, a language can work out anything any computer can work out,
   given enough time and memory. That's called **Turing complete**,
   after Alan Turing. Your Hack computer in Stage 6 was too. So now
   Pickaxe is, officially, a real programming language." Then
   `~/lab/lang/check-pickaxe 12.9`: **they should see** seven `PASS`
   lines (12.8's and 12.9's) and `7 passed, 0 failed.` `cargo fmt`,
   `cargo clippy`, commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| ``error[E0004]: non-exhaustive patterns: `&Stmt::If(_, _, _)` and `&Stmt::While(_, _)` not covered`` | `exec` doesn't handle the new statements yet | Do step 3. |
| A program never stops, and nothing (or the same thing) prints for ever | A `while` whose condition never becomes false, often a missing `n = n + 1;` | Ctrl+C, then fix the loop. |
| `Oops: if and while need true or false, not 5` | `if 5 { ... }` or a sum used as a test | Use a comparison, like `n > 5`. |
| `Oops: I expected { but found say` | An `if` or `while` without curly brackets | Pickaxe always needs `{ }` after `if`, `else` and `while`. |
| `and` gives `Oops: I expected ; but found and` | `expression` still calls `equality`, not `or` | Change `expression` to call `self.or()`. |
| `say false and 1 / 0 == 0;` gives the divide-by-zero error | `and` isn't going to `logic` | Check the `if op == "and" \|\| op == "or"` line comes first in the `Binary` arm. |

## Talk about it

- How does `else if` work in the tree?
- How does Pickaxe's `while` use Rust's `while`?
- What's short-circuiting? When is it useful?
- What does Turing complete mean?

## Challenge *(if there's time, or for next time)*

- Write a Pickaxe program for a times table, or a Numberblocks staircase
  (the sum 1 + 2 + ... + 10).
- Add a `repeat 5 { ... }` statement that runs a block a number of
  times.
- Add `break;` to leave a `while` early. *(Hard: `exec` has to tell the
  loop to stop. Lesson 12.10's `return` shows one way.)*

## Checkpoint

The learner can, without help:
- [ ] Explain how `if`, `else if` and `while` are parsed and run
- [ ] Write Creeper Boom and the hailstone program in Pickaxe
- [ ] Explain short-circuiting with `false and 1 / 0 == 0`
- [ ] Say what Turing complete means

## Lab notebook

Draw the tree for the `if ... else if ... else` in `fizz.pick`. Write
your own Pickaxe program and copy it in. Commit. Add *control flow*,
*condition*, *short-circuit* and *Turing complete* to `dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows *Crafting Interpreters*, Chapter 9 ("Control
Flow"). Lox's `for` loop is "syntactic sugar" for `while`, and is left
out of Pickaxe (it makes a good extension: the parser can turn a `for`
into a block containing a `let` and a `while`, so the interpreter needs
no changes). Chapter 9 also explains why Lox's grammar for `if` has a
"dangling else" problem; Pickaxe avoids it by always requiring `{ }`.

Turing completeness needs unbounded memory in theory; in practice it
means "can express any computation", and conditional repetition plus
variables is enough. Pickaxe's `and` and `or` return true or false
only; Lox's (like Python's) return one of their operands, so
`nil or "default"` gives `"default"`.
