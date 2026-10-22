# Lesson 1.11: The Treasure Cave

**Time:** 40 min · **You need:** a fresh Treasure Cave in the learner's
home (see below) · **New words:** search, recursive

## Goal *(read this to the learner)*

> Deep in your home folder, a cave has appeared, full of ore: coal, iron,
> gold, redstone... and somewhere, ONE diamond. The cave is too big to
> search by hand. Time to learn `find`, the treasure detector.

## Before the lesson *(guide, 5 min)*

- [ ] From **your** account, in the course folder, run:
      ```
      ./scripts/give-lab.sh LEARNER cave
      ```
      (with the learner's account name). It prints the answers. Write them
      down somewhere the learner won't see.

## Warm-up (5 min)

"What does `*` mean? What does `| wc -l` do?"

## Activity

1. **Enter the cave.**
   ```
   cd ~/cave
   ls
   cat QUEST.txt
   ```
   Read the quest together. There are five questions.

2. **Question 1** *(how much coal is in the entrance)*:
   ```
   ls entrance/*.coal
   ```
   They count. Or, even better, they let the computer count:
   ```
   ls entrance/*.coal | wc -l
   ```

3. **Question 2** *(which rooms are where)*: let them explore with `cd`
   and `ls`, then show them the map maker:
   ```
   tree -d
   ```
   (`-d` shows only **d**irectories.)

4. **Question 3** *(where's the diamond?)*. Exploring by hand takes ages.
   ```
   find . -name "*.diamond"
   ```
   **Say:** "`find` searches *everywhere* below a folder. The `.` means
   'start here'. `-name` says what to look for. The quotes stop the
   shell from using the `*` too early."

5. **Question 4** *(how much gold in the whole cave)*:
   ```
   find . -name "*.gold" | wc -l
   ```

6. **Question 5:** `cat` the diamond, using the path that `find` gave.
   Tab completion makes it easy.

7. **Check against your answers.** Celebrate!

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `cd: cave: No such file or directory` | The cave wasn't made, or they're in the wrong folder | `cd ~` first. If it's still missing, run the give-lab command. |
| `find` prints nothing | The name pattern is wrong | Check the quotes and the `*`. Try `find . -name "*diamond*"`. |
| `find: paths must precede expression` | The quotes are missing around `*.gold` | Add the quotes: `"*.gold"`. |

## Talk about it

- Why is `find` better than exploring by hand?
- What does the `.` mean in `find .`? *(Start searching here.)*
- How did we count the gold without counting? *(The pipe into `wc -l`.)*

## Challenge

- Find every file in the cave that's in a room called `bat-roost`:
  `find . -path "*bat-roost*" -type f`
- Find all the folders: `find . -type d`
- How many blocks of *anything* are there? `find . -type f | wc -l`
- Find your own jokes file, starting from home: `find ~ -name "jokes.txt"`

## Checkpoint

The learner can, without help:
- [ ] Use `find` to locate a file by name
- [ ] Count found things with `| wc -l`

## Lab notebook

Write the quest answers. Add `find . -name` and `tree -d` to the dictionary.

## Guide's background *(optional reading)*

`find` walks through a folder and every folder inside it (that's what
**recursive** means) and lists the matches. It has many options: by
type, size, owner or age. The Mineshaft's level 5 needs `find -name`, and
level 12 (in Stage 5) needs more of its options. You can make a new cave
for practice any time; each one is randomly different.
