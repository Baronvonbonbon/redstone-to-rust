# Lesson 11.12: A Secret in Front of Everyone

**Time:** 2 sessions of 45 min · **You need:** a terminal; `~/lab/net/python`;
3 clear cups of water, yellow, red and blue food colouring (or paints
and a palette), a spoon; paper · **New words:** key exchange,
eavesdropper, public, private, AES, man in the middle

## Goal *(read this to the learner)*

> To use a secret code, both people need the same key. But how do you
> agree on a key when anyone could be listening, like `tcpdump` in
> Lesson 11.4? It sounds impossible. Today you'll do it with paint,
> then with clock arithmetic, then use your shared secret to lock a
> file with a real, uncrackable cipher.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once. The mathematics is the clock
      arithmetic from Lesson 11.8, plus powers (Stage 4).
- [ ] Practise step 1 once, so you know how much colouring to use. Put
      newspaper down!

## Warm-up (5 min)

"In Lesson 11.9, both people needed the keyword `OCELOT`. How would you
tell your friend the keyword, if every message you send is read by a
spy?" *(You can't send it! You could meet in person. But what if your
friend is on the other side of the world?)* **Say:** "Every time you
visit an `https` website, your computer has this exact problem with a
computer it's never met. And it solves it in a fraction of a second."

## Activity

### Session 1: mixing secrets

1. **The paint trick.** Three people: Alex (the learner), Steve (the
   guide), and the spy (a toy, or a sibling who watches everything).
   - Everyone agrees, out loud, on a **public** colour: yellow. The spy
     knows it too.
   - Alex secretly chooses red, and Steve secretly chooses blue. These
     are **private**: never shown to anyone.
   - Each mixes their secret colour into a cup of yellow, and gives that
     cup to the other, in front of the spy. *(Alex's cup is orange,
     Steve's green.)*
   - Each adds their own secret colour to the cup they *received*. Alex
     adds red to the green; Steve adds blue to the orange.
   - Compare: **they should see** the same brownish colour in both cups.

   **Ask:** "The spy saw yellow, orange and green. Can they make the
   brown?" *(They'd need to un-mix the red out of the orange, and you
   can't un-mix paint. If they mix orange and green, they get too much
   yellow, and a different colour.)* **Say:** "Mixing is easy; un-mixing
   is impossible. That's the whole trick. It's called a **key
   exchange**."

2. **Un-mixable numbers.** **Say:** "Computers can't mix paint. They use
   clock arithmetic, on a clock with 23 numbers." Make a table on paper,
   starting with 1: multiply by 5, and keep the remainder after dividing
   by 23. Do the first few together:
   ```
   power:   1   2   3   4   5   6   7   8
   number:  5   2  10   4  20   8  17  16
   ```
   *(5; 5 × 5 = 25, and 25 − 23 = 2; 2 × 5 = 10; 10 × 5 = 50, and
   50 − 46 = 4; and so on.)* **Say:** "This is 5 to the power of 6, on a
   23 clock: `pow(5, 6, 23)` in Python. Going forwards is easy. But if I
   tell you a number, say 16, finding which power made it means going
   along the table until you find it. The numbers jump about with no
   pattern." Check a few in Python:
   ```
   python3 -c 'print(pow(5, 6, 23), pow(5, 8, 23))'
   ```
   **They should see:** `8 16`.

3. **The key exchange in Python.** In `~/lab/net/python`, make `dh.py`:
   ```python
   # Alex and Steve agree on a secret number, while everyone listens.
   p = 23  # the clock size: everyone knows it
   g = 5   # the starting number: everyone knows it

   alex_secret = 6     # Alex never tells anyone this
   steve_secret = 15   # Steve never tells anyone this

   alex_sends = pow(g, alex_secret, p)
   steve_sends = pow(g, steve_secret, p)
   print(f"Everyone hears: p={p}, g={g}, Alex sends {alex_sends}, Steve sends {steve_sends}")

   alex_key = pow(steve_sends, alex_secret, p)
   steve_key = pow(alex_sends, steve_secret, p)
   print(f"Alex works out {alex_key}. Steve works out {steve_key}.")
   ```
   `python3 dh.py`. **They should see:**
   ```
   Everyone hears: p=23, g=5, Alex sends 8, Steve sends 19
   Alex works out 2. Steve works out 2.
   ```
   Match it to the paint: `g` is the yellow, the secrets are red and
   blue, `alex_sends` and `steve_sends` are the cups that were passed
   over, and the key is the brown. **Say:** "Steve's 19 is 5 multiplied
   by itself 15 times. Alex multiplies *that* by itself 6 times. That's
   5 multiplied 15 × 6 = 90 times. Steve does the same the other way
   round: 6 × 15 = 90 times. Same answer!"

