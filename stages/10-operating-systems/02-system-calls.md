# Lesson 10.2: Asking the Kernel: System Calls

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text
editor; `strace` (see "Before the lesson"); `~/lab/os` · **New words:**
system call, user mode, kernel mode, `strace`, file descriptor

## Goal *(read this to the learner)*

> A program on its own can only do sums in its own memory. To print a
> word, open a file or even stop, it has to ask the kernel, with a
> **system call**. Today you'll use a spying tool, `strace`, to watch
> every question a program asks the kernel, and every answer it gets.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Check `strace -V` prints a version. If it says `command not
      found`, run `./scripts/install-packages.sh --later` from your own
      account while online (it installs `strace` and the other Stage 10
      tools).

## Warm-up (5 min)

"In the referee game, program A wanted to print. What did it have to
do?" *(Ask the kernel.)* "Why couldn't it just use the printer?" *(The
kernel won't let programs touch the hardware, so they can't break it or
each other.)*

## Activity

### Session 1: spying on `echo`

1. **Two modes.** **Say:** "The CPU has two modes. Your programs run in
   **user mode**, where the CPU itself refuses to touch the screen, the
   disk or other programs' memory. The kernel runs in **kernel mode**,
   where it can do anything. A **system call** is a special instruction
   that jumps into the kernel and says 'please do this for me'." Draw a
   wall across a page: programs above it, the kernel and the hardware
   below, and a little door in the wall marked *system call*.

2. **Watch one.**
   ```
   strace -e trace=write echo hi
   ```
   **They should see:**
   ```
   write(1, "hi\n", 3hi
   )                     = 3
   +++ exited with 0 +++
   ```
   **Say:** "`strace` shows every system call. `-e trace=write` means
   only show the `write` calls. `echo` asked the kernel: write to place
   1, these letters, 3 of them. The kernel answered `= 3`: I wrote 3."
   **Ask:** "Why is `hi` stuck in the middle of the line?" *(The kernel
   printed `hi` while `strace` was still writing its line about it.)*

   Tidier: send `echo`'s own output to nowhere.
   ```
   strace -e trace=write echo hi > /dev/null
   ```
   **They should see:** `write(1, "hi\n", 3)                     = 3`.

3. **Place 1.** **Say:** "The 1 is a **file descriptor**: a number that
   means an open file. Every process starts with three: 0 is the
   keyboard (standard input), 1 is the screen (standard output), and 2 is
   for errors (standard error). You met them in Lesson 8.5." **Ask:**
   "What will `strace -e trace=write ls nowhere` write to?" Try it.
   *(File descriptor 2, standard error: it's an error message.)*

4. **Everything `echo` asks.**
   ```
   strace echo hi
   ```
   **They should see** about 40 lines: `execve(...)` first, then many
   `openat`, `mmap` and `close` lines, `write` near the end, and
   `exit_group(0)` at the bottom. **Say:** "`execve` starts the program. The middle is
   the program loading its libraries into memory. Then the one line we
   wanted, and `exit_group`: please stop me." **Say:** "Even stopping is
   a system call."

5. **Counting.**
   ```
   strace -c ls / > /dev/null
   ```
   **They should see** a table with columns `% time`, `seconds`,
   `usecs/call`, `calls`, `errors` and `syscall`, and a `total` line at
   the bottom: about 70 calls. **Say:** "`-c` counts them instead of
   printing them. `getdents64` is the one that reads a folder's
   entries." **Ask:** "Which call was made most often?"

### Session 2: Rust's system calls

6. **Hello, kernel.**
   ```
   cd ~/lab/os
   cargo new hello
   cd hello
   cargo build
   strace -e trace=write ./target/debug/hello > /dev/null
   ```
   **They should see:** `write(1, "Hello, world!\n", 14)         = 14`.
   **Say:** "`println!` in Rust, `print` in Python, `printf` in C: they
   all end with the same `write` call. Underneath, every language asks
   the kernel the same way."

7. **Files are system calls too.** Make a new project:
   ```
   cd ~/lab/os
   cargo new notes
   cd notes
   ```
   ```rust
   use std::fs;

   fn main() {
       fs::write("notes.txt", "Creepers are green\n").unwrap();
       let words = fs::read_to_string("notes.txt").unwrap();
       print!("{words}");
   }
   ```
   ```
   cargo build
   strace -e trace=openat,read,write,close ./target/debug/notes
   ```
   **They should see**, after some lines about libraries (and one about
   `/proc/self/maps`, which Rust reads to find where its memory is),
   these lines:
   ```
   openat(AT_FDCWD, "notes.txt", O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC, 0666) = 3
   write(3, "Creepers are green\n", 19)    = 19
   close(3)                                = 0
   openat(AT_FDCWD, "notes.txt", O_RDONLY|O_CLOEXEC) = 3
   read(3, "Creepers are green\n", 32)     = 19
   read(3, "", 32)                         = 0
   close(3)                                = 0
   write(1, "Creepers are green\n", 19Creepers are green
   )    = 19
   ```
   Go through it line by line together:
   - `openat` asks to open `notes.txt` for writing (`O_WRONLY`), making
     it (`O_CREAT`), and emptying it (`O_TRUNC`). The kernel answers
     `3`: the next free file descriptor, after 0, 1 and 2.
   - `write(3, ...)` writes to file 3, and `close(3)` says "I've
     finished with it".
   - Then it's opened again for reading (`O_RDONLY`), and read: "up to
     32 bytes, please", and the kernel answers 19. **Ask:** "Why is
     there a second `read` that gets 0 bytes?" *(That's how a
     program finds the end of a file: the kernel says "nothing left".)*
   - The last `write` is to 1, the screen.

