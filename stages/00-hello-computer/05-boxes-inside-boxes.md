# Lesson 0.5: Boxes Inside Boxes

**Time:** 40 min · **You need:** the learner logged in, a few small boxes or
envelopes, paper scraps · **New words:** file, folder (also called a
directory), home folder, save

## Goal *(read this to the learner)*

> Everything you keep on a computer, like a drawing, a story or a game,
> is a **file**. Files live in **folders**, and folders can live inside
> other folders, like boxes inside boxes. Today you'll make your own
> folders and save your own files into them.

## Before the lesson *(guide, 5 min)*

- [ ] Gather 3 or 4 boxes or envelopes of different sizes, and some paper
      scraps with words written on them ("drawing", "story", "song").
- [ ] Check that the learner's account has a `lab` folder (the setup
      script made it).

## Warm-up: real boxes (10 min)

1. Write `HOME` on the biggest box. Inside it, put a box labeled `lab`.
   Inside `lab`, put a box labeled `art`.
2. Hand them a paper scrap that says "dragon drawing" and ask: "Where
   should this go?" They put it in `art`.
3. Ask: "How would you tell someone where the dragon drawing is, without
   pointing?" Help them say: "Open HOME, then lab, then art." Write it
   down like a computer would:

   ```
   home / lab / art / dragon-drawing
   ```

   Say: "That's called a **path**. It's directions through the boxes."

## Activity

1. **Open the Files app.** Press Super, type `files`, and press Enter.
   This is their home folder: the big HOME box. Point out the folders
   that are already there (Documents, Pictures, `lab`, and so on).

2. **Go inside `lab`.** Double-click it. Show the path at the top of the
   window. It's the same idea as the boxes!

3. **Make folders.** Right-click an empty space, choose **New Folder**,
   and name it `art`. Make another one called `stories`.
   *Naming tip:* use lowercase letters and dashes, with no spaces
   (`my-stories`, not `My Stories`). This will matter a LOT in Stage 1.

4. **Save a story.** Open the text editor (Super, type `text editor`).
   Write two or three sentences of a silly story. Choose **File, Save
   As**, find your way to `lab`, then `stories`, name it `silly-story.txt`,
   and click **Save**.

5. **Save a drawing.** Open Tux Paint and draw something. Click **Save**.
   Tux Paint keeps drawings in its own special place, so to get the
   drawing into `lab`, click **Open**, choose the drawing, and click
   **Export** (if your version has it). That puts a copy in `Pictures`.
   Then, in Files, **drag** it from `Pictures` into `lab`, then `art`.
   *(No Export button? Skip this step and just save a second story instead.)*

6. **Check the boxes.** In Files, go back to `lab`. Open each folder.
   Are the files where they should be?

7. **Try to peek.** In Files, type `/home` in the path bar. Can they see
   other people's home folders? Try to open the guide's. *(It's locked:
   "Permission denied", or a padlock icon.)* "Your account keeps your
   things private, and theirs too."

## If something goes wrong

| What happens | What to do |
|---|---|
| Can't find the saved file | Open the editor again and choose File, Save As: the window shows where it was saved last time. |
| Saved it in the wrong folder | Great chance to practise dragging it to the right one. |
| Put spaces in the name | It's fine for now; just rename it (right-click, Rename) using dashes, and explain why it'll matter in Stage 1. |

## Talk about it

- What's the difference between a file and a folder?
  *(A file is a thing; a folder holds things.)*
- Write the path to your silly story. *(home / name / lab / stories / silly-story.txt)*
- Why can't you open your guide's folder?

## Challenge

Make a folder inside a folder inside a folder: `lab/art/dragons/fire-dragons`.
Write its path.

## Checkpoint

The learner can, without help:
- [ ] Make a new folder inside `lab`
- [ ] Save a file into a folder they choose, and find it again later
- [ ] Say the path to a file

## Lab notebook

Draw the folder tree of `lab` as boxes inside boxes, or as a tree with
branches. Write the path to one file.

## Guide's background *(optional reading)*

Files and folders (computer people often say "directories") form a
**tree**: one root at the top, with branches inside branches. On Linux
the very top is `/`, and the learner's home is `/home/theirname`. The
path `/home/sam/lab/stories/silly-story.txt` is that file's full address.

In Stage 1 the learner will move around this same tree by typing
instead of clicking, and things will be much easier if the names have
no spaces in them. That's why we start the habit now.
