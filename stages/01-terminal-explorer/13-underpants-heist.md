# Lesson 1.13: The Great Underpants Heist

**Time:** 45–60 min · **You need:** a fresh mystery in the learner's home
(see below) · **New words:** evidence, suspect, clue

## Goal *(read this to the learner)*

> Something TERRIBLE has happened at Fuzzlewood Elementary. Principal
> Pickles' prize-winning underpants have been STOLEN from the trophy
> case! Only a Terminal Detective can crack this case, using `grep`,
> pipes, and your brain.

## Before the lesson *(guide, 5 min)*

- [ ] From **your** account, in the course folder, run:
      ```
      ./scripts/give-lab.sh LEARNER heist
      ```
      It prints the culprit and the suspects, **for your eyes only**.
      Write them down out of sight.
- [ ] Ham it up. Detective hat optional, but strongly recommended.

## Warm-up (5 min)

"What's the difference between `find` and `grep`? How do you make one
command's output go into another?"

## Activity

1. **Open the case file.**
   ```
   cd ~/heist
   ls
   cat START-HERE.txt
   ```
   Read the story together, dramatically.

2. **Let the detective work.** The learner solves it on their own. Your
   job is to:
   - ask good questions: "What did that clue tell you? How could you use
     it?"
   - remind them about the hints: `cat hints/hint-1.txt`, opening only
     the next one when they're stuck
   - keep a **suspect board** on paper as they go: clues on one side,
     suspects on the other

3. **The solving path** *(for you, the guide; don't read it out!)*:
   1. `grep CLUE crime-scene.txt` shows three clues: a room number, a
      glitter colour, and "check the hall log after 12:30".
   2. `grep "Room 7 " students.txt | grep purple` (with their own room and
      colour) gives three suspects.
   3. `grep "trophy case" hall-log.txt`, or `grep "Name" hall-log.txt` for
      each suspect: only one passed the trophy case after 12:30.
   4. `./accuse "Firstname Lastname"`

   Other routes that work are welcome too. Celebrate any method that solves it!

4. **Case closed!** When `./accuse` prints CASE CLOSED, celebrate loudly.
   Then have them **explain how they solved it**, step by step, as if
   telling a detective trainee.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `cd: heist: No such file or directory` | The mystery wasn't made yet | Run the give-lab command from your account. |
| `./accuse` says "It wasn't me!" | Wrong suspect, or a misspelled name | Check the spelling (copy and paste the name!). Check the times: *after* 12:30. |
| `grep "Room 1 "` finds rooms 10 to 19 too | The space after the number is missing | Add a space inside the quotes: `"Room 1 "`. (Hint 2 explains this.) |
| `bash: ./accuse: Permission denied` | The file lost its run permission | From your account: `sudo chmod +x /home/LEARNER/heist/accuse`. |
| They grep'd a name and got nothing | Typo, or wrong capitals | Try `grep -i`. |

## Talk about it

- Which command was most useful? Why?
- How did the pipe help narrow down the suspects?
- Could you solve this by just reading every file? How long would that take?
  *(crime-scene.txt has 600 lines!)*

## Challenge

- **Play again:** run give-lab again for a brand-new random mystery
  (different culprit, room and colour). Can they solve it faster, without
  hints?
- **Detective stats:** How many students are in the school?
  *(`wc -l students.txt`)* How many have a pet tarantula?
  *(`grep -c tarantula students.txt`)*

## Checkpoint

The learner can, without help:
- [ ] Solve a new mystery using `grep`, pipes, and at most one hint
- [ ] Explain their solving steps in order

## Lab notebook

Write up the case: the clues, the suspects, the culprit, and the commands
that cracked it. Draw the moment Principal Pickles gets the underpants back.

## Guide's background *(optional reading)*

This mystery is original to this course, inspired by the classic Command
Line Murder Mystery (which has a grown-up theme). It's randomly generated,
so siblings or a replay get a different case each time. The answer is
stored only as a scrambled "hash" inside `./accuse`, so the learner can't
peek. Hashes come back in Stage 11.
