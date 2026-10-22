# Stage 1: Terminal Explorer

**Badge:** Terminal Detective · **Needs first:** Stage 0; can find keys
without hunting too long · **Lessons:** 15

The learner puts the mouse away and talks to the computer by typing
**commands** into the **terminal**. They move around the folder tree,
make and destroy files, and learn the shell's superpowers. Along the way
they play a dungeon crawler (bashcrawl), explore a treasure cave, solve
a detective mystery with `grep` and pipes, and connect over SSH to the
**Mineshaft**, a wargame that runs on your own computer.

## Lessons

| # | Lesson | New commands |
|---|---|---|
| 1.1 | [The Magic Talking Box](01-magic-talking-box.md) | `echo` `cowsay` `figlet` `sl` `clear` `exit` |
| 1.2 | [Where Am I?](02-where-am-i.md) | `pwd` `ls` `cd` `~` `..` `tree` |
| 1.3 | [Making Things](03-making-things.md) | `mkdir` `touch` `>` `>>` `cat` `nano` |
| 1.4 | [Moving, Copying and the Shredder](04-moving-copying-shredder.md) | `cp` `mv` `rm` `rmdir` `-r` `-i` |
| 1.5 | [Terminal Superpowers](05-terminal-superpowers.md) | Tab, ↑, `history`, Ctrl+C, Ctrl+L, copy and paste |
| 1.6 | [Asking for Help](06-asking-for-help.md) | `--help` `man` `whatis` |
| 1.7 | [Hidden Things and Wildcards](07-hidden-things-wildcards.md) | `ls -a` `ls -l` `*` `?` |
| 1.8 | [Bashcrawl, Part 1](08-bashcrawl-1.md) | `cp -r` `ls -F` `alias` `./program` |
| 1.9 | [Bashcrawl, Part 2](09-bashcrawl-2.md) | (whatever the dungeon teaches!) |
| 1.10 | [Pipes: Plumbing for Words](10-pipes.md) | `\|` `wc` `sort` `uniq` `head` `tail` `shuf` `lolcat` |
| 1.11 | [The Treasure Cave](11-treasure-cave.md) | `find` `tree` |
| 1.12 | [grep, the Word Detective](12-grep.md) | `grep` `-i` `-c` `-v` `less` |
| 1.13 | [The Great Underpants Heist](13-underpants-heist.md) | Everything so far |
| 1.14 | [Into the Mineshaft](14-into-the-mineshaft.md) | `ssh`; Mineshaft levels 0–4; `file` |
| 1.15 | [Deeper in the Mineshaft](15-deeper-in-the-mineshaft.md) | Mineshaft levels 5–9; `base64`; checkpoint |

## Free play for this stage

- **Typing:** keep going with Tux Typing or Klavaro, then try `gtypist`
  in the terminal.
- **Terminal games:** `moon-buggy`, `ninvaders`, and from bsdgames,
  `robots`, `worm` and `hangman`. Type the name to play; quit with
  `q` or Ctrl+C.
- **Terminus** (a terminal adventure in the web browser, offline): open
  `/srv/redstone-library/games/terminus/Web/index.html` in the browser.
- **cowsay and figlet:** make banners and talking animals for the
  family.

## Setup for this stage

- Lesson 1.8: the offline library must be downloaded ([SETUP.md](../../docs/SETUP.md), step 4).
- Lesson 1.11: `./scripts/give-lab.sh LEARNER cave`
- Lesson 1.13: `./scripts/give-lab.sh LEARNER heist`
- Lesson 1.14: the Mineshaft is running ([SETUP.md](../../docs/SETUP.md), step 5), and the
  [Hacker's Pledge](../../docs/HACKER-PLEDGE.md) is printed.

## Checkpoint (end of Lesson 1.15)

The learner can, without help, and using only the terminal:
- [ ] Say where they are (`pwd`), look around (`ls -a`) and move anywhere (`cd`, `..`, `~`)
- [ ] Make, copy, rename and delete files and folders, and explain why `rm` is dangerous
- [ ] Use Tab completion and the up arrow without being reminded
- [ ] Find out how to use a new command with `--help` or `man`
- [ ] Find a file by name with `find`, and find a line in a file with `grep`
- [ ] Join two commands with a pipe, and explain what the pipe does
- [ ] Log into the Mineshaft with `ssh`, and reach at least level 10
- [ ] Explain the Hacker's Pledge in their own words
