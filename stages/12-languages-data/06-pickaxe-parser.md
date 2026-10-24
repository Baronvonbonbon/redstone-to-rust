# Lesson 12.6: Pickaxe, Part 2: Trees from Tokens

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/lang/pickaxe`; paper and coloured pens · **New words:**
parser, expression, operator, precedence, recursive descent, `Box`,
syntax tree

## Goal *(read this to the learner)*

> The scanner gives a flat row of tokens. But `1 + 2 * 3` isn't flat:
> the `2 * 3` has to happen first, inside. Today you'll write Pickaxe's
> parser, which builds the tree, and make Pickaxe print its trees the
> Scheme way, so you can see exactly what it understood.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once. The parser is the hardest code in the
      stage; it's worth reading slowly together, and the learner wrote a
      parser like it for Jack (Lesson 8.14).
- [ ] Session 1 is on paper. The code is Sessions 2 and 3.

## Warm-up (5 min)

"In Scheme, how do you write `1 + 2 * 3`?" *(`(+ 1 (* 2 3))`.)* "Draw its
tree." **Say:** "Today, Pickaxe learns to turn `1 + 2 * 3` into that
tree, by itself."

## Activity

### Session 1: Pickaxe's grammar

1. **Levels of stickiness.** **Say:** "In `1 + 2 * 3`, the `*` is
   stickier than the `+`: it grabs its numbers first. Which is
   stickiest of all?" Make a ladder on paper, least sticky at the top:
   ```
   == !=           is it equal?
   < <= > >=       comparing
   + -             adding
   * / %           multiplying
   - !             minus one thing, or not
   numbers, texts, names, ( brackets )
   ```
   **Say:** "How sticky an operator is, is called its **precedence**."
   **Ask:** "So in `1 + 2 < 4`, what happens first?" *(`+` is stickier
   than `<`: `(1 + 2) < 4`, which is true.)*

2. **The grammar.** Each level of the ladder becomes a rule:
   ```
   expression → equality
   equality   → comparison ( ( == | != ) comparison )*
   comparison → term ( ( < | <= | > | >= ) term )*
   term       → factor ( ( + | - ) factor )*
   factor     → unary ( ( * | / | % ) unary )*
   unary      → ( - | ! ) unary   |   primary
   primary    → NUMBER | TEXT | true | false | NAME | ( expression )
   ```
   **Say:** "Each rule uses the stickier one below it. The last rule
   goes all the way back to the top for brackets: that's how `(1 + 2) *
   3` works." Draw the tree for `1 + 2 * 3` by following the rules, and
   for `10 - 4 - 3`. **Ask:** "Is `10 - 4 - 3` 3 or 9?" *(3: the loop
   goes left to right, `(10 − 4) − 3`.)*

3. **One function per rule.** **Say:** "The parser has one function for
   each rule. Each one calls the one below. That's called **recursive
   descent**: going down the ladder, and sometimes back up to the top."

### Sessions 2 and 3: the parser in Rust

4. **The tree, and the parser's helpers.** Make `src/parser.rs`:
   ```rust
   // The parser turns tokens into a tree.
   use crate::scanner::Token;

   #[derive(Debug, Clone)]
   pub enum Expr {
       Number(i64),
       Text(String),
       Bool(bool),
       Name(String),
       Unary(String, Box<Expr>),
       Binary(Box<Expr>, String, Box<Expr>),
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

       pub fn at_end(&self) -> bool {
           self.pos >= self.tokens.len()
       }
   }
   ```
   Read it together:
   - "`Expr` is the tree. A `Binary` has a left side, an operator and a
     right side, and each side is a whole `Expr` again, so a tree can
     be as deep as you like."
   - "**`Box`** (from the Rustlings in Lesson 9.18): an `Expr` can't
     hold an `Expr` directly, or it would be infinitely big. A `Box`
     holds it somewhere else in memory (the heap), and just points to
     it."
   - "`pos` is where we've got to in the tokens. `peek` looks; `next`
     takes."
   - "`is` and `either` check for a symbol or word, and use it up only if
     it's there. `expect` is for things that *must* be there, like a
     closing `)`."

5. **The grammar, as functions.** Inside the `impl Parser` block, after
   `at_end`, add one function per rule:
   ```rust
       pub fn expression(&mut self) -> Result<Expr, String> {
           self.equality()
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
               Some(Token::Word(w)) => Ok(Expr::Name(w)),
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
   ```
   Compare `term` with its grammar rule, word by word: "a factor, then,
   while there's a `+` or `-`, another factor, joined on." **Ask:** "Why
   does `left = Expr::Binary(... left ...)` make `10 - 4 - 3` come out
   as `(10 − 4) − 3`?" *(Each time round the loop, the whole tree so far
   becomes the new left side.)* **Say:** "In `primary`, if it's not a
   value at all, we step back one (`pos -= 1`) so the message can say
   what we found."

6. **Show the trees.** Replace `src/main.rs` with a prompt that prints
   each tree the Scheme way:
   ```rust
   mod parser;
   mod scanner;

   use parser::{Expr, Parser};
   use std::io::{self, BufRead, Write};

   // Show a tree the Scheme way: (operator left right).
   fn show(expr: &Expr) -> String {
       match expr {
           Expr::Number(n) => n.to_string(),
           Expr::Text(t) => format!("\"{t}\""),
           Expr::Bool(b) => b.to_string(),
           Expr::Name(name) => name.clone(),
           Expr::Unary(op, inside) => format!("({op} {})", show(inside)),
           Expr::Binary(left, op, right) => format!("({op} {} {})", show(left), show(right)),
       }
   }

   fn parse(line: &str) -> Result<Expr, String> {
       let tokens = scanner::scan(line)?;
       let mut parser = Parser::new(tokens);
       let expr = parser.expression()?;
       if !parser.at_end() {
           return Err("there's something extra at the end".to_string());
       }
       Ok(expr)
   }

   fn main() {
       print!("pickaxe> ");
       io::stdout().flush().unwrap();
       for line in io::stdin().lock().lines() {
           let Ok(line) = line else { break };
           match parse(&line) {
               Ok(expr) => println!("{}", show(&expr)),
               Err(problem) => println!("Oops: {problem}"),
           }
           print!("pickaxe> ");
           io::stdout().flush().unwrap();
       }
       println!();
   }
   ```
   **Say:** "`show` is recursive, like the tree: to show a `Binary`, show
   both sides. `flush` makes the prompt appear before you type." `cargo
   run` (no file this time), and type:
   ```
   pickaxe> 1 + 2 * 3
   (+ 1 (* 2 3))
   pickaxe> (1 + 2) * 3
   (* (+ 1 2) 3)
   pickaxe> 10 - 4 - 3
   (- (- 10 4) 3)
   pickaxe> -x + 4 >= 10 == true
   (== (>= (+ (- x) 4) 10) true)
   pickaxe> "Score: " + 10
   (+ "Score: " 10)
   ```
   **Say:** "Your parser writes Scheme! The brackets show exactly what it
   understood. Each tree is the same as the one you drew." Ctrl+D to
   leave.

7. **Mistakes.** Type `1 +`, `1 2` and `(1 + 2`. **They should see:**
   ```
   pickaxe> 1 +
   Oops: I expected a value but found the end
   pickaxe> 1 2
   Oops: there's something extra at the end
   pickaxe> (1 + 2
   Oops: I expected ) but found the end
   ```
   Then `~/lab/lang/check-pickaxe 12.6`: **they should see** `PASS
   12.6/trees.in` and `1 passed, 0 failed.` `cargo fmt`, `cargo clippy`,
   commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| ``error[E0072]: recursive type `Expr` has infinite size`` | An `Expr` holds an `Expr` without a `Box` | Write `Box<Expr>` in `Unary` and `Binary`. |
| `error[E0308]: mismatched types` ... ``expected struct `Box<Expr>` `` | An `Expr` was given where a `Box` was needed | Wrap it: `Box::new(inside)`. |
| `1 + 2 * 3` shows `(* (+ 1 2) 3)` | `term` and `factor` are swapped: `+` is stickier than `*` | `term` (for `+ -`) must call `factor` (for `* / %`). |
| `10 - 4 - 3` shows `(- 10 (- 4 3))` | The right side calls the same level again, instead of the stickier one | `let right = self.factor()?;` in `term`, and so on. |
| `cargo run` waits, with no prompt | The `flush` is missing | Add `io::stdout().flush().unwrap();` after each `print!`. |

## Talk about it

- What's precedence? Which Pickaxe operator is stickiest?
- How does the grammar become functions? What's recursive descent?
- Why does an `Expr` need a `Box`?
- What does the parser do when the tokens don't fit the grammar?

## Challenge *(if there's time, or for next time)*

- Add a power operator, `^`, stickier than `*`: `2 ^ 3`. (It needs a new
  symbol in the scanner, and a new level in the parser.)
- Draw the tree for `!(1 < 2) == false` on paper, then check it with
  Pickaxe.
- Make `show` draw the tree sideways, with indentation for each level.

## Checkpoint

The learner can, without help:
- [ ] Explain precedence with the stickiness ladder
- [ ] Match each parser function to its grammar rule
- [ ] Predict the tree for an expression, then check it with Pickaxe
- [ ] Explain why `Expr` needs `Box`

## Lab notebook

Copy the stickiness ladder and the grammar. Draw three trees from step
6, and the Scheme-style text Pickaxe printed for each. Commit. Add
*parser*, *precedence*, *recursive descent*, *syntax tree* and *Box* to
`dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows *Crafting Interpreters*, Chapter 5 ("Representing
Code") and Chapter 6 ("Parsing Expressions"). Pickaxe's grammar is
Lox's expression grammar, with `%` added; the "one function per
precedence level, looping for left-associative operators" pattern is
standard recursive descent, and the same technique the Jack parser used
in Lesson 8.14. The tree is an **abstract syntax tree** (AST): it keeps
the meaning (what's inside what) and throws away the brackets and
spaces.

The `show` function prints the tree in s-expression form, which is the
same idea as *Crafting Interpreters*' "AstPrinter"; it ties the
learner's own language to Lesson 12.2's Scheme. Parsers in real
languages also recover from errors so that they can report several at
once; Pickaxe stops at the first, which keeps the code small. Rust
operators like `while let` and `if let` were in Lessons 9.7–9.9.
