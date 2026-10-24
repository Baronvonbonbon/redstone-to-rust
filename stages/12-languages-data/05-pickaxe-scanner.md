# Lesson 12.5: Pickaxe, Part 1: Designing a Language, and a Scanner

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor;
`~/lab/lang`; paper · **New words:** specification, token, scanner,
lexeme, keyword, comment, peek

## Goal *(read this to the learner)*

> For the next six lessons, you'll build a programming language of your
> own, called **Pickaxe**, with an interpreter written in Rust. By the
> end it will have variables, `if`, `while`, and functions that call
> themselves. Today you'll design it on paper, then write the first
> part: the scanner, which chops a program into words.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once, and skim Lessons 12.6 to 12.10, so you
      know where it's going.
- [ ] Run `./scripts/give-lab.sh LEARNER lang` from your account. It puts
      `check-pickaxe` and its tests in `~/lab/lang` (see the [language lab
      handbook](../../labs/lang/README.md)).
- [ ] Rust and Cargo from Stage 9.

## Warm-up (5 min)

"What does a tokenizer do?" *(Chops text into tokens: Lessons 8.13 and
12.4.)* "Tiny Scheme's tokenizer was one line. Why could it be so
short?" *(Scheme only has brackets and words with spaces between.)*
**Say:** "Pickaxe will look more like Rust and Python, so its scanner
has more to do."

## Activity

### Session 1: designing Pickaxe

1. **A specification.** **Say:** "Before building a language, you
   decide what it looks like. That's its **specification**." Write this
   on a big sheet of paper, and talk through each line:
   ```
   # Pickaxe: a language for miners.     <- a comment, to the end of the line
   let diamonds = 3;                     <- a new variable
   diamonds = diamonds + 5;              <- change it
   say "I have " + diamonds;             <- print something
   if diamonds > 5 {                     <- choose
       say "rich!";
   } else {
       say "dig more";
   }
   while diamonds < 10 {                 <- repeat
       diamonds = diamonds + 1;
   }
   fun double(n) {                       <- a function
       return n * 2;
   }
   say double(21);
   ```
   **Say:** "Pickaxe has whole numbers, texts in `"quotes"`, and `true`
   and `false`. Statements end with `;`. Blocks are in `{ }`." **Ask:**
   "What would you change? Should it be `say` or `print`? `fun` or
   `def`?" The learner may change the words: it's their language! (If
   they do, the code below needs the same changes, and `check-pickaxe`
   won't match: that's fine, but decide now and stick to it.)

2. **The plan.** Draw the pipeline from Lesson 12.4, with Pickaxe's
   pieces, and which lesson builds each:
   ```
   program text → [scanner] → tokens → [parser] → tree → [interpreter] → it runs!
                    12.5                  12.6–12.10        12.7–12.10
   ```

3. **What are the tokens?** Take the specification and draw a box round
   every token, in four colours: **numbers** (`3`, `5`), **texts**
   (`"I have "`), **words** (`let`, `diamonds`, `say`, `if`) and
   **symbols** (`=`, `+`, `;`, `{`, `>`, `(`). **Ask:** "Is `==` one token
   or two?" *(One: it means 'is equal to', different from `=`.)* "What
   about spaces, new lines and comments?" *(They aren't tokens: the
   scanner skips them.)* **Say:** "Words like `let` and `if` that mean
   something special are called **keywords**. The scanner doesn't care:
   it calls them all words. The parser decides."

### Session 2: the scanner

4. **A new project.**
   ```
   cd ~/lab/lang
   cargo new pickaxe
   cd pickaxe
   ```
   Make `src/scanner.rs`:
   ```rust
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
   ```
   Read it together:
   - "`Token` is an enum (Lesson 9.7): four kinds, each carrying its
     value."
   - "`.peekable()` lets us **peek**: look at the next letter without
     using it up. `chars.next()` uses it up."
   - "Each `if` looks at the next letter and decides what kind of token
     is starting. Then a little loop eats letters until the token ends."
   - "`=`, `!`, `<` and `>` might have a `=` after them: peek to see."
   - "Anything else is a mistake, with a friendly message."

5. **Try it.** Replace `src/main.rs` with:
   ```rust
   mod scanner;

   use std::{env, fs, process};

   fn main() {
       let args: Vec<String> = env::args().collect();
       let Some(file) = args.get(1) else {
           eprintln!("Which program? Try: cargo run -- hello.pick");
           process::exit(1);
       };
       let Ok(source) = fs::read_to_string(file) else {
           eprintln!("I can't read {file}");
           process::exit(1);
       };
       match scanner::scan(&source) {
           Ok(tokens) => {
               for token in tokens {
                   println!("{token:?}");
               }
           }
           Err(problem) => {
               eprintln!("Oops: {problem}");
               process::exit(1);
           }
       }
   }
   ```
   Make `hello.pick`, in the `pickaxe` folder:
   ```
   # My first Pickaxe program
   let diamonds = 3;
   say "I have " + diamonds + " diamonds!";
   ```
   `cargo run -- hello.pick`. **They should see**, after Cargo's
   `Compiling` lines:
   ```
   Word("let")
   Word("diamonds")
   Symbol("=")
   Number(3)
   Symbol(";")
   Word("say")
   Text("I have ")
   Symbol("+")
   Word("diamonds")
   Symbol("+")
   Text(" diamonds!")
   Symbol(";")
   ```
   **Ask:** "Where did the comment go? And the spaces?" *(Skipped.)*
   "Where's the space inside `"I have "`?" *(Kept: it's part of the
   text.)* **Say:** "`--` tells Cargo 'the rest is for my program, not
   for you'."

