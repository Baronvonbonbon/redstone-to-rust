# Lesson 8.1: Hello, C

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor
(Thonny, or `nano`); the C tools from setup · **New words:** C,
compiler, compile, source code, executable, type, `printf`

## Goal *(read this to the learner)*

> Python reads your program and does it, one line at a time. **C** is
> different: a program called a **compiler** translates your whole
> program into machine code first, like the assembler you wrote in
> Lesson 6.13, but for a much bigger language. Then the computer runs
> the machine code directly, very fast. C is fifty years old, and most of
> Linux is written in it. Today you'll write, compile and run your first
> C programs, and race C against Python.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] The C tools need installing once, while online, from your own
      account: `./scripts/install-packages.sh --later`. Check, in the
      learner's account: `gcc --version` prints a version number.
- [ ] The learner's C programs will live in `~/lab/c`.

## Warm-up (5 min)

"What did your assembler do?" *(Translated Hack assembly into binary
machine code.)* "Python doesn't do that. How does a Python program run?"
*(Python reads it and does each line.)*

## Activity

### Session 1: hello, and compiling

1. **The folder.** In the terminal:
   ```
   mkdir -p ~/lab/c
   cd ~/lab/c
   git init
   ```
   **Say:** "Every C program in this stage lives here, with git watching."

2. **The first program.** In Thonny (or `nano hello.c`), make
   `~/lab/c/hello.c`:
   ```c
   #include <stdio.h>

   int main(void) {
       printf("Hello from C!\n");
       return 0;
   }
   ```
   **Say:** "Lots of new things, but only a few ideas:
   - `#include <stdio.h>` brings in the standard input and output tools,
     like `import` in Python. `printf` lives there.
   - Every C program starts at a function called `main`. `int` means it
     gives back a whole number when it ends: 0 means 'everything went
     fine', like a command's exit code in Lesson 5.
   - Curly brackets `{ }` hold the function's insides, instead of
     indenting. (We indent anyway, for people.)
   - Every statement ends with a semicolon `;`.
   - `\n` is a newline: `printf` doesn't add one by itself."

3. **Compile it, then run it.** In the terminal, in `~/lab/c`:
   ```
   gcc hello.c -o hello
   ./hello
   ```
   **They should see:** `Hello from C!`. **Say:** "`gcc` is the compiler.
   It read `hello.c`, the **source code**, and wrote `hello`, an
   **executable**: a file of machine code. `-o hello` chose its name. The
   `./` runs a program from this folder, like the scripts in Stage 5."

4. **Look at what it made.**
   ```
   ls -l hello hello.c
   file hello
   xxd hello | head -5
   ```
   **They should see:** `hello` is about 16,000 bytes, while `hello.c`
   is under 100. `file` says something like `ELF 64-bit LSB pie
   executable, x86-64`. `xxd` shows bytes that mean nothing to people.
   **Say:** "ELF is the format Linux uses for programs. x86-64 is the
   family of processor in this computer: a real CPU, with a machine
   language much bigger than Hack's, but the same idea. Most of those
   16,000 bytes are the setup that every program needs to start."

   **Ask:** "Could you send `hello` to a friend with a Raspberry Pi?"
   *(No: the Pi's processor speaks a different machine language. They'd
   need `hello.c`, and compile it there.)*

5. **Break it on purpose.** Take away the `;` after the `printf(...)`
   line, save, and compile again. **They should see:**
   ```
   hello.c: In function ‘main’:
   hello.c:4:30: error: expected ‘;’ before ‘return’
       4 |     printf("Hello from C!\n")
         |                              ^
         |                              ;
       5 |     return 0;
         |     ~~~~~~
   ```
   **Say:** "`4:30` means line 4, column 30. The compiler even drew where
   the `;` goes. With an error, there's no new program: `./hello` still
   runs the old one." Put the `;` back, compile, and commit:
   ```
   git add hello.c
   git commit -m "Hello from C"
   ```
   **Say:** "We commit the `.c` file, not `hello`. The program can always
   be made again from the source."

### Session 2: types, and a race

