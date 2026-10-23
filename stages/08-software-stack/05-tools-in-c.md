# Lesson 8.5: Your Own Tools in C

**Time:** 2 sessions of 45 min · **You need:** a terminal and an editor;
`~/lab/c` · **New words:** `argc`, `argv`, standard input, filter,
`EOF`, Makefile, `make`

## Goal *(read this to the learner)*

> `ls`, `cat`, `wc` and `grep` are C programs, just like yours. Today
> you'll write two tools of your own that work the same way: a ROT13
> secret-code machine that works in a pipe, and your own `wc` that
> counts lines, words and letters in a file. Then you'll teach the
> computer how to build them with a **Makefile**, so one word, `make`,
> builds everything.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Remember ROT13 from Stage 1 (`tr 'A-Za-z' 'N-ZA-Mn-za-m'`).

## Warm-up (5 min)

"In bash, how does a script get the words typed after its name?" *(`$1`,
`$2`...)* "In Python?" *(`sys.argv`, from the assembler.)* "What does a
pipe `|` do?" *(Sends one program's output into the next one's input.)*

## Activity

### Session 1: arguments, and a filter

1. **The words after the name.** New file, `~/lab/c/args.c`:
   ```c
   #include <stdio.h>

   int main(int argc, char *argv[]) {
       printf("argc is %d\n", argc);
       for (int i = 0; i < argc; i++) {
           printf("argv[%d] is \"%s\"\n", i, argv[i]);
       }
       return 0;
   }
   ```
   Compile, then run `./args hello "two words" 42`. **They should see:**
   ```
   argc is 4
   argv[0] is "./args"
   argv[1] is "hello"
   argv[2] is "two words"
   argv[3] is "42"
   ```
   **Say:** "`main` can take two things: `argc`, the count of words, and
   `argv`, an array of strings. `char *argv[]` means 'an array of
   pointers to `char`': each one points at a word. Word 0 is the
   program's own name. The quotes made 'two words' into one argument.
   And `42` is a string, not a number: every argument is text." (`\"`
   puts a `"` inside a string.)

2. **ROT13 as a filter.** New file, `rot13.c`:
   ```c
   #include <stdio.h>

   int main(void) {
       int c;
       while ((c = getchar()) != EOF) {
           if (c >= 'a' && c <= 'z') {
               c = 'a' + (c - 'a' + 13) % 26;
           } else if (c >= 'A' && c <= 'Z') {
               c = 'A' + (c - 'A' + 13) % 26;
           }
           putchar(c);
       }
       return 0;
   }
   ```
   **Say:**
   - "`getchar()` reads one character from **standard input**: from the
     keyboard, or from a pipe. At the end, it gives `EOF`, end of file.
   - `(c = getchar()) != EOF` reads a character into `c` *and* checks it,
     both at once.
   - `c - 'a'` turns a to z into 0 to 25. Add 13, and `% 26` wraps it
     round: the Caesar wheel from Stage 0!
   - `&&` means *and*. `putchar` writes one character out."

   Compile, then:
   ```
   echo "Hello, Steve!" | ./rot13
   echo "Hello, Steve!" | ./rot13 | ./rot13
   ```
   **They should see:** `Uryyb, Fgrir!`, then `Hello, Steve!` again.
   **Say:** "A program that reads standard input, changes it, and writes
   standard output is called a **filter**. `sort`, `grep` and `tr` are
   filters too. Doing ROT13 twice brings you back, because 13 + 13 is 26."

   Run `./rot13` on its own and type some lines. Each line comes back
   coded. Press **Ctrl+D** at the start of a line to send `EOF`.

### Session 2: files, errors, and make

3. **Count words.** New file, `count_words.c`:
   ```c
   #include <stdio.h>

   int main(int argc, char *argv[]) {
       if (argc != 2) {
           fprintf(stderr, "Usage: %s FILE\n", argv[0]);
           return 1;
       }
       FILE *f = fopen(argv[1], "r");
       if (f == NULL) {
           perror(argv[1]);
           return 1;
       }
       long lines = 0, words = 0, chars = 0;
       int in_word = 0;
       int c;
       while ((c = fgetc(f)) != EOF) {
           chars++;
           if (c == '\n') {
               lines++;
           }
           if (c == ' ' || c == '\n' || c == '\t') {
               in_word = 0;
           } else if (!in_word) {
               in_word = 1;
               words++;
           }
       }
       fclose(f);
       printf("%ld %ld %ld %s\n", lines, words, chars, argv[1]);
       return 0;
   }
   ```
   **Say:**
   - "`fopen` opens a file, and gives back a pointer to a `FILE`, or
     `NULL` if it can't. `fgetc` is `getchar` for a file.
   - `fprintf(stderr, ...)` prints to **standard error**: a second
     output, just for messages. It shows on the screen too, but `>`
     doesn't catch it, so a message never ends up in your output file.
   - `perror` prints why the last thing failed, in words.
   - `||` means *or*, and `!` means *not*.
   - The word count goes up when a letter comes *after* a space: that's
     what `in_word` remembers."

   Make a test file:
   ```
   printf 'Creepers are green.\nThey go  BOOM\n\nand ruin your house.\n' > poem.txt
   ```
   Compile, then compare with the real `wc`:
   ```
   ./count_words poem.txt
   wc poem.txt
   ```
   **They should see:** `4 10 56 poem.txt` from both (`wc` puts a space
   in front). Then try the mistakes:
   ```
   ./count_words
   echo $?
   ./count_words nothing.txt
   echo $?
   ```
   **They should see:** `Usage: ./count_words FILE`, then `1`;
   `nothing.txt: No such file or directory`, then `1`. Try
   `./count_words > out.txt`: the usage message still appears on the
   screen, and `out.txt` is empty. That's standard error at work.
   **Say:** "`return 1` from `main` is the exit code that `$?` shows,
   like `exit 1` in a bash script. That's how other programs know
   something went wrong."

   Try it on its own source: `./count_words count_words.c` and
   `wc count_words.c`. *(The same: `31 106 703`.)*

