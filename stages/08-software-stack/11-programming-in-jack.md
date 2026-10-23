# Lesson 8.11: Programming in Jack (Project 9)

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the Jack card · **New words:** Jack, class, subroutine,
operating system (OS)

## Goal *(read this to the learner)*

> Writing VM code by hand is slow. **Jack** is a real programming
> language, a bit like Python and a bit like C, made for the Hack
> computer. It has variables, loops, functions and classes, and an
> **operating system** with ready-made tools for printing, drawing and
> reading the keyboard. Today you'll write Jack programs and run them,
> using the official Jack compiler. Later in this stage you'll write the
> compiler yourself.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check that `jackc` and `vme` are in `~/bin` (Lesson 8.6).
- [ ] Have the Jack card printed.

## Warm-up (5 min)

"What does the VM translator do?" *(Turns VM code into Hack assembly.)*
"Where does VM code come from, usually?" *(A compiler makes it, from a
language like Jack.)*

## Activity

### Session 1: hello, and loops

1. **Hello.** Make a folder for each program. In the terminal:
   ```
   mkdir -p ~/lab/n2t/projects/9/Hello
   ```
   In Thonny, make `~/lab/n2t/projects/9/Hello/Main.jack`:
   ```
   // My first Jack program.
   class Main {
       function void main() {
           do Output.printString("Hello from Jack!");
           do Output.println();
           do Output.printString("6 times 7 is ");
           do Output.printInt(6 * 7);
           do Output.println();
           return;
       }
   }
   ```
   **Say:** "Every Jack program starts at `Main.main`. Everything lives in
   a **class**, and the functions inside are called **subroutines**.
   `do` calls a subroutine and ignores its answer. `Output` is part of
   Jack's **operating system**, or **OS**: a set of classes that every
   program can use. Every subroutine ends with `return`, even when it
   gives nothing back."

2. **Compile and run.**
   ```
   cd ~/lab/n2t/projects/9
   jackc Hello
   ls Hello
   ```
   **They should see:** `Compiling ...Hello`, then `Main.jack` and
   `Main.vm`. **Say:** "`jackc` is the official Jack compiler: it turned
   `Main.jack` into VM code, `Main.vm`." Look inside: `cat Hello/Main.vm`.
   **Ask:** "Can you find `push constant 6` and `push constant 7`? What
   comes after?" *(`call Math.multiply 2`: Hack has no multiply, so the
   OS does it.)*

   Open `vme`. **Load Program**, and choose the *folder* `Hello` (click
   it once, then **Load Program**). A box asks whether to use the
   built-in implementation of the OS functions: click **Yes**. Set
   **Animate** to **No animation**, and Run (the double arrow).
   **They should see:** on the emulator's screen, `Hello from Jack!` and
   `6 times 7 is 42`, then a box saying `Program Halted: Main.main
   finished execution`. Click OK.

3. **Loops.** New folder `Squares`, with `Main.jack`:
   ```
   // Prints the square numbers from 1 to 10.
   class Main {
       function void main() {
           var int i;
           let i = 1;
           while (i < 11) {
               do Output.printInt(i);
               do Output.printString(" squared is ");
               do Output.printInt(i * i);
               do Output.println();
               let i = i + 1;
           }
           return;
       }
   }
   ```
   **Say:** "`var int i;` makes a local variable, and it must come at the
   very start of the subroutine. Changing a variable needs `let`. There's
   no `<=` in Jack, so 'up to 10' is `i < 11`." Compile (`jackc Squares`)
   and run it in `vme`. **They should see:** ten lines, from `1 squared is
   1` to `10 squared is 100`. Commit.

### Session 2: the keyboard, and the screen

4. **Guess my number.** New folder `Guess`, with `Main.jack`:
   ```
   // Guess my number.
   class Main {
       function void main() {
           var int secret, guess, tries;
           let secret = 37;
           let tries = 0;
           let guess = 0;
           do Output.printString("I'm thinking of a number from 1 to 100.");
           do Output.println();
           while (~(guess = secret)) {
               let guess = Keyboard.readInt("Your guess? ");
               let tries = tries + 1;
               if (guess < secret) {
                   do Output.printString("Too low!");
                   do Output.println();
               }
               if (guess > secret) {
                   do Output.printString("Too high!");
                   do Output.println();
               }
           }
           do Output.printString("Yes! You got it in ");
           do Output.printInt(tries);
           do Output.printString(" tries.");
           return;
       }
   }
   ```
   **Say:** "`~` means *not*, and `=` compares (Jack has no `==`). So the
   loop goes on while the guess isn't the secret. `Keyboard.readInt`
   prints a question and waits for a number and Enter."

   Compile and run. In the emulator, **click the keyboard bar under the
   screen first**, then type a guess and press Enter. **They should
   see:** `Too high!` or `Too low!`, until 37, then `Yes! You got it in
   ... tries.`

   **Ask:** "Use binary search from Lesson 7.2. How many guesses should
   it take, at most?" *(7: 100 halves to 1 in seven steps.)*

