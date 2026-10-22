# Lesson 4.5: Letters Are Numbers

**Time:** 2 sessions of 45 min · **You need:** Thonny; a terminal;
the code machine from Lesson 3.9 (`~/lab/python/stage3/cipher.py`) ·
**New words:** ASCII, character, encoding, Unicode

## Goal *(read this to the learner)*

> A computer can only store numbers, so how does it store this sentence?
> Every letter has a secret number! Today you'll find the numbers for
> every letter, write messages in pure binary, peek at a text file's
> bytes, and discover why an emoji takes four times as much room as the
> letter A.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Write this on a card, for step 3:
      `01001000 01101001 00100001`

## Warm-up (5 min)

"In Stage 0, we made pictures out of numbers. In the last lesson, colours
were numbers. What do you think letters are?" *(Numbers too!)* "If you
were inventing the code, what number would you give A?"

## Activity

### Session 1: the letter code

1. **Every letter has a number.** In the Shell:
   ```python
   ord("A")
   ord("B")
   ord("a")
   ord(" ")
   ord("0")
   chr(72)
   chr(105)
   ```
   **They should see:** `65`, `66`, `97`, `32`, `48`, `'H'`, `'i'`.

   **Say:** "`ord` gives a letter's number, and `chr` gives the letter for
   a number. This code is called **ASCII**, and it was invented in the
   1960s. Even a space has a number (32), and so does the *digit* 0 (48),
   which isn't the same as the number 0!"

2. **The whole table.** New file, `~/lab/python/binary/ascii_table.py`:
   ```python
   for n in range(32, 127):
       print(n, chr(n), f"{n:08b}")
   ```
   **They should see:** 95 lines, from `32` (a space) to `126 ~`.

   Look for patterns:
   - The capitals are 65 to 90, in order. The small letters are 97 to 122.
   - **The magic gap.** Compare `65 A 01000001` and `97 a 01100001`.
     "What's different?" *(Just one bit! The capital and small letter are
     exactly 32 apart, and 32 is one bit.)* **Say:** "Flipping one bit
     changes a letter between capital and small. That's what `.upper()`
     does, deep down."
   - The digits `0` to `9` are 48 to 57. In binary, the last four bits of
     each digit are its value: `5` is `00110101`, and `0101` is 5.

3. **Decode by hand.** Give the learner the card:
   `01001000 01101001 00100001`. Each group of 8 bits is one byte, one
   character. They turn each byte into a number with the dot cards or the
   doubling trick, then find the letter in the table. *(72, 105, 33:
   `Hi!`)*

4. **A binary message machine.** New file,
   `~/lab/python/binary/secret_bits.py`:
   ```python
   def to_bits(message):
       groups = []
       for letter in message:
           groups.append(f"{ord(letter):08b}")
       return " ".join(groups)

   def from_bits(bits):
       message = ""
       for group in bits.split():
           message = message + chr(int(group, 2))
       return message

   assert to_bits("Hi!") == "01001000 01101001 00100001"
   assert from_bits(to_bits("Captain Underpants")) == "Captain Underpants"

   while True:
       choice = input("e to encode, d to decode, q to quit: ")
       if choice == "e":
           print(to_bits(input("Message: ")))
       elif choice == "d":
           print(from_bits(input("Bits: ")))
       elif choice == "q":
           break
   ```
   **They should see:** the menu. Encode their name, then copy and paste
   the bits back in to decode them. (In Thonny's Shell, select with the
   mouse, then right-click → Copy and right-click → Paste.)

   **Say:** "There's the round-trip test again: turn a message into bits
   and back, and you must get the same message."

### Session 2: inside text files

