# Lesson 13.1: Choose Your Path

**Time:** 2 sessions of 45 min · **You need:** the learner's passport
and lab notebook; paper and coloured pens; the offline library · **New
words:** field, path, quest, milestone, journal

## Goal *(read this to the learner)*

> You've climbed from the terminal down to the gates and back up to
> your own language, operating system, network servers and database.
> That's the whole map of computer science, seen once. Now you choose
> where to go deeper. Today you'll look back at everything you've
> done, explore the fields of computing, and plan your own **quest**.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson, and the [Stage 13 README](README.md),
      which explains how this stage works: four lessons for everyone,
      then a path, then teaching and graduation.
- [ ] Look through the passport and lab notebook yourself first. Note
      the lessons where the learner was most excited, and the ones they
      came back to by themselves. That's the best evidence there is.
- [ ] Think about what the family can support: the Pico path needs about
      $15 of parts (see the [Pico lab handbook](../../labs/pico/README.md));
      the Linux From Scratch path needs the internet for a day and a lot
      of patience.

## Warm-up (5 min)

"If you could only keep one thing you've made in this course, which
would it be?" Let them answer without help, then ask why.

## Activity

### Session 1: looking back, and looking around

1. **The map so far.** On a big sheet of paper, draw the course as a
   mountain (the picture from the syllabus): up from the terminal and
   Python, down through bits, gates and the Hack computer, back up
   through algorithms, C, the compiler, Rust, the operating system,
   networks, security, languages and data. Mark each stage with its
   badge. **Say:** "Every one of these is a whole field. Real
   computer scientists spend their lives in just one or two."

2. **Stars and question marks.** Go through the passport together. For
   each stage, the learner draws a **star** next to the parts they loved,
   and a **question mark** next to the parts they want to understand
   better. Count them up by area. **Ask:** "Where are most of your
   stars?"

3. **The fields of computing.** Read this list together. For each one,
   **Ask:** "Have you seen a bit of this already? Where?"
   - **Embedded systems and control**: tiny computers inside machines,
     reading sensors and driving motors. *(The PLC rungs in Lesson 4.13;
     the scan cycle; Redstone OS.)*
   - **Operating systems**: kernels, drivers, booting. *(Stage 10.)*
   - **Programming languages**: compilers, interpreters, type systems.
     *(Stages 8 and 12.)*
   - **Security**: finding and fixing weaknesses, cryptography.
     *(Stage 11.)*
   - **Networks and the web**: protocols, servers, browsers.
     *(Stage 11.)*
   - **Databases and data**: storing, querying, and making sense of data.
     *(Stage 12.)*
   - **Algorithms and theory**: what can be computed, and how fast.
     *(Stage 7.)*
   - **Games and graphics**: drawing, physics, game engines. *(The turtle;
     Pygame Zero; Creeper Chase.)*
   - **Hardware and computer architecture**: designing chips. *(Stages 4
     and 6.)*
   - **Teaching and writing**: explaining computing to others. *(Every
     lab notebook you've written.)*

4. **Look in the library.** The offline library has a map made by people
   who taught themselves computer science: the OSSU curriculum. In a
   terminal:
   ```
   ls /srv/redstone-library/repos/ossu-computer-science
   less /srv/redstone-library/repos/ossu-computer-science/README.md
   ```
   (Press `/` and type `Core` to search; `q` to leave.) **Say:** "It's
   written for grown-ups, but look at the headings: you've already met
   a piece of nearly every one." Find two that match the learner's stars.

### Session 2: planning a quest

5. **Two paths with lessons.** **Say:** "This stage has two paths with
   step-by-step lessons, and you'll do at least one:" Read the
   descriptions in the [README](README.md):
   - **The Pico path** (Lessons 13.5 to 13.7): a $5 computer the size
     of a stick of gum, programmed in Rust; a real PLC rung on real
     buttons; and a fan controller with a thermometer, like the
     controls a factory uses.
   - **The Linux From Scratch path** (Lesson 13.8): building a whole
     Linux system, one program at a time, from source code, in a
     virtual machine.

   Or a **quest of your own**, in any field from step 3, planned the
   same way as a path.

6. **A quest card.** Whatever they choose, the learner fills in a quest
   card, on paper, then copies it into a new repository:
   ```
   mkdir -p ~/lab/quest
   cd ~/lab/quest
   git init
   ```
   `QUEST.md`:
   ```
   # My quest

   What I want to make or understand:
   Why it matters to me:
   Which earlier lessons it builds on:
   What I'll use (books, tools, parts):
   The first small step (one session):
   Milestones:
     1.
     2.
     3.
   How I'll know I'm done:
   Who I'll show it to:
   ```
   **Say:** "A quest is like the projects in Stages 9 and 12, but you
   choose everything. The first step must be small enough to do in one
   session. That's the most important line on the card."

7. **A journal.** **Say:** "Real engineers keep notes of what they tried,
   what broke, and what they learned. From now on, at the end of every
   session, write three lines in `JOURNAL.md`: what I did, what
   surprised me, what's next." Write the first entry now. Commit both
   files.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ls: cannot access '/srv/redstone-library/...'` | The offline library isn't set up, or is somewhere else | The guide runs `./scripts/mirror-library.sh` (see [docs/SETUP.md](../../docs/SETUP.md)). |
| The learner wants to do everything | That's a good problem | Choose one now; the others can be the next quest. Write them on the back of the card. |
| The learner can't choose | No clear favourite yet | Do the Pico path: it's short, it's hands-on, and it pulls together bits, Rust and control. |
| The first step is "build a game engine" | The step is too big | Ask "What could you finish *today*?" until it's one session's work. |

## Talk about it

- Which stage gave you the most stars? Why do you think that is?
- Which fields of computing have you already touched?
- Why must the first step of a quest be small?
- Why do engineers keep a journal?

## Challenge *(if there's time, or for next time)*

- Interview a grown-up who uses computers at work. What field are they
  in? What do they wish they'd learned first?
- Draw your own map of computing, with the fields as countries and the
  course's stages as roads between them.

## Checkpoint

The learner can, without help:
- [ ] Name five fields of computing, with a lesson from the course for
      each
- [ ] Explain their choice of path or quest, with evidence from the
      passport
- [ ] Write a quest card with a first step small enough for one session
- [ ] Keep a journal entry for the session

## Lab notebook

Glue in the mountain map with its stars and question marks. Copy the
quest card. Add *field*, *quest*, *milestone* and *journal* to
`dictionary.md`.

## Guide's background *(optional reading)*

This stage is deliberately less scripted than the others: the aim is a
learner who can choose a direction, plan, find resources, and finish
things, with the guide as a mentor rather than a script reader. The two
scripted paths keep the course's usual standard (every command shown,
every output real), so a learner can do one of them without the guide
needing new skills.

The OSSU (Open Source Society University) Computer Science curriculum
is a free, self-taught degree built from university courses; *Teach
Yourself Computer Science* (teachyourselfcs.com) is a shorter list of
the nine subjects and the best book for each. Both are for later years,
but they show the learner that their stars map onto real, grown-up
fields. If a learner's quest needs something online with an account
(many courses do), it waits, or the guide does that part, by the
course's rules ([CONTRIBUTING.md](../../CONTRIBUTING.md)).
