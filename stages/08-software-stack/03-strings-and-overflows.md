# Lesson 8.3: Strings, Overflows and Crashes

**Time:** 2 sessions of 45 min · **You need:** a terminal and an editor;
`~/lab/c`; squared paper · **New words:** string, null character,
buffer, buffer overflow, segmentation fault, sanitizer, debugger

## Goal *(read this to the learner)*

> In C, a word is just a row of `char` boxes, with a 0 at the end to
> say "stop here". C never checks that the word fits in its boxes. Today
> you'll overflow a box on purpose, and watch what happens: sometimes
> nothing, sometimes a crash, and sometimes something much worse. Then
> you'll meet two tools that catch these bugs: the **sanitizer** and the
> **debugger**.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Draw eight boxes in a row on squared paper.

## Warm-up (5 min)

"What does `chest[7]` give, in an array of 5?" *(Whatever happens to be
there: C doesn't check.)* "What would Python do?" *(Stop with an
`IndexError`.)*

## Activity

### Session 1: strings are boxes too

1. **A word in boxes.** On the paper, write S, t, e, v, e in the first
   five boxes, and 0 in the sixth. **Say:** "In C, a **string** (a piece
   of text) is an array of `char`s, with a 0 at the end. That 0 is
   called the **null character**. It's how C knows where the word stops:
   there's no length stored anywhere."

2. **A name.** New file, `~/lab/c/name.c`:
   ```c
   #include <stdio.h>
   #include <string.h>

   int main(void) {
       char name[8];
       strcpy(name, "Steve");
       printf("Hello, %s! Your name has %zu letters.\n", name, strlen(name));
       for (int i = 0; i < 8; i++) {
           printf("%d ", name[i]);
       }
       printf("\n");
       strcpy(name, "Captain Underpants");
       printf("Hello, %s!\n", name);
       return 0;
   }
   ```
   **Say:** "`char name[8]` is a row of 8 boxes: a **buffer**, which means
   a place to put data. `strcpy` (string copy) copies a word into it,
   with its 0. `strlen` counts letters until it reaches the 0. `%s`
   prints a string."

3. **Compile it.**
   ```
   gcc name.c -o name
   ```
   **They should see** a warning:
   ```
   name.c: In function ‘main’:
   name.c:12:5: warning: ‘__builtin_memcpy’ writing 19 bytes into a region of size 8 overflows the destination [-Wstringop-overflow=]
      12 |     strcpy(name, "Captain Underpants");
         |     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   name.c:5:10: note: destination object ‘name’ of size 8
       5 |     char name[8];
         |          ^~~~
   ```
   **Say:** "A warning isn't an error: `gcc` still made the program. But
   it's telling us something important. **Ask:** "Why 19 bytes?"
   *("Captain Underpants" is 18 characters, counting the space, plus the
   0 at the end.)*

4. **Run it anyway.**
   ```
   ./name
   ```
   **They should see:**
   ```
   Hello, Steve! Your name has 5 letters.
   83 116 101 118 101 0 0 0
   Hello, Captain Underpants!
   *** stack smashing detected ***: terminated
   Aborted (core dumped)
   ```
   The last two numbers on the second line might be different: nobody
   put anything in those boxes. **Say:** "83 is S, 116 is t... and then
   the 0 that ends the word. Then `strcpy` wrote 19 bytes into 8 boxes.
   The other 11 went *past the end*, over whatever was next in memory.
   This is called a **buffer overflow**. It even printed the whole name!
   But when `main` finished, a guard value that the compiler had put
   after the boxes was smashed, so the program stopped itself."

   **Ask:** "What if the boxes after `name` had held something
   important, like a password, or the address to go back to when the
   function ends?" *(It would be changed. An attacker who chooses what
   gets written could take over the program.)* **Say:** "That's exactly
   how many real attacks have worked, for over thirty years. The guard
   is one of the defences. In Stage 11 you'll see more."

5. **Fix it the safe way.** Change the second `strcpy` line to:
   ```c
   snprintf(name, sizeof(name), "%s", "Captain Underpants");
   ```
   Compile and run. **They should see** a new warning, `‘%s’ directive
   output truncated writing 18 bytes into a region of size 8`, and then
   `Hello, Captain!` and no crash. **Say:** "`snprintf` is told the size
   of the buffer, so it stops before the end and still puts a 0 in the
   last box: 7 letters and a 0. **Truncated** means cut short. That's
   what we wanted here, so this warning is fine: the name is cut, but
   nothing is overwritten." Commit.

### Session 2: catching the bugs

6. **The sanitizer.** Put the bad `strcpy` back (or use `git checkout
   name.c`), and compile with two extra options:
   ```
   gcc -g -fsanitize=address name.c -o name
   ./name
   ```
   **They should see** the first two lines, then a big red report that
   starts:
   ```
   =================================================================
   ==31==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7c81a8100028 ...
   WRITE of size 19 at 0x7c81a8100028 thread T0
       #0 0x... in memcpy ...
       #1 0x... in main /home/sam/lab/c/name.c:12
   ```
   and further down:
   ```
       [32, 40) 'name' (line 5) <== Memory access at offset 40 overflows this variable
   ```
   **Say:** "The **sanitizer** adds checks around every bit of memory, so
   the program stops at the *exact moment* it goes wrong: a write of 19
   bytes, in `main`, at line 12 of `name.c`, overflowing `name` from line
   5. `-g` puts the line numbers in. The program is slower and bigger
   with these checks, so we use them while testing, like a test harness
   in Nand to Tetris."

