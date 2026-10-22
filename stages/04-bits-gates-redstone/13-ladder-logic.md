# Lesson 4.13: Ladder Logic, How Factories Think

**Time:** 2 sessions of 45 min · **You need:** paper; Digital; Thonny;
if the guide works with machines, photos or stories from work ·
**New words:** PLC, ladder diagram, rung, contact, coil, seal-in, scan

## Goal *(read this to the learner)*

> Factories are full of machines that start, stop, sort, stamp, fill and
> pack, all on their own. They're controlled by tough little computers
> called **PLCs**, and engineers program them with pictures that look
> like ladders. Today you'll learn to read ladder diagrams, discover
> they're the same AND, OR, NOT and latch you already know, and program
> your own pretend cookie factory.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] If you work with PLCs or relay panels, pick one simple, real
      example to show or describe: a conveyor, a pump, a door. If you
      don't, the cookie factory in this lesson is all you need.

## Warm-up (5 min)

"Think of a machine that switches itself on and off. What does it need to
know, and what does it control?" *(A washing machine knows if the door is
shut and the water level; it controls the motor, the pump, the heater.)*
**Say:** "Those are **inputs** and **outputs**, like the circuits we've
built."

## Activity

### Session 1: reading ladders

1. **What's a PLC?** **Say:** "PLC stands for **programmable logic
   controller**. It's a computer built to survive dust, heat and shaking.
   Wires from buttons and sensors come into its inputs; wires to motors,
   lights and valves go out of its outputs. Inside, it runs a program that
   decides which outputs to turn on."

2. **The ladder.** Draw this on paper:

   ```
   |                                   |
   |    door_shut    button            |
   |------[ ]----------[ ]--------( )---|
   |                              motor |
   |                                   |
   ```

   **Say:** "The two side lines are the **rails**, like the sides of a
   ladder. Power comes from the left rail. Each line across is a **rung**.
   A `[ ]` is a **contact**: it lets power through when its input is on,
   like a switch. The `( )` at the end is a **coil**: the output. If power
   gets all the way along the rung, the coil turns on."

   Ask: "When does the motor run?" *(When the door is shut AND the button
   is pressed.)* **Say:** "Contacts one after another, in a line, are
   **AND**."

3. **OR and NOT in a ladder.** Draw:

   ```
   |    front_button                   |
   |------[ ]-----+-------------( )-----|
   |              |             bell    |
   |    back_button                    |
   |------[ ]-----+                    |
   |                                   |
   |    daylight                       |
   |------[/]-------------------( )-----|
   |                          porch_light
   ```

   **Say:** "Two contacts side by side, on branches, are **OR**: power can
   go along either one. A contact with a slash, `[/]`, is the opposite: it
   lets power through when its input is **off**. That's **NOT**." So the
   bell rings if the front OR back button is pressed, and the porch light
   is on when it's NOT daylight.

4. **Translate.** On paper, the learner draws ladder rungs for:
   - The vault door from Lesson 4.8 *(two contacts in series)*.
   - The full porch light: motion AND NOT daylight *(`[ ]` then `[/]` in
     series)*.
   - A safety rule: the saw runs when the start button is pressed AND the
     guard is shut AND the emergency stop is NOT pressed.

   **Say:** "In real factories, the vault door idea is called **two-hand
   control**: a big press only moves when the worker has *both* hands on
   two buttons, far apart, so neither hand can be under the press."

### Session 2: the seal-in, and a pretend PLC

5. **The problem with buttons.** **Say:** "A start button springs back
   when you let go. But a conveyor belt should keep running after you
   press start, until someone presses stop. How?" Think back to Lesson
   4.12. *(It needs memory: a latch!)*

6. **The seal-in rung.** Draw the most famous rung in all of factory
   programming:

   ```
   |    start          stop             |
   |------[ ]----+------[/]------( )-----|
   |             |               motor   |
   |    motor    |                       |
   |------[ ]----+                       |
   ```

   **Say:** "There's a contact for the motor *itself*, next to the start
   button. Press start: the motor turns on. Its own contact closes, so
   power has a second way through. Let go of start: the motor keeps
   itself on! It's sealed in. Press stop: the `[/]` opens, the motor goes
   off, its own contact opens, and it stays off." Ask: "What does that
   remind you of?" *(The latch! The motor contact is feedback.)*

   As a formula: **motor = (start OR motor) AND NOT stop**.

7. **Build it in Digital.** Inputs **Start** and **Stop**, an **Or**, a
   **Not**, an **And**, and output **Motor**. Wire the And's output to
   Motor *and* back into the Or's second input: the feedback. Test case:

   ```
   Start Stop Motor
   0 1 0
   0 0 0
   1 0 1
   0 0 1
   0 1 0
   0 0 0
   1 1 0
   ```

   The last row is a question for the learner: "What if someone presses
   start and stop at the same time?" *(Stop wins. Engineers make sure of
   that on purpose, for safety.)* Save as `seal_in.dig`.

