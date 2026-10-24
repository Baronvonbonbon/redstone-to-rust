# Lesson 11.10: Fingerprints: Hashes

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor;
`~/lab/net/python`; paper · **New words:** hash, fingerprint,
collision, SHA-256, checksum, one-way

## Goal *(read this to the learner)*

> A fingerprint is tiny, but it belongs to just one person. Computers
> can take a fingerprint of anything (a word, a photo, a whole game)
> as a short number. Change one letter, and the fingerprint changes
> completely. Today you'll make a toy fingerprint, see where it fails,
> then use a real one to catch a sneaky change to a file, and find
> out what git's long commit numbers really are.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Lesson 7.12 (hash tables) used a small hash to choose a bucket.
      Today's are the same idea, made much bigger and much harder to
      fool.

## Warm-up (5 min)

"In Lesson 11.4, could anyone on the way change your message, without
you knowing?" *(Yes: plain `nc` has no protection.)* "How could you
check that a file you got is exactly the one that was sent?" Guess. One
idea: send it twice. Another: send something much shorter that only
fits that file.

## Activity

### Session 1: toy fingerprints

1. **Letter sums, on paper.** **Say:** "A = 1, B = 2, all the way to
   Z = 26. Add up the letters of a word, and keep only the last two
   digits." Do `CAB` together *(3 + 1 + 2 = 6)*, then `STEVE`
   *(19 + 20 + 5 + 22 + 5 = 71)*. **Say:** "71 is STEVE's
   **fingerprint**. Computer scientists call it a **hash**."

2. **In Python.** In `~/lab/net/python`, make `toyhash.py`:
   ```python
   # A toy fingerprint: add up the letters (A=1, B=2, ... Z=26),
   # and keep only the last two digits.
   def toyhash(word):
       total = 0
       for letter in word.upper():
           if letter.isalpha():
               total = total + ord(letter) - ord("A") + 1
       return total % 100


   for word in ["CREEPER", "ZOMBIE", "STEVE", "ALEX", "LISTEN", "SILENT"]:
       print(word, toyhash(word))
   ```
   `python3 toyhash.py`. **They should see:**
   ```
   CREEPER 70
   ZOMBIE 70
   STEVE 71
   ALEX 42
   LISTEN 79
   SILENT 79
   ```
   **Ask:** "What went wrong?" *(Two pairs share a fingerprint.)*
   **Say:** "That's a **collision**: two different things with the same
   fingerprint. `LISTEN` and `SILENT` have the same letters in a
   different order, so adding can't tell them apart. And `% 100` means
   there are only 100 fingerprints for all the words in the world."

3. **How soon do they clash?** **Ask:** "If we fingerprint mobs one at a
   time, how many before two clash? There are 100 fingerprints." Write
   the learner's guess down. Make `mobs.txt`, one per line:
   ```
   creeper
   skeleton
   spider
   enderman
   witch
   blaze
   ghast
   slime
   pig
   cow
   sheep
   chicken
   wolf
   fox
   ```
   and `clash.py`:
   ```python
   # Give every mob a toy fingerprint, and stop at the first clash.
   def toyhash(word):
       total = 0
       for letter in word.upper():
           total = total + ord(letter) - ord("A") + 1
       return total % 100


   seen = {}
   for line in open("mobs.txt"):
       mob = line.strip()
       fp = toyhash(mob)
       print(mob, fp)
       if fp in seen:
           print(f"Clash! {seen[fp]} and {mob} have the same fingerprint.")
           break
       seen[fp] = mob
   ```
   `python3 clash.py`. **They should see:**
   ```
   creeper 70
   skeleton 1
   spider 71
   enderman 74
   witch 63
   blaze 46
   ghast 55
   slime 58
   pig 32
   cow 41
   sheep 53
   chicken 53
   Clash! sheep and chicken have the same fingerprint.
   ```
   **Say:** "Only 12! It's like birthdays: in a class of 23, it's more
   likely than not that two people share a birthday, even though there
   are 365 days. Every new mob has to miss *all* the ones before it,
   and that gets hard quickly. So a good fingerprint needs a huge
   number of possible values." *(`seen` is a dictionary from Stage 3:
   fingerprint → the mob that had it first.)*

4. **Going backwards.** **Ask:** "I'm thinking of a word with
   fingerprint 70. Which word?" *(CREEPER? ZOMBIE? Any of thousands.
   You can't tell.)* **Say:** "The fingerprint doesn't contain the word.
   Lots of information is thrown away, so you can't run it backwards.
   That's called **one-way**. Real fingerprints are one-way too, but
   without the easy collisions." Commit.