6. **Mistakes.** Make `oops.pick` containing `say 3 @ 4;`, and run it.
   **They should see:** `Oops: I don't know what @ means`. Try `say
   "hello;` *(`Oops: a text is missing its closing "`)* and `say
   99999999999999999999;` *(`Oops: 99999999999999999999 is too big for
   Pickaxe`: it doesn't fit in an `i64`)*. Try `if x<=10 { say x; }`:
   **Ask:** "How many tokens is `x<=10`, with no spaces?" *(Three:
   `Word("x")`, `Symbol("<=")`, `Number(10)`.)*

7. **Check it.** In the `pickaxe` folder:
   ```
   ~/lab/lang/check-pickaxe 12.5
   ```
   **They should see:**
   ```
   Building /home/sam/lab/lang/pickaxe ...
   PASS  12.5/hello.pick
   PASS  12.5/oops-big.pick
   PASS  12.5/oops-symbol.pick
   PASS  12.5/oops-text.pick
   PASS  12.5/symbols.pick
   5 passed, 0 failed.
   ```
   **Say:** "`check-pickaxe` runs your interpreter on test programs and
   compares what comes out with what should. Lines starting `<` show
   what should have appeared; `>` shows what did." Then `cargo fmt`,
   `cargo clippy`, and commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| ``error[E0433]: cannot find module or crate `scanner` in this scope`` | `mod scanner;` is missing from `main.rs` | Add it at the top. |
| `cargo run -- hello.pick` never finishes, and nothing prints | A loop that never uses up its letter: usually `chars.next()` missing in the whitespace branch | Ctrl+C. Check that every branch calls `chars.next()`. |
| `Which program? Try: cargo run -- hello.pick` | No file name, or the `--` was left out | `cargo run -- hello.pick`. |
| `I can't read hello.pick` | The file isn't in this folder | `ls`; make it in `~/lab/lang/pickaxe`. |
| `<=` comes out as `Symbol("<")` then `Symbol("=")` | The `"=!<>"` branch isn't peeking for `=` | Check that branch against the lesson. |
| A `FAIL` from `check-pickaxe` | Different output from the expected | Read the `<` and `>` lines: often a message worded differently. |

## Talk about it

- What's a specification? What did you decide for Pickaxe?
- What are the four kinds of token?
- What does peeking mean, and why does the scanner need it?
- Why does the scanner call `let` a word, and not a keyword?

## Challenge *(if there's time, or for next time)*

- Make the scanner understand `//` comments as well as `#`.
- Count the tokens in `hello.pick` with `.len()`, and print it at the
  end.
- Give each token its line number, so that mistakes can say where they
  are: `Oops: line 3: I don't know what @ means`. *(Count the `\n`s.)*

## Checkpoint

The learner can, without help:
- [ ] Explain Pickaxe's specification, and any changes they made
- [ ] Draw boxes round the tokens of a program, in four colours
- [ ] Explain how the scanner decides what kind of token is starting
- [ ] Run `check-pickaxe 12.5` and read its result

## Lab notebook

Glue in (or copy) the Pickaxe specification. Draw the pipeline. Copy the
token list for `hello.pick`. Commit. Add *specification*, *token*,
*scanner*, *keyword* and *peek* to `dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows *Crafting Interpreters*, Chapters 3 ("The Lox
Language") and 4 ("Scanning"), in the offline library
(`repos/crafting-interpreters/book/`). Lox is Robert Nystrom's teaching
language; Pickaxe is smaller, and its interpreter is written in Rust
rather than Java, but the stages are the same. A scanner is also called
a **lexer**; the piece of text a token came from is its **lexeme**.

The finished Pickaxe interpreter is in `labs/lang/pickaxe` (this
course's own code, MIT), for you to compare with if the learner's
version won't build. Every lesson shows all of its code, so it isn't a
secret, but `give-lab.sh` doesn't copy it, so that the learner types and
thinks first. Pickaxe numbers are `i64`, whole numbers only, so `7 / 2`
will be 3, as in Rust; that keeps the language small and matches the
learner's arithmetic. *(If the learner later wants decimals, `f64` is a
good extension project.)*
