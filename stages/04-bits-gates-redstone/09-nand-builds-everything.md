# Lesson 4.9: NAND Builds Everything

**Time:** 2 sessions of 45 min · **You need:** the Digital simulator
(see below); the lab notebook · **New words:** simulator, NAND,
universal gate, test case

## Goal *(read this to the learner)*

> Building gates in Luanti is fun, but big circuits get huge. Real chip
> designers use a **simulator**: a program for drawing circuits that
> really work. Today you'll learn one called **Digital**, and discover
> something amazing: one gate, called **NAND**, can be used to build
> *every other gate*. In Stage 6, you'll build a whole computer starting
> from nothing but NAND.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once.
- [ ] Check Digital is in the offline library:
      `ls /srv/redstone-library/tools/Digital/Digital.jar`
      If it isn't, run `./scripts/mirror-library.sh` from your account
      while online (see [SETUP.md](../../docs/SETUP.md)).
- [ ] As the learner, in a terminal, give Digital a short name and make a
      folder for circuits:
      ```
      echo "alias digital='java -jar /srv/redstone-library/tools/Digital/Digital.jar'" >> ~/.bashrc
      source ~/.bashrc
      mkdir -p ~/lab/circuits
      ```
      (The learner met `alias` in Bashcrawl. `>>` adds a line to the end
      of `.bashrc`, the file that sets up every new terminal.)
- [ ] Start it once with `digital &`, and try steps 1 to 3 yourself.

**How Digital works (for the guide):**

| To do this | Do this |
|---|---|
| Add a part | **Components** menu → a group → the part. It follows the mouse: click to put it down. **L** puts down another of the last part. |
| Draw a wire | Click on a part's pin (the little dot), move the mouse, and click on another pin. Click in empty space to make a corner. **Esc** cancels. |
| Send one signal to two places | Draw two wires from the same pin. |
| Name an input or output | **Right-click** it, type in **Label**, click **OK**. |
| Move or delete something | Click it to select, then drag it, or press **Delete**. |
| Run the circuit | The **▶** button in the toolbar (or **Space**). Click inputs to switch them between 0 and 1. **■** stops it. |
| See the truth table | **Analysis → Analysis** (or **F9**). Every input and output needs a label. |
| Run the tests | The **✓** button at the right of the toolbar (or **F8**). |

The circuit has to be stopped (■) to change it.

## Warm-up (5 min)

"In the people gates game, what did the AND person and the NOT person do
together?" *(Their output was 0 only when both inputs were 1.)* "That's
NAND: NOT AND."

## Activity

### Session 1: meet Digital

1. **Start Digital.** In a terminal: `digital &`. **They should see:** an
   empty grid with menus along the top. **Say:** "The `&` lets you keep
   using the terminal while Digital runs."

2. **Your first circuit: AND.**
   - **Components → IO → Input**, and click on the left of the grid. Press
     **L** and click again below it, for a second input.
   - **Components → Logic → And**, and place it to the right of the inputs.
   - **Components → IO → Output**, and place it on the right.
   - Draw wires: from each input's dot to one of the AND gate's inputs,
     and from the AND gate's output to the Output.
   - Right-click each input and label them **A** and **B**. Label the
     output **Y**.

   Press **▶**. **They should see:** the wires turn dark green (0). Click
   the inputs: each one turns bright green when it's 1. The output is
   bright only when both are. Press **■**.

   **Say:** "Bright green is 1, dark green is 0. It's the same AND as in
   Luanti, but you can build it in seconds and it fits on the screen."

3. **Ask Digital for the truth table.** **Analysis → Analysis**. **They
   should see:** a table with A, B and Y, exactly the AND table. Close it.
   Save with **File → Save As**, in `lab/circuits`, as `and.dig`.

4. **Test cases.** **Say:** "Remember `assert` in Python? Digital has tests
   too." **Components → Misc. → Test case**, and put it anywhere. Right-
   click it, click **Edit** next to **Test data**, and type:

   ```
   A B Y
   0 0 0
   0 1 0
   1 0 0
   1 1 1
   ```

   The first line names the inputs and outputs; each line after it is
   one test. Click **OK**, then **OK**. Click **✓** in the toolbar. **They
   should see:** a window with a green tick and **passed**, and every row
   green.

   Now break it: change the last line to `1 1 0` and run the tests again.
   **They should see:** **failed**, with the wrong row in red, showing what
   was expected and what was found. Put it back.

### Session 2: NAND makes everything

5. **Meet NAND.** New circuit (**File → New**). Build a **NAnd** gate
   (Components → Logic) with inputs A and B and output Y. Find its truth
   table with **Analysis → Analysis**, and copy it into the notebook:

   | A | B | Y |
   |---|---|---|
   | 0 | 0 | 1 |
   | 0 | 1 | 1 |
   | 1 | 0 | 1 |
   | 1 | 1 | 0 |

   **Say:** "NAND is the opposite of AND. It's 0 only when both are 1. Now,
   the challenge: using **only** NAND gates, build NOT, AND and OR."

