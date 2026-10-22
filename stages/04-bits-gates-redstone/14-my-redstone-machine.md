# Lesson 4.14: Project: My Redstone Machine (Stage 4 Checkpoint)

**Time:** 4–5 sessions of 45 min, plus the checkpoint on a separate day ·
**You need:** squared paper; Digital; Luanti and the **redstone-lab**
world; Thonny; an audience for demo day · **New words:** specification,
design, demo

## Goal *(read this to the learner)*

> You can count in binary, read hex, turn letters into numbers, and build
> gates, adders and memory. Now you'll design a machine of your own, the
> way real engineers do: first on paper, then tested in the simulator,
> then built big in Luanti for everyone to see. Finish it, pass the
> checkpoint, and you become a **Redstone Engineer**.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Agree a **demo day** with the learner, about two weeks away, and
      invite an audience.

## The rules for the project

The machine must:
1. Have at least **three inputs** (switches, buttons or pressure plates)
   and at least **one output** (lamps or a door).
2. Use at least **three gates**, including at least one AND and one NOT
   (made from torches or gate blocks).
3. Start as a **specification**: one sentence saying what it does, and a
   **truth table** with every input combination.
4. Be built and **tested in Digital first**, with a test case that checks
   every row of the truth table.
5. Then be built in **Luanti**, with signs labelling the inputs and
   outputs.

## Ideas

- **The secret vault.** Four switches; the door opens for only one
  combination, like on, off, on, on. Bonus: an alarm lamp for any other
  combination with the "try" lever pulled.
- **The voting machine.** Three people vote yes or no; the lamp shows the
  winner. *(It's on when at least two vote yes: (A AND B) OR (A AND C) OR
  (B AND C).)*
- **The 2-bit adder.** Add two 2-bit numbers and show the answer on three
  lamps. A half adder for the ones column, a full adder for the twos.
- **The trapdoor quiz.** A question on a sign, three answer switches, and a
  door that opens only for the right answer, and only if the other two are
  off.
- **The mob farm controller.** Lights come on when it's night AND the farm
  is switched on AND NOT the "I'm inside" pressure plate.
- **Their own idea.** Anything with three inputs and the rules above.

## Activity

### Session 1: design

1. **Pick and specify.** Choose an idea. Write the one-sentence
   specification at the top of a page. For example: "The door opens only
   when the switches are on, off, on, on."

2. **Truth table.** List every combination of inputs. With 3 inputs there
   are 8 rows; with 4, 16 (Lesson 4.2: each input doubles it!). Fill in
   the output for each.

3. **Gates.** Find a gate circuit that gives that table. Strategies:
   - Look for rows where the output is 1, and write an AND for each
     ("A AND NOT B AND C"), then OR them together.
   - Look for patterns you know: XOR, majority, an adder.
   - Draw it with gate symbols.

### Session 2: test in Digital

4. **Build and test.** Build the gate circuit in Digital, with labelled
   inputs and outputs, and a test case with *every* row of the truth table.
   Run the tests until they pass. **Say:** "Engineers test the design
   before they build the real thing, because changing a drawing is cheap
   and changing a building is expensive."

5. **Simplify (optional).** **Analysis → Analysis** shows the circuit's
   truth table, and below it a short formula. Can they make the circuit
   smaller and keep the tests passing?

### Sessions 3 and 4: build in Luanti

6. **Plan the layout.** On squared paper, from above, like the plans in
   this stage's lessons. Leave space between wires so they don't touch by
   accident. Remember: gate outputs point to your right when you place
   them.

7. **Build it.** Build one part at a time, and test each part before
   adding the next, just as in programming. Label everything with signs.

8. **Test against the table.** Go through every row of the truth table in
   the game, ticking each one off on paper.

### Session 5: demo day

9. **Present it.** The learner explains to the audience:
   - the specification,
   - the truth table,
   - the Digital circuit and its passing tests,
   - a walk through the Luanti build, while the audience tries the
     switches,
   - one problem they had, and how they fixed it.

## The Stage 4 checkpoint

On a separate day, without help (they may use their lab notebook,
Python's Shell, and `help()`):

1. **Numbers.** On paper: write 45 in binary *(101101)*; turn `10110`
   into an ordinary number *(22)*; turn `FF` and `2A` into ordinary
   numbers *(255, 42)*; turn `1010 0111` into hex *(A7)*. Check each with
   Python.
2. **A message.** Decode `01001111 01001011` using an ASCII table *(OK)*.
3. **Counting bits.** Write a Python function `count_ones(n)` that returns
   how many 1s there are in `n` written in binary, using `%` and `//` (no
   `bin`!). Test it with at least three `assert`s, for example
   `count_ones(7) == 3` and `count_ones(8) == 1`.
4. **Truth tables.** From memory, write the truth tables for NOT, AND, OR,
   XOR and NAND.
5. **NAND.** In Digital, build OR using only NAND gates, with a test case
   that passes.
6. **Adding.** On paper, add `0110 + 0111` with carries. Then, in Digital,
   build a half adder with a test case that passes, and explain which gate
   makes the sum and which makes the carry.
7. **Redstone.** In Luanti, build a NOT from a torch, and an AND gate
   block that opens a door with two switches.
8. **Memory and machines.** Explain, with a drawing: how a latch remembers
   a bit, and how the seal-in rung keeps a motor running.

All done means **Redstone Engineer!** Sign and stamp the passport.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The truth table is huge | 4 or more inputs make 16+ rows | That's normal; it's long but simple. Write the inputs by counting in binary: 0000, 0001, 0010... |
| The Digital tests pass, but the Luanti build doesn't work | A building mistake, not a design mistake | Test each gate on its own in Luanti, with a lamp on its output. |
| Wires join where they shouldn't | Mesecons wires connect to every neighbour | Leave an empty block between wires that must stay apart. |
| A gate block points the wrong way | It was placed from a different side | Dig it and place it again, so the picture points towards the output. |
| The project keeps growing | Too many ideas | Build the specification first. Extra features go on a "version 2" list. |

## Talk about it

- Why test in Digital before building in Luanti?
- What was the hardest part: the design, the test, or the build?
- How is building a circuit like writing a program?

## Checkpoint

The learner can, without help:
- [ ] Turn a specification into a truth table, and a truth table into gates
- [ ] Test a design in Digital before building it
- [ ] Build and debug a multi-gate machine in Luanti
- [ ] Pass the Stage 4 checkpoint above

## Lab notebook

Glue in the specification, truth table, gate drawing and Luanti plan.
Write: "The thing I'm proudest of is..." and "If I built it again I
would...". Add *specification*, *design* and *demo* to the dictionary.

## Guide's background *(optional reading)*

The project follows the real hardware design flow: **specify** (what
should it do?), **design** (truth table, then gates), **verify** (the
simulator tests), then **build**. Chip designers spend more time
verifying than building, because a mistake in a chip that's already
made can't be fixed.

The "one AND per row where the output is 1, then OR them together" method
always works. It's called **sum of products**, and it's what Digital's
Analysis window uses as its starting point before simplifying.

After this stage, the course goes *sideways* into tools for a while
(Stage 5: Git, the shell, more of the Mineshaft) before Stage 6, where
the learner takes the NAND gate and the adder from this stage and
builds an entire computer in the Nand to Tetris course.
