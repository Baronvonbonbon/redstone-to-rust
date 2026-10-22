# The Guide's Handbook

You don't need to know anything about computers to lead this course.
Your job isn't to know the answers. Your job is to:

1. Read the lesson before the session (10 minutes).
2. Set things up using the lesson's "Before the lesson" checklist.
3. Read the learner the goal, then let **them** do the typing.
4. When they get stuck, use the lesson's "If something goes wrong"
   table, then the stuck ladder below.
5. Ask the "Talk about it" questions at the end.
6. Tick the checkpoint boxes, and help them write in their lab notebook.

## The shape of a session

Most lessons take 30 to 45 minutes. Short and frequent beats long and rare.

| Part | Time | What happens |
|---|---|---|
| Warm-up | 5 min | Recall last time: "What did the `ls` command do?" |
| Activity | 20–30 min | Follow the lesson's steps |
| Talk about it | 5 min | Questions from the lesson |
| Lab notebook | 5 min | The learner writes down what they learned, in their own words |

A good rhythm is **3 or 4 sessions a week**, plus free play. Free play
means games from the current or an earlier stage, which are listed in
each stage's README. Free play is where a lot of the real learning happens.

## Rules for the guide

**Hands off the keyboard.** This is the most important rule. Point,
read, ask questions, but don't take over typing. If you have to show
something, do it on your own computer, or type it once and then delete
it so they can type it themselves.

**Errors are good news.** When the computer prints an error, say
"Great! The computer is telling us something. What does it say?" Read
error messages out loud together. Most of programming is reading error
messages calmly.

**"I don't know, let's find out" is a great answer.** When you don't
know something, say so. Then show how to find out: `--help`, `man`,
the lesson's background notes, or the offline books. Watching an adult
look things up teaches as much as the lesson does.

**Celebrate creative solutions.** If they solve something a different
way than the lesson expected, and it works, it counts. Ask them to
explain how.

## The stuck ladder

When the learner is stuck, climb one rung at a time:

1. **Wait.** Count to 20 in your head. Most "stuck" fixes itself.
2. **"Read it out loud."** Have them read the error, or their own
   command, letter by letter. Most bugs are typos, and reading aloud
   catches them.
3. **"What did you expect, and what happened instead?"**
4. **Check the lesson's "If something goes wrong" table.**
5. **Give the lesson's hint.** Labs have hint files numbered in order;
   open only the next one.
6. **Take a break.** Walk around, get a snack, come back. This isn't
   giving up; it's how professionals work too.
7. **Do it together**, with them typing as you read the answer out.
   Then do the same thing again tomorrow without help.

Make 20 minutes the limit: if they've been stuck that long on the same
thing, go to step 7 and move on. Being stuck all the time teaches
"I'm bad at this", which is the opposite of what we want.

## Pacing a fast learner

Advanced kids are often fast at *reading* and slower at *doing*. Watch
out for:

- **Racing ahead.** If they can recite what a command does but can't use
  it to solve a new problem, slow down. Every stage has a checkpoint;
  don't skip it.
- **Skipping the boring part.** Typing practice and lab notebooks feel
  slow, and they pay off enormously later. Keep them in.
- **Frustration at the first wall.** Kids who are used to everything
  being easy can melt down when something is hard. Name it: "This is the
  good kind of hard. Your brain is growing right now." Then use the stuck
  ladder.

You *can* skip a lesson if they pass its checkpoint cold. Don't skip
whole stages.

**How long will this take?** It varies a lot, and that's fine. Stages 0
to 5 might take one to two years at a few sessions a week. Stages 6 to 13
are university-level material and may take several years, often mixed
with the learner's own projects. The math track sets some of the pace
(see [MATH-TRACK.md](MATH-TRACK.md)).

## The lab notebook

From Stage 0 to Stage 4 this is a **paper notebook**. After each session
the learner writes:

- the date
- one thing they learned, in their own words
- one command or idea they want to remember
- (optional) a question they still have

From Stage 5 on, the notebook moves into **git** on the computer, and
the old paper notebooks become something to be proud of.

## Badges and the passport

Each stage ends with a checkpoint and a badge. Print
[PASSPORT.md](../PASSPORT.md) and stamp, sign, or sticker it when a
stage is done. Small ceremonies matter: let them show someone, and put
it on the fridge.

## Computer safety and setup

- The learner gets **their own user account without admin powers**.
  [SETUP.md](SETUP.md) shows how. They can't break the family computer,
  and they get used to the idea of users.
- **Never add the learner's account to the `docker` group.** That group
  is secretly as powerful as the admin. You (the guide) start the labs;
  the learner connects to them.
- From Stage 5, the learner gets a **breakable computer** (a Raspberry
  Pi or a virtual machine) where they *are* the admin. Breaking it and
  fixing it is part of the curriculum.
- Security stages come with the [Hacker's Pledge](HACKER-PLEDGE.md).
  Read it together and sign it before Stage 1's Mineshaft.

## Where to get help offline

- `COMMAND --help` and `man COMMAND` in the terminal
- In Python: `help(thing)`
- In Rust: `rustup doc` opens the Rust books and standard library docs offline
- The offline library made by `scripts/mirror-library.sh` (see [RESOURCES.md](RESOURCES.md))
- Each lesson's "Guide's background" section
