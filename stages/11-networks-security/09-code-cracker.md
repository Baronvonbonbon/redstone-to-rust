# Lesson 11.9: The Code Cracker

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; the alphabet wheel; `~/lab/net/python`; the three secret
messages in `~/lab/net/secrets` (from `give-lab.sh LEARNER net`; see the
Stage 11 README) · **New words:** brute force, key space, frequency
analysis, keyword cipher, dictionary attack

## Goal *(read this to the learner)*

> In Stage 0, you made a cipher wheel. In Stage 3, you wrote a secret
> code machine. Now you'll write a program that cracks Caesar ciphers
> by itself, without the key, using a trick that's over a thousand
> years old. Then you'll meet a stronger cipher with a whole word as
> its key, and crack that too, if its owner chose a guessable word.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check that `~/lab/net/secrets` has `message1.txt`, `message2.txt`
      and `message3.txt`. The answers are in the [net lab
      handbook](../../labs/net/README.md), for you only.

## Warm-up (5 min)

"What's the Caesar cipher, in clock arithmetic?" *(Each letter's number,
plus the key, mod 26.)* "How many different keys are there?" *(26, and
key 0 does nothing, so 25 real ones.)*

## Activity

### Session 1: try every key

1. **By hand.** Show the first message:
   ```
   cat ~/lab/net/secrets/message1.txt
   ```
   ```
   TLLA TL IF AOL AYLLOVBZL HMALY SBUJO. IYPUN AOL IHUHUH.
   ```
   **Say:** "Nobody told us the key. But there are only 25. Try some
   with the wheel, on the first word, `TLLA`." Try a few keys by hand.
   **Ask:** "How long would all 25 take?" *(Ages. A job for a
   computer.)*

2. **Brute force.** Make `crack.py` in `~/lab/net/python`:
   ```python
   import sys

   ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
   COMMON = "ETAOINSHR"


   def shift(message, key):
       out = ""
       for letter in message:
           if letter in ALPHABET:
               number = ALPHABET.index(letter)
               out += ALPHABET[(number + key) % 26]
           else:
               out += letter
       return out


   def score(text):
       points = 0
       for letter in text:
           if letter in COMMON:
               points += 1
       return points


   secret = open(sys.argv[1]).read()
   best_key = 0
   best_score = 0
   for key in range(26):
       attempt = shift(secret, -key)
       print(f"{key:2} {score(attempt):3}  {attempt.splitlines()[0][:50]}")
       if score(attempt) > best_score:
           best_key = key
           best_score = score(attempt)
   print(f"The key is probably {best_key}:")
   print(shift(secret, -best_key))
   ```
   **Say:**
   - "`shift` is from Lesson 11.8. We undo each key by shifting
     backwards: `-key`."
   - "`sys.argv[1]` is the file name typed after the program's name."
   - "`score` counts the letters that are most common in English. Real
     English is full of E, T, A, O, I, N, S, H and R. Gibberish isn't."
   - "The loop tries every key, prints the start of each attempt with
     its score, and remembers the best."

   ```
   python3 crack.py ../secrets/message1.txt
   ```
   **They should see** 26 lines, then the answer. A few of them:
   ```
    0  20  TLLA TL IF AOL AYLLOVBZL HMALY SBUJO. IYPUN AOL IH
    1  19  SKKZ SK HE ZNK ZXKKNUAYK GLZKX RATIN. HXOTM ZNK HG
   ...
    7  32  MEET ME BY THE TREEHOUSE AFTER LUNCH. BRING THE BA
   ...
   The key is probably 7:
   MEET ME BY THE TREEHOUSE AFTER LUNCH. BRING THE BANANA.
   ```
   **Ask:** "Which line scored highest? Is it English?" *(Key 7, 32
   points, and yes!)* **Say:** "Trying every key is called **brute
   force**. It works because the **key space**, the number of possible
   keys, is tiny: 26." Commit.

### Session 2: counting letters

