# Lesson 10.10: Build a Shell, Part 2: Pipes and Arrows

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/os/shelly` from Lesson 10.9; a cardboard tube (or a
rolled-up sheet of paper) and some notes · **New words:** pipe,
redirection, `Stdio`, `spawn`, pipeline

## Goal *(read this to the learner)*

> In bash, `ls | wc -l` and `echo hi > out.txt` work because the
> *shell* connects the programs' file descriptors before they start.
> You'll teach Shelly to do the same: send one program's output into a
> file, and into another program, as many as you like in a row.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] A tube and a few scraps of paper for step 3.

## Warm-up (5 min)

"What are file descriptors 0, 1 and 2?" *(Standard input, output and
error: Lesson 10.2.)* "When you type `ls > list.txt` in bash, does `ls`
know about the file?" *(No: the shell opened it, and gave it to `ls` as
its standard output. `ls` just writes to 1, as always.)*

## Activity

### Session 1: arrows

1. **Spy on bash.** In bash:
   ```
   strace -f -e trace=openat,dup2,execve bash -c "echo hi > out.txt; ls" 2>&1 | grep -v "openat.*\.so"
   ```
   **They should see**, among other lines, an `openat` of `out.txt`
   giving back a file descriptor (like `= 3`), then `dup2(3, 1)`.
   **Say:** "`dup2(3, 1)` means: make file descriptor 1 be the same as
   3. After that, anything written to standard output goes into the
   file. That's all `>` is."

2. **Shelly's plan.** **Say:** "Rust's `Command` lets us choose a
   child's standard output before it starts: `command.stdout(file)`. So,
   for `echo hi > out.txt`: split the line at `>`, run the left part, and
   give it the file on the right as its output."

   In `src/main.rs`, add `use std::fs::File;` at the top, and this
   function above `main`:
   ```rust
   /// Runs a line like `echo hi > out.txt`.
   fn run_line(line: &str) -> io::Result<()> {
       let (stage, out_file) = match line.split_once('>') {
           Some((command, file)) => (command, Some(file.trim())),
           None => (line, None),
       };
       let words: Vec<&str> = stage.split_whitespace().collect();
       let Some((&program, args)) = words.split_first() else {
           return Ok(());
       };

       let mut command = Command::new(program);
       command.args(args);
       if let Some(file) = out_file {
           command.stdout(File::create(file)?);
       }
       command.status()?;
       Ok(())
   }
   ```
   Then, in `main`, replace the whole `_ => match ... ,` arm (the one
   that runs programs) with:
   ```rust
               _ => {
                   if let Err(error) = run_line(&line) {
                       eprintln!("shelly: {error}");
                   }
               }
   ```
   **Say:** "`split_once('>')` splits the line at the first `>`, if
   there is one. `?` hands any error back to `main`, which prints it."

   `cargo run`, and try:
   ```
   echo The creeper said hi > hi.txt
   cat hi.txt
   ls > list.txt
   cat list.txt
   creeper
   ```
   **They should see:** nothing from the first `echo` (it went into the
   file), then `The creeper said hi`; then the list of files from `cat
   list.txt`; and for `creeper`, `shelly: No such file or directory (os
   error 2)`. **Say:** "We lost our nice 'command not found'. We'll get
   it back in Session 2." Commit.

### Session 2: pipes

3. **Act it out.** Hold up the tube. **Say:** "A **pipe** is a tube the
   kernel makes, with two ends. One program writes into one end; the
   other program reads from the other end." The learner is `ls`: they
   write file names on scraps and post them into the tube. You are `wc
   -l`: you count the scraps that come out. **Say:** "Neither of us knows
   about the other. `ls` thinks it's writing to standard output, and `wc`
   thinks it's reading from standard input. The shell joined them."

4. **Many stages.** **Say:** "For `ls -l | grep txt | wc -l`, Shelly must
   split the line at each `|`. Each piece is a **stage** of the
   **pipeline**. Every stage except the last writes into a new pipe; every
   stage except the first reads from the one before." Draw three boxes
   with two tubes between them.

   **Say:** "There's one more change. `status()` waits for each program
   to finish before going on. But in a pipeline, all the programs must
   run *at the same time*, or the first one's tube fills up. So we
   `spawn` them all first (start without waiting), and *then* wait for
   all of them."

5. **The new `run_line`.** Change `use std::process::Command;` to `use
   std::process::{Child, Command, Stdio};`, and replace `run_line` with:
   ```rust
   /// Runs a line like `ls -l | grep txt > list.txt`.
   fn run_line(line: &str) -> io::Result<()> {
       let stages: Vec<&str> = line.split('|').collect();
       let mut children: Vec<Child> = Vec::new();
       for (i, stage) in stages.iter().enumerate() {
           let (stage, out_file) = match stage.split_once('>') {
               Some((command, file)) => (command, Some(file.trim())),
               None => (*stage, None),
           };
           let words: Vec<&str> = stage.split_whitespace().collect();
           let Some((&program, args)) = words.split_first() else {
               return Err(io::Error::other("a | with nothing next to it"));
           };

           let mut command = Command::new(program);
           command.args(args);
           if let Some(previous) = children.last_mut() {
               command.stdin(previous.stdout.take().unwrap());
           }
           if let Some(name) = out_file {
               match File::create(name) {
                   Ok(file) => command.stdout(file),
                   Err(error) => return Err(io::Error::other(format!("{name}: {error}"))),
               };
           } else if i < stages.len() - 1 {
               command.stdout(Stdio::piped());
           }
           match command.spawn() {
               Ok(child) => children.push(child),
               Err(error) if error.kind() == io::ErrorKind::NotFound => {
                   return Err(io::Error::other(format!("{program}: command not found")));
               }
               Err(error) => return Err(error),
           }
       }
       for mut child in children {
           child.wait()?;
       }
       Ok(())
   }
   ```
   Go through it together, with the boxes and tubes:
   - "`Stdio::piped()` asks for a new pipe for this child's standard
     output. After `spawn`, the parent holds the reading end, in
     `child.stdout`."
   - "For the next stage, `previous.stdout.take()` takes that reading end
     out of the previous child, and `command.stdin(...)` makes it the new
     child's standard input. The tube is connected!"
   - "The last stage has no pipe, so its output goes to the screen,
     unless there's a `>`."
   - "If the file can't be made, we give back an error with the file's
     name in it. `io::Error::other` makes an error out of our own words:
     that's also how 'command not found' came back."
   - "Finally, we wait for every child."

   `cargo run`. **They should see** something like:
   ```
   shelly:/home/sam/lab/os/shelly> ls | wc -l
   6
   shelly:/home/sam/lab/os/shelly> ls | grep t
   Cargo.toml
   hi.txt
   list.txt
   target
   shelly:/home/sam/lab/os/shelly> ls | grep txt > found.txt
   shelly:/home/sam/lab/os/shelly> cat found.txt
   found.txt
   hi.txt
   list.txt
   shelly:/home/sam/lab/os/shelly> cat hi.txt | tr a-z A-Z
   THE CREEPER SAID HI
   shelly:/home/sam/lab/os/shelly> ls |
   shelly: a | with nothing next to it
   shelly:/home/sam/lab/os/shelly> nosuch | wc -l
   shelly: nosuch: command not found
   shelly:/home/sam/lab/os/shelly> ls > /nope/list.txt
   shelly: /nope/list.txt: No such file or directory (os error 2)
   ```
   (The numbers and file names depend on what's in the folder.) **Ask:**
   "Why is `found.txt` in its own list?" *(Shelly made the file before
   `ls` started, so `ls` saw it.)*

6. **Three stages.** Try `cat src/main.rs | grep fn | wc -l`. **Ask:**
   "How many functions are in Shelly?" *(2: `run_line` and `main`. It
   counts the lines with `fn` in them.)* Then a fun one:
   ```
   ls /usr/games | grep cow
   ```
   *(`cowsay` and `cowthink`, from Stage 1.)* Commit. `cargo clippy` should be clean.

### Session 3 (optional): looking underneath

7. **Spy on Shelly's pipes.**
   ```
   strace -f -e trace=pipe2,dup2,execve,wait4 ./target/debug/shelly 2>&1 | grep -v ENOENT
   ```
   Type `ls | wc -l`, then Ctrl+D. **They should see** a `pipe2([3, 4],
   ...)` line (the kernel giving back the tube's two ends, as file
   descriptors 3 and 4), `dup2` lines in each child (making 4 the first
   child's standard output, and 3 the second one's input), two `execve`
   lines that work, and two `wait4` lines. **Say:** "That's a pipeline,
   from the kernel's side: `pipe`, `fork`, `dup2`, `exec`, `wait`."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ls \| wc -l` crashes Shelly with ``called `Option::unwrap()` on a `None` value`` | The first stage's output wasn't piped, so there's no tube to take | Check the `else if i < stages.len() - 1` lines. |