### Session 2: real fingerprints

5. **SHA-256.** In a terminal, in `~/lab/net/python`:
   ```
   echo "Meet at the treehouse at 4." > note.txt
   sha256sum note.txt
   ```
   **They should see:**
   ```
   c98a16c160a97ee92665dd327d8d54af7b391a35bb68be7ce44a89ffff3f0774  note.txt
   ```
   Change the 4 to a 5 and run it again. **They should see:**
   ```
   9dc9b388985ea859041cac1b752a82399f976d5273227f227d09fe2241ad6a6e  note.txt
   ```
   **Say:** "**SHA-256** is a real fingerprint, used all over the world.
   It's always 64 hexadecimal digits (Stage 4): 256 bits, whatever the
   size of the file. One tiny change, and the whole thing is different."
   Try it on something big: `sha256sum /usr/bin/ls`. *(Still 64
   digits, for a 142,000-byte program.)*

6. **How different?** Make `avalanche.py`:
   ```python
   import hashlib

   a = hashlib.sha256(b"creeper").hexdigest()
   b = hashlib.sha256(b"Creeper").hexdigest()
   print(a)
   print(b)

   # Turn each fingerprint into 256 ones and zeros, and count the differences.
   bits_a = bin(int(a, 16))[2:].zfill(256)
   bits_b = bin(int(b, 16))[2:].zfill(256)
   different = 0
   for n in range(256):
       if bits_a[n] != bits_b[n]:
           different = different + 1
   print(f"{different} of the 256 bits are different")
   ```
   `python3 avalanche.py`. **They should see:**
   ```
   8f0b49be84aba883a225569f87359227261e79b4d76cff56888ca4ab9c7a15ee
   edcf837a324d27b4e2c9e362dbfc411c8cd2a3f019f67e95fa0740e498594aa3
   130 of the 256 bits are different
   ```
   **Say:** "`c` is 99 and `C` is 67. In binary that's `01100011` and
   `01000011`: just one bit apart. One bit in, about half the bits out.
   That's called the **avalanche**: no clue about what changed, or how
   much." *(`b"..."` means bytes, from Stage 9: fingerprints work on
   bytes.)*

7. **Catch a sneaky change.** **Say:** "The Creeper Club keeps its files
   in a folder. Let's write down their fingerprints, so we'll know if
   anyone changes them." In `~/lab/net/python`:
   ```
   mkdir club
   cd club
   echo "No exploding indoors." > rules.txt
   echo "Ssssss!" > motto.txt
   sha256sum rules.txt motto.txt > ../fingerprints.txt
   cat ../fingerprints.txt
   sha256sum -c ../fingerprints.txt
   ```
   **They should see:**
   ```
   ab95463c82a1b4c6edab1a1d2738a355bb4813cc08df19a3911e12bc0c104ecd  rules.txt
   629a4fc5bf12c87bd485b187099346dd8c29865b15c42307ca6e77924257cf7b  motto.txt
   rules.txt: OK
   motto.txt: OK
   ```
   Now the guide is the sneaky one: while the learner looks away, run
   `echo "No exploding indoors. Except Tuesdays." > rules.txt`. The
   learner checks again with `sha256sum -c ../fingerprints.txt`. **They
   should see:**
   ```
   rules.txt: FAILED
   motto.txt: OK
   sha256sum: WARNING: 1 computed checksum did NOT match
   ```
   **Say:** "Caught! A fingerprint used to check a file is often called a
   **checksum**. Pop!_OS publishes the SHA-256 of its download, so
   anyone can check theirs wasn't changed on the way. And `apt` checks
   the fingerprint of every package before it installs it." **Ask:** "What
   if the sneaky person changed `fingerprints.txt` too?" *(Then it would
   say OK! The fingerprints have to come from somewhere you trust. Lesson
   11.13 has the answer to that: signatures.)*

