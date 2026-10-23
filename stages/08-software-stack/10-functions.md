# Lesson 8.10: Functions: Call and Return (Project 8)

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the VM card and the Hack card; squared paper; a stack of
sticky notes in two colours · **New words:** call, return, frame,
return address, bootstrap

## Goal *(read this to the learner)*

> When one function calls another, the computer has to remember where it
> was, keep the caller's variables safe, give the new function its own
> fresh variables, and later put everything back exactly as it was. In
> Python that just happens. On your Hack computer, *your translator*
> will make it happen. This is the hardest part of the translator, and
> when it's done, your computer can run real programs made of many
> functions and many files.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once, slowly. The frame (step 2) is the one
      idea that everything else depends on. Act it out yourself first.
- [ ] BasicLoop and FibonacciSeries should pass (Lesson 8.9).

## Warm-up (5 min)

"In Lesson 7.5, what did the nesting dolls show?" *(Each call opens a
new doll; each return closes one, back to the one before.)* "What's the
call stack?" *(The list of functions waiting for an answer, newest on
top.)*

## Activity

### Session 1: acting out a call

1. **The VM commands.** Read the Functions part of the VM card together.
   **Say:**
   - "`function Main.double 1` starts a function called `Main.double`
     with 1 local variable.
   - `call Main.double 1` calls it, after 1 argument has been pushed.
   - `return` goes back, and leaves the answer where the arguments were."

   Write this tiny program on paper:
   ```
   function Main.main 0
   push constant 21
   call Main.double 1
   ...                   (the answer, 42, is now on top)

   function Main.double 0
   push argument 0
   push argument 0
   add
   return
   ```

2. **The frame, with sticky notes.** Use the RAM column from Lesson 8.8,
   starting at 256, and one colour of note for the caller's things.
   Play it:
   - `Main.main` pushes 21. That's the argument.
   - `call Main.double 1` must save **five** things on the stack, in the
     other colour: the **return address** (where `Main.main` carries on
     afterwards), then the caller's `LCL`, `ARG`, `THIS` and `THAT`.
   - Then `ARG` must point at the argument (the 21), and `LCL` at the
     next free place, where `Main.double`'s locals begin.
   - `Main.double` works above all that, using `argument 0`.
   - `return` puts the answer (42) where the 21 was, takes the five
     notes back to restore `LCL`, `ARG`, `THIS` and `THAT`, sets `SP` just
     above the answer, and jumps to the return address.

   **Say:** "The argument, the five saved things and the locals together
   are called the function's **frame**. Compare with the picture on the
   VM card." **Ask:** "Why save `LCL` and `ARG`?" *(The new function
   changes them. Without saving them, the caller would lose its own
   variables.)*

3. **Watch the real thing.** Open `vme` and load the *folder*
   `~/lab/n2t/projects/8/FunctionCalls/FibonacciElement` (choose the
   folder itself, not a file inside). Single-step, and watch the **Call
   Stack** box and the Global Stack. **They should see:** `Sys.init`,
   then `Main.fibonacci` being added and taken off as it calls itself.
   Stop after a while.

### Session 2: function and call

4. **`function`.** **Say:** "`function Main.double 2` marks where the
   function starts, and makes room for 2 locals, each set to 0." Hints:
   - The start is a Hack label with the function's name: `(Main.double)`.
   - "Make room for k locals, set to 0" is the same as pushing 0, k
     times. A Python loop can write those lines.

