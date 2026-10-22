# Lesson 5.6: Shell Scripts, Part 1: Your Own Commands

**Time:** 2 sessions of 45 min · **You need:** a terminal on the family
computer; nano or vim; cowsay · **New words:** script, shebang,
variable, argument, `PATH`

## Goal *(read this to the learner)*

> You've typed hundreds of commands. What if you could save a list of
> commands in a file, give it a name, and run it like any other command?
> That's a **shell script**. Today you'll make your very own commands:
> a greeter, a dice roller, and a random Minecraft fact machine that
> works from anywhere on the computer.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] This lesson happens on the **family computer**, in the learner's
      own account (not the Sandbox), so the commands they make are theirs
      to keep.

## Warm-up (5 min)

"What does `chmod +x` do?" *(Lets a file be run as a program.)* "In
Python, what's a variable?" *(A labelled box holding a value.)* "What
does `$( )` do in `cd "$(mktemp -d)"`?" *(Runs the command inside and
uses its output.)*

## Activity

### Session 1: a command of your own

1. **A home for your commands.**
   ```
   mkdir -p ~/bin
   cd ~/bin
   nano hello
   ```
   (Or `vim hello`.) Type this:
   ```bash
   #!/bin/bash
   # hello: says hello, and what day it is.
   echo "Hello, $USER!"
   echo "Today is $(date +%A)."
   ```
   Save and quit.

   **Say:** "The first line, `#!/bin/bash`, is called the **shebang**
   (from 'hash' and 'bang', the names of `#` and `!`). It tells the
   computer which program should read the file: bash, the shell you've
   been typing into all along. Lines starting with `#` are comments, like
   in Python."

2. **Make it runnable, and run it.**
   ```
   ./hello
   chmod +x hello
   ./hello
   ```
   **They should see:** `bash: ./hello: Permission denied` the first time
   (Lesson 5.2: no `x`!), then `Hello, sam!` and the day of the week.

   **Say:** "`$USER` is a variable the shell already knows: your name.
   `$(date +%A)` runs the `date` command and puts the answer right there.
   Try `date +%A` on its own."

3. **Run it from anywhere.** `cd ~` and type `hello`. **They should see:**
   `hello: command not found`. **Say:** "When you type a command, the shell
   looks for it in a list of folders called the `PATH`." Look at it:
   ```
   echo $PATH
   ```
   **They should see:** folders separated by colons, like
   `/usr/local/bin:/usr/bin:/bin:/usr/games`. **Say:** "Our `bin` folder
   isn't in the list. Let's add it, for every terminal from now on."
   ```
   echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   hello
   which hello
   ```
   **They should see:** the greeting, then `/home/sam/bin/hello`. **Say:**
   "You've made a real command. Real Linux commands like `ls` work exactly
   the same way: they're files in a folder on the `PATH`."

4. **Variables.** In the terminal (not a script yet):
   ```
   mob="creeper"
   echo "Watch out for the $mob!"
   ```
   **They should see:** `Watch out for the creeper!`. Now try it with
   spaces: `mob = "creeper"`. **They should see:** `mob: command not
   found`. **Say:** "In bash, there must be **no spaces** around the `=`.
   With spaces, bash thinks `mob` is a command. Bash is fussier than
   Python!"

5. **Arguments.** Make `~/bin/greet`:
   ```bash
   #!/bin/bash
   # greet: says hello to whoever you name.
   echo "Hello, $1! Welcome to the server."
   ```
   `chmod +x ~/bin/greet`, then `greet Alex`, and `greet "Captain Underpants"`.
   **They should see:** `Hello, Alex! Welcome to the server.`

   **Say:** "Whatever you type after the command's name are its
   **arguments**. Inside the script, `$1` is the first one, `$2` the
   second, and so on. The quotes keep 'Captain Underpants' as *one*
   argument."

   What happens with just `greet`? *(`Hello, !`.)* Change the line to:
   ```bash
   echo "Hello, ${1:-friend}! Welcome to the server."
   ```
   **Say:** "`${1:-friend}` means 'the first argument, or `friend` if there
   isn't one'." Try `greet` again.

### Session 2: tools that do things

