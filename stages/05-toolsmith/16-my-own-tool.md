# Lesson 5.16: Project: My Own Tool (Stage 5 Checkpoint)

**Time:** 3–4 sessions of 45 min, plus the checkpoint on a separate day ·
**You need:** a terminal on the family computer; nano or vim; the
`~/bin` folder from Lesson 5.6; the Sandbox, for the checkpoint; an
audience for demo day · **New words:** usage message, symbolic link,
test script, README

## Goal *(read this to the learner)*

> Real programmers build their own tools: small commands that do one
> job they need again and again. Now you'll make one of your own. It
> will live in `~/bin` so it works from anywhere, it will check that
> it's used properly, it will have a test script that proves it works,
> and it will be kept safe in git with a README so anyone can use it.
> Finish it, pass the checkpoint, and you become a **Toolsmith**.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once. Session 1 walks through a complete
      example tool, `stacks`, so the learner sees every piece before
      making their own.
- [ ] Agree a **demo day** with the learner, about two weeks away, and
      invite an audience.

## The rules for the project

The tool must:
1. Be a **command in `~/bin`** that works from any folder: a bash script
   (or a Python one, with `#!/usr/bin/env python3` as its first line).
2. Take at least one **argument** (`$1`), and print a **usage message**
   and exit with code 1 if it's used without one.
3. Use at least one `if`, and at least one loop or pipe.
4. Have a **test script** that checks at least three answers and prints
   `ok` or `FAIL` for each.
5. Live in its **own git repository** in `~/lab/tools/`, with a
   `README.md`, at least five commits with good messages, one feature
   built on a **branch** and merged, and a push to a remote in
   `~/remotes`.

## Ideas

- **stacks** (the example in Session 1, so pick something else, or make
  it much bigger): blocks into stacks of 64.
- **nether**: turn Overworld coordinates into Nether ones (divide `x` and
  `z` by 8), for building portals that link up.
- **mob**: look up a mob in the database from Lesson 5.14:
  `sqlite3 -box ~/lab/sql/minecraft.db "SELECT * FROM mobs WHERE name = '$1';"`
- **todo**: `todo add buy diamonds` adds a line to a file; `todo` on its
  own lists them with numbers (`cat -n`).
- **quiz**: asks questions from a file, one per line, and keeps score.
- **times**: prints a times table for any number, or a power-of-two
  table (Lesson 4.2) up to any power.
- **Their own idea.** Anything that follows the rules.

## Activity

### Session 1: a complete example

1. **A home for tools.**
   ```
   mkdir -p ~/lab/tools/stacks
   cd ~/lab/tools/stacks
   nano stacks
   ```
   Type this in:
   ```bash
   #!/bin/bash
   # stacks: turns a number of blocks into stacks of 64.
   if [ $# -eq 0 ]; then
       echo "Usage: stacks NUMBER"
       echo "Example: stacks 200"
       exit 1
   fi
   full=$(( $1 / 64 ))
   left=$(( $1 % 64 ))
   echo "$1 blocks is $full stacks and $left more."
   ```
   **Say:** "Two new things. `$#` is *how many* arguments there are, so
   `$# -eq 0` means 'nobody gave me a number'. And `exit 1` stops the
   script straight away with exit code 1, which means 'something went
   wrong'. The message telling people how to use it is called a **usage
   message**: every good tool has one."

2. **Try it.**
   ```
   chmod +x stacks
   ./stacks 200
   ./stacks
   echo $?
   ```
   **They should see:** `200 blocks is 3 stacks and 8 more.`; then the
   usage message; then `1`. Check the 200 on paper: 3 × 64 = 192, and
   192 + 8 = 200.

3. **Make it a command, with a link.** The tool lives in its own folder,
   but commands go in `~/bin`. Instead of keeping two copies, make a
   **symbolic link**: a signpost in `~/bin` that points at the real file.
   ```
   ln -s ~/lab/tools/stacks/stacks ~/bin/stacks
   ls -l ~/bin
   cd /
   stacks 1000
   cd ~/lab/tools/stacks
   ```
   **They should see:** `stacks -> /home/sam/lab/tools/stacks/stacks`
   (with their name), and `1000 blocks is 15 stacks and 40 more.` from
   the `/` folder. **Say:** "The arrow means 'this is a link to that'. When
   you change the real file, the command changes too, because there's
   only one copy."

