# Lesson 0.7: Pictures Made of Numbers

**Time:** 40 min · **You need:** graph paper (or a hand-drawn grid of 10×10
squares), pencils, a magnifying glass if you have one · **New words:**
pixel, resolution, compression

## Goal *(read this to the learner)*

> Last time you found out computers store numbers as 0s and 1s. But how
> does a computer store a *picture*? Today you'll send a picture to
> someone using only numbers, and they'll draw it without ever seeing it.

## Before the lesson *(guide, 10 min)*

- [ ] Draw two 10×10 grids (or use graph paper).
- [ ] On a scrap of paper, write out this secret picture code (it's a
      heart), but don't show the drawing:

      ```
      Row 1:  0 1 1 0 0 0 1 1 0 0
      Row 2:  1 1 1 1 0 1 1 1 1 0
      Row 3:  1 1 1 1 1 1 1 1 1 0
      Row 4:  1 1 1 1 1 1 1 1 1 0
      Row 5:  0 1 1 1 1 1 1 1 0 0
      Row 6:  0 0 1 1 1 1 1 0 0 0
      Row 7:  0 0 0 1 1 1 0 0 0 0
      Row 8:  0 0 0 0 1 0 0 0 0 0
      Row 9:  0 0 0 0 0 0 0 0 0 0
      Row 10: 0 0 0 0 0 0 0 0 0 0
      ```

## Warm-up (5 min)

If you have a magnifying glass, look closely at the computer screen (or a
phone screen). "See the tiny dots? Every picture on a screen is made of
tiny coloured squares called **pixels**." No magnifying glass? Zoom far
into a picture on the computer until it goes blocky.

## Activity

1. **Decode the secret picture.** Read the code out loud, row by row. The
   learner colours a square for each **1** and leaves each **0** blank. What
   is it? *(A heart!)*

2. **Make your own.** They draw their own picture on a 10×10 grid: a
   Creeper face, a sword, a smiley, a letter. Then they write its code,
   row by row.

3. **Send it.** Swap codes. You draw *their* picture from just the
   numbers, without peeking. Compare the drawings. Same? *(It should be,
   if nobody made a mistake. If not, find the bug!)*

4. **Shrink it: "how many in a row".** Writing all those 0s is boring. A
   shorter way: say how many of each colour come in a row. Row 1 of the
   heart, `0 1 1 0 0 0 1 1 0 0`, becomes:

   ```
   1 white, 2 black, 3 white, 2 black, 2 white
   ```

   Have them write the shortened version of their own picture. Is it
   shorter? Say: "Making data shorter without losing anything is called
   **compression**."

5. **Colours.** "What if we want colours?" Use a number for each colour:
   0 = white, 1 = black, 2 = green, 3 = red. Make a 6×6 coloured Creeper
   face using those numbers.

## If something goes wrong

| What happens | What to do |
|---|---|
| Loses their place in a row | Use a ruler or a finger under the row being read. |
| The drawings don't match | Debug it! Go row by row and compare. Bugs are normal; finding them is the skill. |

## Talk about it

- How did the computer turn your picture into numbers? *(One number for
  each square.)*
- Why would a bigger grid make a better picture? *(More, smaller squares
  show more detail. That's called higher **resolution**.)*
- When would "how many in a row" not save space? *(When the colours keep
  changing: 0 1 0 1 0 1...)*

## Challenge

Make a 16×16 pixel version of your favourite Minecraft item, with 4
colours. How many numbers does it need? *(16 × 16 = 256.)*

## Checkpoint

The learner can, without help:
- [ ] Draw a picture from a grid of 0s and 1s
- [ ] Turn their own drawing into numbers that someone else can redraw

## Lab notebook

Glue in your pixel picture and its code. Write: "A picture on a computer
is a grid of **pixels**, and each pixel is a number."

## Guide's background *(optional reading)*

Screens and image files really work like this. Each pixel's colour is
stored as numbers (usually three of them: how much red, green and blue).
"How many in a row" is a real compression method called **run-length
encoding**, used in fax machines and some image formats. In Stage 4 the
learner will write a picture file *by hand*, as numbers in a text file,
and open it in a real image viewer.

This activity is adapted from CS Unplugged's "Image Representation"
(csunplugged.org), which has more variations.
