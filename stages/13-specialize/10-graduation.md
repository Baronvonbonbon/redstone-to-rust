# Lesson 13.10: Graduation

**Time:** 2 sessions of 45 min, plus a show-and-tell (as long as it
takes) · **You need:** the learner's quest (finished, or at a
milestone); the passport; every lab notebook; the mountain map from
Lesson 13.1; an audience · **New words:** retrospective, portfolio,
lifelong learning

## Goal *(read this to the learner)*

> You started this course learning to type and to count on your
> fingers in binary. Since then you've built a computer from NAND
> gates, written a compiler, a kernel, a network server and a
> programming language, and sent code to a real project. Today you'll
> look back at the whole climb, show your quest to an audience, and
> earn the last badge. Then: what's next is up to you.

## Before the lesson *(guide, 20 min)*

- [ ] Read this whole lesson once.
- [ ] Invite an audience for Session 2's show-and-tell: family,
      friends, grandparents on a video call, the student from Lesson
      13.9. Tell them it's about 20 minutes, and they should ask
      questions.
- [ ] Collect everything: all the lab notebooks, the passport, the
      Stage 0 robot sandwich drawing (if you kept it), and the mountain
      map.
- [ ] Look at the Stage 13 checkpoint (in the [README](README.md)) and
      decide, honestly, whether the badge is earned. If the quest isn't
      finished, a real milestone is enough; graduation isn't the end of
      the quest.

## Warm-up (5 min)

"What's the first thing you remember doing in this course?" *(Lesson
0.1: the robot sandwich. Telling a "robot" exactly what to do, and
watching it go wrong.)* "Was that programming?"

## Activity

### Session 1: the retrospective

1. **Then and now.** Find the oldest lab notebook page, and the newest.
   Put them side by side. **Ask:** "What can you do now that you
   couldn't do then?" Let the learner list as many as they can, and
   write them down.

2. **The mountain, finished.** Take the mountain map from Lesson 13.1.
   Colour in the whole climb. Add the quest on top, as a flag. **Say:**
   "Most adults who program never see the whole mountain: the gates,
   the compiler, the kernel and the network. You have."

3. **A retrospective.** **Say:** "At the end of a project, engineering
   teams have a meeting called a **retrospective**: looking back, to do
   better next time. There are three questions." Write them, and answer
   each with three things:
   - What went well?
   - What was hard, and how did I get through it?
   - What would I do differently next time?

4. **The portfolio.** **Say:** "A **portfolio** is a collection of your
   best work, to show people." Choose five things from the whole course
   (one is the quest). For each, write one sentence: what it is, and
   why it's in the portfolio. Put them in a new file in the quest
   repository, `PORTFOLIO.md`, with where each one lives (like
   `~/lab/n2t/projects/5/CPU.hdl`). Commit. *(Not on the internet:
   it's for showing in person, unless the family decides otherwise.)*

### Session 2: show and tell

5. **Prepare** (15 minutes). The show-and-tell has three parts, like
   Stage 0's (Lesson 0.11):
   - **The quest**: show it working (the Pico blinking, LFS booting, the
     game running...). Explain one part of how it works, in words the
     audience will understand.
   - **The climb**: the mountain map, and one surprising thing from it
     (a favourite: "this computer is made of NAND gates I built", or
     "a pressed button reads low").
   - **Questions** from the audience.

   Practise once with the guide.

6. **Show and tell.** The learner presents. The guide's job is to
   enjoy it, and to ask one good question if nobody else does.

7. **The badge.** Go through the Stage 13 checkpoint together, in the
   [README](README.md). Fill in the passport's last line: **Open Source
   Contributor**, with the date. **Say:** "That's the last badge in the
   course. It isn't the last thing you'll learn."

8. **What's next.** Together, write a "next" list in `QUEST.md`. Some
   ideas, all in the offline library:
   - *The Embedded Rust Book* (`repos/embedded-rust-book`), after the
     Pico path.
   - *Writing an OS in Rust* (`repos/writing-an-os-in-rust`), after
     Stage 10.
   - The rest of *Crafting Interpreters* (closures, classes, a bytecode
     VM in C), after Pickaxe.
   - The OSSU curriculum (`repos/ossu-computer-science`): a whole
     university degree's worth, for the years ahead, and the
     mathematics in [MATH-TRACK.md](../../docs/MATH-TRACK.md).
   - Another quest, another patch, another lesson.

   **Say:** "People who are good at computing never stop learning: the
   field changes every year. That's called **lifelong learning**, and
   you've already started."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The quest isn't finished | Quests often take longer than a stage | Show the last milestone. "Still going" is a real engineering status. |
| The demo breaks during the show-and-tell | Demos always do, sometimes | Explain what it should do, and what you'd check first. That's impressive too. |
| The learner can't think of what went well | Modesty, or tiredness | Read their own lab notebook pages back to them. |
| The audience doesn't understand | Too much jargon | Use an analogy: the Cookie Factory, Numberblocks, Minecraft. |

## Talk about it

- What's the most important thing you learned in the whole course? Not
  the hardest: the most important.
- Which badge was hardest to earn?
- What would you tell a younger kid who's about to start Stage 0?
- What do you want to learn next?

## Challenge *(if there's time, or for next time)*

- Write a letter to yourself, to open in five years: what you can do
  now, and what you hope you'll be able to do then. Seal it.
- Lead a whole lesson from Stage 0 or 1 for a younger child, from the
  course as it is.

## Checkpoint

The learner can, without help:
- [ ] Answer the three retrospective questions with real examples
- [ ] Choose five portfolio pieces and explain each
- [ ] Present their quest to an audience and answer questions
- [ ] Say what they'll learn next, and where to find it

## Lab notebook

The last page: the finished mountain map, the retrospective, and the
"next" list. Sign it and date it. Add *retrospective*, *portfolio* and
*lifelong learning* to `dictionary.md`.

## Guide's background *(optional reading)*

A retrospective is standard practice in software teams (from agile
methods); the three questions are the common "start, stop, continue"
format in kid words. The portfolio stays offline by default, because a
child's work posted publicly is hard to take back; if your family
decides to share it later, use a first name or handle, as in Lesson
13.4.

Graduation from the course isn't graduation from computing. A learner
who has finished this course has met, at a beginner's depth, most of an
undergraduate computer science curriculum's core: architecture, systems
programming, algorithms, operating systems, networks, security,
programming languages and databases. What they haven't had, mostly, is
the mathematics; [MATH-TRACK.md](../../docs/MATH-TRACK.md) and OpenStax
are the way on.