4. **A test script.** `nano test-stacks`:
   ```bash
   #!/bin/bash
   # test-stacks: checks that stacks gives the right answers.
   check() {
       if [ "$1" = "$2" ]; then
           echo "ok:   $2"
       else
           echo "FAIL: wanted '$2' but got '$1'"
       fi
   }
   check "$(./stacks 200)" "200 blocks is 3 stacks and 8 more."
   check "$(./stacks 64)" "64 blocks is 1 stacks and 0 more."
   check "$(./stacks 10)" "10 blocks is 0 stacks and 10 more."
   ./stacks > /dev/null
   check "$?" "1"
   ```
   ```
   chmod +x test-stacks
   ./test-stacks
   ```
   **They should see:** four lines starting with `ok:`. **Say:** "`check`
   is a **function**, like `def` in Python: it compares what the tool
   said with what it should say. It's the same idea as `assert` in
   Stage 3. The last test checks that using it wrong gives exit code 1.
   `> /dev/null` throws the usage message away so it doesn't clutter the
   results."

   Break it on purpose: change `64` to `46` in the line that works out
   `full`, run the tests (**They should see:** `FAIL` lines), and put it
   back.

5. **A README.** `nano README.md`:
   ```
   # stacks

   Turns a number of blocks into stacks of 64, for planning Minecraft builds.

   ## How to use it

       stacks 200

   says `200 blocks is 3 stacks and 8 more.`

   ## Testing

   Run `./test-stacks`. Every line should start with `ok`.
   ```
   **Say:** "A **README** is the first thing people read. It says what the
   tool is for, how to use it, and how to check it works. On every code
   website in the world, the README is the front page."

6. **Into git, and a feature on a branch.**
   ```
   git init
   git add .
   git commit -m "First working version of stacks"
   git switch -c shulker
   ```
   Add these lines at the end of `stacks`:
   ```bash
   if [ "$full" -ge 27 ]; then
       echo "That's $(( full / 27 )) full shulker boxes!"
   fi
   ```
   Test, commit, merge, and push to a new remote:
   ```
   ./stacks 2000
   ./test-stacks
   git commit -am "Count shulker boxes for big numbers"
   git switch main
   git merge shulker
   git init --bare ~/remotes/stacks.git
   git remote add origin ~/remotes/stacks.git
   git push -u origin main
   git log --oneline --graph --all
   ```
   **They should see:** `31 stacks and 16 more.` and `That's 1 full
   shulker boxes!`; all tests `ok`; `Fast-forward`; and two commits in
   the log. **Say:** "That's the whole job. Now you'll do it again, with
   your own idea."

### Sessions 2 and 3: your own tool

7. **Plan on paper first.** Write:
   - its name, and one sentence saying what it does;
   - three examples of using it, with exactly what it should print (these
     become the tests);
   - what it should say if someone uses it wrong.

8. **Build it a piece at a time**, like the example: the simplest
   version that works, then the tests, then commit; then one feature at a
   time, each on a branch, each with a new test, each committed. Link it
   into `~/bin` with `ln -s`. Run the tests after every change.

9. **Finish the README**, and push to `~/remotes/TOOLNAME.git`.

### Session 4: demo day

10. **Present it.** The learner shows the audience:
    - the README, and the tool working from a different folder;
    - what happens when you use it wrong (the usage message);
    - the test script, all `ok`;
    - `git log --oneline --graph`, explaining the branch;
    - one problem they had, and how they fixed it.

    Then let the audience use the tool themselves.

## The Stage 5 checkpoint

On a separate day, without help (they may use their lab notebook,
`dictionary.md`, `man` pages and `--help`). Answers for the guide are in
brackets.

1. **Admin.** Log in to the Sandbox. Make a user called `alex` with
   `sudo adduser alex`. Then make a file, set its permissions to `750`,
   and read the label with `ls -l`. Explain what each part means.
   *(`-rwxr-x---`: the owner can read, write and run it; the group can
   read and run it; others can't do anything. 7 is 111 in binary, 5 is
   101, 0 is 000.)*
2. **Packages.** In the Sandbox, install `cowsay`, list two of its files
   with `dpkg -L`, use it, and remove it again.
3. **vim.** Open a file in vim, add a line, save and quit. Open it again,
   change something, and quit *without* saving.
