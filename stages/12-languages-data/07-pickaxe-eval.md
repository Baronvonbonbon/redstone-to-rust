# Lesson 12.7: Pickaxe, Part 3: Working Out the Answer

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor;
`~/lab/lang/pickaxe` · **New words:** evaluate, value, runtime error,
tree-walking interpreter, `Display`

## Goal *(read this to the learner)*

> Pickaxe can read `1 + 2 * 3` and build its tree. Now it's time to
> climb the tree and work out the answer, `7`. Today Pickaxe becomes a
> real calculator, with texts and true-or-false as well as numbers, and
> friendly messages when you ask it something impossible.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] `check-pickaxe 12.6` passes. If not, finish Lesson 12.6 first.

## Warm-up (5 min)

"In tiny Scheme, how did `evaluate` work out `(+ 1 2)`?" *(Work out each
part, then do the operator.)* Draw the tree for `(1 + 2) * 3` and work
it out from the bottom, writing each answer next to its branch.
**Say:** "That's exactly what Pickaxe's interpreter will do."

## Activity

### Session 1: values and evaluating

1. **Values.** **Say:** "A tree is the *question*. The answer is a
   **value**: a number, a text, or true or false." Make
   `src/interpreter.rs`:
   ```rust
   // The interpreter walks the tree and works out the answer.
   use crate::parser::Expr;
   use std::fmt;

   #[derive(Debug, Clone, PartialEq)]
   pub enum Value {
       Number(i64),
       Text(String),
       Bool(bool),
   }

   impl fmt::Display for Value {
       fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
           match self {
               Value::Number(n) => write!(f, "{n}"),
               Value::Text(t) => write!(f, "{t}"),
               Value::Bool(b) => write!(f, "{b}"),
           }
       }
   }
   ```
   **Say:** "`Display` (a trait, from Lesson 9.13) says how a value looks
   when it's printed with `{}`: just the number, or the text without
   quotes."

2. **Evaluate.** Below it:
   ```rust
   pub fn eval(expr: &Expr) -> Result<Value, String> {
       match expr {
           Expr::Number(n) => Ok(Value::Number(*n)),
           Expr::Text(t) => Ok(Value::Text(t.clone())),
           Expr::Bool(b) => Ok(Value::Bool(*b)),
           Expr::Name(name) => Err(format!("I don't know what {name} is")),
           Expr::Unary(op, inside) => match (op.as_str(), eval(inside)?) {
               ("-", Value::Number(n)) => Ok(Value::Number(-n)),
               ("!", Value::Bool(b)) => Ok(Value::Bool(!b)),
               (op, value) => Err(format!("I can't do {op} to {value}")),
           },
           Expr::Binary(left, op, right) => {
               let left = eval(left)?;
               let right = eval(right)?;
               binary(left, op, right)
           }
       }
   }
   ```
   **Say:** "One `match` arm for each kind of tree. A number is just
   itself. A `Binary` works out its left, works out its right, then hands
   both to `binary`. Names don't mean anything yet: that's next lesson."
   **Ask:** "Where's the recursion?" *(`eval` calls `eval` for the
   insides, all the way down the tree.)* **Say:** "This kind of
   interpreter is called **tree-walking**: it walks the tree."

3. **The operators.** Below `eval`:
   ```rust
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
   ```
   Read it as a table: **Say:** "Each line is a rule of Pickaxe: 'a number,
   `+`, a number: add them'. The order matters: Rust uses the first line
   that fits. Dividing by zero comes before dividing. The last line
   catches everything else." Point out:
   - "`checked_add` (Lesson 11.6) gives `None` instead of overflowing.
     `.map(Number)` wraps a good answer as a `Number` value, and
     `.ok_or_else(too_big)` turns `None` into our friendly error."
   - "A text `+` anything joins them up, like `"Score: " + 10`. That's a
     design choice: Python says no, JavaScript says yes. In Pickaxe,
     you decided."
   - "`==` works on any two values, because `Value` derives `PartialEq`."

### Session 2: a calculator

