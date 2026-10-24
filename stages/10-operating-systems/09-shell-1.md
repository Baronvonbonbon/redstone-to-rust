# Lesson 10.9: Build a Shell, Part 1: Shelly

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/os` · **New words:** shell, prompt, built-in command,
`Command`, `let ... else`, end of file

## Goal *(read this to the learner)*

> You've typed thousands of commands into `bash`. Now you'll write your
> own shell, **Shelly**, in Rust. It shows a prompt, reads what you
> type, and runs it, with `fork`, `exec` and `wait` underneath. Then
> you'll find out why `cd` can't be a program, and build it into
> Shelly.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"What three things does a shell do for every command?" *(Lesson 10.3:
`fork`, `exec` in the child, `wait` in the parent.)* "And before that?"
*(Show a prompt, and read a line.)*

## Activity

### Session 1: a shell in 20 lines

1. **Start.**
   ```
   cd ~/lab/os
   cargo new shelly
   cd shelly
   ```
   ```rust
   use std::io::{self, Write};
   use std::process::Command;

   fn main() {
       loop {
           print!("shelly> ");
           io::stdout().flush().unwrap();

           let mut line = String::new();
           if io::stdin().read_line(&mut line).unwrap() == 0 {
               println!();
               return;
           }
           let words: Vec<&str> = line.split_whitespace().collect();
           let Some((&program, args)) = words.split_first() else {
               continue;
           };

           Command::new(program).args(args).status().unwrap();
       }
   }
   ```

2. **Read it together.** **Say:**
   - "`print!` doesn't end the line, so Rust keeps the prompt in a bucket
     until it's flushed, like `fflush` in Lesson 10.3. `flush` sends it
     to the screen now."
   - "`read_line` gives back how many bytes it read. 0 means **end of
     file**: there's nothing more to read, ever. On a terminal, you send
     that with **Ctrl+D**."
   - "`split_first` splits the words into the first one and the rest:
     the program, and its arguments. If there are no words (an empty
     line), there's no first one: it gives `None`."
   - "`let ... else` says: if it matches, carry on with these new
     variables; if not, do the `else`, which must leave: here, `continue`
     the loop."
   - "`Command` is Rust's way to run a program. `status()` does the
     `fork`, the `exec` and the `wait` for you, and gives back how it
     finished."

3. **Try it.** `cargo run`. **They should see** the prompt `shelly> `.
   Type, one at a time: `ls`, `ls -l`, `echo hello   there`, `cowsay
   moo`, `pwd`, and an empty line. **They should see** each command work,
   and `hello there` with one space (`split_whitespace` threw the extra
   spaces away). Then press Ctrl+D. **They should see** the normal prompt
   again. **Say:** "You're running programs in your own shell!"

4. **Spy on it.** Run Shelly under `strace`, watching only the
   interesting calls:
   ```
   strace -f -e trace=clone,clone3,execve,wait4 ./target/debug/shelly
   ```
   Type `ls`, then Ctrl+D. **They should see**, among the lines:
   - a `clone3` line: that's the fork;
   - several `execve` lines from the child (with `[pid 8123]` in front:
     `-f` follows the child), trying `ls` in one folder after another,
     each `= -1 ENOENT`, until `execve("/usr/bin/ls", ...` works;
   - a `wait4` line: the wait.

   **Say:** "Shelly looked for `ls` in each folder of your `PATH`, in
   order. Try `echo $PATH` in bash to see the list." Commit.

### Session 2: errors, and `exit`

5. **A command that doesn't exist.** `cargo run`, and type `creeper`.
   **They should see:**
   ```
   thread 'main' (8200) panicked at src/main.rs:19:51:
   called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
   ```
   and Shelly is gone. **Say:** "A shell must never crash because of a
   typo. `status()` gives back an `Err` if the program couldn't start,
   and `unwrap` panicked." Replace the `Command` line with:
   ```rust
           match Command::new(program).args(args).status() {
               Ok(status) => {
                   if !status.success() {
                       eprintln!("shelly: {program} finished with {status}");
                   }
               }
               Err(error) if error.kind() == io::ErrorKind::NotFound => {
                   eprintln!("shelly: {program}: command not found");
               }
               Err(error) => eprintln!("shelly: {program}: {error}"),
           }
   ```
   **Say:** "`if` after a pattern in a `match` is a **guard**: this arm
   only matches if the error is `NotFound`." `cargo run`, and try
   `creeper` and `ls nowhere`. **They should see:**
   ```
   shelly> creeper
   shelly: creeper: command not found
   shelly> ls nowhere
   ls: cannot access 'nowhere': No such file or directory
   shelly: ls finished with exit status: 2
   ```
   **Say:** "The first is Shelly's message. In the second, `ls` ran, but
   finished with an exit code that isn't 0: Shelly tells you."

6. **`exit`.** Type `exit` in Shelly. **They should see:** `shelly: exit:
   command not found`! **Ask:** "Why?" *(There's no program called
   `exit`.)* **Say:** "So Shelly has to understand `exit` itself. That's
   a **built-in command**." Wrap the `match` from step 5 inside another
   `match`, on the program's name:
   ```rust
           match program {
               "exit" => return,
               _ => match Command::new(program).args(args).status() {
                   // ... the arms from step 5, unchanged ...
               },
           }
   ```
   (Move the three arms in, so the whole thing is one `match` inside
   another, as in the full program in step 9.) `cargo run`, then `exit`.
   **They should see:** the normal prompt again. Commit.

### Session 3: `cd`

7. **`cd` doesn't work.** In Shelly, type `cd /tmp`. **They should see:**
   `shelly: cd: command not found`. **Say:** "There's no program called
   `cd` either. But even if there were, it couldn't work. Watch:" in
   *bash* (your normal terminal):
   ```
   pwd
   bash -c "cd /tmp; pwd"
   pwd
   ```
   **They should see:** your folder, then `/tmp`, then your folder again.
   **Ask:** "Why didn't the second `bash` move *you*?" *(It's a child
   process. Each process has its own current folder, kept by the kernel
   (Lesson 10.1's `cwd`); a child can change its own, but not its
   parent's.)* **Say:** "So `cd` *must* be built into the shell: the
   shell has to change its own folder."

8. **Build in `cd`.** Add `use std::env;` at the top, and a second arm
   to the outer `match`, after `"exit"`:
   ```rust
               "cd" => {
                   let home = env::var("HOME").unwrap();
                   let place = args.first().copied().unwrap_or(&home);
                   if let Err(error) = env::set_current_dir(place) {
                       eprintln!("shelly: cd: {place}: {error}");
                   }
               }
   ```
   **Say:** "`set_current_dir` asks the kernel to change *this process's*
   folder. `cd` on its own goes home, like in bash: `HOME` is an
   **environment variable** holding your home folder's path."

9. **A better prompt.** Change the two lines that print the prompt to:
   ```rust
           let here = env::current_dir().unwrap();
           print!("shelly:{}> ", here.display());
   ```
   The whole program is now:
   ```rust
   use std::env;
   use std::io::{self, Write};
   use std::process::Command;

   fn main() {
       loop {
           let here = env::current_dir().unwrap();
           print!("shelly:{}> ", here.display());
           io::stdout().flush().unwrap();

           let mut line = String::new();
           if io::stdin().read_line(&mut line).unwrap() == 0 {
               println!();
               return;
           }
           let words: Vec<&str> = line.split_whitespace().collect();
           let Some((&program, args)) = words.split_first() else {
               continue;
           };

           match program {
               "exit" => return,
               "cd" => {
                   let home = env::var("HOME").unwrap();
                   let place = args.first().copied().unwrap_or(&home);
                   if let Err(error) = env::set_current_dir(place) {
                       eprintln!("shelly: cd: {place}: {error}");
                   }
               }
               _ => match Command::new(program).args(args).status() {
                   Ok(status) => {
                       if !status.success() {
                           eprintln!("shelly: {program} finished with {status}");
                       }
                   }
                   Err(error) if error.kind() == io::ErrorKind::NotFound => {
                       eprintln!("shelly: {program}: command not found");
                   }
                   Err(error) => eprintln!("shelly: {program}: {error}"),
               },
           }
       }
   }
   ```
   `cargo run`, and try `cd /tmp`, `pwd`, `cd`, and `cd nowhere`.
   **They should see:**
   ```
   shelly:/home/sam/lab/os/shelly> cd /tmp
   shelly:/tmp> pwd
   /tmp
   shelly:/tmp> cd
   shelly:/home/sam> cd nowhere
   shelly: cd: nowhere: No such file or directory (os error 2)
   shelly:/home/sam> exit
   ```
   `cargo clippy`, and commit.

10. **One more try.** In Shelly, type `echo hi > out.txt`, then `ls | wc
    -l`. **They should see:** `hi > out.txt` (it printed the `>`!), and
    errors from `ls` about files called `|` and `wc`. **Say:** "In bash,
    `>` and `|` are handled by the *shell*, not by the programs. Shelly
    doesn't know them yet. That's next lesson."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The prompt doesn't appear until after typing | The `flush` line is missing | Add `io::stdout().flush().unwrap();` after the `print!`. |
| `error[E0599]: no method named \`flush\` found` | The `Write` trait isn't imported | `use std::io::{self, Write};` |
| Shelly goes round and round printing prompts for ever | End of file isn't handled: `read_line` keeps giving 0 | Add the `if ... == 0 { ... return; }` lines. |
| `cd` with no folder panics: ``called `Result::unwrap()` on an `Err` value: NotPresent`` | `HOME` isn't set (very rare) | Run Shelly from a normal terminal. |
| Ctrl+C stops Shelly, not just the program | Ctrl+C goes to every process in the terminal's group | That's normal for now (see Challenge). |

## Talk about it

- What does a shell do, step by step?
- What does `status()` do underneath? How did `strace` show it?
- What's a built-in command? Why can't `cd` be a program?
- What's end of file? How do you send it from the keyboard?

## Challenge *(if there's time, or for next time)*

- Add a built-in `help` that lists Shelly's built-ins.
- Add a built-in `history` that shows the commands typed so far (keep
  them in a `Vec<String>`).
- Make the prompt show `~` instead of the home folder's path.
- Ctrl+C stops Shelly too. Real shells ignore it themselves, and only
  the program they're running stops. Find out how in the Rust Cookbook
  or Rust by Example (hint: it needs a crate, so ask the guide).

## Checkpoint

The learner can, without help:
- [ ] Explain each part of Shelly's loop
- [ ] Explain what `Command::status` does, using `fork`, `exec` and
      `wait`
- [ ] Explain why `cd` and `exit` are built in
- [ ] Handle a command that doesn't exist without crashing

## Lab notebook

Draw Shelly's loop as a flowchart: prompt, read, end of file?, split,
built-in?, run, wait. Copy the `bash -c "cd /tmp; pwd"` experiment, and
explain it. Commit. Add *shell*, *prompt*, *built-in command* and *end
of file* to `dictionary.md`.

## Guide's background *(optional reading)*

Writing a shell is a classic operating systems project (it's one of
OSTEP's homework projects, in C). Rust's `std::process::Command` hides
`fork` and `exec` behind one call (on Linux it actually uses a faster
relative of `fork`: `strace` shows `clone3` with the flags
`CLONE_VM|CLONE_VFORK`, where the child borrows the parent's memory
until its `exec`; inside some containers `clone3` is blocked, and it
falls back to `clone`). It also finds the program by searching each
folder in the `PATH` environment variable, as bash does: `echo $PATH`
shows the list.

`cd` and `exit` must be built into every shell, because they change the
shell process itself. bash has about 60 built-ins (`help` lists them);
some, like `echo` and `pwd`, also exist as programs (`/usr/bin/echo`),
and bash uses its own version for speed.

The panic message in step 5 includes the line and column: `19:51` is
where `unwrap` was in the learner's file, so their numbers may differ if
their layout does.
