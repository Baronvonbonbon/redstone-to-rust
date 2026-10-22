# Lesson 3.9: Secret Code Machine

**Time:** 2 sessions of 45 min · **You need:** Thonny; the Caesar cipher
wheel from Lesson 0.10 · **New words:** encode, decode, key, brute force,
frequency

## Goal *(read this to the learner)*

> Remember the cipher wheel from Stage 0, and ROT13 in the Mineshaft?
> Today you'll build your own code machine in Python. It will scramble any
> message with any key, unscramble it again, and then (the really sneaky
> part) **crack** a message when you *don't* know the key.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Find the cipher wheel from Lesson 0.10, or make a quick new one.
- [ ] Write a secret message for Session 2 (see step 7). You can encode it
      with the terminal: `echo "your message here" | caesar 11`. Pick
      any key from 1 to 25 and don't tell the learner. Make the message at
      least two sentences long.

## Warm-up (5 min)

Using the wheel, encode `cat` with key 3. *(fdw.)* "What did you do for
each letter?" *(Found it, moved 3 along, wrote the new letter.)* "What
happens to `x`, `y` and `z`?" *(They wrap round to `a`, `b`, `c`.)* That
wrapping round is the key to the code.

## Activity

### Session 1: the machine

1. **Letters as numbers.** In the Shell:
   ```python
   ALPHABET = "abcdefghijklmnopqrstuvwxyz"
   ALPHABET.index("a")
   ALPHABET.index("d")
   ALPHABET[3]
   ```
   *(0, 3, `'d'`.)* **Say:** "`index` finds where a letter is. Square
   brackets go the other way: from a number to a letter."

2. **Wrapping round with `%`.**
   ```python
   ALPHABET.index("y") + 3
   (ALPHABET.index("y") + 3) % 26
   ALPHABET[(ALPHABET.index("y") + 3) % 26]
   ```
   *(27, 1, `'b'`.)* **Say:** "There are only 26 letters, numbered 0 to 25.
   `% 26` is the remainder after dividing by 26, which wraps any number
   back round into 0 to 25. It's exactly what the wheel does, like a clock
   going from 12 back to 1."

3. **The code machine.** New file, `~/lab/python/stage3/cipher.py`:
   ```python
   ALPHABET = "abcdefghijklmnopqrstuvwxyz"

   def shift_letter(letter, key):
       if letter not in ALPHABET:
           return letter
       position = ALPHABET.index(letter)
       return ALPHABET[(position + key) % 26]

   def encode(message, key):
       secret = ""
       for letter in message.lower():
           secret += shift_letter(letter, key)
       return secret

   def decode(secret, key):
       return encode(secret, -key)

   assert encode("cat", 3) == "fdw"
   assert encode("xyz", 3) == "abc"
   assert encode("hello, world!", 1) == "ifmmp, xpsme!"
   assert decode("fdw", 3) == "cat"
   print("All tests passed!")
   ```
   **Say:** "Letters that aren't in the alphabet, like spaces and
   punctuation, go through unchanged. And look at `decode`: to undo a
   shift of 3, shift by -3! Python's `%` even wraps negative numbers
   correctly: `-1 % 26` is 25."

4. **ROT13, again.** In the Shell, after running the file:
   ```python
   encode("hello", 13)
   encode(encode("hello", 13), 13)
   ```
   **Say:** "ROT13 is a Caesar shift of 13, the one from Mineshaft level
   10. Shifting by 13 twice is 26, the whole way round, so the same key
   both scrambles and unscrambles."

   Compare in the terminal: `echo hello | rot13`.

5. **Make it usable.** Add to the bottom of `cipher.py`:
   ```python
   while True:
       choice = input("e to encode, d to decode, q to quit: ").lower()
       if choice == "q":
           break
       if choice not in ["e", "d"]:
           continue
       message = input("Message: ")
       key = int(input("Key (1 to 25): "))
       if choice == "e":
           print("Secret:", encode(message, key))
       else:
           print("Message:", decode(message, key))
   ```
   Send each other secret messages, with the key written on a slip of paper.

### Session 2: cracking

