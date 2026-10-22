# Lesson 1.5: Terminal Superpowers

**Time:** 30 min · **New words:** tab completion, history, interrupt

## Goal *(read this to the learner)*

> Typing long names gets tiring. Real terminal wizards barely type at all:
> they have **superpowers**. Today you unlock five of them.

## Before the lesson *(guide, 2 min)*

- [ ] Make sure there are a few files and folders in `~/lab` to practise with.

## Warm-up (5 min)

"Show me how to copy a file. And how to rename one."

## Activity

1. **Superpower 1: Tab completion.** Go home (`cd`), type `cd la`, then
   press the **Tab** key (don't press Enter yet).
   It finishes the word for you: `cd lab/`! Now press Enter.

   Now type `cat ~/lab/jo` and press **Tab**. It completes `jokes.txt`.

   When there's more than one match, press **Tab twice** to see all the
   choices. Try `cd ~/lab/` and press Tab twice.

   **Say:** "Tab completion also stops typos, because the computer only
   completes things that really exist. Use Tab ALL THE TIME."

2. **Superpower 2: Time travel (the up arrow).** Press **↑**. The last
   command appears again! Press ↑ again for older commands, and **↓** to
   come forward. Press Enter to run one again, or change it first.

3. **Superpower 3: Your whole history.**
   ```
   history
   ```
   Every command you've typed, numbered. (They'll see their first
   `cowsay`!)

4. **Superpower 4: The emergency stop (Ctrl+C).** Run something that
   doesn't stop by itself:
   ```
   cat
   ```
   It sits and waits, forever. Press **Ctrl+C**. Back to the prompt!
   Try `yes` too: it prints `y` forever, very fast. **Ctrl+C** stops it.
   **Say:** "Ctrl+C means 'stop!' Whenever the terminal seems stuck, try
   Ctrl+C first."

5. **Superpower 5: Copy and paste.** In the terminal, the normal Ctrl+C
   is taken (it means stop!). So:
   - **Copy:** select text with the mouse, then press **Ctrl+Shift+C**
   - **Paste:** **Ctrl+Shift+V**

   Practise: run `echo abracadabra-hocus-pocus-42`, copy the output, then
   type `echo ` and paste it.
   They'll need this a lot in the Mineshaft (Lesson 1.14).

6. **Bonus moves.**
   - **Ctrl+L**: clear the screen (same as `clear`)
   - **Ctrl+A** / **Ctrl+E**: jump to the start / end of the line
   - **Ctrl+U**: delete everything before the cursor (start over)

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Tab does nothing | Nothing matches what's typed so far, or there are several matches | Press Tab twice to see the options. Check the spelling of the start. |
| A `^C` appears | That's just Ctrl+C showing | Normal! |
| Pasted the wrong thing | | Ctrl+U clears the line. |

## Talk about it

- Which superpower will you use most? *(Tab!)*
- What do you do if the terminal seems stuck? *(Ctrl+C)*
- Why is copy in the terminal Ctrl+**Shift**+C?

## Challenge

**Typing golf.** You name a command; they run it using the fewest key
presses (Tab and ↑ allowed). For example: "Show what's in
`~/lab/stories/silly-story.txt`."

## Checkpoint

The learner can, without help:
- [ ] Use Tab to complete a file name
- [ ] Rerun an old command with ↑
- [ ] Stop a running command with Ctrl+C
- [ ] Copy and paste in the terminal

## Lab notebook

Draw five "superpower" badges: Tab, ↑, `history`, Ctrl+C and Ctrl+Shift+C/V.

## Guide's background *(optional reading)*

These shortcuts belong to **bash** (the shell) and the terminal app. Tab
completion matters more than it seems: it saves typing, *and* it's an
instant check that a file really exists. Watch for the habit in later
lessons, and gently remind them: "Tab!"
