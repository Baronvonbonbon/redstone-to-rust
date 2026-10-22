# Lesson 5.15: The Final Vault (Mineshaft Level 19)

**Time:** 2 sessions of 45 min · **You need:** the Mineshaft running;
the miner19 password; the [guide's handbook](../../labs/mineshaft/README.md)
· **New words:** protocol, socket, client, automate

## Goal *(read this to the learner)*

> The bottom of the Mineshaft is guarded by a vault that asks twenty
> sums, and gives you one second for each. No human can type that fast.
> But a program can! Today you'll write a Python program that connects to
> the guard over the network, reads its questions, works out the answers
> and sends them back, all by itself. Beat the vault, and the trophy at
> the very bottom is yours.

## Before the lesson *(guide, 10 min)*

- [ ] Re-read level 19 in the [guide's handbook](../../labs/mineshaft/README.md),
      including the full solution. Use it only if the learner is truly
      stuck, a piece at a time.
- [ ] Check the Mineshaft is up: `./mineshaft.sh status`.

## Warm-up (5 min)

"How did you talk to the gatekeeper on level 16?" *(`nc localhost
30016`.)* "In Python, how do you split a sentence into words?"
*(`.split()`.)* "How do you turn `"42"` into a number?" *(`int("42")`.)*

## Activity

### Session 1: understanding the guard

1. **Read the notes.** Log in as miner19.
   ```
   cat GOAL.txt
   cat vault-notes.txt
   ```
   Read the notes together, slowly. **Say:** "These notes describe exactly
   how the guard talks: what it says first, what each question looks like,
   what it wants back, and what happens if you're wrong. An agreed way of
   talking between two programs is called a **protocol**. Programs only
   understand each other if they follow it exactly."

2. **Try it by hand.**
   ```
   nc localhost 30019
   ```
   **They should see:** `HELLO MINER. 20 QUESTIONS. 1 SECOND EACH.` and
   a sum. Try to type the answer quickly. **They should see:** `BOOM`, and
   the guard hangs up. **Say:** "Impossible by hand. That's the point: some
   jobs need a program. Making a computer do a job for you is called
   **automating** it."

3. **A scratch folder and the first step.** The home folder is
   read-only, as before:
   ```
   cd "$(mktemp -d)"
   nano vault.py
   ```
   (Or `vim vault.py`.) Start small, with just connecting and listening:
   ```python
   import socket

   s = socket.create_connection(("localhost", 30019))
   f = s.makefile("rw")
   print(f.readline())
   print(f.readline())
   ```
   Save, then run it: `python3 vault.py`. **They should see:** the hello
   line and the first question, for example `WHAT IS 4821 + 9932?`.

   **Say:** "A **socket** is one end of a network connection, a program's
   telephone. `create_connection` dials the guard's port. `makefile`
   lets us read and write the connection like a file, with `readline`.
   Our program is now the **client**, like `nc` was."

4. **Take the question apart.** Change the end of the program:
   ```python
   print(f.readline())
   question = f.readline()
   words = question.split()
   print(words)
   ```
   **They should see:** something like
   `['WHAT', 'IS', '4821', '+', '9932?']`.

   Ask: "Which words are the numbers? What's in the way?" *(Positions 2
   and 4, and the `?` stuck to the second number.)* Try in the Python
   Shell: `"9932?".rstrip("?")` *(`'9932'`: `rstrip` strips characters off
   the right-hand end.)*

### Session 2: beating the vault

5. **Answer one question.** Change the end again:
   ```python
   words = question.split()
   answer = int(words[2]) + int(words[4].rstrip("?"))
   f.write(f"{answer}\n")
   f.flush()
   print(f.readline())
   ```
   Run it. **They should see:** `CORRECT`! **Say:** "`f.write` sends the
   answer, with `\n` at the end because the guard reads whole lines.
   `flush` means 'send it now, don't wait'. Without `flush`, the answer
   would sit in a waiting area and the guard would say BOOM."

6. **All twenty.** Put the question part in a loop, and read the prize at
   the end. The whole program:
   ```python
   import socket

   s = socket.create_connection(("localhost", 30019))
   f = s.makefile("rw")
   print(f.readline())

   for number in range(20):
       question = f.readline()
       words = question.split()
       answer = int(words[2]) + int(words[4].rstrip("?"))
       f.write(f"{answer}\n")
       f.flush()
       print(number + 1, question.strip(), answer, f.readline().strip())

   print(f.readline())
   ```
   Run it. **They should see:** twenty lines ending in `CORRECT`, flashing
   past in a blink, and then `THE VAULT OPENS. The password for miner20
   is: ...`. Save it!

   **Say:** "Twenty sums in a fraction of a second. You just wrote a
   network client that speaks a protocol. That's what browsers, games and
   chat apps do all day."

7. **The bottom of the Mineshaft.** Log in as miner20:
   ```
   cat trophy.txt
   ```
   **They should see:** an ASCII trophy, and a list of the commands
   they used on the way down. Celebrate properly! Read the list out loud,
   and add the trophy to the lab notebook (copy it into a file in the
   notebook repo and commit it).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ConnectionRefusedError: [Errno 111] Connection refused` | Wrong port, or the program ran on the family computer instead of in the Mineshaft | It's port `30019`, and the program must run *inside* the Mineshaft (as miner19). |
| `BOOM` after the first question | The answer didn't arrive in time, or wasn't a whole line | Check for `\n` in the `write`, and `f.flush()` straight after it. |
| `ValueError: invalid literal for int() with base 10: '9932?'` | The `?` is still attached | Use `words[4].rstrip("?")`. |
| `IndexError: list index out of range` | `words` isn't a question: maybe the guard said `BOOM`, or a `readline` is missing | Print `question` to see what the guard really said. Each question needs one `readline` for the question and one for `CORRECT`. |
| nano says `[ Error writing vault.py: Permission denied ]` | Trying to save in the read-only home folder | Exit nano without saving, `cd "$(mktemp -d)"`, then make the file there. |
| The program hangs, printing nothing | It's waiting for a line that never comes, often because it read one line too many | Press Ctrl+C. Count the `readline`s against the notes: hello, then question and reply, twenty times, then the prize. |

## Talk about it

- What's a protocol? What would happen if the program sent `14753` with
  no newline?
- What does `flush` do, and why does it matter here?
- What other boring jobs could a program like this do for you?
- What was your favourite level in the whole Mineshaft?

## Challenge *(if there's time, or for next time)*

- Make the program cope with *any* sum, even if the guard used `-` or
  `*`. *(Look at `words[3]`, and use `if`.)*
- Time it: `import time`, then `start = time.time()` at the beginning
  and `print(time.time() - start)` at the end. How fast was it?
- Keep it for later: Stage 11 builds proper network programs. The
  scratch folder doesn't last, so type the program into
  `~/lab/python/vault.py` on the family computer (it will only run inside
  the Mineshaft, but it's worth keeping) and commit it to a repository.

## Checkpoint

The learner can, without help:
- [ ] Read a protocol description and say what the client must send
- [ ] Write a Python client that connects, reads lines and sends answers
- [ ] Explain `split`, `rstrip`, `write` and `flush` in their program
- [ ] Reach the bottom of the Mineshaft

## Lab notebook

Add levels 19 and 20 to the level log. Copy the final program into the
notebook (it's a great thing to look back on), and commit. Add
*protocol*, *socket* and *automate* to `dictionary.md`.

## Guide's background *(optional reading)*

The guard is a small Python server (`services.py` in `labs/mineshaft`)
that sends 20 random sums and allows one second each. The learner's
program is a **client**: it opens a TCP connection, reads the server's
lines, and replies. Network protocols are mostly agreements about
exactly this kind of thing: who speaks first, how each message is
formatted, and how a message ends (here, a newline).

The most common bug is buffering: Python collects written text and sends
it in batches, so without `flush()` the answer may never leave before
the guard's one-second timer runs out. The second most common is reading
one line too few or too many, which puts the program out of step with
the guard. Printing exactly what was received is the best debugging
tool.

Finishing the Mineshaft is a real achievement: it covers most of the
everyday Linux command line, plus processes, networking and git. Bandit,
the online wargame it's modelled on, is optional in Stage 11 for a
learner who wants more.
