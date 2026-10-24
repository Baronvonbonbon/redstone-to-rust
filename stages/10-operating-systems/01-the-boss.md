# Lesson 10.1: The Boss of the Computer

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text
editor; three pencils and paper; `~/lab/os` (see the Stage 10 README) ·
**New words:** operating system, kernel, process, PID, `/proc`

## Goal *(read this to the learner)*

> In Stage 8 you wrote the Jack OS: a library that helped programs draw,
> read keys and find memory. A real operating system does all that, and
> it has a bigger job: it runs hundreds of programs at once on a few
> CPUs, and stops them treading on each other. It's the boss of the
> computer. Today you'll meet it, see every program it's running, and
> read its secret files.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Make sure `~/lab/os` exists in the learner's account (the Stage 10
      README, "Setup notes").
- [ ] Have three pencils (or crayons) and three sheets of paper ready,
      and one sheet you'll call "the printer".

## Warm-up (5 min)

"In the Jack OS, what did `Screen.drawLine` do?" *(It drew a line, so
programs didn't have to set every pixel themselves.)* "How many programs
could Hack run at once?" *(One.)* "How many do you think this computer is
running right now?" Write their guess down.

## Activity

### Session 1: the referee, and the programs

1. **Act it out.** **Say:** "You're three programs, and I'm the
   **kernel**: the heart of the operating system. There's only one
   pencil, which is the CPU. Each program wants to write its name over
   and over." Give the learner the three sheets, labelled A, B and C,
   and keep the pencil.
   - Give the pencil for program A, count "one, two, three", and take it
     back. Then B, then C, then A again. **Say:** "That's **sharing the
     CPU**. I switch so fast on the real computer, about a thousand
     times a second, that all the programs seem to run at once."
   - **Say:** "Each program has its own sheet of paper: its **memory**.
     Can A write on B's paper?" *(No: the kernel won't let it.)*
   - **Say:** "Now A wants to print. It can't touch the printer itself.
     It has to *ask* me." Write A's name on the printer sheet for them.
     "Asking the kernel to do something is a **system call**."

   **Say:** "That's this stage: how the kernel shares the CPU and the
   memory, how programs ask it for things, and how it keeps files safe.
   At the end, you'll write a tiny kernel of your own."

2. **Every program in this terminal.** Open a terminal.
   ```
   ps
   ```
   **They should see** something like:
   ```
       PID TTY          TIME CMD
      4321 pts/0    00:00:00 bash
      4398 pts/0    00:00:00 ps
   ```
   **Say:** "A running program is a **process**. Every process has a
   number, its **PID** (process ID). `bash` is the shell you're typing
   into. `ps` is `ps` itself: it was running when it looked!"

   Run `ps` again. **Ask:** "Did `bash`'s PID change? Did `ps`'s?" *(The
   shell's stays the same; `ps` is a new process each time, so it gets a
   new number.)*

3. **Every program on the computer.**
   ```
   ps -e | wc -l
   ```
   **They should see** a number, often between 200 and 400. Compare it
   with their guess. **Say:** "`-e` means every process, and `wc -l`
   counts the lines. Most of them are asleep, waiting for something to
   happen." Then look through them:
   ```
   ps -e | less
   ```
   Space for the next page, `q` to quit. Find `firefox` or the
   terminal's own name, if they're running.

4. **The family tree.**
   ```
   pstree -p | less
   ```
   **They should see** a tree, with `systemd(1)` at the very top.
   **Say:** "Every process was started by another one, its **parent**.
   Follow the lines back up, and you always reach PID 1, `systemd`: the
   first program the kernel starts when the computer boots. It starts
   everything else." Find `bash` in the tree, with `pstree` next to it.
   **Say:** "In Lesson 10.12, *your* program will be PID 1."

5. **Live.**
   ```
   top
   ```
   **They should see** a table that updates every few seconds: the
   busiest processes at the top, with `%CPU` and `%MEM`. Press `M` to
   sort by memory, `P` to sort by CPU, and `q` to quit. **Ask:** "Which
   program uses the most memory?" *(Often the web browser.)*

### Session 2: the kernel's secret files

6. **`/proc`.**
   ```
   ls /proc
   ```
   **They should see** lots of numbers, then names like `cpuinfo` and
   `meminfo`. **Say:** "Each number is a process: there's a folder for
   every PID. But these aren't real files on the disk. When you read
   one, the kernel makes up the answer, there and then."

7. **Ask the kernel about the computer.**
   ```
   grep "model name" /proc/cpuinfo
   grep MemTotal /proc/meminfo
   cat /proc/uptime
   uname -r
   ```
   **They should see:** one `model name` line for each CPU the kernel can
   use; the total memory in kB; two numbers; and the kernel's version,
   something like `6.12.10-76061203-generic`. **Say:** "The first number
   in `uptime` is how many seconds the computer has been on." **Ask:**
   "How many hours is that?" *(Divide by 3600.)* "How many CPUs do you
   have?" *(Count the `model name` lines.)*

