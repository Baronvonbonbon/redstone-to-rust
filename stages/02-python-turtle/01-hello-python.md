# Lesson 2.1: Hello, Python

**Time:** 45 min · **You need:** Thonny (installed by setup) · **New words:**
program, Python, shell, editor, print, operator

## Goal *(read this to the learner)*

> Until now you've been *using* programs that other people wrote. Today
> you start **writing your own**, in a language called **Python**. By the
> end, you'll have saved your very first program, and you'll know how to
> make Python do maths faster than any calculator.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Log in as the learner and open Thonny once yourself (Super key, type
      `thonny`, press Enter). The first time, it asks for a language and
      "Initial settings": choose **English** and **Standard**, then
      **Let's go!**
- [ ] In a terminal, make the folder for this stage's programs:
      `mkdir -p ~/lab/python`
- [ ] Close Thonny again, so the learner can open it.

## Warm-up (5 min)

"Remember the robot sandwich, from the very first lesson? The robot did
*exactly* what the instructions said, even when that was silly. A
**program** is a list of instructions for a computer. Python is one of the
languages we can write them in. Python was named after a comedy show, not
the snake!"

## Activity

1. **Open Thonny.**

   **Say:** "Press the Super key, type `thonny`, and press Enter."

   **They should see:** a window with a big empty area at the top (the
   **editor**) and a smaller area at the bottom labelled **Shell**, with
   `>>>` in it.

   **Say:** "The bottom part, the Shell, is like the terminal: you type
   one line, press Enter, and Python answers straight away. The top part
   is for writing whole programs that you save and keep."

2. **Python as a calculator.** Click in the Shell, next to `>>>`.

   **Learner types** (one line at a time, pressing Enter after each):
   ```python
   2 + 3
   100 - 37
   7 * 8
   20 / 4
   ```
   **They should see:** `5`, `63`, `56`, and `5.0`.

   **Say:** "`*` is how computers write 'times', because `x` is a letter.
   `/` means 'divided by'. Notice that `20 / 4` gave `5.0` with a dot:
   dividing always gives a number with a decimal point, just in case."

3. **Big numbers and new tricks.**
   ```python
   2 ** 10
   12345679 * 9
   99999999 * 99999999
   ```
   **Say:** "`**` means 'to the power of': `2 ** 10` is ten 2s multiplied
   together. And Python never runs out of room for big numbers. Try an
   even bigger one!"

   Let them experiment for a few minutes. Ask: "What's `2 ** 100`?"

4. **Sharing out sweets: `//` and `%`.**

   **Say:** "17 sweets, shared between 5 friends. How many each, and how
   many left over?" Let them work it out (3 each, 2 left over). Then:
   ```python
   17 // 5
   17 % 5
   ```
   **They should see:** `3` and `2`.

   **Say:** "`//` is how many each friend gets: divide and throw away the
   leftovers. `%` is the leftovers, called the **remainder**. Programmers
   use `%` all the time. Is 10 even? Try `10 % 2`. A remainder of 0
   means it shares out perfectly."

5. **Words in Python.**
   ```python
   print("Hello!")
   print("Hello " * 3)
   "ha" * 10
   ```
   **Say:** "Words go inside quote marks, so Python knows they're words
   and not instructions. Programmers call words in quotes a **string**,
   like letters on a string of beads. And yes, you can multiply them!"

6. **The first real program.** Click in the editor (the top part).

   **Learner types:**
   ```python
   print("Hello, I am a programmer!")
   print("My name is ...")
   print("7 times 8 is", 7 * 8)
   ```
   (They put their own name in line 2.)

   **Say:** "Nothing happened, because this is a program, not a
   conversation. Programs run when you tell them to."

7. **Save it.** Press **Ctrl+S**. In the save box, go into the `lab`
   folder, then `python`, and call the file `hello.py`. Click **Save**.

   **Say:** "The `.py` on the end tells everyone 'this is Python'."

8. **Run it.** Press **F5** (or click the green ▶ button).

   **They should see** in the Shell:
   ```
   Hello, I am a programmer!
   My name is ...
   7 times 8 is 56
   ```

   **Say:** "That's your first program! Notice the third line: Python did
   the maths for you, and `print` showed the words and the answer
   together, with a comma between them."

9. **Run it from the terminal, too.** Open a terminal (Ctrl+Alt+T).
   ```
   cd ~/lab/python
   ls
   python3 hello.py
   ```
   **They should see:** the same three lines.

   **Say:** "Same program, two ways to run it. Thonny is a helpful
   workshop, but your program is just a file, and the terminal can run it
   too. Everything you learned in Stage 1 still works."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `SyntaxError: invalid syntax` | Python didn't understand the line | Check for a missing quote mark or bracket. Every `(` needs a `)`, every `"` needs a partner. |
| `NameError: name 'Hello' is not defined` | Words without quote marks | Python thought `Hello` was an instruction. Put it in quotes: `"Hello"`. |
| `SyntaxError: unterminated string literal` | A quote mark is missing at the end | Add the closing `"`. |
| Pressing F5 asks to save first | The program isn't saved yet | Save it in `~/lab/python/`, then F5 again. |
| `python3: can't open file 'hello.py'` | The terminal is in the wrong folder | `cd ~/lab/python` first, then `ls` to check the file is there. |
| `print ("hi")` with a space works too | Not an error | Python doesn't mind, but the usual style is no space. |

## Talk about it

- What's the difference between the Shell and the editor?
  *(The Shell runs one line straight away; the editor holds a whole
  program you can save and run again.)*
- Why does Python need quote marks around words?
  *(So it can tell words-to-show apart from instructions.)*
- What would `100 % 7` be? Work it out first, then check.
  *(100 = 14 × 7 + 2, so 2.)*

## Challenge *(if there's time, or for next time)*

- How many seconds are there in a day? In a year? Write the sum in Python
  (`60 * 60 * 24`).
- Make a program `big-hello.py` that prints a box made of `*`:
  `print("*" * 20)` and so on.
- Is 1001 even or odd? Use `%`. Is 1001 divisible by 7? By 11? By 13?

## Checkpoint

The learner can, without help:
- [ ] Open Thonny and use the Shell as a calculator, with `+ - * / ** // %`
- [ ] Explain `//` and `%` with the sweets example
- [ ] Write, save (in `~/lab/python`) and run a program with `print`
- [ ] Run the same program from the terminal with `python3`

## Lab notebook

Start a new section called **Python**. Write the seven operators
(`+ - * / ** // %`) with an example of each. Copy out `hello.py`. Add
*program*, *shell*, *editor*, *string* and *remainder* to the dictionary.

## Guide's background *(optional reading)*

Python is one of the most popular programming languages in the world.
It's used by scientists, game makers and websites, and it was designed
to be easy to read. Thonny is a free editor made at the University of
Tartu specially for beginners: it shows what Python is doing step by
step, which we'll use later.

The **Shell** (sometimes called the REPL, for read-evaluate-print loop)
answers one line at a time, which makes it perfect for experiments. The
**editor** is where real programs live. A habit worth building now:
experiment in the Shell, then put what works into a saved program.

`//` (floor division) and `%` (modulo, or remainder) come up constantly
in programming: for odd and even numbers, for clocks that wrap round from
12 to 1, for repeating colour patterns, and much more. It's worth getting
comfortable with them now, using sharing problems.
