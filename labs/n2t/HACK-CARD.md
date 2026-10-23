# Hack Card

The Hack computer's machine language, on one page: everything you need
for Lessons 6.10 to 6.14. Print it and keep it next to the keyboard.

## Registers and memory

- **A**: the address register. `@` puts a number in it. It also chooses
  which memory word `M` means.
- **D**: the data register, for working out values.
- **M**: the word in memory (RAM) at address A. `M` *is* `RAM[A]`.
- **PC**: the program counter: the address of the next instruction.
- **ROM** holds the program, **RAM** the data. Both have 16-bit words.

| RAM addresses | What's there |
|---|---|
| 0–15 | `R0` to `R15`: handy variables (`R0` is `RAM[0]`) |
| 16–16383 | your variables (from 16 upwards), and more data |
| 16384–24575 | the **screen**: `SCREEN` is 16384 |
| 24576 | the **keyboard**: `KBD` |

## The A-instruction: `@value`

```
@21        A = 21
@R2        A = 2
@sum       A = the address of the variable sum (16, 17, ... in order of first use)
@LOOP      A = the address of the label (LOOP) in the program
```

In binary: `0` then the number in 15 bits. `@21` is `0000000000010101`.

## The C-instruction: `dest=comp;jump`

Work out **comp**, store it in **dest** (optional), then **jump**
(optional) to the instruction at address A if comp passes the test.

```
D=M        D = RAM[A]
M=D+1      RAM[A] = D + 1
AM=M-1     A and RAM[A] both = RAM[A] - 1
0;JMP      always jump to address A
D;JGT      jump if D > 0
```

In binary: `111` `a c1 c2 c3 c4 c5 c6` `d1 d2 d3` `j1 j2 j3`.

### comp

| comp (a=0) | c1–c6 | comp (a=1) |
|---|---|---|
| `0` | 101010 | |
| `1` | 111111 | |
| `-1` | 111010 | |
| `D` | 001100 | |
| `A` | 110000 | `M` |
| `!D` | 001101 | |
| `!A` | 110001 | `!M` |
| `-D` | 001111 | |
| `-A` | 110011 | `-M` |
| `D+1` | 011111 | |
| `A+1` | 110111 | `M+1` |
| `D-1` | 001110 | |
| `A-1` | 110010 | `M-1` |
| `D+A` | 000010 | `D+M` |
| `D-A` | 010011 | `D-M` |
| `A-D` | 000111 | `M-D` |
| `D&A` | 000000 | `D&M` |
| `D\|A` | 010101 | `D\|M` |

The `a` bit is 0 for the left column (uses A) and 1 for the right (uses
M). The c bits are the ALU's control bits, in order: zx, nx, zy, ny, f,
no.

### dest

| dest | d1 d2 d3 | Stores in |
|---|---|---|
| *(none)* | 000 | nothing |
| `M` | 001 | RAM[A] |
| `D` | 010 | D |
| `MD` | 011 | RAM[A] and D |
| `A` | 100 | A |
| `AM` | 101 | A and RAM[A] |
| `AD` | 110 | A and D |
| `AMD` | 111 | all three |

d1 means A, d2 means D, d3 means M. (The book's second edition also
writes `DM` and `ADM`, but these tools only understand `MD` and `AMD`.)

### jump

| jump | j1 j2 j3 | Jump if comp is... |
|---|---|---|
| *(none)* | 000 | never |
| `JGT` | 001 | > 0 |
| `JEQ` | 010 | = 0 |
| `JGE` | 011 | ≥ 0 |
| `JLT` | 100 | < 0 |
| `JNE` | 101 | ≠ 0 |
| `JLE` | 110 | ≤ 0 |
| `JMP` | 111 | always |

## Symbols

| Symbol | Value |
|---|---|
| `R0` to `R15` | 0 to 15 |
| `SP`, `LCL`, `ARG`, `THIS`, `THAT` | 0, 1, 2, 3, 4 (used in Stage 8) |
| `SCREEN` | 16384 |
| `KBD` | 24576 |
| `(LABEL)` | the address of the next instruction (labels take no space) |
| any other name | a variable: 16, 17, 18... in the order they first appear |

## The screen and the keyboard

- The screen is 512 pixels wide and 256 high, black and white. Each row
  is 32 words of 16 pixels, so row `r`, word `w` is at
  `SCREEN + 32*r + w`. In a word, bit 0 is the **leftmost** pixel of the
  16. A 1 is black. `-1` (all ones) is 16 black pixels.
- `RAM[KBD]` holds the code of the key being pressed, or 0 for none. It
  uses ASCII for letters and numbers (`A` is 65), plus a few more:
  newline 128, backspace 129, left 130, up 131, right 132, down 133,
  space 32.

## Habits

```
(END)
@END
0;JMP      // every program ends with a loop that goes nowhere
```

- Comments start with `//`. Spaces at the start of a line are fine.
- Labels in CAPITALS, variables in lowercase.
- Run programs in the CPU Emulator (`cpu`): **Load Program** (folder
  button), set **Animate** to **No animation** for speed, then Run.