8. **Ask the kernel about the shell.**
   ```
   echo $$
   head -9 /proc/$$/status
   ls -l /proc/$$/cwd
   ```
   **Say:** "`$$` is the shell's own PID." **They should see:** the
   shell's PID; lines including `Name: bash` and `State: S (sleeping)`;
   and an arrow from `cwd` to the folder they're in. **Ask:** "Why is the
   shell sleeping?" *(It's waiting for you to type.)* Now `cd /tmp`, and
   `ls -l /proc/$$/cwd` again. **Say:** "`cwd` means current working
   directory. The kernel remembers where every process is."

9. **A program that asks about itself.**
   ```
   cd ~/lab/os
   cargo new me
   cd me
   ```
   Type this into `src/main.rs`:
   ```rust
   use std::fs;
   use std::os::unix::process::parent_id;
   use std::process;

   fn main() {
       println!("My PID is {}.", process::id());
       println!("My parent's PID is {}.", parent_id());
       let status = fs::read_to_string("/proc/self/status").unwrap();
       for line in status.lines() {
           for name in ["Name:", "State:", "Threads:", "VmRSS:"] {
               if line.starts_with(name) {
                   println!("{line}");
               }
           }
       }
   }
   ```
   ```
   cargo build
   ./target/debug/me
   ./target/debug/me
   echo $$
   ```
   **They should see**, each time, something like:
   ```
   My PID is 6012.
   My parent's PID is 4321.
   Name:	me
   State:	R (running)
   VmRSS:	    2104 kB
   Threads:	1
   ```
   **Ask:** "Who's the parent?" *(The shell: the same number as `echo
   $$`.)* "Why is the PID different each time?" *(Each run is a new
   process.)* "Why is it `R (running)` and not sleeping?" *(It's running
   while it reads its own status.)* **Say:** "`/proc/self` is a shortcut:
   it always means the process that's reading it. `VmRSS` is how much
   real memory it's using." Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `pstree: command not found` | The `psmisc` package isn't installed | Ask the guide: `sudo apt install psmisc`. |
| `top` fills the terminal and won't stop | That's what it does | Press `q`. |
| `cat: /proc/4321/status: No such file or directory` | That process has finished (or the number is mistyped) | Use `$$`, or a PID that `ps` shows now. |
| `cargo new` says `destination ... already exists` | There's a `me` folder already | `cd me`, or choose another name. |
| `error[E0432]: unresolved import` at `parent_id` | A typing mistake in the `use` line | Copy it exactly: `std::os::unix::process::parent_id`. |

## Talk about it

- What's a process? What's a PID?
- Why can't a program use the printer (or the screen, or the disk) by
  itself?
- Who started your shell? Who started *that*?
- Are the files in `/proc` real? Where do their answers come from?

## Challenge *(if there's time, or for next time)*

- `ps -o pid,ppid,stat,cmd` shows each process's parent (`PPID`) and
  state. Follow the parents back from `ps` to PID 1 by hand.
- `cat /proc/loadavg`: the first three numbers are how busy the CPUs
  have been, over 1, 5 and 15 minutes. Run something busy and watch them
  climb.
- Change `me` to print its `cwd` too: `fs::read_link("/proc/self/cwd")`.
  Run it from two different folders.

## Checkpoint

The learner can, without help:
- [ ] Explain the kernel's three jobs with the pencil and paper
- [ ] Use `ps`, `pstree` and `top`, and say what a PID is
- [ ] Read something from `/proc`, and explain where the answer comes
      from
- [ ] Explain why `me` gets a new PID each time, and who its parent is

## Lab notebook

Draw the referee game: three programs, one pencil, the kernel in the
middle. Write how many processes your computer was running, and copy
the top of the `pstree` family tree. Commit. Add *operating system*,
*kernel*, *process*, *PID* and */proc* to `dictionary.md`.

## Guide's background *(optional reading)*

This stage follows the plan of *Operating Systems: Three Easy Pieces*
(OSTEP), by Remzi and Andrea Arpaci-Dusseau, a free university textbook:
**virtualization** (the kernel makes one CPU and one memory look like
many, one for each process), **concurrency** (programs doing several
things at once), and **persistence** (files that survive the power going
off). Its Chapters 2 and 4 match this lesson. The chapters are free
PDFs on its website; see the Stage 10 README.

The operating system is everything that comes with the computer before
you add your own programs; the **kernel** is its core, the one program
that runs with full power over the hardware. Linux is a kernel; Pop!_OS
is an operating system built around it, with systemd, the desktop and
thousands of tools. Ordinary programs run in **user mode**, where the
CPU itself refuses to let them touch the hardware or other programs'
memory; to do those things they must make a system call, which hands
control to the kernel (Lesson 10.2).

`/proc` is a **pseudo-file system**: nothing in it is stored anywhere,
and each read calls a function in the kernel that writes the answer.
That's why `ls -l /proc/cpuinfo` shows a size of 0, although `cat`
prints plenty.