5. **`call`: the steps.** These steps come from the Nand to Tetris book.
   For `call f n`:
   1. push the return address (a new unique label, like `RETURN7`)
   2. push `LCL`
   3. push `ARG`
   4. push `THIS`
   5. push `THAT`
   6. `ARG` = `SP` − 5 − n
   7. `LCL` = `SP`
   8. jump to `f`
   9. put the return address label here: `(RETURN7)`

   Hints:
   - Step 1 pushes an *address*, a number: `@RETURN7` then `D=A`, then
     `push_d()`. Use your label counter from Lesson 8.7.
   - Steps 2 to 5 push what's *in* `LCL` and the others: `@LCL`, `D=M`.
   - For step 6, work out 5 + n in Python while translating, so the Hack
     only needs one `@`.

   Write `function` and `call`, and test with SimpleFunction (which only
   has `function` and `return`, so it won't pass yet):
   ```
   cd ~/lab/n2t/projects/8
   check-vm FunctionCalls/SimpleFunction
   ```

### Session 3: return

6. **`return`: the steps**, also from the book:
   1. `frame` = `LCL` (keep it in `R13`)
   2. `return address` = the number at `frame` − 5 (keep it in `R14`)
   3. pop the answer, and put it where `ARG` points
   4. `SP` = `ARG` + 1
   5. `THAT` = the number at `frame` − 1
   6. `THIS` = the number at `frame` − 2
   7. `ARG` = the number at `frame` − 3
   8. `LCL` = the number at `frame` − 4
   9. jump to the return address

   **Ask:** "Why must step 2 happen before step 3?" Hint: what if the
   function had no arguments? *(Then `ARG` points at the place where the
   return address was saved, and step 3 would write the answer over it.)*

   Hints: for steps 5 to 8, `@R13`, `AM=M-1`, `D=M` walks one place
   down the frame each time. For step 9, `@R14`, `A=M`, `0;JMP`.

   ```
   check-vm FunctionCalls/SimpleFunction
   ```
   **They should see:** `ALL GOOD! SimpleFunction passes.` Commit.

### Session 4: whole programs

7. **Folders and the bootstrap.** **Say:** "A real program is a folder of
   `.vm` files, one for each class. It starts with a little piece of
   code called the **bootstrap**: set `SP` to 256, then `call Sys.init
   0`." Change the main part of `vm.py`:
   - If `sys.argv[1]` is a folder (`os.path.isdir`), translate every
     `.vm` file in it (`os.listdir`, keeping names ending in `.vm`), one
     after another, into one file: `Folder/Folder.asm`. Start that file
     with the bootstrap.
   - If it's one file, do what it did before, with no bootstrap.

   Hints: `os.path.join(folder, name)` builds a path. The `.asm` name is
   `os.path.join(folder, os.path.basename(folder) + ".asm")`. Remember,
   each file needs its own name for its `static` variables.

8. **Labels belong to functions.** **Say:** "Two functions might both
   have `label LOOP`. In Hack, every label must be different." Keep the
   name of the function you're in (set it at each `function` command),
   and make `label`, `goto` and `if-goto` use `FunctionName$LOOP`, like
   `Main.run$LOOP`.

9. **The big tests.**
   ```
   check-vm FunctionCalls/NestedCall
   check-vm FunctionCalls/FibonacciElement
   check-vm FunctionCalls/StaticsTest
   ```
   **They should see:** `ALL GOOD!` three times. FibonacciElement works
   out the 4th Fibonacci number by calling itself, like Lesson 7.5.
   StaticsTest checks that two files keep their statics apart.

   Run all of Project 8 again, then commit:
   ```
   for t in ProgramFlow/BasicLoop ProgramFlow/FibonacciSeries FunctionCalls/SimpleFunction FunctionCalls/NestedCall FunctionCalls/FibonacciElement FunctionCalls/StaticsTest; do check-vm $t; done
   ```
   **Say:** "Your translator is finished. Any program written in VM code,
   with as many functions and files as you like, can now run on the Hack
   computer. Next, we stop writing VM code by hand, and use a real
   language."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `At line 30: Expression involves M but A=-2 is an illegal memory address.` | No bootstrap: `SP` was never set to 256 | Put the bootstrap at the start of a folder's `.asm`. |
| SimpleFunction's row starts `304`, where `311` should be | The return address wasn't saved before the answer was written | Step 2 before step 3, using `R14`. |
| FibonacciElement's row shows `267` and `4`, where `262` and `3` should be | `ARG` is set to `SP` − n, forgetting the five saved things | `ARG` = `SP` − 5 − n. |
| StaticsTest's row shows `8` where `-2` should be | Two files share their statics | Name statics with each file's own name. |
| NestedCall or FibonacciElement fails, but SimpleFunction passes | Usually one of the five saved things is restored to the wrong place | Check steps 5 to 8 of `return` against the frame picture: THAT is nearest to `LCL`. |
| `NOT YET: vm.py didn't make NestedCall.asm` | Folder mode isn't written yet, or the `.asm` has the wrong name | `Folder/Folder.asm`, made by joining the folder and its own name. |

## Talk about it

- What's in a function's frame? Draw it.
- What does `call` save, and why?
- Why does `return` save the return address before writing the answer?
- What's the bootstrap for?

## Challenge *(if there's time, or for next time)*

- Write `mine/Power/Main.vm` and `Sys.vm` by hand: `Sys.init` calls
  `Main.power 2 10` (two arguments), which works out 2¹⁰ with a loop.
  Translate the folder and run it in `cpu`. *(1024.)*
- How many Hack lines does one `call` make in your translator? And one
  `return`? A big program calls things thousands of times. Write the
  numbers down for Lesson 8.18.

## Checkpoint

The learner can, without help:
- [ ] Draw a frame, and explain each part
- [ ] Say the steps of `call` and `return`, and why the order matters
- [ ] Explain the bootstrap, and labels inside functions
- [ ] Pass all six Project 8 tests

## Lab notebook

Draw the stack during `Main.double`, with the frame labelled. Write the
steps of `call` and `return` in their own words. Commit. Add *call*,
*return*, *frame*, *return address* and *bootstrap* to `dictionary.md`.
Tick Project 8 on the passport.

## Guide's background *(optional reading)*

This completes Nand to Tetris Project 8, and the VM translator. The
function-call protocol is the heart of how all compiled languages work:
a **calling convention** that both caller and callee follow. On real
processors the same jobs are done partly in registers and partly on the
stack, and C's frames, which the learner met in `gdb`'s backtrace
(Lesson 8.3), work in much the same way. The saved return address is
also exactly what a stack buffer overflow overwrites in an attack.

The steps for `call` and `return` in this lesson are the book's, in
words. The Hack code for them is left to the learner, as the authors
ask. The commonest mistakes are in the table, each found by running a
translator with that one bug against the official tests.

The tests NestedCall, FibonacciElement and StaticsTest are whole
programs (folders with a `Sys.vm`), so `check-vm` translates the folder;
SimpleFunction is one file, so it doesn't. Translating each folder into
`Folder/Folder.asm` is what the official test scripts expect.