6. **Brute force.** **Say:** "If someone steals a secret message but
   doesn't know the key, how could they read it?" Let them think. *(Try
   every key! There are only 25.)* New file, `crack.py`, with
   `ALPHABET`, `shift_letter`, `encode` and `decode` copied in, then:
   ```python
   secret = input("Secret message to crack: ")
   for key in range(1, 26):
       print(f"{key:2}: {decode(secret, key)}")
   ```
   **Say:** "`{key:2}` makes the number take up 2 spaces, so everything
   lines up." Test it on one of their own messages.

7. **Crack the guide's message.** Give them the secret message you made
   before the lesson. They run `crack.py`, paste it in, and look down the
   25 lines for the one that's English.

   **Say:** "That's called a **brute-force** attack: trying every possible
   key. It works because the Caesar cipher only has 25 keys. Real codes
   have so many keys that trying them all would take longer than the age of
   the universe."

8. **Can the computer spot English?** In the terminal:
   ```
   echo "khoor zruog" | caesar
   echo "the quick brown fox jumps over the lazy dog and meets me at the treehouse" | caesar 11 | caesar
   ```
   The `caesar` command, given no key, tries to guess. **They should see:**
   it gets the short message *wrong* (`ebiil tloia`) but the long one right.

   **Say:** "It guesses by **frequency**: in English, `e` is the most
   common letter, then `t`, `a` and `o`. It picks the key that makes the
   message look most like English. With only 10 letters, there isn't enough
   to go on. With a long message, it works."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ValueError: substring not found` | `ALPHABET.index` was given something not in the alphabet, like a capital or a space | Check `if letter not in ALPHABET: return letter` comes first, and the message is `.lower()`ed. |
| `IndexError: string index out of range` | The `% 26` is missing | Use `ALPHABET[(position + key) % 26]`. |
| Decoding gives nonsense | Wrong key, or encoding again instead of decoding | Decode with the same key that was used to encode. |
| Only the first letter comes out | `return secret` is indented inside the loop | Line it up with the `for`. |
| `ValueError: invalid literal for int()` for the key | Typed a word for the key | Type a number from 1 to 25. |

## Talk about it

- How does `% 26` make the letters wrap round?
- Why is the Caesar cipher easy to crack? *(Only 25 keys to try, and the
  letter patterns of English still show through.)*
- Why did `caesar` guess the short message wrong?
- Is base64 (Mineshaft level 9) a code like this? *(No: base64 has no key
  at all. It's an encoding, not a cipher.)*

## Challenge *(if there's time, or for next time)*

- **Auto-crack:** write `english_score(text)` that counts how many of the
  letters are `e`, `t`, `a` or `o`. Make `crack.py` print only the key with
  the best score. Does it fail on short messages too?
- Keep capital letters as capitals. *(Hint: a second alphabet in capitals.)*
- **A stronger code:** use a different key for each letter, taken from a
  keyword. For keyword `cab`, shift the first letter by 2, the second by 0,
  the third by 1, then repeat. This is the **Vigenère cipher**, which was
  called "unbreakable" for 300 years. (Use `i % len(keyword)` to repeat
  the keyword, like the rainbow colours in Lesson 2.13.)

## Checkpoint

The learner can, without help:
- [ ] Explain how `% 26` wraps letters round
- [ ] Encode and decode messages with their program
- [ ] Crack a Caesar message by brute force
- [ ] Explain why short messages are harder to crack by frequency

## Lab notebook

Write a secret message in the notebook, encoded, with the key hidden
somewhere on the page. Write "brute force = try every key". Add *encode*,
*decode*, *key*, *brute force* and *frequency* to the dictionary.

## Guide's background *(optional reading)*

This lesson is part of the course's secret-code thread: the cipher wheel
(Stage 0), ROT13 and base64 in the terminal (Stages 1 and 5), letters as
numbers (Stage 4) and real cryptography (Stage 11). The two ways of
breaking a cipher here, **brute force** (try every key) and **frequency
analysis** (look for the patterns of the language), are the two classic
attacks. Frequency analysis was first described by the Arab scholar
al-Kindi in the 9th century.

Modern ciphers like AES have so many possible keys (2 to the power of 128
or more) that brute force is hopeless, and they mix the message up so
thoroughly that no letter patterns survive. That's what makes them safe.

A note for the Hacker's Pledge: cracking codes is a fun puzzle and a real
job, but we only crack messages that are meant for us, or that someone has
given us as a challenge.