4. **A script.** Write a command `evens` in `~/bin` that prints the even
   numbers from 2 up to a number: `evens 10` prints 2, 4, 6, 8 and 10,
   each on its own line. Run it from a different folder. *(A `while` loop
   with `if [ $(( n % 2 )) -eq 0 ]` works, and so does
   `for n in $(seq 2 2 "$1")`.)*
5. **git.** In a new repository: make two commits; make a branch and
   commit on it; switch back to `main` and change the same line
   differently there; merge, fix the conflict, and commit. Then show the
   first version of the file with `git show`.
6. **Processes and ports.** Start `sleep 600 &`, find its PID with `ps`,
   and stop it with `kill`. Show the ports with servers listening on them,
   and point out the Sandbox's. *(`ss -ltn`, `127.0.0.1:2222`.)*
7. **SQL.** Build `minecraft.db` again from `~/lab/sql/minecraft.sql`.
   Write queries for: every neutral mob, toughest first *(iron golem
   100, enderman 40, panda 20, piglin 16, bee 10, wolf 8)*; how many
   mobs live in the overworld *(17)*; what a skeleton drops *(bone,
   arrow)*.
8. **Explain.** What root is, and why the Toolsmith uses `sudo` carefully.
   Why a password on a command line, or deleted from a git file, isn't
   secret. What a port is, and the difference between a server and a
   client.

All done means **Toolsmith!** Sign and stamp the passport.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `bash: ./stacks: Permission denied` | The script isn't executable | `chmod +x stacks` |
| `stacks: command not found` | The link isn't in `~/bin`, or `~/bin` isn't on the `PATH` | `ls -l ~/bin`; if it's there, open a new terminal (Lesson 5.6 put `~/bin` on the `PATH` in `.bashrc`). |
| `ln: failed to create symbolic link '/home/sam/bin/stacks': File exists` | There's already a link, or a copy, with that name | `ls -l ~/bin/stacks`. If it's an old copy, `rm ~/bin/stacks` and make the link again. |
| `ls -l ~/bin` shows the link in red | It points at a file that has moved or been renamed | `rm` the link, and make it again with the real file's full path. |
| `stacks lots` says `lots blocks is 0 stacks and 0 more.` | Bash treats a word it doesn't know in `$(( ))` as 0 | A good feature for a branch: check the argument is a number. (Look up `[[ $1 =~ ^[0-9]+$ ]]` together.) |
| A test says `FAIL`, but the answer looks the same | A tiny difference: a space, a full stop, or a capital letter | Copy the real output into the test exactly, if the real output is right. |
| The usage message prints, then the sum too | `exit 1` is missing | `exit 1` goes inside the `if`, before `fi`. |
| `fatal: remote origin already exists.` | The remote was already added | `git remote -v` to check it, then just `git push`. |

## Talk about it

- Why does a tool need a usage message? Who is it for?
- Why make a link instead of copying the script into `~/bin`?
- What did the test script catch, if anything?
- Which of this stage's tools do you think you'll use most?

## Checkpoint

The learner can, without help:
- [ ] Plan a tool with examples before writing it
- [ ] Write a command with arguments, a usage message and exit codes
- [ ] Write a test script and use it after every change
- [ ] Keep a project in git with a README, branches and a remote
- [ ] Pass the Stage 5 checkpoint above

## Lab notebook

Write the tool's plan, and a page about demo day: "The thing I'm proudest
of is..." and "Version 2 would...". Commit the notebook. Add *usage
message*, *symbolic link*, *test script* and *README* to
`dictionary.md`.

## Guide's background *(optional reading)*

This project is the real working habit of programmers, in miniature:
small tools that do one job, a clear interface (arguments, a usage
message, and exit codes so other scripts can tell whether it worked),
automated tests, version control, and documentation. It's often called
the **Unix philosophy**: "Write programs that do one thing and do it
well. Write programs to work together."

A **symbolic link** (`ln -s`) is a small file that points at another
path. The learner will meet links again in Stage 10, with the file
system.

The `mob` idea builds an SQL query by pasting `$1` into it. A mob name
containing a `'` breaks the query, and a cleverly chosen one could change
what it does: that's called **SQL injection**, one of the most common
security bugs on the web. It's harmless here, but it's a perfect thing to
come back to in Stage 11.

After this stage, the course goes back down into the machine: in Stage
6, the learner takes the NAND gates from Stage 4 and builds an entire
computer, in the Nand to Tetris course.