4. **Connect it.** In `src/main.rs`: add `mod interpreter;` at the top,
   **delete the `show` function** (and `Expr` stays in the `use` line),
   and change the `match parse(&line)` part to:
   ```rust
           match parse(&line) {
               Ok(expr) => match interpreter::eval(&expr) {
                   Ok(value) => println!("{value}"),
                   Err(problem) => println!("Oops: {problem}"),
               },
               Err(problem) => println!("Oops: {problem}"),
           }
   ```
   `cargo run`, and try:
   ```
   pickaxe> 1 + 2 * 3
   7
   pickaxe> (1 + 2) * 3
   9
   pickaxe> 10 - 4 - 3
   3
   pickaxe> 7 / 2
   3
   pickaxe> 7 % 2
   1
   pickaxe> "Score: " + 10
   Score: 10
   pickaxe> 3 < 5
   true
   pickaxe> !(3 < 5)
   false
   pickaxe> 5 == "5"
   false
   ```
   **Ask:** "Why is `7 / 2` 3?" *(Whole numbers only, like Rust's `i64`:
   the remainder is thrown away, and `%` gives it.)* "Why is `5 == "5"`
   false?" *(A number and a text are different kinds of value.)*

5. **Runtime errors.** Try each:
   ```
   pickaxe> 1 / 0
   Oops: you can't divide by zero
   pickaxe> true + 1
   Oops: I can't do true + 1
   pickaxe> x
   Oops: I don't know what x is
   pickaxe> 9223372036854775807 + 1
   Oops: that number is too big for Pickaxe
   pickaxe> -true
   Oops: I can't do - to true
   ```
   **Say:** "These are **runtime errors**: the syntax was fine, so the
   parser was happy, but the meaning was impossible (Lesson 12.1). Rust
   would have panicked at `1 / 0`. Pickaxe checks first, and says so
   kindly. A good language always explains."

6. **Check it.** `~/lab/lang/check-pickaxe 12.7`. **They should see**
   `PASS  12.7/values.in` and `1 passed, 0 failed.` `cargo fmt`, `cargo
   clippy`, commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| ``error[E0004]: non-exhaustive patterns: `&Value::Bool(_)` not covered`` | A `match` on `Value` is missing a kind | Add the missing arm (here, in `Display`). |
| ``error[E0308]: `match` arms have incompatible types`` | One line of `binary` gives a `Value` instead of `Ok(Value)` | Wrap it: `Ok(Number(a / b))`. |
| ``warning: function `show` is never used`` | `show` wasn't deleted | Delete it, or keep it for the challenge. |
| `1 / 0` crashes with `attempt to divide by zero` (and the build warned `unreachable pattern`) | The divide-by-zero line is *after* the divide line | Move it above: the first matching line wins. |
| `"Score: " + 10` gives `Oops: I can't do Score:  + 10` | The text lines are missing or below the last catch-all line | Put them before `(a, op, b) =>`. |

## Talk about it

- What's the difference between a tree and a value?
- What's a tree-walking interpreter? Where's the recursion?
- Why does the order of the lines in `binary` matter?
- What's a runtime error? How is it different from a syntax error?

## Challenge *(if there's time, or for next time)*

- Make `"ha" * 3` give `hahaha`. *(One more line in `binary`, with
  `.repeat()`.)*
- Make texts comparable with `<`, so `"apple" < "banana"` is true.
- Make Pickaxe print the tree *and* the answer: keep `show` in `main.rs`,
  and print `(+ 1 (* 2 3)) is 7`.

## Checkpoint

The learner can, without help:
- [ ] Work out a tree by hand, from the bottom up
- [ ] Explain how `eval` walks the tree
- [ ] Explain three lines of `binary`, including the order rule
- [ ] Give a syntax error and a runtime error in Pickaxe

## Lab notebook

Draw the tree for `(1 + 2) * 3 > 8` with each branch's value written
next to it. Copy three of Pickaxe's runtime errors. Commit. Add
*value*, *evaluate*, *runtime error* and *tree-walking interpreter* to
`dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows *Crafting Interpreters*, Chapter 7 ("Evaluating
Expressions"). Lox converts between types loosely and has `nil`;
Pickaxe is stricter (only `+` mixes texts and other values, and `if` will
require true or false), which gives clearer errors for a young learner.
`binary` matches on a tuple of `(Value, &str, Value)`, which lets Rust
check every combination in one place; the `"/" | "%"` pattern is an
or-pattern.

Every arithmetic operation is checked: `checked_add` and friends
return `None` on overflow, so Pickaxe reports a friendly error where
Rust would panic in a debug build. Division by zero is checked before
dividing for the same reason. Negating the smallest `i64` would
overflow, but Pickaxe can't write that number (its digits are too big
for the scanner), so `-n` is safe here.
