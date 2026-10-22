# Lesson 4.4: Hex, Binary's Shorthand

**Time:** 2 sessions of 40 min · **You need:** Thonny; a terminal;
`miner.png` from Lesson 3.13 · **New words:** hexadecimal, hex digit,
nibble

## Goal *(read this to the learner)*

> Binary is great for computers but long for people: 255 is `11111111`.
> Programmers use a shortcut called **hex**, with sixteen digits, where
> every hex digit is exactly four bits. You've already seen hex without
> knowing it: colour codes like `#FF8800`! Today you'll crack colour codes,
> mix any colour you like, and peek inside a picture file.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check `xxd` works in a terminal: `xxd --version`. (Setup installs
      it. If it's missing, `sudo apt install xxd`.)
- [ ] Check the miner picture is there:
      `ls ~/lab/python/catch/images/miner.png`

## Warm-up (5 min)

"How many digits do our numbers use?" *(Ten: 0 to 9.)* "Binary?" *(Two.)*
"What if we wanted sixteen digits? We've run out of number shapes after
9. What could we use?" Let them suggest ideas. *(Letters!)*

## Activity

### Session 1: sixteen digits

1. **The hex digits.** **Say:** "Hex uses 0 to 9, and then A, B, C, D, E
   and F for ten to fifteen." Write the table together, filling in the
   binary with the dot cards (only 8, 4, 2, 1):

   ```
   number  binary  hex       number  binary  hex
     0      0000    0          8      1000    8
     1      0001    1          9      1001    9
     2      0010    2         10      1010    A
     3      0011    3         11      1011    B
     4      0100    4         12      1100    C
     5      0101    5         13      1101    D
     6      0110    6         14      1110    E
     7      0111    7         15      1111    F
   ```

   **Say:** "Four bits make exactly sixteen patterns, so **one hex digit
   is always four bits**. Four bits is called a **nibble**, because it's
   half a byte. Really. Programmers like jokes."

2. **Bytes in hex.** A byte is two nibbles, so it's two hex digits. Split
   the byte in the middle and turn each half into one hex digit:

   ```
   1111 1111  =  F F  =  FF  = 255
   0010 1010  =  2 A  =  2A  = 42
   1000 0000  =  8 0  =  80  = 128
   ```

   **Say:** "That's why programmers love hex: 255 is `11111111` in binary,
   but just `FF` in hex, and you can switch between them in your head."

3. **Python speaks hex.** In the Shell:
   ```python
   hex(255)
   hex(42)
   0xFF
   int("2A", 16)
   f"{200:X}"
   f"{10:02X}"
   ```
   **They should see:** `'0xff'`, `'0x2a'`, `255`, `42`, `'C8'`, `'0A'`.

   **Say:** "`0x` means 'hex', like `0b` means binary. In f-strings, `X`
   means hex with capital letters, and `02` means two places, filled with
   zeros."

4. **Count in hex.** Count from 0 to 32 out loud, in hex, together. "What
   comes after 9?" *(A.)* "After F?" *(10! Which means sixteen.)* "After
   1F?" *(20, which means thirty-two.)* Check with
   `for n in range(33): print(n, f"{n:X}")`.

### Session 2: colours and files

5. **Crack the colour code.** **Say:** "A colour code like `#FF8800` is
   three bytes in hex: red, green and blue. Each goes from 00 (none) to FF
   (as much as possible)."

   ```
   #FF8800  =  red FF (255),  green 88 (136),  blue 00 (0)  =  orange
   ```

   Ask: what colour is `#FF0000`? *(Red.)* `#000000`? *(Black: no light at
   all.)* `#FFFFFF`? *(White: all of them.)* `#FFFF00`? *(Yellow! Red and
   green light make yellow, which surprises everyone.)*

6. **The colour mixer.** New file, `~/lab/python/binary/mixer.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.speed(0)

   while True:
       red = int(input("Red (0-255, or -1 to stop): "))
       if red < 0:
           break
       green = int(input("Green (0-255): "))
       blue = int(input("Blue (0-255): "))
       code = f"#{red:02X}{green:02X}{blue:02X}"
       print("The colour code is", code)
       t.fillcolor(code)
       t.begin_fill()
       for side in range(4):
           t.forward(150)
           t.left(90)
       t.end_fill()

   turtle.done()
   ```
   **They should see:** a square filled with their colour, and its code.
   Try 255, 136, 0 *(`#FF8800`, orange)*, then invent colours. "Can you
   make Minecraft grass green? Steve's shirt? A creeper?"

   Close the turtle window after typing `-1`.

7. **Peek inside a picture.** In the terminal:
   ```
   cd ~/lab/python/catch/images
   xxd miner.png | head -3
   ```
   **They should see:** lines starting `00000000: 8950 4e47 0d0a 1a0a`,
   with `.PNG` in the right-hand column.

   **Say:** "`xxd` shows the bytes of a file in hex, two hex digits per
   byte. Every PNG picture in the world starts with exactly these bytes.
   `50 4e 47` are the letters P, N, G! Remember the `file` command from
   Stage 1? This is how it knows what a file is: it looks at the first
   few bytes. They're called the **magic number**." Try `file miner.png`.

8. **Find your own colour.** If they made a sprite with a custom colour
   like `x = #FF8800` (Lesson 3.13), look for those bytes. They're
   squashed (compressed) inside the PNG, so they might not be there,
   which is a good thing to discover too! Look at the end of the file:
   `xxd miner.png | tail -2`. *(It ends with `IEND`: every PNG ends that
   way.)*

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `xxd: command not found` | It isn't installed | The guide runs `sudo apt install xxd`. |
| `ValueError: invalid literal for int() with base 16: 'G'` | G isn't a hex digit | Hex only goes up to F. |
| `turtle.TurtleGraphicsError: bad color string: #FF880` | The code is too short: a number wasn't given two places | Use `{red:02X}`, with the `02`. |
| `bad color string`, or a strange colour, after a number over 255 | 256 is three hex digits (`100`), so the code is the wrong length | Keep each number from 0 to 255. (The challenge fixes this.) |
| `xxd: miner.png: No such file or directory` | You're in a different folder, or the sprite has another name | `cd ~/lab/python/catch/images`, then `ls`. |

## Talk about it

- Why is one hex digit exactly four bits? *(Four bits make 16 patterns,
  and hex has 16 digits.)*
- How many different colours can a colour code make? *(256 × 256 × 256 =
  16,777,216. In Python: `256 ** 3`, or `2 ** 24`.)*
- How does `file` know a file is a picture, even if it's renamed?

## Challenge *(if there's time, or for next time)*

- Make the mixer refuse numbers below 0 or above 255, and ask again.
- Draw a row of squares that fade from black to red: red goes 0, 51, 102,
  153, 204, 255.
- Look at the first bytes of other files with `xxd FILE | head -1`: a
  text file, `/bin/ls` (programs start with `7f 45 4c 46`, which is ELF),
  a sound file. What letters can you spot?

## Checkpoint

The learner can, without help:
- [ ] Turn a 4-bit number into a hex digit, and a byte into two hex digits
- [ ] Read a colour code as three numbers from 0 to 255
- [ ] Use `hex()`, `int(..., 16)` and `:02X`
- [ ] Use `xxd` to look at a file's bytes, and explain what a magic number is

## Lab notebook

Copy the hex table. Write three colour codes you invented, coloured in
next to them. Write "PNG files start with 89 50 4E 47". Add
*hexadecimal*, *nibble* and *magic number* to the dictionary.

## Guide's background *(optional reading)*

Hexadecimal (base 16) exists purely for human convenience. Because 16 is
2⁴, each hex digit maps to exactly four bits, so you can translate
between hex and binary digit by digit, without arithmetic. That's why
memory addresses, colour codes, network card addresses and file dumps
are all written in hex.

Screens mix light, not paint, so red and green light make yellow, and all
three at full strength make white. Each channel is one byte, which is
where "24-bit colour" and "16.7 million colours" come from.

`xxd` prints a "hex dump": the position in the file on the left (in
hex), then the bytes, then the same bytes as text on the right, with dots
for bytes that aren't printable letters. Many file formats start with a
fixed "magic number", and the `file` command identifies files by checking
those, not by their names. The learner will use hex dumps again when they
look at programs and memory in later stages.
