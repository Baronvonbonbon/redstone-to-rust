# Lesson 4.8: Torch Logic and Gate Blocks

**Time:** 2 sessions of 45 min · **You need:** Luanti and the
**redstone-lab** world from Lesson 4.7; the lab notebook · **New words:**
De Morgan's law, logic gate block, combination

## Goal *(read this to the learner)*

> Last time you made NOT from a torch and OR from wires. But there's no
> AND! Today you'll build an AND gate out of nothing but torches and
> wires, the way Minecraft engineers do, and find out why it works. Then
> you'll get the shortcut, ready-made gate blocks, and use them to build a
> vault door that needs two keys and a stair light that works from both
> ends.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] If you can, build the torch AND (step 2) yourself first, in the
      learner's world, a good distance from where they'll build. It's the
      trickiest build in the stage, and it helps to have seen one working.

## Warm-up (5 min)

"What's NOT 0?" *(1.)* "What's NOT NOT 1?" *(1: two NOTs cancel out.)*
"If I say 'I'm NOT NOT hungry', am I hungry?" *(Yes!)*

## Activity

### Session 1: AND from torches

1. **The puzzle.** **Say:** "We have NOT (a torch) and OR (joining
   wires). Can we make AND out of just those?" Let them think and try on
   paper for a few minutes. Hint: "What if you NOT both inputs first?"

2. **The torch AND.** Build this. Each character is one block: `A` and
   `B` are switches, `=` is a wire on the ground, `#` is a Stone block,
   `t` is a Mesecon Torch on the side of the stone *away* from the wire,
   `L` is a lightstone, and `.` is an empty block:

   ```
   seen from above:

   A=#t=
   ....==#t=L
   B=#t=
   ```

   Build it in this order:
   - The top row: a switch, a wire, a stone, a torch on the far side of
     the stone, and a wire. Leave a gap of one empty block below it.
   - The bottom row, the same, two blocks below the top row.
   - The two end wires of the rows are now one gap apart. Put a wire in
     the gap to join them, then carry on to the right: one more wire, a
     stone, a torch on its far side, a wire, and a lamp.

   Test all four combinations of the switches, and fill in the truth table.
   **They should see:** the lamp lights **only when both switches are
   on**. (Give the torches a second to catch up.)

3. **Why does it work?** Trace it with a finger, writing on the drawing:
   - Each first torch is **NOT** its switch.
   - The two torch wires join: that's **OR**. So the middle wire is "NOT A
     OR NOT B".
   - The last torch is **NOT** of that.

   Fill in a big table together:

   | A | B | NOT A | NOT B | middle wire (OR) | lamp (NOT middle) |
   |---|---|---|---|---|---|
   | 0 | 0 | 1 | 1 | 1 | 0 |
   | 0 | 1 | 1 | 0 | 1 | 0 |
   | 1 | 0 | 0 | 1 | 1 | 0 |
   | 1 | 1 | 0 | 0 | 0 | 1 |

   **Say:** "The last column is exactly AND! 'Both are on' is the same as
   'it's NOT true that either one is off'. That's a famous rule called
   **De Morgan's law**, after the mathematician Augustus De Morgan. Gate
   designers use it all the time to swap one kind of gate for another."

4. **Check it in Python.** Add to `~/lab/python/binary/gates.py` from
   Lesson 4.6, before the `table` lines:
   ```python
   def TORCH_AND(a, b):
       return NOT(OR(NOT(a), NOT(b)))
   ```
   and at the end: `table("TORCH_AND", TORCH_AND)`. **They should see:**
   the same table as AND.

### Session 2: gate blocks

5. **The shortcut.** In the inventory, search `gate`. **They should see:**
   seven blocks with gate pictures on them, called **Logic Gate: and**,
   **or**, **not**, **xor**, **nand**, **nor** and **diode**. Put the
   **and**, **xor** and **not** gates in the hotbar.

6. **Which way round?** A gate block has a picture of the gate on top,
   pointing towards its **output**. **Say:** "When you place a gate, its
   output is on your **right**. The two inputs are the side **nearest
   you** and the **far side**." Place an **and** gate and look at the
   picture to check. Then:
   - a wire and a lamp on its right (the output),
   - a wire and a switch on the side nearest you,
   - a wire and a switch on the far side.

   ```
   seen from above, standing at the bottom of the picture:

   S
   =
   &=L
   =
   S

   you
   ```

   (`&` is the and gate.)

   Test all four combinations. **They should see:** the same truth table as
   the torch AND, but built in seconds, and it reacts instantly.

