# Lesson 13.2: Reading Real Code

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor;
`gcc` (Stage 8); the offline library; `~/lab/quest`; Pickaxe's
`scanner.rs` (Lesson 12.5) · **New words:** codebase, entry point,
navigate, convention, NaN

## Goal *(read this to the learner)*

> Programmers spend more time reading code than writing it, and most of
> it was written by someone else. Today you'll explore a real program
> you didn't write: **clox**, the interpreter from *Crafting
> Interpreters*, in C. You'll build it, run it, find its scanner, and
> compare it with yours. You'll be surprised how much you recognise.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check that `/srv/redstone-library/repos/crafting-interpreters/c`
      exists (the offline library, from [docs/SETUP.md](../../docs/SETUP.md)).
- [ ] `gcc --version` works in the learner's account (Stage 8).

## Warm-up (5 min)

"When you open a big book you've never seen, what do you look at
first?" *(The cover, the back, the contents page.)* **Say:** "Code is
the same. Nobody reads a program from the first line to the last."

## Activity

### Session 1: finding your way around

1. **Five rules for reading code.** Write them on a card, to keep:
   1. Read the README and the file names first.
   2. Find where it starts (the **entry point**: `main`).
   3. Run it, so you know what it does.
   4. Follow one path through it, not everything.
   5. Skip what you don't understand yet. Come back later.

2. **Get a copy.** The library is read-only (so nobody breaks it), so
   copy the C part:
   ```
   cp -r /srv/redstone-library/repos/crafting-interpreters/c ~/lab/quest/clox
   cd ~/lab/quest/clox
   ls
   wc -l *.c | sort -n
   ```
   **They should see** pairs of files (`scanner.c` and `scanner.h`,
   `vm.c` and `vm.h`...) and the sizes, ending:
   ```
      933 vm.c
     1524 compiler.c
     4090 total
   ```
   **Ask:** "From the names, which file do you think does what?" Guess
   for each: `scanner` *(tokens!)*, `compiler`, `vm` *(a virtual
   machine, like Stage 8)*, `memory`, `table` *(a hash table?)*. **Say:**
   "In C, the `.h` file says what's inside, and the `.c` file has the
   code. That's a **convention**: a habit everyone follows, so code is
   easier to find your way around."

