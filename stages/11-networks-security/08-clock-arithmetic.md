# Lesson 11.8: Clock Arithmetic, and Random Numbers That Aren't

**Time:** 3 sessions of 45 min · **You need:** a clock face (a real one,
or drawn: 12 numbers in a circle); a paper alphabet wheel (the cipher
wheel from Lesson 0.10, if you still have it); a terminal; a text
editor; `~/lab/net/python` · **New words:** modular arithmetic, `mod`,
remainder, inverse, seed, pseudo-random, predictable, `secrets`

## Goal *(read this to the learner)*

> All of cryptography, the maths of secrets, is built on one strange
> kind of arithmetic: the kind clocks do, where 9 + 5 = 2. You'll
> learn it, use it to rebuild your Caesar cipher in one line, find a
> multiplying cipher that works and one that doesn't, and then use it
> to crack the "random" secret codes of a vault, by predicting the
> future.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] A clock face, and an alphabet wheel (A to Z in a circle, numbered
      0 to 25: A is 0, B is 1, ... Z is 25).
- [ ] For Session 3, you'll run a program the learner doesn't see the
      output of: either turn the screen away, or run it in your own
      account.

## Warm-up (5 min)

"It's 9 o'clock. What time will it be in 5 hours?" *(2 o'clock.)* "But 9
+ 5 is 14!" *(Clocks go round: after 12, they start again.)* "In 24
hours?" *(9 again!)*

## Activity

### Session 1: clock arithmetic

1. **Mod.** **Say:** "When you count round a clock, you only care about
   the **remainder** after taking away whole circles. 14 hours is one
   circle of 12, and 2 left over. Mathematicians write 14 mod 12 = 2.
   That's **modular arithmetic**, or clock arithmetic." Practise on the
   clock face: 15 mod 12, 24 mod 12, 25 mod 12. *(3, 0, 1.)* **Ask:**
   "What's 17 mod 5?" *(17 = 3 × 5 + 2, so 2.)*

2. **Mod in Python.** `%` is mod:
   ```
   python3
   ```
   ```
   >>> (9 + 5) % 12
   2
   >>> 14 % 12
   2
   >>> divmod(17, 5)
   (3, 2)
   >>> 29 % 26
   3
   >>> -2 % 26
   24
   ```
   **Say:** "`divmod` gives both: how many whole times, and the
   remainder. And going backwards round the clock works too: two steps
   back from 0 is 24, on a 26-clock." **Ask:** "Why 26?" *(The letters!)*

3. **The Caesar cipher is clock arithmetic.** Use the alphabet wheel.
   **Say:** "Caesar with key 3 moves every letter 3 forward, and Z comes
   round to C. That's +3 mod 26!" Make `clock.py` in `~/lab/net/python`:
   ```python
   ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


   def shift(message, key):
       out = ""
       for letter in message:
           if letter in ALPHABET:
               number = ALPHABET.index(letter)
               out += ALPHABET[(number + key) % 26]
           else:
               out += letter
       return out


   secret = shift("ZOMBIES ATTACK AT DAWN", 3)
   print(secret)
   print(shift(secret, -3))
   ```
   `python3 clock.py`. **They should see:**
   ```
   CRPELHV DWWDFN DW GDZQ
   ZOMBIES ATTACK AT DAWN
   ```
   **Ask:** "How did the Z become a C?" *(Z is 25. 25 + 3 = 28, and 28 mod
   26 = 2, which is C.)* "And how does −3 undo it?" *(It goes back round
   the clock.)* Commit.

### Session 2: multiplying round the clock

4. **A times cipher.** **Say:** "What if, instead of adding the key, we
   *multiply* by it?" Add to `clock.py`:
   ```python
   def times(message, key):
       out = ""
       for letter in message:
           if letter in ALPHABET:
               number = ALPHABET.index(letter)
               out += ALPHABET[(number * key) % 26]
           else:
               out += letter
       return out


   print(times("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 3))
   print(times("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 2))
   ```
   **They should see**, as the last two lines:
   ```
   ADGJMPSVYBEHKNQTWZCFILORUX
   ACEGIKMOQSUWYACEGIKMOQSUWY
   ```
   **Ask:** "Look at times 3. Does every letter turn into a different
   one?" *(Yes: all 26 are there, mixed up.)* "Now times 2?" *(Only half
   the letters! A and N both turn into A; B and O both into C.)* "Could
   you decode a times-2 message?" *(No: an A could have been A or N.)*

