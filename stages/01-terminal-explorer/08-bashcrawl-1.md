# Lesson 1.8: Bashcrawl, Part 1

**Time:** 45 min · **You need:** the offline library downloaded
([SETUP.md](../../docs/SETUP.md), step 4) · **New words:** alias, program,
script, relative path

## Goal *(read this to the learner)*

> You're going on a quest into a dark dungeon, armed with nothing but the
> terminal. Every room is a folder, and every scroll is a file. Find the
> treasure, drink the potions, and watch out for monsters!

## Before the lesson *(guide, 15 min)*

- [ ] **Preview the game yourself.** Bashcrawl is a fantasy dungeon. Some
      rooms are spooky (a graveyard, a "blood"-written warning on the wall).
      Most kids who like adventure stories love it; you know your learner
      best. Play it for 10 minutes from your own account:
      `cp -r /srv/redstone-library/games/bashcrawl ~/bashcrawl-preview && cd ~/bashcrawl-preview/entrance && cat scroll`
- [ ] Check that the learner's account can read the library: log in as the
      learner and run `ls /srv/redstone-library/games/bashcrawl`.

## Warm-up (5 min)

"What does `ls -a` show? How would you make a hidden room in a dungeon?"

## Activity

1. **Copy the dungeon into your home.**
   ```
   cp -r /srv/redstone-library/games/bashcrawl ~/bashcrawl
   cd ~/bashcrawl/entrance
   ```
   **Say:** "Remember `cp -r`? You just copied a whole dungeon! If you ever
   want to restart the game, delete it and copy it again."

2. **Start the quest.**
   ```
   cat scroll
   ```
   **From here, the game is the teacher.** The learner reads every scroll
   (out loud is great) and does what it says. Things the early scrolls
   teach:
   - `ls -F`: rooms (folders) end in `/` and things you can use (programs)
     end in `*`
   - `alias ls='ls -F'`: an **alias** is a nickname for a command
   - `./treasure`: run a program in this room (`.` means "right here")
   - `cd ..`: go back to the previous room

3. **The guide's job:** sit beside them and ask questions instead of
   giving answers:
   - "What did the scroll say to try?"
   - "What does `ls -a` show in this room?" (hidden rooms!)
   - "Where are you?" (`pwd`)

4. **Keep a dungeon map** on paper as they explore: draw each room and
   what they found there.

5. **Stop while it's fun**, after about 30 minutes of play. Note in the
   notebook which room they're in, for next time.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `cp: cannot stat '/srv/redstone-library/...'` | The library isn't downloaded, or it's somewhere else | Do [SETUP.md](../../docs/SETUP.md), step 4. |
| `bash: ./treasure: Permission denied` | They're running something that isn't a program, or the copy lost its permissions | Check `ls -F`: only things ending in `*` can be run. |
| They opened a game file with `cat` and saw code | They wandered "out of bounds" | Great! The game itself says that's okay. Peeking at code is how hackers learn. |
| The inventory is empty after opening a new terminal | The game keeps your inventory in a shell variable (`$I`), which only lasts as long as that terminal | Keep the same terminal open while playing. The rooms you've opened stay open. |
| They want hints | | The scrolls *are* the hints. Read the last scroll again; try `ls -a` in every room. |

## Talk about it

- What does `./` mean before a name? *(Run the program that's right here.)*
- What's an alias? Make one of your own! *(`alias moo='cowsay moo'`)*
- How did the game hide rooms?

## Challenge

Make a new alias that makes `cowsay` always use the dragon:
`alias dragon='cowsay -f dragon'`, then run `dragon hello`. (It goes away
when you close the terminal; in Stage 5 you'll learn how to keep it.)

## Checkpoint

The learner can, without help:
- [ ] Copy the game, and start it from the entrance
- [ ] Explain what `ls -F`, `./name` and `alias` do

## Lab notebook

Draw the dungeon map so far. Add `ls -F`, `alias` and `./program` to the
dictionary.

## Guide's background *(optional reading)*

Bashcrawl (by Seth Kenlon, GPL licensed) turns the folder tree into a
dungeon: rooms are directories, scrolls are text files, and items are tiny
programs called **shell scripts**. It quietly teaches running programs,
hidden directories, aliases, variables and reading code. It's a joy to
watch a kid realise that the "magic items" are just text files they can
open and read.
