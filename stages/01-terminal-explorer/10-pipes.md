# Lesson 1.10: Pipes, Plumbing for Words

**Time:** 45 min · **You need:** `~/lab/jokes.txt` from Lesson 1.3 (with at
least 5 jokes, one per line) · **New words:** pipe, input, output, filter

## Goal *(read this to the learner)*

> Each command does one small job. The real magic is **joining commands
> together**, so the words coming *out* of one go *into* the next, like
> water through pipes. Today you'll build a joke machine where a random
> joke comes out of a cow's mouth!

## Before the lesson *(guide, 5 min)*

- [ ] Check that `~/lab/jokes.txt` exists and has a few jokes in it. If
      not, they'll write it in step 1.
- [ ] Draw on paper: `[ command A ] ──|──▶ [ command B ] ──|──▶ screen`

## Warm-up (5 min)

"Remember `>`, which pours output into a file? Today's symbol is `|`. On
most keyboards it's Shift and the backslash key `\`. Find it!"

## Activity

1. **Count things with `wc`.**
   ```
   cd ~/lab
   wc -l jokes.txt
   ```
   **They should see:** something like `7 jokes.txt`. `wc` is **w**ord
   **c**ount; `-l` counts **l**ines.

2. **The first pipe.**
   ```
   ls /usr/bin | wc -l
   ```
   **Say:** "`ls` makes a giant list, and instead of showing it, the pipe
   `|` sends it into `wc -l`, which counts the lines. That's how many
   programs are in `/usr/bin`!" Show them the paper drawing.

3. **Top and bottom: `head` and `tail`.**
   ```
   ls /usr/bin | head
   ls /usr/bin | tail -n 3
   head -n 2 jokes.txt
   ```
   `head` shows the first 10 lines, and `tail` the last 10. `-n 3` means 3 lines.

4. **Sort.**
   ```
   sort jokes.txt
   ```
   Alphabetical! Make a file of animals to sort:
   ```
   printf 'zebra\ncat\naardvark\ncat\nmoose\ncat\n' > animals.txt
   sort animals.txt
   sort animals.txt | uniq
   sort animals.txt | uniq -c
   ```
   `uniq` removes repeats that are *next to each other*, which is why we
   sort first. `uniq -c` **c**ounts them. And `uniq -u` shows only things
   that appear exactly once:
   ```
   sort animals.txt | uniq -u
   ```
   *(Remember `uniq -u`! The Mineshaft needs it.)*

5. **The joke machine!**
   ```
   shuf -n 1 jokes.txt
   ```
   `shuf` **shuf**fles lines; `-n 1` picks one. Run it a few times. Now
   connect it to the cow:
   ```
   shuf -n 1 jokes.txt | cowsay
   ```
   And make it rainbow:
   ```
   shuf -n 1 jokes.txt | cowsay -f dragon | lolcat
   ```
   Three commands, two pipes, one dragon telling a rainbow joke.

6. **Big pipelines.** "Which letter do the most programs in `/usr/bin` start with?"
   ```
   ls /usr/bin | cut -c 1 | sort | uniq -c | sort -n | tail -n 3
   ```
   Build it up one piece at a time: run `ls /usr/bin | cut -c 1 | head`
   first, then add each next piece. (`cut -c 1` keeps just the first
   **c**haracter of each line. `sort -n` sorts by **n**umber.)

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Can't find the `\|` key | | Usually Shift and the `\` key, above Enter. |
| `uniq` didn't remove repeats | They weren't next to each other | Put `sort` first: `sort file \| uniq`. |
| `shuf: jokes.txt: No such file or directory` | Wrong folder | `cd ~/lab` first. |
| A long pipeline gives nothing | One piece is wrong | Build it up one pipe at a time, and check each step. That's debugging! |

## Talk about it

- What does `|` do? How is it different from `>`?
  *(`|` sends output into another command; `>` sends it into a file.)*
- Why do we sort before `uniq`?
- Describe the joke machine as a picture: what flows where?

## Challenge

- Save the joke machine's output to a file: `shuf -n 1 jokes.txt | cowsay > cow-joke.txt`
- How many words are in all your stories? `cat ~/lab/stories/* | wc -w`
- Count how many times each animal appears in `animals.txt`, with the
  biggest number first. *(`sort animals.txt | uniq -c | sort -rn`)*

## Checkpoint

The learner can, without help:
- [ ] Explain what a pipe does
- [ ] Count the lines of a command's output with `| wc -l`
- [ ] Use `sort | uniq -u` to find lines that appear only once
- [ ] Use `head` and `tail` to show part of a file

## Lab notebook

Draw the joke machine as pipes. Add `|`, `wc -l`, `head`, `tail`, `sort`,
`uniq`, `uniq -c`, `uniq -u` and `shuf` to the dictionary.

## Guide's background *(optional reading)*

Pipes are the heart of the "Unix philosophy": small programs that each do
one thing well, joined together into bigger tools. Every command reads
from **standard input** and writes to **standard output**; the pipe
connects one's output to the next one's input. Data scientists and
system administrators still build pipelines like this every day.

(We use the learner's own jokes file instead of the classic `fortune`
program, because `fortune`'s default quotes include adult topics.)
