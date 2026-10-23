# Lesson 8.18: Project: My Whole Stack

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t` with every project so far; the cards · **New words:** build,
toolchain, optimise, shared routine

## Goal *(read this to the learner)*

> This is the top of the climb. You'll take your Jack game and send it
> down the whole ladder, using only programs you wrote: *your* compiler
> turns it into VM code, *your* VM translator into Hack assembly, *your*
> assembler into binary, and it runs with *your* Math and Memory, on the
> computer you designed from NAND gates. There's one problem on the way:
> it won't fit. You'll make your translator smarter, until it does.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once.
- [ ] Check what's needed, in the learner's account:
      `ls ~/lab/n2t/projects/6/assembler.py ~/lab/n2t/projects/8/vm.py
      ~/lab/n2t/projects/11/compiler.py ~/lab/n2t/projects/12/Math.jack`.
- [ ] Plan a demo day for the last session.

## Warm-up (5 min)

Draw the ladder from Lesson 8.6 from memory. "Which rungs did you
write?" *(All of them except the gates' simulator!)*

## Activity

### Session 1: the build script

1. **One command for the whole ladder.** **Say:** "Putting a program
   through all the tools in order is called a **build**, and the tools
   together are a **toolchain**. A script does it." Make `~/bin/build-all`:
   ```bash
   #!/bin/bash
   # build-all: turns a Jack program folder into a .hack file, with MY tools.
   set -e
   tools=/srv/redstone-library/tools/nand2tetris/tools
   game=$(realpath "$1")
   name=$(basename "$game")
   out=~/lab/n2t/whole/$name
   rm -rf "$out"
   mkdir -p "$out"
   cp "$game"/*.jack "$out/"
   sed -i '/Sys.wait/d' "$out"/*.jack                  # the CPU Emulator is slow enough already
   cp ~/lab/n2t/projects/12/{Math,Memory,Array}.jack "$out/"     # my OS
   for class in Screen Output String Keyboard Sys; do            # the rest of the OS
       cp "$tools/OS/$class.vm" "$out/"
   done
   python3 ~/lab/n2t/projects/11/compiler.py "$out"
   python3 ~/lab/n2t/projects/8/vm.py "$out"
   python3 ~/lab/n2t/projects/6/assembler.py "$out/$name.asm"
   echo "$name.hack: $(wc -l < "$out/$name.hack") instructions. The ROM holds 32768."
   ```
   `chmod +x ~/bin/build-all`. **Say:** "`set -e` stops the script at the
   first thing that fails. The game is copied into a new folder, with
   your Math, Memory and Array, and the official versions of the rest of
   the OS, as VM code. Your Screen draws one pixel at a time, which is
   too slow on the CPU Emulator, so the official one is used (making
   yours faster is a challenge). Then each of your tools runs in turn."

2. **Build Diamond Dash.**
   ```
   build-all ~/lab/n2t/projects/9/DiamondDash
   ```
   **They should see** something like `DiamondDash.hack: 47745
   instructions. The ROM holds 32768.` (Their number will be different;
   it depends on how their compiler and translator write things.)
   Open `cpu`, Load Program, and choose
   `~/lab/n2t/whole/DiamondDash/DiamondDash.hack`. **They should see:**
   `Program too large`.

   **Ask:** "What's using up all the room?" Look inside:
   ```
   grep -c "call " ~/lab/n2t/whole/DiamondDash/*.vm
   ```
   **They should see:** each file's number of calls: a few in some, and
   over a hundred in others. All together there are a few hundred.
   **Say:** "In Lesson 8.10 you counted how many Hack lines one `call`
   makes: about 45. 350 calls times 45 is about 16,000: half the ROM, just
   for calls!"

### Sessions 2 and 3: making it fit

3. **One shared copy.** **Say:** "Every `call` makes the same 45 or so
   lines, with only the function, the number of arguments and the return
   label different. What if those lines were written *once*, at the end of the
   program, and each `call` just jumped there? That's a **shared
   routine**: a subroutine for the translator's own code." To
   **optimise** means to make a program smaller or faster without
   changing what it does.

   The plan for each `call f n`:
   ```
   put 5 + n in R13
   put the address of f in R14
   put the return address (a new label) in D
   jump to ($CALL)
   (the return address label goes here)
   ```
   and once, at the end of the `.asm`:
   ```
   ($CALL)
   push D (the return address)
   push LCL, ARG, THIS, THAT
   ARG = SP - R13
   LCL = SP
   jump to the address in R14
   ```
   Hints:
   - `@Main.main` then `D=A` gives a function's address, like a label.
   - The shared routines go after the whole program, so nothing runs into
     them by accident. In a single file (like SimpleFunction), the
     program would run off its end straight into them, so put an endless
     loop just before them: `($END)`, `@$END`, `0;JMP`.
   - Label names can contain `$`, so `$CALL` can't clash with any VM
     label.

4. **Test everything again.** **Say:** "We changed a working program. The
   tests prove it still works."
   ```
   cd ~/lab/n2t/projects/8
   for t in ProgramFlow/BasicLoop ProgramFlow/FibonacciSeries FunctionCalls/SimpleFunction FunctionCalls/NestedCall FunctionCalls/FibonacciElement FunctionCalls/StaticsTest; do check-vm $t; done
   cp vm.py ../7/vm.py
   cd ../7
   for t in StackArithmetic/SimpleAdd StackArithmetic/StackTest MemoryAccess/BasicTest MemoryAccess/PointerTest MemoryAccess/StaticTest; do check-vm $t; done
   ```
   **They should see:** eleven `ALL GOOD!` lines. Then build again:
   ```
   build-all ~/lab/n2t/projects/9/DiamondDash
   ```
   **They should see** something like `35320 instructions`: over 12,000
   fewer! But still more than 32,768. Commit anyway: it's progress.

5. **Making it fit.** Two more shrinks, each followed by all eleven tests
   and a build:
   - **`return`** is the same every time too: make one shared `($RETURN)`
     routine, and make each `return` jump to it.
   - **`push`**: `push_d()` can be four lines instead of five: `@SP`,
     `AM=M+1`, `A=A-1`, `M=D`. **Ask:** "Why does it work?" *(SP goes up
     first, and A is pointed at the box just below the new SP.)*

   Each one makes the build smaller. With the course's own tools, the
   numbers went 47,745, then 35,320 (shared call), 31,880 (shared
   return: it fits!), and 28,268 (shorter push, leaving room to spare).
   Write down yours, and load the `.hack` in `cpu` after each build until
   it stops saying `Program too large`. Commit.

### Session 4: play it

6. **The moment.** Open `cpu`, Load Program,
   `~/lab/n2t/whole/DiamondDash/DiamondDash.hack`. Set **Animate** to **No
   animation**, Run, and click the keyboard bar. **They should see:** the
   title, slowly: the CPU Emulator is a program pretending to be the Hack
   computer, much slower than the VM Emulator. Press a key, wait for the
   world to be drawn, and play with the arrow keys.

   **Say:** "Every instruction running now was made by your compiler,
   your translator and your assembler. It does its sums with your Math,
   and keeps its objects with your Memory. It runs on the computer you
   designed, from NAND gates. That's the whole of Nand to Tetris."

7. **Your game.** Build the learner's own game from Lesson 8.12 the same
   way. If it doesn't fit, try the challenges below, or make the game a
   little smaller. Commit, and tick the top of the climb on the
   passport.

### Session 5: demo day, and the checkpoint

8. **Demo day.** The learner shows someone the whole ladder: the Jack
   source, the VM code, the assembly, the binary, and the game running.
   They explain one rung in detail, their choice.

9. **The Stage 8 checkpoint.** Without notes, the learner explains,
   with drawings if they like:
   - What a pointer is, and what goes wrong with buffer overflows, leaks
     and use after free (Lessons 8.2 to 8.4).
   - How `push local 2` and `add` become Hack (8.7, 8.8).
   - What `call` saves, and why (8.10).
   - The three jobs of a compiler, and what recursive descent means
     (8.13, 8.14).
   - How a method call passes the object, and how `a[i]` works (8.16).
   - How `Math.multiply` works with only adding (8.17).

   If any is shaky, go back to that lesson's checkpoint.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Program too large` | More than 32,768 instructions | Shrink the translator (steps 3 and 5), or the game. |
| `KeyError: 'M+D'` (or another comp) from the assembler | The translator writes a spelling that the Hack card doesn't have | Change the translator to the card's spelling: `D+M`, `D&M`, `D\|M`. |
| `build-all` stops after the compiler, with a Python error | The compiler can't handle something in the game or the OS files | Run `python3 ~/lab/n2t/projects/11/compiler.py` on the folder by hand, and read the error. |
| A test that passed before now fails | The shrink broke something | Compare with the last commit: `git diff`. Check the shared routines come after an endless loop. |
| The game draws, then nothing happens when keys are pressed | The keyboard bar isn't active, or the program is still drawing | Click the bar, and wait: it's slow. |
| The game runs much too fast or slow | The `sed` line removed the waits; the CPU Emulator's speed depends on the computer | Change the game's `speed` and try again. |

## Talk about it

- What does each tool in the toolchain do? Draw it.
- Why didn't the game fit at first? What did the shared routines change?
- Why run every test again after optimising?
- What would make the whole thing faster?

## Challenge *(if there's time, or for next time)*

- Make `eq`, `gt` and `lt` shared routines too.
- `push local 1` can be done without adding: `@LCL`, `A=M`, `A=A+1`,
  `D=M`. Use that for small offsets.
- Make your own `Screen.drawRectangle` fast enough to use instead of the
  official one: in the middle of each row, set whole words of 16 pixels
  to −1 at once, and only draw single pixels at the two ends.
- Run Pong through your whole stack.

## Checkpoint

The learner can, without help:
- [ ] Build a Jack program with their own toolchain, and explain each step
- [ ] Explain why the first build was too big, and how shared routines
      fix it
- [ ] Re-run every test after changing the translator
- [ ] Play their game on the CPU Emulator, from their own `.hack` file
- [ ] Answer the Stage 8 checkpoint questions (step 9)

## Lab notebook

Draw the toolchain from `.jack` to `.hack`, with the size at each step.
Write the instruction counts before and after each shrink. Commit. Add
*build*, *toolchain*, *optimise* and *shared routine* to
`dictionary.md`. Stamp the Stage 8 badge, **Stack Climber**, on the
passport.

## Guide's background *(optional reading)*

This lesson completes the "build it all yourself" promise of Nand to
Tetris. The book notes that a straightforward VM translator produces
code too large for the 32K ROM once the OS is included, and suggests
the shared call/return routines used here. These are the kind of
**code-size optimisations** real compilers make: the same machine code
written once and reached by a jump, instead of copied many times. It
costs a few extra jumps at run time, and saves most of the space.

The numbers in step 5 came from the course's own reference tools, kept
out of the repository: Diamond Dash with the learner-style Math, Memory
and Array, built by a naive translator, then with each shrink. The
learner's numbers will differ, but the pattern (the shared `call` saves
by far the most) is the same for any straightforward translator.

`build-all` uses the official `Screen.vm` because a pixel-at-a-time
Screen, run as Hack code on the CPU Emulator, takes about a minute to
draw the game's world. It also removes `Sys.wait`, which is tuned for
the VM Emulator's speed. The game was tested in the CPU Emulator in this
form, in a slow virtual screen: it plays, slowly. On a real desktop it
should be faster. In Stage 9, the assembler is rebuilt in Rust; the
"build it again" thread continues.