| `error[E0433]: cannot find type \`Stdio\` in this scope` | It isn't imported | `use std::process::{Child, Command, Stdio};` |
| `error[E0433]: cannot find type \`File\` in this scope` | It isn't imported | `use std::fs::File;` |
| `echo hi > out.txt` makes a file that `ls` shows as `' out.txt'$'\n'` | The file name wasn't trimmed, so it kept the space before it and the Enter after it | `Some(file.trim())`. Delete the strange file with `rm ./*out.txt*` in bash. |
| `cd` stopped working | The `cd` arm was replaced too | Only replace the `_ =>` arm; keep `exit` and `cd`. |

## Talk about it

- What does `>` do? Who handles it: the shell or the program?
- What's a pipe? Act it out again, with three people.
- Why must all the programs in a pipeline run at the same time?
- What does `dup2` do?

## Challenge *(if there's time, or for next time)*

- Add `>>`: add to the end of a file instead of replacing it. (Look for
  `OpenOptions` and `append` in `rustup doc --std`. Check for `>>`
  *before* `>`!)
- Add `<`: read standard input from a file, as in `wc -l < hi.txt`.
- `ls | nosuch` leaves the `ls` child behind without waiting for it. Run
  it, then `ps -o pid,stat,cmd` in Shelly. Can you see a zombie? Fix it,
  by waiting for the children already started before giving back the
  error.
