# Lesson 11.16: Project: The Puzzle Trail

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/net`; paper and coloured pens; a player (the guide, a
sibling or a grown-up) · **New words:** specification, play-test,
walkthrough

## Goal *(read this to the learner)*

> You've sent packets, written servers, cracked old codes, made
> uncrackable ones, signed files and built a firewall. Now you'll use
> them to make something for someone else: a puzzle trail on the family
> computer, where every step needs a different trick. Then you'll
> watch someone play it, and earn the **Net Ninja** badge.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once, and the example trail in the [net
      lab handbook](../../labs/net/README.md#an-example-puzzle-trail).
      Don't show it to the learner unless they're stuck: designing the
      trail is the project.
- [ ] Choose the player now, and agree a time for them to play
      (Session 4). If the player is the guide, try not to watch the
      learner build it!
- [ ] The trail stays on the family computer and in the Sandbox, and any
      server listens on `127.0.0.1` only. The player plays at the same
      computer.

## Warm-up (5 min)

"Which Stage 11 lesson was the most fun? Which trick would make the
best puzzle?" Make a list of everything from the stage: `ping`, routes,
`/etc/hosts`, `dig`, `nc`, `tcpdump`, servers, the vault, HTTP, ciphers,
fingerprints, passphrases, key exchange, signatures, firewalls.

## Activity

### Session 1: designing the trail

1. **The rules of the trail.** A trail is a chain of **steps**. Each step
   gives the player a clue to the next. Rules:
   - At least **four steps**, each needing a *different* Stage 11 idea.
   - At least one **Rust or Python server** on `127.0.0.1` that the
     player talks to with `nc` or a browser.
   - At least one **cipher** (Lesson 11.8 or 11.9).
   - The **end** is a treasure file the player can check is real with a
     fingerprint or a signature (Lesson 11.10 or 11.13).
   - Every step must be fair: the player has learned it, or the clue
     teaches it.
   - Nothing on the trail touches anyone else's files or computers. (The
     Pledge.)

2. **Ideas for steps.** The learner can use these, or their own:
   - A note in Caesar or keyword code, whose answer is a port number.
   - A **riddle door**: a server that asks a riddle, and gives the next
     clue for the right answer.
   - A web page from the Lesson 11.7 server, with the clue hidden in the
     page's source (Firefox: Ctrl+U) or in a header (`curl -i`).
   - A name added to the Sandbox's `/etc/hosts`, which only `ping` or
     `getent hosts` can find.
   - A word only visible in `tcpdump -A` (in the Sandbox), when the
     player sends something to a server there.
   - A file locked with `openssl enc` (Lesson 11.12), whose passphrase is
     the answer to an earlier step.
   - A treasure file with a `.sig`, and a `signers.txt` to check it with.

3. **A specification.** On paper, draw the trail as a map: a box for
   each step, and an arrow to the next, with what the player must do on
   the arrow. Under it, write:
   - Each clue, word for word.
   - Each answer.
   - Which programs and files are needed, and where they go.
   - Three **milestones**: (1) the first two steps working; (2) all
     steps working; (3) the treasure, with its fingerprint or signature,
     and a starting note for the player.

   **Ask:** "What could go wrong for the player? Where might they get
   stuck?" Write a hint for each step, for the guide to give if asked.

### Sessions 2 and 3: building

4. **Build in milestones.** Same habits as Stage 9's project:
   - Build one step, then test it yourself, as if you were the player.
   - Servers: `cargo new`, one project each, in `~/lab/net`. Start from
     the Shouty server (Lesson 11.5) or the vault (Lesson 11.6). Bind to
     `127.0.0.1`.
   - Every server must survive sneaky input (Lesson 11.14): try a wrong
     answer, an empty line, a very long line, and the rude visitor from
     Lesson 11.5 (`printf 'caf\xe9\n' | nc -N 127.0.0.1 PORT`). If it
     crashes, fix it.
   - Before each commit: `cargo fmt`, `cargo clippy`.
   - Commit at the end of every session, even if it's not finished.
   - Keep the answers in a file called `ANSWERS.md` in a separate
     repository, `~/lab/net/trail-answers`, so that the player doesn't
     find them. (Is that safe enough? See the challenge.)

5. **A starting note.** Write `START.txt` for the player: a short story
   (a missing diamond? a creeper on the loose? Captain Underpants-style
   nonsense is welcome) and the first clue. Put it somewhere the player
   will look, like their own home folder (the guide can copy it there),
   or print it out.

### Session 4: play-test

6. **Play-test.** The **player** follows the trail, at the family
   computer. The learner watches, *without helping*, and writes down:
   - Where the player got stuck, and for how long.
   - Which hints they needed.
   - What they enjoyed.

   **Say:** "This is called a **play-test**. Game designers do it all the
   time. Watching someone else play is the only way to find out if your
   clues make sense." Afterwards, fix one thing the play-test showed.

7. **A walkthrough.** The learner writes `WALKTHROUGH.md` in
   `trail-answers`: each step, what the player does, and why it works.
   This is the trail's documentation, like the guide's sections of every
   lesson.

### Session 5: the Stage 11 checkpoint

8. **Show and tell.** The learner explains, with the map from step 3,
   how each step works underneath: which layer, which port, which
   program.

9. **The checkpoint.** Without notes, the learner explains, with
   drawings if they like:
   - How a packet gets from the Sandbox to the internet: addresses,
     routes, the gateway, and TTL.
   - What DNS does, and how `/etc/hosts` could fool it.
   - Ports, the handshake, and what `tcpdump` can and can't see.
   - Why their servers listen on `127.0.0.1`, and why they check every
     input.
   - Why Caesar and keyword ciphers break, and what "possibilities"
     have to do with it.
   - What a fingerprint is, and what a signature adds.
   - How two people agree a secret in front of a spy.
   - A firewall's default deny, and why updates matter.

10. **The Pledge.** Read the Hacker's Pledge together again
    ([docs/HACKER-PLEDGE.md](../../docs/HACKER-PLEDGE.md)). **Ask:** "Now
    that you know these tricks, which rule matters most?" Talk about
    it. If the learner wants to try more wargames, look at OverTheWire
    together (Guide's background).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `AddrInUse` when starting a server | Another server is using that port | Each server needs its own port; `ss -tln` shows which are taken. |
| The player can't connect to a server | It isn't running, or it's on a different port from the clue | Start every server before the play-test, and check each with `nc`. |
| The player found the answers | They're somewhere the player can read | Move them; see the challenge for a better way. |
| A step needs something the player hasn't learned | The step isn't fair yet | Add a hint to the clue, or choose a different step. |
| The trail is too long to finish in one go | It's too big | Cut it to four steps; save the rest for a sequel. |

## Talk about it

- Which step was hardest to build? Which was hardest to play?
- What did the play-test show that you didn't expect?
- How did you keep your servers safe from sneaky input?
- Which Stage 11 idea do you think is most important for keeping
  people safe online?

## Challenge *(if there's time, or for next time)*

- Lock `ANSWERS.md` with `openssl enc` (Lesson 11.12), with a dice
  passphrase that only you and the guide know.
- Make a sequel trail for a different player, harder or easier.
- Add a step that needs two people: a key exchange (Lesson 11.12), one
  number each.
- Make the riddle door count how many wrong answers each visitor gives,
  and tell them a hint after three.

## Checkpoint

The learner can, without help:
- [ ] Plan a trail of at least four steps, with a map and milestones
- [ ] Build each step, including a server on `127.0.0.1` that survives
      sneaky input
- [ ] Run a play-test without helping, and fix something it showed
- [ ] Explain every step of the Stage 11 checkpoint in step 9

## Lab notebook

Glue in the trail map. Write what the play-test showed, and what you
changed. Commit, and push the trail's repositories to the guide's
backup if you have one. Stamp the Stage 11 badge, **Net Ninja**, on the
passport.

## Guide's background *(optional reading)*

Puzzle trails like this are a gentle version of **capture the flag**
(CTF) contests, where teams solve security puzzles for points. Designing
puzzles is harder than solving them: the learner has to understand
each idea well enough to hide it fairly, and to predict where someone
else will get stuck, which is the same skill as writing good error
messages and documentation. The [net lab
handbook](../../labs/net/README.md) has an example trail with a tested
riddle-door server, for the guide only.

**OverTheWire** (overthewire.org) runs free online wargames with shared
public logins and no personal account: **Bandit**, which the Mineshaft
was modelled on, then **Krypton** (classical ciphers, like Lesson 11.9)
and **Natas** (web security, like Lesson 11.14). They are played on
OverTheWire's own servers, which invite exactly this, so they're within
the Pledge; the guide should sit with the learner, and the learner
should follow the site's rules (no sharing passwords or solutions).
They need the internet and are optional. **picoCTF**, run by Carnegie
Mellon University, is aimed at school students but needs an account, so
it's for later, if the family decides to.

Everything in Stage 11 fits in an hour-long talk for a grown-up, too:
the learner explaining step 9 to a relative is a fine extra checkpoint.