6. **Every variable has a type.** New file, `types.c`:
   ```c
   #include <stdio.h>

   int main(void) {
       int diamonds = 64;
       double health = 9.5;
       char letter = 'C';
       printf("%d diamonds, %.1f hearts, letter %c\n", diamonds, health, letter);
       printf("letter as a number: %d\n", letter);
       printf("7 / 2 = %d, but 7.0 / 2 = %.1f\n", 7 / 2, 7.0 / 2);
       int big = 2147483647;
       big = big + 1;
       printf("biggest int plus one: %d\n", big);
       return 0;
   }
   ```
   Compile with `gcc types.c -o types` and run `./types`. **They should
   see:**
   ```
   64 diamonds, 9.5 hearts, letter C
   letter as a number: 67
   7 / 2 = 3, but 7.0 / 2 = 3.5
   biggest int plus one: -2147483648
   ```
   **Say:** "In C, you say what **type** each variable is when you make
   it, and it can never change: `int` for whole numbers, `double` for
   numbers with a point, `char` for one letter. In `printf`, `%d` means
   'put a whole number here', `%.1f` a number with one place after the
   point, and `%c` a letter. A `char` is really a number: 'C' is 67, the
   ASCII code from Stage 4."

   **Ask:** "Why did the biggest int plus one go negative?" *(An `int` is
   32 bits here. It wraps round, like the 16-bit numbers in Lesson 6.5:
   two's complement!)* "Python's numbers grow as big as they need. C's
   don't, because C uses the CPU's own registers, exactly as they are."

7. **Loops in C.** New file, `blocks.c`:
   ```c
   #include <stdio.h>

   int main(void) {
       int blocks = 0;
       for (int row = 1; row <= 5; row++) {
           for (int i = 0; i < row; i++) {
               printf("[]");
           }
           blocks = blocks + row;
           printf("  %d blocks so far\n", blocks);
       }
       return 0;
   }
   ```
   **They should see:**
   ```
   []  1 blocks so far
   [][]  3 blocks so far
   [][][]  6 blocks so far
   [][][][]  10 blocks so far
   [][][][][]  15 blocks so far
   ```
   **Say:** "A C `for` loop has three parts: start (`int row = 1`), keep
   going while (`row <= 5`), and after each time round (`row++`, which
   means add 1). It's the same as Python's `for row in range(1, 6)`."
   **Ask:** "Where have you seen 1, 3, 6, 10, 15 before?" *(Triangle
   numbers: the staircase from Lesson 7.9.)*

8. **The race.** Two programs that add up the numbers below 100 million.
   `count.py`:
   ```python
   total = 0
   for i in range(100000000):
       total = total + i
   print(total)
   ```
   and `count.c`:
   ```c
   #include <stdio.h>

   int main(void) {
       long total = 0;
       for (long i = 0; i < 100000000; i++) {
           total = total + i;
       }
       printf("%ld\n", total);
       return 0;
   }
   ```
   **Say:** "`long` is a 64-bit whole number, because the answer is too
   big for an `int`. `%ld` prints one." Then:
   ```
   gcc count.c -o count
   time ./count
   time python3 count.py
   ```
   **They should see:** both print `4999999950000000`. C takes something
   like a quarter of a second; Python something like 15 seconds, about
   50 times longer. (Your times will be different; the gap won't be.)

   **Ask:** "Why is C so much faster?" *(It was translated to machine
   code once, before running. Python works out what each line means
   again, every time round the loop.)* Commit all three programs.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `gcc: command not found` | The C tools aren't installed | The guide runs `./scripts/install-packages.sh --later`. |
| `error: expected ‘;’ before ...` | A missing semicolon, usually at the end of the line *before* the one named | Add the `;`. |
| `bash: ./hello: No such file or directory` | It wasn't compiled, or the compile failed | Compile again, and read the errors. |
| The program does the old thing | The file was changed but not compiled again | Save, compile, then run. Every time! |
| `warning: implicit declaration of function ‘printf’` | `#include <stdio.h>` is missing | Add it at the top. |
| A `%d` prints a strange number | The `%` code doesn't match the type (`%d` with a `double`) | `%d` for `int`, `%ld` for `long`, `%f` for `double`, `%c` for `char`. |

## Talk about it

- What does a compiler do? How is it like your assembler?
- Why can't you send the compiled program to a computer with a different
  processor?
- What's a type? Why does C need you to say it?

## Challenge *(if there's time, or for next time)*

- Write `table.c`: the 7 times table, using a `for` loop and `printf`.
- Try `gcc -O2 count.c -o count` (that's a capital O, for "optimise"),
  and time it again. It's so fast that the compiler must have done
  something clever. What might it be? *(It worked out the answer while
  compiling, so the loop never runs at all!)*
- Make `int big` a `long` instead. How big can it get now?

## Checkpoint

The learner can, without help:
- [ ] Write, compile and run a C program with `printf` and a `for` loop
- [ ] Explain the difference between source code and an executable
- [ ] Read a compile error's line and column, and fix it
- [ ] Say why C is faster than Python, and why its `int`s wrap round

## Lab notebook

Copy the race times. Write down the four `printf` codes. Commit. Add
*C*, *compiler*, *source code*, *executable* and *type* to
`dictionary.md`.

## Guide's background *(optional reading)*

C was made by Dennis Ritchie at Bell Labs around 1972, to write the Unix
operating system; Linux, Python itself, and most of the software
underneath everything else are written in it. It's a **compiled**
language: `gcc` (the GNU Compiler Collection) translates C into x86-64
assembly, assembles it, and **links** it with the C library to make an
ELF executable. Python is **interpreted**: the `python3` program reads
your code and carries it out. That's the main reason for the speed gap
in the race.

C is in this course briefly and on purpose. It shows memory as it really
is (addresses, bytes, and nothing checking what you do with them), which
is exactly what the next three lessons explore, and exactly the set of
problems Rust (Stage 9) was designed to prevent. The second half of this
stage then builds a compiler of the learner's own, for the Jack language
of Nand to Tetris.

The race numbers came from one computer: about 0.27 seconds for C and
15 for Python. With `-O2`, gcc notices that the loop's answer can be
worked out without running it.