7. **The vault door.** Find a **Wooden Door** (search `door`) and place it
   on the ground. Replace the lamp on the AND gate with a wire that
   touches the bottom of the door. **They should see:** the door opens only
   when **both** switches are on. **Say:** "A bank vault needs two people
   with two keys, so one person alone can't open it. That's an AND." Build
   a little wall around the vault, and put the switches far apart.

8. **The stair light.** Use an **xor** gate, two switches and a lamp,
   wired the same way. One switch is "the bottom of the stairs", the other
   is "the top". **They should see:** either switch changes the lamp, from
   either end. Check it against the table from Lesson 4.6.

9. **The NOT block.** A **not** gate has one input: the side on your
   **left** when you place it, opposite the output. Finish the porch light
   from Lesson 4.7: "someone walks past" AND NOT "daytime", using a not
   gate and an and gate.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The torch AND lamp is always off | A torch is on top of a stone instead of on its side, or the middle wire doesn't touch both row wires | Check each torch is on the far *side* of its stone. Check the joining wire touches both row-end wires. |
| The torch AND lamp is always on | The last torch isn't on the far side of the last stone, or the wire into it is missing | The last stone needs a wire coming in from the left, and the torch on its right side. |
| Two rows short-circuit (both lamps act as one) | The rows are next to each other, so their wires joined | Leave one empty block between the rows, except where the joining wire goes. |
| A gate block does nothing | It's facing the wrong way | Look at the picture on top: it points to the output. Dig it, stand somewhere else, and place it again. |
| A gate disappears, and drops as an item | It **overheated**: its output was connected straight back to its input, and it flicked on and off very fast | Don't connect a gate's output to its own input. |
| The door doesn't open | The wire isn't touching the door, or the gate isn't getting both inputs | The wire must end right next to the bottom half of the door. |
| The door opens but won't close | The AND output is still on | Turn a switch off. |

## Talk about it

- How did three torches and some wires make an AND?
- Say De Morgan's law in your own words. *(For example: "both are on" is
  the same as "not either is off".)*
- What else could the vault door idea guard? *(A rocket launch: two keys.
  A secret base: a switch AND a pressure plate.)*

## Challenge *(if there's time, or for next time)*

- Build OR using only NOT and AND gate blocks. *(De Morgan backwards:
  NOT(NOT a AND NOT b).)*
- A secret combination lock: four switches, and the door opens only for
  one pattern, like on, off, on, on. *(Put a not gate on each switch that
  should be off, then AND everything together.)*
- Find the **Wooden Pressure Plate** (search `pressure`): it's a switch you
  stand on. Use it to open a door automatically.

## Checkpoint

The learner can, without help:
- [ ] Build an AND gate from torches and wires, and explain why it works
- [ ] Place a gate block the right way round and wire its inputs and output
- [ ] Build the two-key vault door and the stair light
- [ ] Explain De Morgan's law with a truth table

## Lab notebook

Draw the torch AND from above and copy the big truth table. Draw the vault
door circuit. Add *De Morgan's law*, *logic gate block* and *combination*
to the dictionary.

## Guide's background *(optional reading)*

**De Morgan's laws** say: NOT (A AND B) = (NOT A) OR (NOT B), and NOT (A
OR B) = (NOT A) AND (NOT B). They let you build any gate from a few
basic ones, and swap ANDs for ORs by adding NOTs. Minecraft players
discovered the torch AND gate on their own, because redstone torches and
joined wires are the only gates the game gives you.

The gate blocks (from the `mesecons_gates` mod) take inputs on two sides
and output on a third, rotated by the direction the player faces when
placing them. The course's automated checks confirmed this orientation,
and confirmed that a powered wire next to a door opens it. Mesecons also
protects the game from very fast flickering loops by "overheating" a gate
that changes too often, which pops it off as an item.

A real vault, and many real machines, use exactly this "two keys" logic,
often called **two-hand control** in industry: a press only cycles when
both of the operator's hands are on the buttons, so neither hand can be
under the press. Lesson 4.13 looks at how machines like that are
programmed.
