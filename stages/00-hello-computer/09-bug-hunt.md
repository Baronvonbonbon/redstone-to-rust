# Lesson 0.9: Bug Hunt

**Time:** 40 min · **You need:** masking tape (or chalk outside), paper cut
into about 20 cards, a marker, a small toy as the "treasure" · **New words:**
bug, debug, program

## Goal *(read this to the learner)*

> Programmers make mistakes ALL the time. Even the best ones. A mistake
> in a program is called a **bug**, and finding and fixing it is called
> **debugging**. Today you'll write programs for a robot using arrow
> cards, and become a bug hunter.

## Before the lesson *(guide, 10 min)*

- [ ] Tape a 5×5 grid on the floor (each square about one big step). Or
      draw it on paper and use a toy as the robot.
- [ ] Make cards: about 8 that say **↑ FORWARD**, 4 that say
      **↰ TURN LEFT** and 4 that say **↱ TURN RIGHT**.
- [ ] Put the treasure in one square, and pick a start square. Decide
      which way "the robot" faces at the start.

## Warm-up (5 min)

Tell the story of the first "bug": in 1947, a computer at Harvard
stopped working, and the engineers found a real moth stuck inside it!
They taped it into their notebook and wrote "First actual case of bug
being found." (Programmers had already been calling problems "bugs", but
the moth made it famous.)

## Activity

1. **Rules.** The robot (you, the guide) stands on START, facing the way
   you chose. It only understands three cards: **FORWARD** (one square),
   **TURN LEFT** and **TURN RIGHT** (turn on the spot, without moving).

2. **Write a program.** The learner lays the cards in a line on the table
   to get the robot to the treasure. **No testing while writing!**

3. **Run it.** Read the cards in order and do *exactly* what each one
   says. If the robot walks off the grid or misses the treasure: "BUG!"

4. **Debug.** Ask: "Which card is the first one that went wrong?" They
   find it and fix it, then run the *whole* program again from the start.

5. **Planted bugs.** Now **you** write a program with one bug planted in
   it: a wrong turn, or one forward too many. They "run" it in their head,
   or walking the grid, and find the bug.

6. **Swap.** They plant a bug for you to find.

7. **Repeat cards** *(if things are going well)*. Add a card: **REPEAT 3
   TIMES: [ ]**. Put a card inside it. "How could you make the program
   shorter using REPEAT?"

## If something goes wrong

| What happens | What to do |
|---|---|
| Mixes up left and right while the robot faces them | Totally normal! Have them stand behind the robot, facing the same way. |
| Fixes the wrong card | "Let's run it again and stop at each card. Where does it first go wrong?" |
| Gets cross about bugs | Celebrate bugs out loud: "Ooh, a bug! Let's catch it!" |

## Talk about it

- What's a bug? What's debugging?
- What's the best way to find a bug? *(Go step by step, and find the
  FIRST step that went wrong.)*
- Is it bad to have bugs? *(No! Everyone has them. Finding them is the skill.)*

## Challenge

Put an obstacle (a pillow "lava block") on the grid. Write the shortest
program that gets around it. Use REPEAT to make it even shorter.

## Checkpoint

The learner can, without help:
- [ ] Write an arrow program that gets the robot to the treasure
- [ ] Find the first wrong step in a buggy program, and fix it

## Lab notebook

Draw the grid, the obstacles and your program. Write: "A **bug** is a
mistake in a program. **Debugging** means finding the first step that
goes wrong."

## Guide's background *(optional reading)*

"Find the first step that goes wrong" is the most useful debugging
advice there is, and it works for every programming language. The
REPEAT card is a **loop**, one of the most important ideas in
programming. Your learner will write loops in Python in Stage 2, with a
turtle that moves exactly like this robot (forward, left, right).