3. **Run it.** Build it with every `.c` file at once:
   ```
   gcc -o clox *.c
   ```
   Make `hello.lox`:
   ```
   print "Hello from Lox!";
   var diamonds = 3;
   print diamonds * 2 + 1;
   fun fact(n) { if (n <= 1) return 1; return n * fact(n - 1); }
   print fact(10);
   for (var i = 0; i < 3; i = i + 1) print i;
   ```
   `./clox hello.lox`. **They should see:**
   ```
   Hello from Lox!
   7
   3.6288e+06
   0
   1
   2
   ```
   **Say:** "Lox, the book's language, is Pickaxe's big cousin: `var`
   instead of `let`, `print` instead of `say`, and a `for` loop."
   **Ask:** "What's strange about `fact(10)`?" *(It's `3628800`, but
   written like a calculator: 3.6288 × 10⁶. Lox's numbers must be
   decimals, not whole numbers. We'll check that in the code.)*

4. **Find the entry point.**
   ```
   grep -n "int main" *.c
   grep -n "^static void repl\|^static void runFile" main.c
   ```
   **They should see** `main.c:81:int main(int argc, const char* argv[]) {`,
   and two helpers at lines 20 and 71. **Say:** "With a file name, it
   runs the file; without one, a prompt, like Pickaxe." Try `./clox` with
   no file: **they should see** a `> ` prompt. Type `print 1 + 2;`
   *(3)*, then Ctrl+D.

### Session 2: following one path

5. **The scanner.** **Ask:** "Pickaxe's scanner had a function called
   `scan`. What might clox's be called?"
   ```
   grep -n "Token scanToken" *.c
   ```
   **They should see** `scanner.c:205:Token scanToken() {`. Open
   `scanner.c` in the editor, and go to line 205. Read it together.
   **They should see** a `switch` with `case '(': return
   makeToken(TOKEN_LEFT_PAREN);` and friends, and:
   ```c
       case '=':
         return makeToken(
             match('=') ? TOKEN_EQUAL_EQUAL : TOKEN_EQUAL);
   ```
   **Ask:** "What is that doing?" *(Exactly Pickaxe's `"=!<>"` branch:
   peek for a second `=`.)* Make a two-column table on paper:

   | Pickaxe (Rust) | clox (C) |
   |---|---|
   | `Token::Symbol("(")` | `TOKEN_LEFT_PAREN` |
   | `chars.peek() == Some(&'=')` | `match('=')` |
   | `c.is_ascii_digit()` | `isDigit(c)` |
   | `Err(format!("I don't know what {c} means"))` | `errorToken("Unexpected character.")` |

   **Say:** "Different language, different names, same idea. You
   already understand this code, because you've written your own."

6. **Things you don't understand.** **Ask:** "What are all the lines
   like `//> scan-char` and `//< scan-char`?" Count them: `grep -c
   "^//[<>]" scanner.c` *(57)*. **Say:** "Rule 5: skip them for now. (They
   mark which piece of code belongs to which part of the book, so the
   author can print the book from the code. You'd only find that out by
   reading the README, rule 1.)" Most real code has parts like this: you
   don't need to understand everything to understand something.

7. **Answer a question by reading.** **Ask:** "Why was `fact(10)`
   `3.6288e+06`?" Search for the kind of number Lox uses:
   ```
   grep -n "double" value.h
   ```
   **They should see**, among others, `110:typedef double Value;` and
   `117:    double number;`. **Say:** "`double` is C's decimal number
   (`f64` in Rust). Every Lox number is a double, so big ones print like
   a calculator. Pickaxe chose `i64`. Different design decisions, and
   now you know why." *(The other lines, with `memcpy`, are a clever
   trick called NaN boxing: rule 5!)*

8. **Error messages.** `echo 'print 1 +;' > bad.lox` and `./clox
   bad.lox`. **They should see:** `[line 1] Error at ';': Expect
   expression.` **Ask:** "Which is friendlier, this or Pickaxe's `I
   expected a value but found ;`? What does clox do that Pickaxe
   doesn't?" *(Line numbers!)* Find where the message is made: `grep -rn
   "Expect expression" *.c`. Write in the journal what you'd steal for
   Pickaxe.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `cp: cannot stat '/srv/redstone-library/repos/crafting-interpreters/c'` | The offline library isn't there | The guide runs `./scripts/mirror-library.sh`. |
| `gcc: command not found` | `gcc` isn't installed | The guide runs `./scripts/install-packages.sh --later` (Stage 8). |
| `undefined reference to 'main'` or `undefined reference to 'interpret'` | Only some of the `.c` files were given to `gcc` | `gcc -o clox *.c`, with the `*`. |
| `./clox` waits with `> ` | No file name, so it's a prompt | Type Lox, or Ctrl+D to leave. |
| `[line 1] Error at '1': Expect ';' after expression.` | Pickaxe's `say` in a Lox file (Lox thinks `say` is a variable) | Lox uses `print` and `var`. |
| `[line 1] Error: Unexpected character.` | A character Lox doesn't know, like `%` | Lox has no `%`. See the Challenge. |

## Talk about it

- What are the five rules for reading code? Which helped most?
- How was clox's scanner like yours? How was it different?
- How did reading the code answer the `3.6288e+06` question?
- Why is it OK to skip parts you don't understand?

## Challenge *(if there's time, or for next time)*

- Find clox's keywords: `grep -n "checkKeyword" scanner.c`. How does it
  recognise `while` without a list of words? *(Letter by letter, in a
  `switch`: a tiny tree!)*
- Does Lox have `%`, for Creeper Boom? Find out by reading the `switch`
  in `scanToken`, then try `print 7 % 2;`. *(No: `Unexpected character.`
  Write Creeper Boom in Lox without it: `n - 3 * floor`... Lox has no
  `floor` either! Can you do it with a counter that goes 1, 2, 3, 1, 2,
  3?)*
- Explore another codebase in the library with the five rules: the
  Rust Cookbook (`repos/rust-cookbook`), or xv6 (`repos/xv6-riscv`).

## Checkpoint

The learner can, without help:
- [ ] Say the five rules for reading code
- [ ] Find a program's entry point and a named function with `grep`
- [ ] Build and run clox
- [ ] Compare clox's scanner with Pickaxe's, with three matching pieces
- [ ] Answer a question about a program by reading its code

## Lab notebook

Copy the five rules and the Pickaxe/clox table. Write in `JOURNAL.md`
what you'd borrow from clox. Commit. Add *codebase*, *entry point* and
*convention* to `dictionary.md`.

## Guide's background *(optional reading)*

clox is the bytecode interpreter from Part III of *Crafting
Interpreters* (the code is MIT-licensed; the repository's `c` folder
holds the finished version). Its scanner is the same as Pickaxe's in
spirit but scans "on demand", one token at a time as the compiler asks,
rather than making the whole list first. The `//>` and `//<` markers are
the author's tool for weaving the book's text and code together.

`typedef double Value;` is the simple version; the `NAN_BOXING`
version above it packs every Lox value into a single 64-bit double,
using the many unused bit patterns of "not a number". Reading strategies
like these five rules are what professional programmers use when they
join a new project; tools like `grep`, `ctags` and an editor's "go to
definition" help with bigger codebases.