3. **The long message.**
   ```
   cat ../secrets/message2.txt
   ```
   **Say:** "Before using the program, let's crack this one a cleverer
   way, the way people did 1,100 years ago, before computers." In
   `python3`:
   ```
   >>> from collections import Counter
   >>> secret = open("../secrets/message2.txt").read()
   >>> Counter(letter for letter in secret if letter.isalpha()).most_common(5)
   [('X', 29), ('T', 23), ('H', 20), ('G', 20), ('M', 18)]
   ```
   **Say:** "`Counter` counts things. X appears 29 times: far more than
   anything else. What's the most common letter in English?" *(E.)* "So
   X is probably E. How far is it from E to X, round the clock?" *(E is
   4, X is 23: 23 − 4 = 19.)* Check with the program:
   ```
   python3 crack.py ../secrets/message2.txt
   ```
   **They should see** `The key is probably 19:`, and a story about a
   school inspector. Read it together. **Say:** "Counting letters is
   called **frequency analysis**. The scholar al-Kindi described it in
   Baghdad, in the 800s. And it's what our `score` does, too."

4. **Why it works.** **Ask:** "Would counting work on a really short
   message, like `HI`?" *(No: there's not enough to count.)* "What
   about a message with no E in it?" *(It might fool it. Long messages
   in normal English always have plenty.)*

### Session 3: a keyword cipher

5. **A stronger cipher.** **Say:** "The weakness of Caesar is one key for
   every letter. What if every letter had a *different* shift? Choose a
   key word, like `TNT`. T is 19, N is 13. Shift the first letter by 19,
   the second by 13, the third by 19, then start the word again." Do
   `CRE` by hand with the wheel: *(C+19 = V, R+13 = E, E+19 = X.)* Make
   `wordlock.py`: copy `crack.py`'s first part (the `import`, the two
   constants, `shift` and `score`), and add:
   ```python
   def keyword(message, word, direction):
       out = ""
       n = 0
       for letter in message:
           if letter in ALPHABET:
               key = ALPHABET.index(word[n % len(word)])
               out += shift(letter, key * direction)
               n += 1
           else:
               out += letter
       return out


   secret = keyword("CREEPERS ARE GREEN", "TNT", 1)
   print(secret)
   print(keyword(secret, "TNT", -1))
   ```
   `python3 wordlock.py`. **They should see:**
   ```
   VEXXCXKF TKR ZKRXG
   CREEPERS ARE GREEN
   ```
   **Say:** "`n % len(word)` goes round the key word, like a clock with
   three numbers. `direction` is 1 to lock, −1 to unlock." **Ask:**
   "Find every E in `CREEPERS ARE GREEN`. Does each one turn into the
   same letter?" *(No! The Es in `CREEPERS` became X, but the E of `ARE`
   became R, and `GREEN`'s became R and X. Different shifts.)* This is
   called the **Vigenère cipher**, and for 300 years people called it
   unbreakable.

6. **Does counting still work?**
   ```
   >>> secret = open("../secrets/message3.txt").read()
   >>> Counter(letter for letter in secret if letter.isalpha()).most_common(5)
   [('O', 8), ('T', 8), ('H', 7), ('I', 6), ('V', 6)]
   ```
   **Say:** "No letter stands out any more. The Es have been spread over
   six different letters." Try `crack.py` on it: **they should see**
   gibberish, whatever the key.

7. **How many keys?** **Ask:** "With a 6-letter key word, each letter
   has 26 choices. How many keys?" *(26⁶ = 308,915,776.)* "A 20-letter
   key of random letters?"
   ```
   >>> 26 ** 20
   19928148895209409152340197376
   ```
   **Say:** "Too many to try, even for a computer. But people don't
   choose random letters. They choose words they can remember. What
   word would a Minecraft fan choose?"

8. **A dictionary attack.** Make `keys.txt`, with Minecraft words, as
   many as they can think of. Start with these:
   ```
   CREEPER ZOMBIE SKELETON SPIDER ENDERMAN WITCH
   OCELOT WOLF HORSE LLAMA AXOLOTL PARROT
   DIAMOND EMERALD REDSTONE OBSIDIAN TORCH PICKAXE
   ```
   In `wordlock.py`, replace the last three lines with:
   ```python
   secret = open(sys.argv[1]).read()
   best_word = ""
   best_score = 0
   for word in open("keys.txt").read().split():
       attempt = keyword(secret, word, -1)
       print(f"{word:10} {score(attempt):3}  {attempt.splitlines()[0][:45]}")
       if score(attempt) > best_score:
           best_word = word
           best_score = score(attempt)
   print(f"The key word is probably {best_word}:")
   print(keyword(secret, best_word, -1))
   ```
   ```
   python3 wordlock.py ../secrets/message3.txt
   ```
   **They should see** a line for each word, then:
   ```
   The key word is probably OCELOT:
   THE SECRET DIAMOND STASH IS UNDER THE THIRD SPRUCE TREE NORTH OF THE
   VILLAGE WELL. DIG DOWN SEVEN BLOCKS AND WATCH OUT FOR LAVA.
   ```
   **Say:** "That's a **dictionary attack**: instead of every possible
   key, try the ones people actually choose. The cipher wasn't broken.
   The *key* was guessable." Commit.