8. **Git's fingerprints.** Still in `club`:
   ```
   git init
   git add .
   git commit -m "Club files"
   git hash-object motto.txt
   git cat-file -p HEAD
   ```
   **They should see** something like:
   ```
   0de22c7e879b5bf3697104c15544a1dbe0a689e5
   tree de4940f7b07054f78bf782a5fdefbba4bd1eb4bc
   author Sam <sam@example.com> 1792857344 -0400
   committer Sam <sam@example.com> 1792857344 -0400

   Club files
   ```
   The first line is the same on every computer. The tree's number will
   be different if `rules.txt` was changed back. **Say:** "Every file
   git keeps is named by its fingerprint (git uses an older one called
   SHA-1, 40 digits). A commit is a little note saying which tree, who,
   when and why, and *its* fingerprint is the commit number you've been
   seeing since Stage 5." Run `git cat-file -p 'HEAD^{tree}'`: the files,
   each with its fingerprint. **Ask:** "If someone changed an old file in
   the history, what would happen to every commit after it?" *(All
   their numbers would change, because each commit includes the one
   before it. You can't quietly change history.)* Commit `~/lab/net/python`
   (git will mention the `club` repository inside it: that's fine, or
   move `club` somewhere else first).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| A different SHA-256 for `note.txt` | The text isn't exactly the same: a missing full stop, or a space | It must match exactly, including the full stop. That's the point! |
| `sha256sum: rules.txt: No such file or directory` | `sha256sum -c` was run from the wrong folder | Run it inside `club`, where the files are. |
| `FileNotFoundError: ... 'mobs.txt'` | `clash.py` is in a different folder from `mobs.txt` | Put them together in `~/lab/net/python`. |
| A clash at a different mob | A typing mistake in a mob's name | Check `mobs.txt`; any clash still proves the point. |
| `git hash-object` prints a different number | `motto.txt` isn't exactly `Ssssss!` and a new line | That's fine: it's still that file's fingerprint. |
| `warning: adding embedded git repository: club` | The `club` repository is inside the `python` one | Move `club` out (`mv club ~/lab/net/`), or ignore it. |

## Talk about it

- What's a fingerprint (hash)? Why is it so short?
- What's a collision? Why did the toy one have so many?
- Why can't you work out a word from its fingerprint?
- How can a fingerprint prove a download wasn't changed? What else do
  you need to trust?
- What are git's commit numbers made from?

## Challenge *(if there's time, or for next time)*

- Make `toyhash` better: multiply the total by 31 before adding each
  letter (like Lesson 7.12), and keep `% 1000`. Do `LISTEN` and
  `SILENT` still clash? How many mobs before a clash now?
- How many people do you need before two share a birthday, more often
  than not? Write a Python program that tries it 1000 times with
  `random.randint(1, 365)`. *(About 23.)*
- `sha256sum` a photo, then change one pixel in an editor and do it
  again.

## Checkpoint

The learner can, without help:
- [ ] Explain a hash as a fingerprint, and what a collision is
- [ ] Explain why bigger fingerprints clash less (the birthday idea)
- [ ] Use `sha256sum -c` to catch a changed file
- [ ] Explain what a git commit number is a fingerprint of

## Lab notebook

Draw a word going into a fingerprint machine, and a short number coming
out, with an arrow back that's crossed out ("one-way"). Write down how
many mobs it took to get a clash. Commit. Add *hash*, *collision*,
*SHA-256*, *checksum* and *one-way* to `dictionary.md`.

## Guide's background *(optional reading)*

A **cryptographic hash function** like SHA-256 has three properties the
toy one lacks: given a fingerprint, you can't find something that makes
it (one-way); given one input, you can't find another with the same
fingerprint; and you can't find *any* two inputs that collide. With 2²⁵⁶
possible fingerprints, the birthday effect means a collision would take
about 2¹²⁸ tries, which is far beyond every computer on Earth. SHA-1
(which git uses) has had a collision found deliberately, in 2017, which
is why git is moving to SHA-256 and has protections against that attack.

Fingerprints are how a program can check something without keeping it.
The Underpants Heist's `./accuse` (Lesson 1.13) worked that way: it
kept only the fingerprint of the answer, and compared it with the
fingerprint of the learner's guess. Linux and websites store passwords
the same way, which Lesson 11.11 explains, with a deliberately slow
fingerprint so that each check costs time.

Lesson 7.12's hash tables use small, fast hashes that only need to
spread keys out; the security kind is slower and much bigger. Python's
`hashlib` and the `sha256sum` command use the same algorithm, so
`hashlib.sha256(b"Meet at the treehouse at 4.\n").hexdigest()` gives
the same answer as step 5 (`echo` adds the `\n`). *Computer Networks: A
Systems Approach*, Section 8.2 ("Cryptographic Building Blocks"), covers
hashes; the offline Python docs have `hashlib`.