8. **The scan.** **Say:** "A PLC doesn't think about everything at once.
   It goes round and round, over and over, very fast: **read** all the
   inputs, **solve** every rung from top to bottom, **write** all the
   outputs. One time round is called a **scan**." Ask: "Have you seen a
   loop like that before?" *(The game loop in Pygame Zero: update, then
   draw, sixty times a second.)*

9. **The Cookie Factory.** A pretend PLC in Python, where every press of
   Enter is one scan. New file, `~/lab/python/binary/cookie_factory.py`:
   ```python
   motor = False
   stamper = False
   cookies = 0
   scan = 0

   print("THE COOKIE FACTORY")
   print("Type start, stop or cookie (a cookie reaches the sensor),")
   print("or just press Enter for a scan with no buttons. quit to finish.")

   while True:
       # 1. Read the inputs
       pressed = input(f"scan {scan} > ").strip().lower()
       if pressed == "quit":
           break
       start = pressed == "start"
       stop = pressed == "stop"
       sensor = pressed == "cookie"

       # 2. Solve the rungs, top to bottom
       motor = (start or motor) and not stop
       stamper = motor and sensor
       if stamper:
           cookies = cookies + 1

       # 3. Write the outputs
       belt = "RUNNING" if motor else "stopped"
       stamp = "STAMP!" if stamper else "-"
       print(f"   belt {belt}   stamper {stamp}   cookies {cookies}")
       scan = scan + 1
   ```
   Play it: `cookie` (nothing: the belt isn't running), `start`, Enter,
   `cookie`, `cookie`, `stop`, `cookie`. **They should see:** the belt keep
   running after `start` with no buttons pressed, two stamps, and no stamp
   after `stop`.

   **Say:** "`start = pressed == "start"` puts True or False in the box:
   is the thing they typed equal to "start"? The rungs are just your
   formulas, using Python's `and`, `or` and `not`."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Digital: the motor goes off as soon as Start is let go | The feedback wire from the And's output to the Or is missing | Wire the And's output to the Or's second input, as well as to Motor. |
| Digital: the motor won't stop | Stop isn't going through the Not into the And | Check the path: Stop → Not → And. |
| Digital: the first test row fails | The test doesn't start with Stop pressed | Keep the first row `0 1 0`, a "reset", like the latch. |
| Python: the belt stops on the next scan after `start` | The rung doesn't include `motor` itself | It's `motor = (start or motor) and not stop`. |
| Python: stamps when the belt is stopped | `stamper = sensor`, without the motor | It's `stamper = motor and sensor`. |

## Talk about it

- In a ladder, which shape is AND, which is OR, and which is NOT?
- Why does the seal-in rung need the motor's own contact?
- Why should Stop always win over Start?
- What's a scan, and what does it have in common with a game loop?

## Challenge *(if there's time, or for next time)*

- Add a **red light** that's on whenever the belt is stopped, and a
  **green light** when it's running (two more rungs).
- Make the factory stop by itself after 10 cookies, because the box is
  full. *(Add `or cookies >= 10` to the stop part: `and not (stop or
  cookies >= 10)`.)*
- Add an **emergency stop** that, once pressed, keeps everything off until
  a `reset` command. *(It's another latch!)*
- Ask the guide: what's the most complicated machine they've seen
  controlled by a PLC?

## Checkpoint

The learner can, without help:
- [ ] Read a ladder rung and say when its coil turns on
- [ ] Draw ladder rungs for AND, OR and NOT
- [ ] Explain the seal-in rung, and build it in Digital with a test
- [ ] Explain the read, solve, write scan, and run the cookie factory

## Lab notebook

Draw the seal-in rung and write its formula. Draw the scan as a circle:
read → solve → write. Add *PLC*, *ladder diagram*, *rung*, *contact*,
*coil*, *seal-in* and *scan* to the dictionary.

## Guide's background *(optional reading)*

Ladder logic was designed in the 1960s so that electricians who knew
relay panels could program the first PLCs: each rung looks like a relay
circuit, with contacts (normally open `[ ]`, normally closed `[/]`) and a
coil `( )`. It's one of the five PLC languages in the IEC 61131-3
standard, and it's still the most common.

If you work in controls, this lesson is your chance to bring your job
home: photos of a panel, a story about a fault you tracked down, or a
real program printout. Your learner has now seen every idea needed to
read a simple rung, and the seal-in is the bridge between Lesson 4.12's
latch and the real world. (In the field the stop button is usually
wired normally-closed, so that a broken wire stops the machine; inside
the program it then appears as a normally open contact. That's a good
"why" to share with an older learner, and a nice example of designing
for safety.)

The scan cycle (read inputs, execute the program, write outputs) is
also how the game loop works, and how the CPU in Stage 6 works:
fetch an instruction, execute it, repeat. The course's controls thread
comes back in Stage 13, with real control loops on a Raspberry Pi Pico.
Open-source tools like **OpenPLC** let a learner program a Raspberry Pi
as a real PLC, if this lesson sparks a big interest.