4. **Be the spy.** **Say:** "The spy heard 23, 5, 8 and 19. With such a
   small clock, they can just try every power." Make `spy.py`:
   ```python
   # The spy heard everything. Can they find Alex's secret?
   p = 23
   g = 5
   alex_sends = 8
   steve_sends = 19

   for guess in range(1, p):
       if pow(g, guess, p) == alex_sends:
           print(f"Alex's secret must be {guess}")
           print(f"So the key is {pow(steve_sends, guess, p)}")
           break
   ```
   `python3 spy.py`. **They should see:**
   ```
   Alex's secret must be 6
   So the key is 2
   ```
   **Ask:** "How many tries did the spy need, at most?" *(22.)* "So how
   do we beat the spy?" *(A much bigger clock, just like a longer
   passphrase in Lesson 11.11.)* Commit.

### Session 2: big numbers and real locks

5. **A huge clock.** Copy `dh.py` to `dh2.py`, and change the top to:
   ```python
   # Alex and Steve agree on a secret number, while everyone listens.
   import secrets

   p = 2**127 - 1  # a prime with 39 digits
   g = 3

   alex_secret = secrets.randbelow(p)
   steve_secret = secrets.randbelow(p)
   ```
   (the rest stays the same). `python3 dh2.py`. **They should see** two
   enormous numbers that everyone hears, then the same 38- or 39-digit
   number twice, like:
   ```
   Alex works out 30587687124244683345987467721133527297. Steve works out 30587687124244683345987467721133527297.
   ```
   Different every time. **Ask:** "How many tries would `spy.py` need
   now?" *(Up to a 39-digit number of them: counting a billion a second,
   far longer than the universe has existed.)* **Say:** "Python's `pow` is quick even for numbers this
   big, because it uses a clever shortcut, but there's no known shortcut
   for going backwards. Real computers use clocks with over 600 digits,
   or a newer kind of maths with curves." *(`2**127 - 1` is a prime:
   Lesson 3.6's prime hunters would take a while to check it!)*

6. **Lock a file.** **Say:** "Now Alex and Steve share a secret number.
   They use it as the key for a real cipher, called **AES**. It's like
   the keyword cipher, but nobody has found a way to break it." On the
   family computer, in `~/lab/net/python`, using the small key `2` from
   step 3 as the passphrase:
   ```
   echo "Meet at the treehouse at 4." > note.txt
   openssl enc -aes-256-cbc -pbkdf2 -in note.txt -out note.enc -pass pass:2
   xxd note.enc
   ```
   **They should see** 48 bytes of nonsense, starting with `Salted__`:
   ```
   00000000: 5361 6c74 6564 5f5f f472 ab6c 6323 7a2a  Salted__.r.lc#z*
   00000010: 08f5 7f84 1b17 63ab ad87 4f6a f63b 1674  ......c...Oj.;.t
   00000020: bd3c 8cad 06e8 9202 d5e9 f218 a6d2 d1ea  .<..............
   ```
   (yours will be different nonsense: there's a random part, the salt,
   so locking the same file twice looks different). Unlock it:
   ```
   openssl enc -d -aes-256-cbc -pbkdf2 -in note.enc -pass pass:2
   ```
   **They should see:** `Meet at the treehouse at 4.` Then with the
   wrong key, `pass:3`. **They should see** `bad decrypt`, an error
   line, and some garbage. **Say:** "A key of `2` is far too easy to
   guess, of course. With the big number from step 5 as the key, nobody
   could open it." Try that: lock it with `-pass pass:` followed by the
   big number, and unlock it again.

7. **The spy in the middle.** Back to the paint, but now the spy sits
   *between* Alex and Steve, and every cup has to be passed through
   them. **Ask:** "What could a sneaky spy do?" Act it out: the spy
   keeps Alex's cup, and gives Steve a cup made with the *spy's own*
   secret colour instead; and does the same the other way. *(Now Alex
   shares a secret with the spy, and so does Steve, and they each think
   they're talking to each other. The spy can read everything, and
   pass it on.)* **Say:** "That's called a **man in the middle**. The
   key exchange keeps out people who only listen, but it can't tell you
   *who* you're talking to. For that, you need something only Steve can
   make, that anyone can check. That's next lesson: signatures."