5. **A text file's bytes.** In the terminal:
   ```
   cd ~/lab/python/binary
   echo "Hi Sam" > hi.txt
   xxd hi.txt
   ```
   (Use the learner's own name.) **They should see:** something like
   `00000000: 4869 2053 616d 0a   Hi Sam.`

   **Say:** "`48` is hex for 72, which is H. `69` is i. `20` is the space.
   And look at the very end: `0a`. That's an invisible character, number
   10, called **newline**. It means 'start a new line'. Every line in a
   text file ends with one. The dot on the right is how `xxd` shows it."

   Try `xxd ~/lab/jokes.txt | head` (the jokes file from Stage 1) and find
   the `0a`s between the lines.

6. **Bigger than ASCII.** ASCII only has 128 characters: no accents, no
   other alphabets, no emoji. In the Shell:
   ```python
   ord("é")
   ord("🙂")
   "A".encode()
   "é".encode()
   "🙂".encode()
   len("🙂".encode())
   ```
   **They should see:** `233`, `128578`, `b'A'`, `b'\xc3\xa9'`,
   `b'\xf0\x9f\x99\x82'`, `4`.

   **Say:** "Today every character in every language, and every emoji, has
   a number. That big list is called **Unicode**. The smiley is number
   128,578, which is far too big for one byte, so it's stored as four
   bytes. The way characters are turned into bytes is called an
   **encoding**, and the one almost everything uses is called UTF-8.
   `.encode()` shows the bytes: `\x` means the next two characters are hex.
   An A is still just one byte, the same as ASCII."

   In the terminal: `echo -n "🙂" | xxd`. *(`f09f 9982`: the same four
   bytes.)*

7. **Upgrade the code machine.** Open `cipher.py` from Lesson 3.9.
   **Say:** "Your code machine found each letter's position
   with `ALPHABET.index(letter)`. Now you know a second way:
   `ord(letter) - ord("a")`. For `"d"` that's 100 − 97 = 3." Try it in
   the Shell. The learner can keep the old way: both work, and it's a
   good discussion about which is clearer.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `TypeError: ord() expected a character, but string of length 2 found` | `ord` was given more than one letter | `ord` takes exactly one character: `ord("A")`. |
| `ValueError: invalid literal for int() with base 2` when decoding | Something that isn't 0, 1 or a space was pasted in, maybe the `Bits:` prompt itself | Paste only the bits. |
| Decoding gives strange symbols | A group isn't exactly 8 bits, so everything after it is shifted | Check each group has 8 bits, with spaces between groups. |
| The emoji shows as a box | The font doesn't have that emoji | It's still the same bytes. Try a different emoji. |
| `xxd` shows `0a` where you didn't type anything | That's the newline `echo` adds | `echo -n` leaves it out. |

## Talk about it

- How does a computer store the word "creeper"? *(As seven numbers, one
  byte each.)*
- Why are capital and small letters exactly 32 apart?
- Why does an emoji need more than one byte?

## Challenge *(if there's time, or for next time)*

- Write `shout(message)` that turns small letters into capitals using only
  `ord`, `chr` and the number 32. Test it against `.upper()`.
- Add hex to the machine: `h` encodes to hex, like `48 69 21`.
- Hide a message for the family: print it in binary, and stick it on the
  fridge with an ASCII table.

## Checkpoint

The learner can, without help:
- [ ] Use `ord` and `chr`, and find a letter's number in binary
- [ ] Decode a short binary message by hand
- [ ] Explain what `0a` is in a hex dump
- [ ] Explain the difference between ASCII and Unicode in their own words

## Lab notebook

Write their name in binary. Copy the capitals A to Z with their numbers.
Write "A = 65, a = 97, space = 32, newline = 10". Add *ASCII*,
*character*, *newline*, *Unicode* and *encoding* to the dictionary.

## Guide's background *(optional reading)*

ASCII (American Standard Code for Information Interchange, 1963) gives
each of 128 characters a number from 0 to 127: control characters (like
newline, 10, and tab, 9), punctuation, digits, and the English alphabet.
It was cleverly arranged: letters are in order so sorting works, and
capitals differ from small letters by exactly one bit.

Unicode extends the idea to every writing system, with over 150,000
characters so far. UTF-8 stores each one as 1 to 4 bytes, and it's
backwards compatible: plain ASCII text is already valid UTF-8, byte for
byte. Python 3 strings are Unicode, and `.encode()` turns them into
UTF-8 bytes. A lot of "weird character" bugs in real software (like `Ã©`
instead of `é`) come from bytes being read with the wrong encoding.

The letter-to-number idea is the backbone of the secret-code thread: the
Caesar cipher is just arithmetic on letter numbers, and the real
cryptography in Stage 11 is arithmetic on very big numbers made from
bytes.