5. **Why?** **Say:** "Times 2 only ever lands on even numbers, and 26 is
   even, so it never reaches the odd ones. 2 and 26 share a factor:
   2. Times 3 works because 3 and 26 share no factor." **Ask:** "Which
   keys from 1 to 12 work?" Try them: `times("ABC...Z", 13)` and so on.
   *(The odd ones: 1, 3, 5, 7, 9 and 11. 26 = 2 × 13, so any key with a
   factor of 2 or 13 fails: all the even keys, and 13 itself.)* This is the prime factors from
   Lesson 3.6 at work.

6. **Undoing a multiply.** **Ask:** "To undo times 3, normal maths would
   divide by 3. But 7 ÷ 3 isn't a whole number. What could we do?"
   **Say:** "Find a number that multiplies with 3 to make 1, round the
   clock." Try them: 3 × 9 = 27, and 27 mod 26 = 1! So times 9 undoes
   times 3. In Python:
   ```
   >>> pow(3, -1, 26)
   9
   >>> pow(2, -1, 26)
   ValueError: base is not invertible for the given modulus
   ```
   **Say:** "9 is the **inverse** of 3, mod 26. 2 hasn't got one, which is
   why times 2 can't be undone." Add `print(times(times("ZOMBIES", 3),
   9))` to `clock.py`, and run it. *(`ZOMBIES` comes back.)* Commit.

### Session 3: random numbers that aren't

7. **Remember Redstone OS.** **Say:** "In Lesson 10.14, Creeper Chase put
   diamonds in 'random' places. How did it pick?" *(It multiplied the
   seed by a huge number, added another, and the new seed made the next
   number.)* **Say:** "And the wrapping round was mod 2⁶⁴: clock
   arithmetic, on a gigantic clock. It *looks* random. But is it?"

8. **Same seed, same "random".**
   ```
   python3 -c "import random; random.seed(7); print([random.randint(1, 6) for _ in range(5)])"
   ```
   Run it twice. **They should see** the same five dice both times:
   ```
   [3, 2, 4, 6, 1]
   [3, 2, 4, 6, 1]
   ```
   **Say:** "Python's `random` is a recipe too. Same seed, same numbers,
   every time. That's called **pseudo-random**. Great for games: you can
   replay the same level. Terrible for secrets."

9. **The vault's codes.** Make `codes.py`:
   ```python
   # The vault's secret codes for the next three days, made with
   # Redstone OS's random number recipe, seeded with the clock.
   import time

   seed = int(time.time())


   def random(top):
       global seed
       seed = (seed * 6364136223846793005 + 1442695040888963407) % 2**64
       return (seed >> 33) % top


   for day in ["Today", "Tomorrow", "The day after"]:
       print(f"{day}'s code: {random(10000):04}")
   ```
   **Say:** "`time.time()` is the number of seconds since 1970. The
   vault uses it as the seed, makes three 4-digit codes, and you're only
   told today's." The **guide** runs it, where the learner can't see,
   and reads out only the first line, for example:
   ```
   Today's code: 5554
   Tomorrow's code: 4090
   The day after's code: 2167
   ```
   *(Write the other two down secretly.)*

10. **Predict the future.** **Say:** "You know the recipe: everyone can
    read the code. You know today's code. And you know the vault made its
    codes some time in the last hour. How many seeds is that?" *(3,600:
    one for every second.)* "A computer can try 3,600 seeds in no time."
    Make `predict.py`:
    ```python
    # Work out the vault's next codes from today's, by trying every
    # seed (every second) in the last hour.
    import time


    def codes_from(seed):
        codes = []
        for day in range(3):
            seed = (seed * 6364136223846793005 + 1442695040888963407) % 2**64
            codes.append((seed >> 33) % 10000)
        return codes


    today = int(input("Today's code? "))
    now = int(time.time())
    for seed in range(now - 3600, now + 1):
        codes = codes_from(seed)
        if codes[0] == today:
            print(f"The seed could be {seed}: then the next codes are {codes[1]:04} and {codes[2]:04}.")
    ```
    `python3 predict.py`, and type today's code. **They should see**
    something like:
    ```
    Today's code? 5554
    The seed could be 1792850355: then the next codes are 4090 and 2167.
    ```
    The guide reveals the secret two. **Ask:** "How did you know the
    future?" *(The seed was the time, which isn't secret, and the recipe
    isn't secret either.)* (Once in a while, two seeds fit; then there
    are two guesses, and one is right.)

11. **The fix.** **Say:** "For secrets, the seed must be something nobody
    could guess. Linux collects tiny, unpredictable timings from the
    hardware (key presses, disk and network timing) and mixes them up.
    Python's `secrets` module uses that."
    ```
    python3 -c "import secrets; print([secrets.randbelow(6) + 1 for _ in range(5)])"
    ```
    Run it twice. **They should see** different dice each time, like
    `[5, 6, 2, 1, 6]` and `[4, 5, 1, 1, 4]`, and there's no seed to
    find. Change `codes.py` to use `secrets.randbelow(10000)` (and
    `import secrets`). **Ask:** "Can `predict.py` crack it now?" *(No.)*
    Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NameError: name 'times' is not defined` | `times` is used before it's defined, or not saved | Put the `def` above the `print` lines. |
