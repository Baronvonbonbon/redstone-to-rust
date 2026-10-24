# Lesson 10.3: Making Processes: Fork, Exec and Zombies

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; `gcc` (from Stage 8); `~/lab/os` · **New words:** `fork`, `exec`,
`wait`, child, zombie, signal

## Goal *(read this to the learner)*

> How does a new process get made? On Linux, in a strange way: a process
> makes an exact copy of itself, and then the copy can turn itself into
> a different program. You'll do it in C, make a real **zombie** process
> (that's its official name!), and stop processes with **signals**.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Check `gcc --version` works (Stage 8).

## Warm-up (5 min)

"In `pstree`, every process had a parent. Who's the parent of a program
you run in the terminal?" *(The shell.)* "So how does the shell make a
new process?" *(Today's lesson!)*

## Activity

### Session 1: fork

1. **A copy of yourself.** **Say:** "Today's programs are in C, because C
   can call the kernel's `fork` directly. In Rust it's hidden inside the
   standard library." In `~/lab/c`, which has the Stage 8 programs, make
   `fork.c`:
   ```c
   #include <stdio.h>
   #include <sys/wait.h>
   #include <unistd.h>

   int main(void) {
       printf("I'm PID %d, and I'm about to fork.\n", getpid());
       fflush(stdout);
       int child = fork();
       if (child == 0) {
           printf("I'm the child! My PID is %d.\n", getpid());
       } else {
           wait(NULL);
           printf("I'm the parent. My child was PID %d.\n", child);
       }
       return 0;
   }
   ```
   ```
   gcc -Wall -o fork fork.c
   ./fork
   ```
   **They should see** (with different numbers):
   ```
   I'm PID 7120, and I'm about to fork.
   I'm the child! My PID is 7121.
   I'm the parent. My child was PID 7121.
   ```

2. **How did that happen?** Act it out. **Say:** "`fork` asks the kernel
   to copy this whole process: its memory, its variables, even where
   it's up to in the program. Now there are two, both just coming back
   from `fork`." Draw two boxes, one labelled *parent* and one *child*,
   both with an arrow at the line `int child = fork();`.
   - "`fork` gives back a different answer to each: 0 in the child, and
     the child's PID in the parent. That's how each one knows which it
     is."
   - "`wait(NULL)` makes the parent wait until the child finishes.
     That's why the child always prints first."

   **Ask:** "What would happen without the `wait`?" Try it: delete the
   `wait(NULL);` line, compile, and run it a few times. *(Now the parent
   usually prints first, and the child's line can even come after the
   next prompt. The parent and child run at the same time, and the
   kernel decides who goes first.)* Put the `wait` back.

3. **Why `fflush`?** Run it into a pipe:
   ```
   ./fork | cat
   ```
   It's the same. Now delete the `fflush(stdout);` line, compile, and
   run `./fork | cat` again. **They should see** the first line *twice*.
   **Say:** "When the output goes into a pipe, `printf` keeps the words
   in a bucket in memory, and writes them later. `fork` copied the
   bucket, words and all, so both processes wrote them. `fflush` empties
   the bucket before the copy." Put the line back.

### Session 2: exec, and zombies

4. **Becoming a different program.** Make `run.c`:
   ```c
   #include <stdio.h>
   #include <sys/wait.h>
   #include <unistd.h>

   int main(void) {
       int child = fork();
       if (child == 0) {
           execlp("echo", "echo", "Hello from a brand new program!", NULL);
           printf("This line never runs, unless exec failed.\n");
           return 1;
       }
       wait(NULL);
       printf("The child is finished, and I'm still here.\n");
       return 0;
   }
   ```
   ```
   gcc -Wall -o run run.c
   ./run
   ```
   **They should see:**
   ```
   Hello from a brand new program!
   The child is finished, and I'm still here.
   ```
   **Say:** "`exec` throws away the program the process is running and
   loads a new one: here, `echo`. The PID stays the same, but everything
   inside is new. That's why the next `printf` never runs: it's not
   there any more." **Ask:** "What's the first system call you saw in
   `strace` in Lesson 10.2?" *(`execve`: that's `exec`.)*

   **Say:** "This is exactly what the shell does for every command you
   type: `fork`, then `exec` in the child, then `wait`. In Lesson 10.9
   you'll write a shell of your own." Change `"echo"` to `"creeper"`
   (both times) and run it again. *(Now the `printf` does run: there's no
   program called `creeper`, so `exec` failed and came back.)* Change it
   back.

5. **A zombie!** Make `zombie.c`:
   ```c
   #include <stdio.h>
   #include <unistd.h>

   int main(void) {
       int child = fork();
       if (child == 0) {
           printf("Child %d: I'm done!\n", getpid());
           return 0;
       }
       printf("Parent %d: I'm not going to wait for my child for 60 seconds...\n", getpid());
       fflush(stdout);
       sleep(60);
       return 0;
   }
   ```
   ```
   gcc -Wall -o zombie zombie.c
   ./zombie &
   ps -o pid,ppid,stat,cmd
   ```
   **They should see** something like:
   ```
   Parent 7302: I'm not going to wait for my child for 60 seconds...
   Child 7303: I'm done!
       PID    PPID STAT CMD
      4321    4310 Ss   bash
      7302    4321 S    ./zombie
      7303    7302 Z    [zombie] <defunct>
      7304    4321 R+   ps -o pid,ppid,stat,cmd
   ```
   **Say:** "`&` runs a program in the background, so you can keep typing.
   Look at the child: `Z`, `<defunct>`. It's a **zombie**: it has
   finished, but it isn't completely gone. The kernel keeps a tiny
   record of it, with its exit code, until its parent `wait`s for it.
   This parent never does." **Ask:** "What's the `S` for the parent?"
   *(Sleeping: it's in `sleep(60)`.)*

   After 60 seconds (or press Enter until `Done` appears), run `ps -o
   pid,ppid,stat,cmd` again. **They should see:** the zombie has gone.
   **Say:** "When a parent ends, PID 1 adopts its children, and `wait`s
   for them, so zombies never last for ever."

### Session 3: signals

6. **Stopping things.**
   ```
   sleep 300 &
   jobs
   kill %1
   jobs
   ```
   **They should see:** `[1] 7400` (the job number and its PID), then
   `[1]+  Running                 sleep 300 &`, and after the `kill`,
   `[1]+  Terminated              sleep 300`. **Say:** "`kill` sends a
   **signal**: a message from the kernel that interrupts a process. The
   normal one, `TERM`, means 'please stop'." Show the list:
   ```
   kill -l
   ```
   **Say:** "Ctrl+C sends `INT` (interrupt), and `KILL` (number 9) can't
   be caught or ignored: the kernel just removes the process."

7. **Pausing.** Run `sleep 300` (no `&`), then press **Ctrl+Z**. **They
   should see:** `[1]+  Stopped                 sleep 300`. **Say:**
   "Ctrl+Z sends `TSTP`: pause. The process is frozen, not gone." Type
   `fg` to bring it back (it carries on sleeping), then Ctrl+C to stop
   it. **They should see** `^C` and the prompt. Commit the C programs.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `warning: implicit declaration of function ‘getpid’` (or ‘fork’, ‘sleep’) | `#include <unistd.h>` is missing | Add it at the top. |
| `warning: implicit declaration of function ‘wait’` | `#include <sys/wait.h>` is missing | Add it at the top. |
| The first line is printed twice | The `fflush(stdout);` line is missing | Put it back (step 3 explains why). |
| No `Z` in `ps` | More than 60 seconds have passed, or `ps` was too quick | Run `./zombie &` and `ps` straight away. |
| `bash: kill: %1: no such job` | No background job 1 in *this* terminal | `jobs` shows the right number. |
| The terminal seems frozen after `sleep 300` | It's waiting 5 minutes | Ctrl+C. |

## Talk about it

- What does `fork` do? How do the parent and the child know which one
  they are?
- What does `exec` do? What happens to the old program?
- What's a zombie? Who gets rid of it?
- What's a signal? Which signals do Ctrl+C and Ctrl+Z send?

## Challenge *(if there's time, or for next time)*

- What does this print, and how many processes are there at the end?
  Draw it, then try it.
  ```c
  fork();
  fork();
  printf("Hello!\n");
  ```
  *(Four Hellos: each `fork` doubles the processes. Numberblocks!)*
- Change `run.c` to run `ls -l` instead (`execlp("ls", "ls", "-l",
  NULL);`).
- `strace -f -e trace=clone,execve,wait4 ./run` shows the system calls
  of both processes. (On Linux, `fork` is done with `clone`.)

## Checkpoint

The learner can, without help:
- [ ] Explain `fork`, `exec` and `wait`, with the two boxes
- [ ] Explain why `fork.c` needs `fflush`
- [ ] Make a zombie and find it with `ps`
- [ ] Stop and pause processes with `kill`, Ctrl+C and Ctrl+Z

## Lab notebook

Draw the parent and child boxes after `fork`. Write the three steps a
shell does for every command. Copy the zombie line from `ps`. Commit. Add
*fork*, *exec*, *wait*, *child*, *zombie* and *signal* to
`dictionary.md`.

## Guide's background *(optional reading)*

This is OSTEP Chapter 5, "Process API", whose own examples are very
like these. Splitting "make a process" (`fork`) from "run a program"
(`exec`) looks odd, but it's what lets a shell set things up in between,
like redirecting the child's output into a file or a pipe before the
new program starts (Lesson 10.10).

`fork` doesn't really copy all the memory at once: the kernel shares
the pages between parent and child, and copies a page only when one of
them writes to it ("copy-on-write"). That's why forking a big process is
fast.

A zombie uses almost no memory, only an entry in the kernel's process
table, kept so that the parent can still collect the exit code. If a
buggy program makes thousands, the table can fill up. When the parent
dies, its children are "re-parented" to PID 1 (or a nearby "subreaper"
process), which `wait`s for them.