7. **A crash.** New file, `crash.c`:
   ```c
   #include <stdio.h>

   int count_blocks(int *row) {
       return row[0] + row[1];
   }

   int main(void) {
       int row[2] = {3, 4};
       int *missing = NULL;
       printf("%d\n", count_blocks(row));
       printf("%d\n", count_blocks(missing));
       return 0;
   }
   ```
   ```
   gcc -g crash.c -o crash
   ./crash
   ```
   **They should see:**
   ```
   7
   Segmentation fault (core dumped)
   ```
   **Say:** "`NULL` is address 0: a pointer that points at nothing. Linux
   doesn't let any program use address 0, so it stopped it. A
   **segmentation fault** means 'you touched memory that isn't yours'.
   It doesn't say where. For that, we need a detective."

8. **The debugger.** Run it inside `gdb`, the GNU debugger:
   ```
   gdb ./crash
   ```
   At the `(gdb)` prompt, type `run`. **They should see**, after some
   start-up lines:
   ```
   Program received signal SIGSEGV, Segmentation fault.
   0x00005820c1c47179 in count_blocks (row=0x0) at crash.c:4
   4	    return row[0] + row[1];
   ```
   Then type `bt` (backtrace):
   ```
   #0  0x00005820c1c47179 in count_blocks (row=0x0) at crash.c:4
   #1  0x00005820c1c471e8 in main () at crash.c:11
   ```
   **Say:** "The **debugger** runs the program and catches it when it
   falls over. Line 4, in `count_blocks`, and `row=0x0`: the pointer was
   0. The backtrace is the call stack, like the nesting dolls in Lesson
   7.5: `main` called `count_blocks` from line 11." Type `quit` (and `y`
   if it asks).

   Fix `crash.c` so that `count_blocks` checks first:
   ```c
   int count_blocks(int *row) {
       if (row == NULL) {
           return 0;
       }
       return row[0] + row[1];
   }
   ```
   Compile and run: `7`, then `0`. Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `*** stack smashing detected ***: terminated` | A buffer on the stack was overflowed | Compile with `-g -fsanitize=address` to find where. |
| `Segmentation fault (core dumped)` | The program used memory that isn't its own: often a `NULL` pointer, or an index far past the end | Run it in `gdb`, then `run` and `bt`. |
| `gdb` says `in count_blocks ()`, with no file or line number | It was compiled without `-g` | Compile again with `-g`. |
| The name prints with strange letters after it | The 0 at the end is missing, so `%s` kept going | Leave room for the 0, and use `snprintf`. |
| No red report from the sanitizer | It was compiled without `-fsanitize=address` | Compile with both options. |
| `(gdb)` won't go away | Still in the debugger | `quit`, then `y`. |

## Talk about it

- How does C know where a string ends?
- What's a buffer overflow? Why is it dangerous, not just a crash?
- What does the sanitizer tell you that a segmentation fault doesn't?
- What's a backtrace?

## Challenge *(if there's time, or for next time)*

- Write your own `my_strlen(char *s)`, which counts up to the 0. Check
  it against `strlen`.
- What does `printf("%s\n", name)` print if the 0 is replaced with a
  letter (`name[5] = 'X';`)? Try it with the sanitizer on, too.
- In `gdb`, try `break count_blocks`, then `run`, then `print row[0]`,
  then `continue`. A **breakpoint** stops the program at a function
  before anything goes wrong.

## Checkpoint

The learner can, without help:
- [ ] Draw a C string in boxes, with its null character
- [ ] Explain a buffer overflow, and why it's dangerous
- [ ] Find a bug with `-fsanitize=address`
- [ ] Find where a program crashed with `gdb`, `run` and `bt`

## Lab notebook

Draw "Steve" in eight boxes, then "Captain Underpants" spilling over the
end. Copy the backtrace. Commit. Add *string*, *null character*,
*buffer overflow*, *segmentation fault*, *sanitizer* and *debugger* to
`dictionary.md`.

## Guide's background *(optional reading)*

C strings are **null-terminated**: arrays of `char` ending with a 0
byte. Functions like `strcpy` copy until they reach the 0, with no idea
how big the destination is. Writing past the end of a buffer on the
**stack** can overwrite other local variables and the saved **return
address**, which is how classic "stack smashing" attacks took over
programs, starting with the Morris worm in 1988. Modern defences
include the **stack protector** (a "canary" value checked when the
function returns, which is what printed `stack smashing detected`),
ASLR (Lesson 8.2), and memory that can't be both written and run. They
make attacks harder, not impossible.

**AddressSanitizer** (`-fsanitize=address`) puts "poisoned" bytes around
every variable and checks every memory access, at a cost of roughly
twice the time and memory. **gdb** is the standard debugger on Linux;
with `-g`, the executable carries a map from machine code back to
source lines. Rust (Stage 9) makes this whole family of bugs impossible
in ordinary code: the compiler refuses to build a program that could
write past the end of a buffer or use a null pointer.

The red sanitizer report's numbers (`==31==`, the addresses) differ
every run. Only the words matter.
