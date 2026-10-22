# Lesson 1.4: Moving, Copying and the Shredder

**Time:** 40 min · **New words:** copy, move, rename, delete, recursive

## Goal *(read this to the learner)*

> Today you'll learn to copy things, move them, rename them... and use
> the **shredder**. The terminal has no recycle bin. When you delete
> something here, it's gone **forever**. With great power comes great
> responsibility!

## Before the lesson *(guide, 2 min)*

- [ ] Check that `~/lab/terminal-fun` exists from Lesson 1.3.
- [ ] Today's practice happens in a sandbox folder, so nothing important
      can get shredded.

## Warm-up (5 min)

"What's the difference between `>` and `>>`? How do you see what's inside
a file?"

## Activity

1. **Make a sandbox.**
   ```
   mkdir ~/lab/sandbox
   cd ~/lab/sandbox
   echo I am a potato > potato.txt
   ls
   ```

2. **Copy.**
   ```
   cp potato.txt potato-copy.txt
   ls
   cat potato-copy.txt
   ```
   "`cp` = **c**o**p**y. First what to copy, then the name of the copy."

3. **Rename, with `mv`.**
   ```
   mv potato-copy.txt french-fry.txt
   ls
   ```
   "`mv` = **m**o**v**e. Moving a file to a new name is the same as renaming it!"

4. **Move into a folder.**
   ```
   mkdir kitchen
   mv french-fry.txt kitchen/
   ls
   ls kitchen
   ```

5. **Copy a whole folder** (this needs `-r`):
   ```
   cp -r kitchen kitchen-backup
   ls
   ```
   "`-r` means **r**ecursive: copy the folder *and everything inside it*."

6. **The shredder.** Read this part slowly and seriously.
   ```
   rm potato.txt
   ls
   ```
   **Say:** "Gone. Not in a bin, not anywhere. `rm` = **r**e**m**ove. There's
   **no undo**."

7. **The safety catch.** `-i` makes `rm` ask first:
   ```
   rm -i kitchen/french-fry.txt
   ```
   **They should see:** `rm: remove regular file 'kitchen/french-fry.txt'?`
   They type `y` and press Enter.

8. **Removing folders.**
   ```
   rmdir kitchen
   ```
   That works when the folder is empty. Try removing the backup:
   ```
   rmdir kitchen-backup
   ```
   **They should see:** `rmdir: failed to remove 'kitchen-backup': Directory not empty`.
   "Good! The computer is protecting you." To remove a folder with things
   inside, use `rm -r`, carefully:
   ```
   rm -ri kitchen-backup
   ```
   It asks about each thing. Answer `y` each time.

9. **The Shredder Rules.** Write these in the notebook together:
   1. Before `rm`, run `pwd` and `ls` to check where you are and what's there.
   2. Use `rm -i` when you're unsure.
   3. Never type `rm` with `*` or `-r` near your home folder, unless your
      guide is watching.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `cp: -r not specified; omitting directory` | Tried to copy a folder without `-r` | Add `-r`. |
| `rm: cannot remove 'x': Is a directory` | `rm` won't remove folders on its own | `rmdir` for empty folders, or `rm -r` (carefully). |
| They deleted something important | It's gone, unfortunately | If it was in `lab`, it's a lesson learned. (From Stage 5, git will make undo possible!) |
| `mv` "lost" a file | It was probably moved into the wrong folder, or renamed | `ls` around, and `find ~ -name 'NAME'` (Lesson 1.11). |

## Talk about it

- What's the difference between `cp` and `mv`?
- Why is `rm` dangerous? How can you be safer?
- Why does copying a folder need `-r`?

## Challenge

In the sandbox: make `a.txt`, copy it to `b.txt`, make a folder `box`, move
both files into `box`, rename `box` to `crate`, then delete `crate` and
everything in it. Check with `tree` after each step.

## Checkpoint

The learner can, without help:
- [ ] Copy and rename a file, and move it into a folder
- [ ] Delete a file and an empty folder
- [ ] Say the Shredder Rules

## Lab notebook

Add `cp`, `cp -r`, `mv`, `rm`, `rm -i`, `rmdir` and `rm -r` to the command
dictionary. Copy the Shredder Rules on a page by themselves.

## Guide's background *(optional reading)*

The learner's account can only delete its *own* files, so the worst
case is losing their own work, not breaking the computer. That's why
they have a non-admin account. Still, `rm -r` is the most dangerous
everyday command, and the habits taught here (look before you delete,
and use `-i` when unsure) are exactly what professionals do.
