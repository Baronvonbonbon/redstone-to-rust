# Lesson 4.12: Circuits That Remember

**Time:** 2 sessions of 40 min · **You need:** Digital; Thonny; the lab
notebook · **New words:** memory, feedback, latch, set, reset, state

## Goal *(read this to the learner)*

> Every circuit so far forgets everything instantly: let go of the switch,
> and the answer is gone. But a computer remembers your game, your score,
> the words you typed. How can gates *remember*? Today you'll discover the
> trick, a loop where a gate's output comes back round to its own input,
> and build a circuit that remembers one bit: the very smallest piece of
> computer memory.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"When you press a doorbell, it rings. When you let go?" *(It stops.)*
"What if you wanted a light that stays on after someone rings, so you know
somebody came while you were out?" Let them suggest ideas.

## Activity

### Session 1: the latch

1. **Gates forget.** **Say:** "Every circuit we've built so far only
   depends on what its inputs are *right now*. The adder doesn't remember
   the last sum. That's useful for adding, but useless for remembering."

2. **The loop idea.** Draw an OR gate whose output wire curls back round
   into one of its own inputs. Ask: "If the other input is switched on for
   a moment, what happens to the output? And what happens when you switch
   it off again?" *(The output becomes 1, goes back into the OR, and keeps
   it at 1 forever. It remembers! But it can never be turned off.)*

   **Say:** "A wire that brings an output back to an input is called
   **feedback**. It's the secret of memory. Now we need a way to turn it
   off again too."

3. **Meet NOR.** In Digital, find **Components → Logic → NOr** and get its
   truth table (**Analysis → Analysis**). *(Only 0, 0 gives 1.)* **Say:**
   "NOR is NOT OR. It's universal too, like NAND."