8. **It's already happening.** **Ask:** "In Lesson 11.4, `tcpdump` saw
   `ssh` say its version, and then nothing readable. Why?" *(Right after
   saying hello, the two computers did a key exchange, like `dh.py`, and
   locked everything after that with the shared key.)* **Say:** "Every
   `ssh` login and every `https` page starts with exactly this."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Alex and Steve work out different keys | A mix-up: each must use *their own* secret with the *other's* number | Check `pow(steve_sends, alex_secret, p)`. |
| `TypeError: pow() 3rd argument not allowed unless all arguments are integers` | A number has a `.` in it, like `5.0` | Use whole numbers only. |
| `NameError: name 'secrets' is not defined` | `import secrets` is missing in `dh2.py` | Add it at the top. |
| `bad decrypt` with the right key | The `-pass` was typed differently, or `-pbkdf2` was missing on one side | Use exactly the same options to lock and unlock. |
| The wrong key gives garbage *without* `bad decrypt` | It happens about 1 time in 256 | It's still garbage, so it's still safe. |
| The paint is all brown | Too much colouring | Use one drop of each secret colour. |

## Talk about it

- How can two people agree on a secret when a spy hears everything they
  say?
- Why is `pow` on a clock like mixing paint?
- Why did the spy win with 23 but not with `2**127 - 1`?
- What's a man in the middle? Why doesn't the key exchange stop one?

## Challenge *(if there's time, or for next time)*

- Finish the table from step 2, all 22 powers. Does every number from
  1 to 22 appear exactly once? *(Yes! That's why 5 is a good `g` for 23.
  Try 2: which numbers are missing?)*
- Three friends: can Alex, Steve and Sunny all end up with one shared
  key? *(Hint: pass the numbers round twice.)*
- Use the key from `dh.py` as a Caesar key for `clock.py`'s `shift`
  from Lesson 11.8. Why is that a bad idea? *(Only 26 Caesar keys:
  the spy doesn't even need the key exchange.)*

## Checkpoint

The learner can, without help:
- [ ] Explain the paint key exchange: public, private, mix, swap, mix
- [ ] Run `dh.py`, and explain why both keys are the same
- [ ] Explain why the spy wins on a small clock and loses on a huge one
- [ ] Lock and unlock a file with `openssl enc`
- [ ] Explain what a man in the middle can do

## Lab notebook

Draw the paint exchange, with the spy watching, and the numbers from
`dh.py` next to each cup. Draw the man in the middle. Commit. Add *key
exchange*, *public*, *private*, *eavesdropper*, *AES* and *man in the
middle* to `dictionary.md`.

## Guide's background *(optional reading)*

This is the **Diffie–Hellman key exchange**, published by Whitfield
Diffie and Martin Hellman in 1976 (and found earlier, in secret, at the
UK's GCHQ). Its security rests on the **discrete logarithm problem**:
given `g`, `p` and `pow(g, x, p)`, finding `x` is believed to be
impossibly slow for large well-chosen `p`. The numbers in step 3 are the
standard textbook example. The paint analogy is also standard; real
paint can't quite be un-mixed, which is the point.

Real systems use 2048-bit or larger primes, or (now more often)
**elliptic-curve** Diffie–Hellman, such as X25519, which gets the same
security from much smaller numbers. `ssh` and TLS (https) both begin
with one. `2**127 - 1` is a Mersenne prime, fine for a demonstration
but not a recommended choice for real use. Python's three-argument
`pow` uses **square-and-multiply**, which needs about 2 × 127
multiplications for these numbers instead of billions.

**AES** (the Advanced Encryption Standard, 2001) is the cipher that does
the actual locking almost everywhere. `openssl enc` with `-pbkdf2` turns
the passphrase into a 256-bit key with a deliberately slow fingerprint
and a random salt (the `Salted__` header). It's fine for learning; for
real file encryption, tools like `age` or `gpg` are better designed.
The man-in-the-middle problem is solved with authentication (Lesson
11.13), and *Computer Networks: A Systems Approach*, Sections 8.2–8.3,
covers both.
