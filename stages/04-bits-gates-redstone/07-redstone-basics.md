# Lesson 4.7: Redstone Basics

**Time:** 2 sessions of 45 min · **You need:** Luanti (called
**Minetest** on Pop!_OS 24.04 and older) with the Mesecons mod, both
installed by setup; the learner's world, made below; the lab notebook ·
**New words:** circuit, signal, power source, inverter

## Goal *(read this to the learner)*

> If you've built redstone in Minecraft, you're going to feel right at
> home. Luanti is a free, open-source game a lot like Minecraft, and
> **Mesecons** is its redstone. Today you'll get your own flat creative
> world, then build real circuits: a switch that turns on a lamp, a NOT
> gate made from a torch, and an OR gate made from wires. They're the same
> gates you drew on paper, but now you can walk around inside them.

## Before the lesson *(guide, 20 min)*

- [ ] Read this whole lesson once.
- [ ] From **your own** account, in the course folder, make the world:
      ```
      ./scripts/give-lab.sh LEARNER redstone
      ```
      (Use the learner's account name.) It makes a world called
      **redstone-lab**: flat, with no trees, in creative mode (every block
      is free, and nothing can hurt you), with Mesecons switched on.
- [ ] As the learner, start the game once to check it: open the
      applications menu and choose **Minetest** (or **Luanti**), or type
      `minetest &` in a terminal. If a box says "A new Minetest version is
      available", click **Never**. Along the bottom of the menu there are
      small game pictures: click the one that looks like a **grass block**
      ("Minetest Game"). On the **Start Game** tab, click **redstone-lab**,
      check **Creative Mode** is ticked and **Enable Damage** isn't, and
      click **Play Game**. The first start takes a little while.
- [ ] Practise the controls below for five minutes. Then press **Esc** and
      click **Exit to Menu**.

**The controls:**

| Key | What it does |
|---|---|
| **W A S D** | Walk forward, left, back, right |
| Move the mouse | Look around |
| **Space** | Jump (or go up, when flying) |
| **Shift** | Sneak (or go down, when flying) |
| **K** | Flying on and off |
| **Left-click** (hold) | Dig a block |
| **Right-click** | Place the block you're holding, or use a thing (flick a switch, open a door) |
| **1** to **8**, or the mouse wheel | Choose what you're holding, from the bar at the bottom (the **hotbar**) |
| **I** | Inventory |
| **T** | Chat, for typing commands like `/time 12:00` |
| **Esc** | Pause menu (and **Exit to Menu** to stop) |

**Getting blocks, in creative mode:** press **I**. Click in the green
search box, type part of the name (like `switch`), and press **Enter**.
Click the item to pick it up, then click an empty square in the **row
just below the search box**: that row is the hotbar. Press **I** or
**Esc** to close the inventory. Hovering over an item shows its name.

## Warm-up (5 min)

"What does a NOT gate do?" *(Flips its input.)* "OR?" *(1 if at least
one input is 1.)* If the learner knows Minecraft redstone: "What's a
redstone torch for?" Let them explain; they may already know more than
you!

## Activity

### Session 1: power and wires

1. **Get the parts.** In the inventory, find and put in the hotbar:
   - **Mesecon** (the wire: search `mesecon` and hover to find the one
     called just "Mesecon"),
   - **Switch**,
   - **Red Lightstone** (the lamp: search `lightstone`),
   - **Mesecon Torch**,
   - **Stone** (search `stone`, and pick plain grey Stone).

2. **The simplest circuit.** On the ground, in a straight line: a
   **Switch**, then three **Mesecon** wires on the ground, then a **Red
   Lightstone** touching the last wire.

   ```
   seen from above:   S===L
   ```

   (In these plans, each character is one block: `S` is a switch, `=` is
   a wire, and `L` is a lightstone.)

   Right-click the switch. **They should see:** the wire brighten and
   the lightstone glow. Right-click again to turn it off.

   **Say:** "That's a **circuit**: a **power source** (the switch), a path
   for the **signal** (the wire), and something that uses it (the lamp).
   On is 1. Off is 0. It's the same as a wire inside a computer chip,
   just much, much bigger."

3. **Wire rules.** Experiment, and write down what they find:
   - Put a wire next to the line, sideways. Does it join? *(Yes: wires
     join to every neighbour.)*
   - Make a branch with two lamps. *(Both light.)*
   - Run a wire up a step: a block, with wire on top, next to the wire on
     the ground. *(Wires go up and down one block.)*
   - Make a really long wire: 30 blocks. *(It still works. In Minecraft,
     redstone fades after 15 blocks. Mesecons doesn't.)*

4. **Light it up at night.** Press **T**, type `/time 21:00` and press
   **Enter**. The lightstones look great in the dark. `/time 12:00`
   brings the day back.

### Session 2: torches and gates

5. **The torch is a NOT gate.** Build this, from the side:

   ```
   seen from above:   S=#t==L
   ```

   (`#` is a Stone block, and `t` is the torch stuck on its far side.)

   A switch, one wire, a **Stone** block, then a **Mesecon Torch**
   on the *far side* of the stone (aim at the side face of the stone and
   right-click), then two wires and a lightstone.

   **They should see:** with the switch **off**, the torch is lit and the
   lamp is **on**. Flick the switch **on**: after a moment, the torch goes
   out and the lamp goes **off**.

   **Say:** "The wire powers the stone block, and a torch on a powered
   block goes out. So the torch always does the opposite of its input.
   That's a NOT gate! In electronics it's called an **inverter**." Fill in
   the truth table in the notebook.

6. **OR is just joining wires.** Build two switches, each with a wire,
   joining into one wire that goes to a lamp:

   ```
   seen from above:   S==
                      ..==L
                      S==
   ```

   (`.` is an empty block.)

   Try all four combinations of the two switches, and fill in the truth
   table. **They should see:** the lamp is on if **either** switch is on.
   **Say:** "Two wires joining together is an OR gate. You don't even need
   a special block!"

7. **The porch light, for real.** From Lesson 4.6: the porch light comes on
   when someone walks past AND it's NOT daytime. Can they build the NOT
   part? *(The "daytime" switch goes into a torch.)* The AND part comes
   next lesson, so leave a sign or a gap for it.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| No **redstone-lab** world in the list | The world wasn't made, or a different game is selected at the bottom | The guide runs `./scripts/give-lab.sh LEARNER redstone`. Click the grass-block game picture at the bottom of the menu. |
| The search finds nothing | The text is spelt differently, or Enter wasn't pressed | Try a shorter word, like `light` or `switch`, and press Enter. |
| Searching `mesecon` shows lots of things | Many Mesecons items have "mesecon" in their names | Hover over each one: the wire is called just **Mesecon**. It looks like a thin yellow line. |
| Hearts at the bottom of the screen, and things hurt | Damage is on | Exit to the menu, untick **Enable Damage**, and play again. |
| Digging takes forever | Creative mode is off | Exit to the menu, tick **Creative Mode**, play again. |
| The lamp doesn't light | A gap between the parts, or the lamp isn't touching the end of the wire | Look along the wire for a gap. Every part must touch the next one. |
| The torch never goes out | The torch is on top of the block or on the wrong side | It goes on the *side* of the block, opposite where the wire comes in. Dig it and place it again. |
| The torch goes out, but only after a second | That's normal | Torches in Mesecons check their input about once a second. |
| Can't fly | Fly mode is off | Press **K**. Space goes up, Shift goes down. |
| Stuck in the dark | It's night | Press T and type `/time 12:00`. |

## Talk about it

- What are the three parts of a circuit?
- Why does a torch on a powered block act like NOT?
- Why is joining two wires the same as OR?

## Challenge *(if there's time, or for next time)*

- Build a NOT of a NOT: switch → stone → torch → wire → stone → torch →
  lamp. What does it do? *(The same as a plain wire, but slower!)*
- Find the **Lever** and **Button**. How are they different from a switch?
  *(The button turns itself off after a moment.)*
- Make a row of 4 lightstones, each with its own switch, and show the
  numbers 0 to 15 in binary. (Lesson 4.10 uses this!)

## Checkpoint

The learner can, without help:
- [ ] Get blocks from the creative inventory into the hotbar
- [ ] Build a switch, wire and lamp circuit
- [ ] Build a NOT gate with a torch, and explain how it works
- [ ] Build an OR gate by joining wires, with its truth table

## Lab notebook

Draw each circuit from above, and write its truth table. Write the wire
rules they discovered. Add *circuit*, *signal*, *power source* and
*inverter* to the dictionary.

## Guide's background *(optional reading)*

Luanti (called Minetest until 2024) is an open-source voxel game engine,
and "Minetest Game" is the basic Minecraft-like game that comes with it.
**Mesecons** is a mod that adds wires, switches, lamps, gates and pistons,
much like Minecraft's redstone. The mod is installed for every account by
setup; `give-lab.sh redstone` makes a world with it switched on. The
world lives in the learner's `~/.minetest/worlds/redstone-lab/`.

Mesecons signals are just on or off; there's no "signal strength" like
Minecraft has, which keeps it closer to real digital logic. A Mesecon
torch reads the block it's attached to and outputs the opposite, which is
exactly how Minecraft players build NOT gates. The checks run with this
course found Mesecons torches update about once a second, so a lamp
behind a torch takes a moment to change.

In real electronics, a NOT gate is a transistor arranged so that a high
input pulls the output low, and an OR is a little more than joining wires
(you need diodes, so the signals can't flow backwards into each other).
In a block game, the simplification is fine and makes the idea easy to
see.