5. **Drawing.** New folder `Tower`, with `Main.jack`:
   ```
   // Draws Numberblocks towers: block n is a tower of n squares.
   class Main {
       function void main() {
           var int n;
           let n = 1;
           while (n < 11) {
               do Main.tower(n, (n * 40) + 20);
               let n = n + 1;
           }
           return;
       }

       /** Draws a tower of height squares, with its left side at x. */
       function void tower(int height, int x) {
           var int i, top;
           let i = 0;
           while (i < height) {
               let top = 230 - (i * 20);
               do Screen.drawRectangle(x, top, x + 18, top + 18);
               let i = i + 1;
           }
           return;
       }
   }
   ```
   **Say:** "The screen is 512 dots across and 256 down, and y counts
   *down* from the top, so `230 - (i * 20)` moves each square up.
   **Jack works strictly left to right**, with no times-before-plus:
   `n * 40 + 20` would be fine, but `20 + n * 40` would be `(20 + n) *
   40`. Always use brackets." Compile and run. **They should see:** ten
   towers, from one square to ten, getting taller from left to right.
   Commit.

### Session 3: mistakes, and your own program

6. **Read the compiler's messages.** In `Squares/Main.jack`, take the `;`
   off `let i = i + 1;` and compile. **They should see:**
   ```
   In Main.jack (line 12): In subroutine main: Expected ;
   ```
   Put it back. Try `while (i <= 10)`: `Expected - or ~ or ( in term`.
   **Say:** "That one means Jack didn't expect `=` after `<`: there's no
   `<=`." Put it back.

7. **Your own program.** The learner writes a program of their own, in a
   new folder. Ideas:
   - the times table of any number, using `Keyboard.readInt`;
   - a Collatz program (Stage 3) that prints every step;
   - a picture with `Screen.drawLine` and `Screen.drawCircle`.

   Compile, run and commit it.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Expected ;` | A missing semicolon on that line | Add it. |
| `Expected statement(do, let, while, return or if)` | A line that isn't a statement: often `i = i + 1;` without `let`, or a call without `do` | Start every statement with its word. |
| `Program flow may reach end of subroutine without 'return'` | The subroutine has no `return` at the end | Add `return;`, even in a `void` one. |
| `j is not defined as a field, parameter or local or static variable` | A variable used without `var`, or a typo | Add it to the `var` line, or fix the name. |
| `Expected - or ~ or ( in term` | Something Jack doesn't have, like `<=` or `'a'` | Use `~(a > b)`, and 97 for `a`. |
| The emulator says `output.printInt not found` | A capital letter is missing: `output` instead of `Output` | Class names start with a capital. |
| Nothing happens when typing | The keyboard bar wasn't clicked | Click the bar under the screen, then type. |
| A sum gives a strange answer | Jack works left to right: `2 + 3 * 4` is 20 | Use brackets: `2 + (3 * 4)`. |
| Loading asks about built-in functions | The OS isn't in the folder (that's normal) | Click Yes. |

## Talk about it

- What's a class? What's a subroutine?
- What's the operating system for? Name three OS classes.
- How is Jack like Python? How is it different?
- Why does `2 + 3 * 4` give 20 in Jack?

## Challenge *(if there's time, or for next time)*

- Change `Guess` so the secret is different each time. *(Hint: count how
  long the player takes to press a key at the start, like a stopwatch,
  and use that. There's no random in Jack!)*
- Draw a Creeper face with `Screen.drawRectangle`, using
  `Screen.setColor(false)` to draw in white.
- Look at the Nand to Tetris examples in `~/lab/n2t/projects/9`
  (`Square`, `Pong`, `List`, `Fraction`), and run them.

## Checkpoint

The learner can, without help:
- [ ] Write a Jack program with variables, `while`, `if` and functions
- [ ] Compile it with `jackc`, and run it in `vme`
- [ ] Use `Output`, `Keyboard` and `Screen` from the OS
- [ ] Read a Jack compile error and fix it

## Lab notebook

Copy one program, and label `class`, `function`, `var`, `let`, `do` and
`return`. Sketch the towers. Commit. Add *Jack*, *class*, *subroutine*
and *operating system* to `dictionary.md`.

## Guide's background *(optional reading)*

This is Nand to Tetris Project 9: learn Jack by writing programs in it.
Jack is deliberately small, so that a compiler for it fits in two
lessons: no operator precedence, no `for`, statements that each begin
with a keyword (`let`, `do`, `if`, `while`, `return`), variables
declared at the top. Its OS (Lesson 8.17) provides arithmetic,
strings, memory, screen, text output and keyboard input.

The VM Emulator can run the OS in two ways: its own **built-in** version
(written in Java, so it's fast), which it offers when the folder has no
OS `.vm` files; or the OS written in Jack, as VM code. Later in this
stage, the learner's own OS classes replace the built-in ones one by
one.

`Keyboard.readInt` reads digits until Enter. The emulator only sees keys
while its keyboard bar is active (yellow), which is the most common
"it's not working" moment in this lesson.