6. **Asking questions.** Make `~/bin/mobquiz`:
   ```bash
   #!/bin/bash
   # mobquiz: asks one question and checks the answer.
   read -p "Which mob explodes? " answer
   if [ "$answer" = "creeper" ]; then
       echo "Correct! Sssssss... BOOM."
   else
       echo "Nope, it's the creeper."
   fi
   ```
   **Say:** "`read` is bash's `input()`. And `if` works a lot like Python's,
   with different punctuation: square brackets with spaces inside them,
   `then`, and `fi` (which is `if` backwards!) at the end. Next lesson is
   all about `if`."

7. **Maths and dice.** In the terminal:
   ```
   echo $((6 * 7))
   echo $((2 ** 10))
   echo $RANDOM
   echo $((RANDOM % 6 + 1))
   ```
   **They should see:** `42`, `1024`, a random number, and a number from 1
   to 6. **Say:** "`$(( ))` does arithmetic. `$RANDOM` is a new random
   number from 0 to 32767 every time, and `% 6 + 1` turns it into a dice
   roll, like the remainders in Stage 3." Make `~/bin/dice` that rolls two
   dice and prints them and their total.

8. **The fact machine.** Make a facts file, one fact per line (at least
   five, in their own words):
   ```
   nano ~/lab/facts.txt
   ```
   For example: `Creepers were made by accident, from a broken pig model.`
   Then make `~/bin/mobfact`:
   ```bash
   #!/bin/bash
   # mobfact: prints one random fact from my facts file.
   shuf -n 1 ~/lab/facts.txt
   ```
   `chmod +x ~/bin/mobfact`, then:
   ```
   mobfact
   mobfact | cowsay
   ```
   **Say:** "Your own command works in a pipe, just like the real ones."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `bash: ./hello: Permission denied` | The script isn't executable | `chmod +x hello` |
| `hello: command not found` | `~/bin` isn't on the `PATH` in this terminal | `source ~/.bashrc`, or open a new terminal. Check with `echo $PATH`. |
| `mob: command not found` | Spaces around `=` | `mob="creeper"`, no spaces. |
| ``[: missing `]'`` | No space before `]` | It's `[ "$answer" = "creeper" ]`, with spaces inside both brackets. |
| `syntax error: unexpected end of file` | An `if` without its `fi` | Every `if` ends with `fi`. |
| The script prints `$USER` literally | Single quotes `'...'` were used | Variables only work inside double quotes `"..."`. |
| `shuf: /home/sam/lab/facts.txt: No such file or directory` | The facts file is somewhere else | Make it at `~/lab/facts.txt`. |
| `cannot execute: required file not found` | A typo in the shebang line, like `#!/bin/bsh` | It's exactly `#!/bin/bash`, on the very first line. |

## Talk about it

- What's the shebang line for?
- How does the shell find a command when you type its name?
- What's the difference between `$1` and `$USER`?
- What else would you like to make into a command?

## Challenge *(if there's time, or for next time)*

- `greet` with two names: use `$1` and `$2`. What's in `$#`? *(How many
  arguments there are.)*
- Make `binary` that prints a number in binary using Python:
  `python3 -c "print(bin($1))"`. Try `binary 42`.
- A command `today` that prints the date, a fact and a dice roll, by
  calling your other commands.

## Checkpoint

The learner can, without help:
- [ ] Write a script with a shebang, make it executable and run it
- [ ] Put their own commands in `~/bin` and run them from anywhere
- [ ] Use variables, `$1`, `read` and `$(( ))` in a script
- [ ] Explain what `PATH` is

## Lab notebook

List every command they made, with one line about what it does. Copy
the shebang line and explain it. Add *script*, *shebang*, *variable*,
*argument* and *PATH* to the dictionary.

## Guide's background *(optional reading)*

A shell script is just commands in a file. The shebang line tells the
kernel which interpreter to run, so the same trick works for Python
(`#!/usr/bin/env python3`). Putting scripts in `~/bin` and adding it to
`PATH` is how programmers build up a personal toolbox over years.

(Ubuntu's `~/.profile` also adds `~/bin` to `PATH` at the next login if
the folder exists, so after a reboot it may appear twice in
`echo $PATH`. That's harmless.)

Bash's syntax is famously fussy: no spaces around `=`, but spaces
required inside `[ ]`, and variables expand inside double quotes but not
single quotes. Most beginner bugs are one of those three. The
troubleshooting table covers them; it's worth pointing them out when
they happen rather than in advance.