4. **A Makefile.** Typing `gcc` lines gets boring. Make a file called
   exactly `Makefile` (capital M, no ending):
   ```
   all: rot13 count_words

   rot13: rot13.c
   	gcc -Wall -g rot13.c -o rot13

   count_words: count_words.c
   	gcc -Wall -g count_words.c -o count_words

   clean:
   	rm -f rot13 count_words
   ```
   **The indented lines must start with a Tab, not spaces.** (Thonny puts
   spaces; use `nano`, which keeps a Tab.) **Say:** "Each rule says: to
   make *this* (before the colon), you need *these* (after it), and here's
   the command. `-Wall` turns on all the useful warnings."

   ```
   make clean
   make
   make
   touch rot13.c
   make
   ```
   **They should see:** the first `make` runs both `gcc` lines. The second
   says `make: Nothing to be done for 'all'.` After `touch` (which makes a
   file look changed), only rot13 is compiled again. **Say:** "`make`
   looks at the times on the files. It only rebuilds what's older than
   what it's made from. Big programs, like Linux itself, have thousands
   of files, so this saves hours." Commit the Makefile and the programs
   (not the compiled ones: add a `.gitignore` with `rot13`,
   `count_words`, and the others).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Makefile:4: *** missing separator.  Stop.` | The command line starts with spaces, not a Tab | Delete the spaces and press Tab, in `nano`. |
| `make: *** No rule to make target 'rot13.c'` | The file's name is different, or it's in another folder | `ls`, and match the names. |
| `./rot13` waits for ever | It's reading the keyboard | Type a line, or press Ctrl+D to finish. |
| The word count is too high | Two spaces in a row count two words | Only count when `in_word` was 0. |
| `count_words` agrees with `wc` on lines but not words | `wc` also counts other kinds of space | Fine for us: our files only use spaces, newlines and Tabs. |

## Talk about it

- What are `argc` and `argv`? Why is `argv[0]` the program's name?
- What's a filter? Name three.
- Why does `main` return a number?
- What does `make` do, and how does it know what to rebuild?

## Challenge *(if there's time, or for next time)*

- Make `count_words` work on any number of files, like `wc`: loop over
  `argv[1]` to `argv[argc - 1]`, and print a total line.
- Write `upper.c`, a filter that turns every letter into a capital.
  (`'a' - 'A'` is 32.)
- Write `mycat.c`: print each file named in `argv`, or standard input if
  there are none.
- Run `make` with `-Wall` and fix every warning in your Stage 8 programs.

## Checkpoint

The learner can, without help:
- [ ] Use `argc` and `argv` in a C program
- [ ] Write a filter with `getchar` and `putchar`, and use it in a pipe
- [ ] Open a file, handle errors, and return an exit code
- [ ] Write a Makefile, and explain how `make` decides what to rebuild

This is the end of the C unit. The learner can also, without help:
- [ ] Explain pointers, the stack and the heap, and find a memory bug
      with the sanitizer or valgrind (Lessons 8.2 to 8.4)

## Lab notebook

Write the Makefile out by hand, with arrows from each thing to what it's
made from. Commit. Add *argv*, *standard input*, *filter*, *EOF* and
*Makefile* to `dictionary.md`.

## Guide's background *(optional reading)*

Unix programs are built to be small and to combine: each reads standard
input or files named in `argv`, writes standard output, sends messages
to standard error, and reports success or failure with its exit code.
The learner's `rot13` and `count_words` follow all of these rules, so
they work with pipes, redirection and `$?` exactly like the tools from
Stages 1 and 5.

`make` (1976) compares file modification times and runs the commands of
any rule whose target is older than its prerequisites. The Tab rule is a
famous early design mistake that can't be changed now, because too many
Makefiles depend on it. Rust (Stage 9) uses `cargo` instead, which does
`make`'s job and fetches libraries too.

This lesson ends the short C unit. The rest of the stage goes back to
the Hack computer from Stage 6 and climbs from machine code up to a
high-level language, an operating system and a game: Nand to Tetris,
Projects 7 to 12.