| `ValueError: base is not invertible for the given modulus` | That number has no inverse mod 26 | That's step 6's point: choose 3, 5, 7, 9, 11... |
| `predict.py` prints nothing | The code was mistyped, or it was made more than an hour ago | Check the code; run `codes.py` again. |
| `codes.py` gives the same codes twice | It ran twice in the same second: the same seed! | That's the problem, shown. Wait a second. |
| `ValueError: invalid literal for int()` | Something other than digits was typed | Type just the four digits. |

## Talk about it

- What's 20 mod 12? What's mod for, in clocks and in ciphers?
- Why does a times-2 cipher break, and a times-3 one work?
- What's an inverse? What's the inverse of 3, mod 26?
- How did `predict.py` see the future? What made it possible?
- When is pseudo-random fine, and when isn't it?

## Challenge *(if there's time, or for next time)*

- Find the inverses of 5, 7 and 11 mod 26, by hand, then check with
  `pow`.
- An **affine** cipher multiplies, then adds: `(number * 5 + 8) % 26`.
  Write it, and its decoder.
- Make `predict.py` work if the vault was made any time *today*. How
  many seeds is that? *(86,400.)* Is it still quick?

## Checkpoint

The learner can, without help:
- [ ] Work out a mod by hand and with `%`
- [ ] Explain the Caesar cipher as `(number + key) % 26`
- [ ] Explain why some multiplying keys can't be undone, and find an
      inverse
- [ ] Explain why a time-seeded "random" code can be predicted, and
      what to use instead

## Lab notebook

Draw the 26-clock with the letters on it. Write 3 × 9 = 27 = 1 (mod 26).
Write how `predict.py` worked, and the rule: *secrets need real
randomness*. Commit. Add *modular arithmetic*, *mod*, *remainder*,
*inverse*, *pseudo-random* and *seed* to `dictionary.md`.

## Guide's background *(optional reading)*

Modular arithmetic is the arithmetic of remainders; mathematicians
write 14 ≡ 2 (mod 12). Addition, subtraction and multiplication all work
"round the clock", but division is only possible by numbers that share
no factor with the modulus: those have an **inverse**. That fact is the
basis of RSA (Lesson 11.13), which works mod a huge number. The MATH
TRACK's Stage 11 row (modular arithmetic and primes) is this lesson.
*Mathematics for Computer Science* (in the offline library), Chapter 9,
covers it properly, for later.

A **linear congruential generator** (Redstone OS's recipe) is fast and
fine for games, but anyone who knows a little of its output can work
out the rest. Seeding with the time makes it worse: the attacker only
has to try every plausible second. This exact mistake has broken real
systems, including an early web browser's encryption and some online
card games' shuffles. Real secrets use a **cryptographically secure**
generator, seeded from the operating system's collected randomness
(`/dev/urandom` and the `getrandom` system call on Linux; Python's
`secrets`). The Hacker's Pledge applies here too: we predicted our
*own* vault's codes.
