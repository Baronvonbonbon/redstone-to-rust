# Lesson 1.7: Hidden Things and Wildcards

**Time:** 40 min · **New words:** hidden file, dotfile, wildcard, quotes

## Goal *(read this to the learner)*

> Your home folder has **secret files** in it that `ls` doesn't show you!
> Today you'll learn the spell that reveals hidden things, and the
> **wildcard** `*`, which matches *anything*.

## Before the lesson *(guide, 2 min)*

- [ ] Nothing special.

## Warm-up (5 min)

"How do you find out what options `ls` has?" *(`ls --help` or `man ls`.)*

## Activity

1. **Reveal hidden files.**
   ```
   cd
   ls
   ls -a
   ```
   **They should see:** lots more files with `ls -a`, all starting with a
   dot: `.bashrc`, `.profile`, `.config`... **Say:** "Files whose names
   start with a dot are **hidden**. They're usually settings files.
   People call them **dotfiles**. `-a` means show **a**ll."

   Point out `.` and `..` in the list: "`.` means *this* folder, and `..`
   means the folder above. They're in every folder!"

2. **Make your own secret.**
   ```
   cd ~/lab
   echo The treasure is under the couch > .secret
   ls
   ls -a
   cat .secret
   ```

3. **The long view.**
   ```
   ls -l
   ```
   Each line shows details: who owns it, its size, and when it was
   changed. The first letter is `d` for directory, or `-` for a file.
   Combine options: `ls -la`.

4. **Wildcards: `*` means "anything".** Make a test folder:
   ```
   mkdir ~/lab/zoo && cd ~/lab/zoo
   touch cat.txt dog.txt cow.txt bat.png rat.png cat.png
   ls *.txt
   ls *.png
   ls cat*
   ls *at*
   ```
   **Say:** "`*.txt` means 'anything that ends in .txt'."

5. **`?` means "exactly one letter".**
   ```
   ls ?at.*
   ```
   That matches `cat`, `bat` and `rat`, but not `dog` or `cow`.

6. **Spaces in names, and quotes.** Remember how spaces caused trouble?
   ```
   touch "my pet dragon.txt"
   ls
   cat my pet dragon.txt
   ```
   **They should see:** three errors, for `my`, `pet` and `dragon.txt`.
   **Say:** "The terminal thinks a space means 'next thing'. Quotes glue
   it together:"
   ```
   cat "my pet dragon.txt"
   ```
   Also try: type `cat my` and press **Tab**. It writes `my\ pet\ dragon.txt`.
   The backslash `\` means "this space is part of the name".

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ls: cannot access '*.jpg': No such file or directory` | Nothing matched the wildcard | That's the answer: there are none! |
| A `>` prompt after typing a quote | The quote wasn't closed | Ctrl+C, and type it again with both quotes. |

## Talk about it

- How do you make a hidden file? *(Start its name with a dot.)*
- What's the difference between `*` and `?`
- Why do people avoid spaces in file names?

## Challenge

In `zoo`: list only files with exactly 3 letters before the dot
*(`ls ???.*`)*. Delete all the `.png` files in one command *(`rm *.png`;
run `ls *.png` FIRST to see what would be deleted! That's the Shredder
Rules in action.)*

## Checkpoint

The learner can, without help:
- [ ] Show hidden files, and make one
- [ ] List files with a wildcard
- [ ] Work with a file name that has spaces in it

## Lab notebook

Add `ls -a`, `ls -l`, `*`, `?`, quotes and `\` to the dictionary. Add a
fourth Shredder Rule: **`ls` the wildcard before you `rm` it.**

## Guide's background *(optional reading)*

The shell itself expands wildcards *before* the command runs: `ls *.txt`
becomes `ls cat.txt cow.txt dog.txt`. This is called **globbing**. It's
also why `rm *` is so dangerous: it quietly turns into "remove every file
here". Bashcrawl, next lesson, hides rooms using dotfiles, so this lesson
comes first.