- Make Shelly read commands from a file: `./target/debug/shelly <
  script.txt`. (It already works! Why?)

## Checkpoint

The learner can, without help:
- [ ] Explain redirection with `>` and file descriptor 1
- [ ] Explain a pipe with the tube, and draw a three-stage pipeline
- [ ] Explain `Stdio::piped`, `take` and `stdin` in `run_line`
- [ ] Explain why a pipeline uses `spawn` and then `wait`

## Lab notebook

Draw the three-stage pipeline: boxes, tubes, and which file descriptor
each end is. Write the list of system calls a shell uses for a pipeline.
Commit. Add *pipe*, *redirection*, *spawn* and *pipeline* to
`dictionary.md`.

## Guide's background *(optional reading)*

Pipes were added to Unix in 1973, at Doug McIlroy's insistence, and
became the heart of the "Unix philosophy": small programs that each do
one thing, joined by pipes. Every program in a pipeline runs at once;
the kernel's pipe holds a small buffer (64 KB on Linux), and a writer
that fills it is put to sleep until the reader catches up, so a
pipeline never needs more memory than that, however much flows through
it.

The most common bug in hand-written shells is the first row of the
error table: if any process (including the shell) keeps the writing end
of a pipe open, the reader never sees end of file, and waits for ever.
Rust's `take()` moves the reading end into the next child's `Command`,
and `Command` closes the parent's copies after `spawn`, so the parent
holds no stray ends.

The final Shelly is in the course repository, in `labs/os/shelly/`, for
you to compare with. It's the course's own code, so it's fine to look
after the learner has tried.
