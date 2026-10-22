# Lesson 1.12: grep, the Word Detective

**Time:** 40 min · **New words:** search, pattern, match

## Goal *(read this to the learner)*

> `find` finds *files*. But what if you need to find a *line inside* a
> giant file, like one sentence in a whole book? Meet `grep`, the word
> detective. Next lesson, you'll need it to solve a crime...

## Before the lesson *(guide, 5 min)*

- [ ] Nothing special. The lesson uses files already on every Linux computer.

## Warm-up (5 min)

"How did you find the diamond? How do you count lines?"

## Activity

1. **A giant file.** There's a file listing every user account the
   computer knows about:
   ```
   wc -l /etc/passwd
   cat /etc/passwd
   ```
   (Despite its name, it has **no passwords** in it. Those were moved
   somewhere secret long ago.)

2. **Find a line.**
   ```
   grep sam /etc/passwd
   ```
   (Use their own account name.) **They should see:** just the line about
   them. **Say:** "grep showed only the lines that **match**."

3. **Search your own files.**
   ```
   cd ~/lab
   grep cat animals.txt
   grep -c cat animals.txt
   ```
   `-c` **c**ounts the matching lines instead of showing them.

4. **Ignore capitals with `-i`.**
   ```
   grep dragon ~/lab/terminal-fun/dragons.txt
   grep -i DRAGON ~/lab/terminal-fun/dragons.txt
   ```

5. **Everything *except*: `-v`.**
   ```
   grep -v cat animals.txt
   ```

6. **grep in a pipe.** Which programs have "zip" in their name?
   ```
   ls /usr/bin | grep zip
   ```
   Which commands in your history used `cowsay`?
   ```
   history | grep cowsay
   ```

7. **Scrolling big files with `less`.**
   ```
   less /etc/passwd
   ```
   It works like `man`: arrows to move, `/word` to search, `q` to quit.

8. **Words with spaces need quotes:**
   ```
   grep "Dragons like" ~/lab/terminal-fun/dragons.txt
   ```

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `grep` prints nothing | Nothing matched, so no lines | Check the spelling and capitals; try `-i`. |
| `grep` seems stuck | It was given no file, so it's waiting for typing | Ctrl+C, then add the file name. |
| `grep: like: No such file or directory` | Searched for two words without quotes | Put quotes around the words: `"Dragons like"`. |

## Talk about it

- What's the difference between `find` and `grep`? *(`find` finds files by
  name; `grep` finds lines inside files.)*
- What do `-i`, `-c` and `-v` do?

## Challenge

How many programs in `/usr/bin` have "git" in their name?
*(`ls /usr/bin | grep git | wc -l`)*. Which of your jokes contain the word
"why"? *(`grep -i why ~/lab/jokes.txt`)*

## Checkpoint

The learner can, without help:
- [ ] Use `grep` to find lines containing a word in a file
- [ ] Use `grep` after a pipe
- [ ] Use `-i`, `-c` and `-v`

## Lab notebook

Add `grep`, `grep -i`, `grep -c`, `grep -v` and `less` to the dictionary.
Write: "`find` finds **files**. `grep` finds **lines**."

## Guide's background *(optional reading)*

`grep` is one of the most-used commands in all of computing. Programmers
use it constantly to search through code. The name comes from an old
editor command, `g/re/p`: "**g**lobally search for a **r**egular
**e**xpression and **p**rint". Regular expressions, a powerful mini-language
for patterns, come in Stage 5.