6. **NOT from NAND.** Hint: "What does NAND do if both its inputs are the
   same?" Let them experiment. *(Wire input A to **both** inputs of one
   NAND: 0 NAND 0 = 1, and 1 NAND 1 = 0. That's NOT!)*

   Label the input **A** and the output **Y**. Add a test case:

   ```
   A Y
   0 1
   1 0
   ```

   Run the tests until they pass. Save as `not_from_nand.dig`.

7. **AND from NAND.** Hint: "NAND is NOT-AND. What would undo the NOT?"
   *(A NAND, then a NOT made from a second NAND: two NANDs.)* Test it with
   the AND test from step 4. Save as `and_from_nand.dig`.

8. **OR from NAND.** This one's harder. Hint: "Remember the torch AND?
   De Morgan's law works the other way round too: OR is NAND of the two
   inputs NOTted." *(Three NANDs: NOT A, NOT B, then NAND them together.)*
   Test:

   ```
   A B Y
   0 0 0
   0 1 1
   1 0 1
   1 1 1
   ```

   Save as `or_from_nand.dig`.

   **Say:** "A gate that can build every other gate is called a
   **universal gate**. NAND is one. That's why real chips are full of
   NANDs, and why the course you'll do in Stage 6, *Nand to Tetris*,
   starts with a single NAND gate and ends with a computer that plays
   Tetris."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `digital: command not found` | The alias isn't loaded in this terminal | Run `source ~/.bashrc`, or open a new terminal. |
| `Error: Unable to access jarfile` | Digital isn't in the library | The guide runs `./scripts/mirror-library.sh` while online. |
| A wire doesn't connect | Wires only connect at their **ends**, exactly on a pin | Delete the wire and draw it again, starting and ending on the dots. |
| `Nothing connected to input 'In_2' at component 'And'. Open inputs are not allowed.` | One of a gate's inputs has no wire | Every input pin needs a wire. Look for an unconnected dot. |
| `More than one output is active on a wire, causing a short circuit.` | Two outputs are wired to each other, for example input A wired straight to input B | Each wire may have only one output (one red dot) feeding it. |
| Can't move or change anything | The simulation is still running | Press **■** first. |
| `Test signal B not found in the circuit!` | An input or output has no label, or a different label from the test | Right-click and label it exactly as in the test's first line (capitals matter). |
| The test fails | The circuit doesn't do what the table says | Read the red row: **E** is what was expected, **F** is what was found. Fix the circuit, not the test! |

## Talk about it

- Why is a simulator useful, when we could build circuits in Luanti?
- What does it mean that NAND is "universal"?
- How are Digital's test cases like Python's `assert`?

## Challenge *(if there's time, or for next time)*

- Build NOR from NANDs (it's OR, then NOT: four NANDs).
- Build **XOR** from four NANDs. It's a famous puzzle! (Hint: the first
  NAND takes A and B; the next two each take one input and the first
  NAND's output.) Test it with the XOR table from Lesson 4.6.
- **NOR** is universal too. Can you make NOT from a NOR?
- **(Online, optional, no account):** *nandgame.com* is a puzzle game
  that starts with NAND and builds up to a computer, level by level. It
  saves progress in the browser.

## Checkpoint

The learner can, without help:
- [ ] Build a circuit in Digital with inputs, gates and an output, and run it
- [ ] Label inputs and outputs, and get the truth table from Analysis
- [ ] Write a test case and use it to check a circuit
- [ ] Build NOT, AND and OR using only NAND gates

## Lab notebook

Draw each NAND-only circuit. Copy the NAND truth table. Add *simulator*,
*NAND*, *universal gate* and *test case* to the dictionary.

## Guide's background *(optional reading)*

**Digital**, by Helmut Neemann, is an open-source logic simulator made
for teaching. It runs on Java (installed by setup) and lives in the
offline library. Its built-in test cases are the circuit-building version
of the learner's Python `assert`s: write down what should happen, then
check the circuit does it. The course's own checks ran every test table in
this stage through Digital's test runner.

NAND (and NOR) are **functionally complete**: any logic function at all
can be built from enough of them. In real chips, NAND is also one of the
cheapest gates to make from transistors, which is why it's so common.
*The Elements of Computing Systems* (the Nand to Tetris book) uses that
idea as its starting point: you're given NAND, and you build everything
else, all the way up to an operating system.

The XOR-from-four-NANDs challenge: N1 = A NAND B; N2 = A NAND N1;
N3 = B NAND N1; Y = N2 NAND N3.