8. **When the kernel says no.**
   ```
   strace -e trace=openat cat /secret-diamonds.txt
   ```
   **They should see**, at the end:
   ```
   openat(AT_FDCWD, "/secret-diamonds.txt", O_RDONLY) = -1 ENOENT (No such file or directory)
   cat: /secret-diamonds.txt: No such file or directory
   ```
   **Say:** "The kernel answered -1, which means 'no', and `ENOENT`, which
   means there's no such file. `cat` turned that into the message you
   know." Try `strace -e trace=openat cat /etc/shadow`. *(The kernel says
   `EACCES (Permission denied)`: the file of passwords is only for
   root.)* Commit both projects.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `strace: command not found` | `strace` isn't installed | See "Before the lesson". |
| Hundreds of lines fly past | `strace` with no `-e` shows everything | Add `-e trace=write`, or `-c`, or pipe through `less`... but see the next line. |
| `strace ... \| less` shows the program's output, not the calls | `strace` writes to standard error, not standard output | `strace -o calls.txt PROGRAM`, then `less calls.txt`. |
| `./target/debug/notes: No such file or directory` | Not built yet, or in the wrong folder | `cargo build` in the `notes` folder. |

## Talk about it

- What's a system call? Why can't programs do those things themselves?
- What are file descriptors 0, 1 and 2?
- Why do Python, C and Rust all end with the same `write`?
- How does a program find out a file doesn't exist?

## Challenge *(if there's time, or for next time)*

- `strace -c python3 -c 'print("hi")'`: how many system calls does
  Python make to say hi? Compare with `strace -c ./target/debug/hello`.
- `strace -e trace=openat ls`: which files does `ls` open before it
  even looks at the folder?
- Run `strace -o calls.txt ./target/debug/notes` and count the lines
  with `wc -l calls.txt`.

## Checkpoint

The learner can, without help:
- [ ] Explain user mode, kernel mode and system calls with the wall
      drawing
- [ ] Use `strace -e trace=...` and `strace -c`
- [ ] Read an `openat` line: the file, how it's opened, and the file
      descriptor it gets back
- [ ] Explain what `-1 ENOENT` means

## Lab notebook

Draw the wall with the door. Copy the `openat`, `write` and `close` lines
from `notes`, and label each part. Commit. Add *system call*, *user
mode*, *kernel mode*, *strace* and *file descriptor* to `dictionary.md`.

## Guide's background *(optional reading)*

This is OSTEP Chapter 6, "Limited Direct Execution": programs run
directly on the CPU at full speed, but in a restricted mode; the CPU
traps into the kernel on a system call, an error or a timer tick. On
x86-64 the instruction is literally called `syscall`. Linux has about
350 system calls; `man 2 write` (or `man 2 openat`) documents each one,
offline.

`strace` uses a system call of its own, `ptrace`, which lets one process
watch and stop another. Debuggers like `gdb` (Stage 8) use it too. Some
security settings, including Docker's default one, block it, which is
the second row of the error table.

`openat` with `AT_FDCWD` means "relative to the current working
directory", which the kernel keeps for each process (Lesson 10.1's
`cwd`). Programs ask for the next free file descriptor, so after 0, 1 and
2 the first file opened is nearly always 3.