9. **What real ciphers do.** **Say:** "Today's ciphers, like the one `ssh`
   used in Lesson 11.4, mix the letters up so thoroughly that no
   counting works, and use keys made by `secrets`, not by people. Their
   key space is 2¹²⁸ or bigger."
   ```
   >>> 2 ** 128
   340282366920938463463374607431768211456
   ```
   **Ask:** "Could brute force try them all?" *(If every computer on
   Earth tried a billion keys a second since the dinosaurs, they still
   wouldn't be close.)*

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `IndexError: list index out of range` at `sys.argv[1]` | No file name after the program's name | `python3 crack.py ../secrets/message1.txt`. |
| `FileNotFoundError: ... '../secrets/message1.txt'` | Running from the wrong folder, or no secrets | `cd ~/lab/net/python`. If `~/lab/net/secrets` is missing, the guide runs `give-lab.sh LEARNER net`. |
| `FileNotFoundError: ... 'keys.txt'` | `keys.txt` isn't in this folder | Make it in `~/lab/net/python`. |
| The best key gives gibberish | A very short message, or a typing mistake in `COMMON` | Check `COMMON`; look at all the lines yourself. |
| `ImportError: cannot import name ... from 'keyword'` (or another strange import error) | A file in this folder has the same name as a part of Python (like `keyword.py` or `random.py`) | Rename your file, and delete the `__pycache__` folder. |
| `ValueError: substring not found` in `keyword` | The key word has lower-case letters | Key words in capitals. |

## Talk about it

- What's brute force? Why did it work on Caesar?
- What's frequency analysis? Who first described it?
- Why doesn't counting letters crack the keyword cipher?
- How did we crack it anyway? Whose mistake was it: the cipher's, or
  the person's?

## Challenge *(if there's time, or for next time)*

- Make your own keyword message for the guide, with a word that's *not*
  in `keys.txt`, and a long one. Can the guide crack it?
- Make `crack.py` work with lower-case messages too (`.upper()`).
- For a keyword of known length, every 6th letter is a plain Caesar
  cipher. Split `message3.txt`'s letters into six piles and count each
  pile. *(That's how Charles Babbage and Friedrich Kasiski broke
  Vigenère in the 1800s.)*

## Checkpoint

The learner can, without help:
- [ ] Crack a Caesar message with brute force, and explain the score
- [ ] Use frequency analysis to find a Caesar key by hand
- [ ] Explain the keyword cipher, and why counting fails on it
- [ ] Explain a dictionary attack, and why it's the key's fault

## Lab notebook

Write the three cracked messages and their keys. Draw the letter counts
of message 2 as a bar chart, with the X bar the tallest. Write 26, 26⁶
and 2¹²⁸, and what each one means. Commit. Add *brute force*, *key
space*, *frequency analysis*, *keyword cipher* and *dictionary attack*
to `dictionary.md`.

## Guide's background *(optional reading)*

The two classic attacks on ciphers are both here: **brute force**
(try every key, which only works when there are few) and **frequency
analysis** (use the patterns of the language, which only works when the
cipher leaves them in place). Al-Kindi's *Manuscript on Deciphering
Cryptographic Messages* (9th century) is the oldest known description
of frequency analysis. The Vigenère cipher (1500s) defeats simple
frequency analysis; it was broken in the 1800s by first finding the
key's length (Kasiski's method), after which each position is just a
Caesar cipher (the third challenge).

The **dictionary attack** is the important modern lesson: real
cryptography is rarely broken by beating the maths; it's broken by
guessable keys and passwords. Lesson 11.11 applies this to passwords.
Modern ciphers like AES are designed so that the ciphertext shows no
patterns at all, and their keys come from a secure random generator
(Lesson 11.8).

Python looks for modules in the program's own folder first, so a file
named like a standard module (`keyword.py`, `random.py`, `secrets.py`)
hides the real one and breaks other parts of Python that use it. That's
why the file here is `wordlock.py`.