4. **Build the latch.** New circuit. Two **NOr** gates, one above the
   other, and two inputs, **S** (for **set**) and **R** (for **reset**),
   and one output **Q**. Wire it like this:

   ```
   R ───────────►┌─────┐
                 │ NOR ├────┬───────► Q
            ┌───►└─────┘    │
            │               │
            │    ┌──────────┘
            │    │
            │    └─────►┌─────┐
            │           │ NOR ├────┐
   S ───────┼──────────►└─────┘    │
            │                      │
            └──────────────────────┘
   ```

   (Where two lines cross without a corner, they aren't joined.)

   - The top NOR's inputs: **R**, and the bottom NOR's output.
   - The bottom NOR's inputs: **S**, and the top NOR's output.
   - The top NOR's output is **Q**.

   The two crossing wires are the feedback: each gate's output goes into
   the other gate. (Digital lets you draw wires anywhere; use corners to
   make it tidy.)

5. **Try it.** Press **▶**. First, click **R** on and off. **Say:** "Q is
   now 0." Then:
   - Click **S** on. **They should see:** Q turns on.
   - Click **S** off again. **They should see:** Q **stays on**!
   - Click **R** on, then off. **They should see:** Q turns off, and stays
     off.

   **Say:** "It remembers! Set makes it 1, Reset makes it 0, and when both
   are off it keeps whatever it was. This circuit is called a **latch**,
   and it stores exactly one bit. What's stored inside is called its
   **state**."

6. **Test it.** Add a test case. This time the rows run **in order**, one
   after another, like a story, because the circuit remembers what
   happened in the row before:

   ```
   S R Q
   0 1 0
   0 0 0
   1 0 1
   0 0 1
   0 0 1
   0 1 0
   0 0 0
   ```

   Read it out like a story: "Reset: it's 0. Let go: still 0. Set: 1. Let
   go: still 1..." Run the tests until they pass. Save as `latch.dig`.

7. **The mystery start.** Stop the simulation (**■**), then start it again
   (**▶**) without touching anything. What's Q? Do it a few times. **They
   might see:** sometimes 0, sometimes 1!

   **Say:** "When the latch first gets power, both gates try to win at once,
   and nobody knows which will. Real computers have the same problem. That's
   why they do a **reset** when they're switched on: to put every bit of
   memory into a known state first. It's also why the test starts with
   reset."

### Session 2: memory everywhere

8. **The doorbell memory light.** Replace the **S** input with a **Button**
   (Components → IO → Button) labelled S, and add an **LED** (Components →
   IO → LED) on Q. Run it. Press the button: the LED comes on and stays on,
   until you reset it. **Say:** "That's the 'someone rang while you were
   out' light."

9. **A Python latch.** **Say:** "In Python, memory is easy: it's a
   variable. Let's write the latch as a program that remembers between
   loops." New file, `~/lab/python/binary/latch.py`:
   ```python
   from gates import NOT, OR

   def NOR(a, b):
       return NOT(OR(a, b))

   q = 0
   q_bar = 1
   while True:
       command = input("s to set, r to reset, n for nothing, q to quit: ")
       if command == "q":
           break
       s = 1 if command == "s" else 0
       r = 1 if command == "r" else 0
       for settle in range(3):
           q = NOR(r, q_bar)
           q_bar = NOR(s, q)
       print("Q is", q)
   ```
   **They should see:** the tables from `gates.py` printed first (because
   importing runs the file), then the menu. Type `s`, `n`, `n`, `r`, `n`.
   *(Q is 1, 1, 1, 0, 0.)*

   **Say:** "Each time round, the two NORs are worked out a few times,
   until they settle down, like the real gates do. `1 if ... else 0` is a
   short way to write an `if` that picks one of two values."

10. **How much memory?** **Say:** "One latch stores one bit. A byte needs 8.
    This computer has gigabytes of memory." In the terminal: `free -h`.
    **They should see:** a `Mem:` line with a total, like `15Gi`. **Say:**
    "That's about 15 × 1024 × 1024 × 1024 bytes, times 8 bits each: more
    than a hundred billion bits. Modern memory chips store bits in a
    slightly different way, but the idea is the same: billions of tiny
    things that each remember a 1 or a 0."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Q follows S, and forgets straight away | The feedback wires are missing, so the gates don't feed each other | Each NOR needs the *other* NOR's output as one input. |
| Q never changes | S and R are wired to the same gate, or the output is taken from the wrong NOR | Top NOR: R and feedback, output Q. Bottom NOR: S and feedback. |
| The first test row fails | The rows are in the wrong order, or the first row isn't a reset | Start the test with `0 1 0`, a reset. |
| The test fails on the "remember" rows | Q is wired to the bottom NOR instead of the top | Q must come from the top NOR (the one with R). |
| Q is different each time the simulation starts | That's real, not a bug! | Reset it first, every time. |
| Python: the tables from `gates.py` print first | Importing runs the whole file | That's expected (Lesson 4.3 explains why). |

## Talk about it

- What is feedback, and why does it make memory possible?
- Why does the test case have to be read in order, from top to bottom?
- Why do computers reset when they're switched on?

## Challenge *(if there's time, or for next time)*

- What happens if S and R are **both** on? Try it, then let go of both at
  once. *(Q and its partner are both 0, and when you let go, it's the
  mystery start again. Designers call this the "not allowed" input.)*
- Build a latch from two **NAnd** gates instead. What's different?
  *(The inputs work upside down: 0 sets and resets, so they're often
  called S̄ and R̄.)*
- Digital has ready-made memory parts in **Components → Flip-Flops**. Find
  the **RS-Flip-flop**: it's a latch with a **clock**, which only listens
  when a "tick" arrives. Stage 6 builds a computer's memory from those.
- Build the latch in Luanti, with two **Logic Gate: nor** blocks (`N`).
  Place both gates standing at the bottom of the plan, facing up, so
  their outputs point right. `S` and `R` are switches, `=` is wire, `L` is
  a lightstone, and `.` is empty:

  ```
  ======.
  =....=.
  =..R.=.
  =..N==L
  ==.=...
  .N==...
  .S.....
  ```

  Flick R on and off first, then try set and reset. The long wire round
  the outside is the feedback.

## Checkpoint

The learner can, without help:
- [ ] Explain what feedback is and why gates need it to remember
- [ ] Build an SR latch from two NOR gates, and test it with an ordered
      test case
- [ ] Explain set, reset and state
- [ ] Explain why computers reset when they start

## Lab notebook

Draw the latch, with the feedback wires in a different colour. Write the
latch test as a story. Add *memory*, *feedback*, *latch*, *set*, *reset*
and *state* to the dictionary.

## Guide's background *(optional reading)*

The **SR latch** (set-reset latch) is the simplest memory circuit. Each
NOR gate's output feeds the other's input, so the pair has two stable
states: Q = 1 or Q = 0. Pulsing S or R pushes it into one state, and it
stays there after the input goes away. Every register and flip-flop in a
processor is built on this idea, with extra gates to control *when* it
listens (a clock).

Digital really does simulate the start-up uncertainty: the course's tests
found the latch's starting value differs from run to run, which is why
the test case begins with a reset. Real hardware is the same, and
"power-on reset" circuits exist for exactly this reason.

If you work with PLCs, you've used this all your working life: a
**seal-in** (or "latching") rung, where a motor's own contact keeps it
running after the start button is released, *is* a latch with a
feedback path. Lesson 4.13 is built around that.

Modern RAM (DRAM) stores each bit as charge in a tiny capacitor, which has
to be refreshed many times a second. The latch-style memory (SRAM) is
faster and is used for a processor's caches and registers. Either way,
it's billions of cells each holding one bit.
