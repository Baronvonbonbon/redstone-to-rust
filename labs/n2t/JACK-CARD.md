# Jack Card

The Jack language and its operating system, on one page: everything you
need for Lessons 8.11 to 8.18. Print it and keep it next to the
keyboard.

## A program

A program is a folder of `.jack` files, one class in each. The file
`Main.jack` holds `class Main`, and the program starts at `Main.main`.

```
class Main {
    function void main() {
        do Output.printString("Hello, Steve!");
        do Output.println();
        return;
    }
}
```

## Inside a class

```
class Creeper {
    field int x, y;              // each Creeper has its own x and y
    static int count;            // one count, shared by all Creepers

    constructor Creeper new(int startX, int startY) {
        let x = startX;
        let y = startY;
        return this;             // a constructor always ends like this
    }

    method void move(int dx) {   // works on one Creeper: a.move(1)
        let x = x + dx;
        return;
    }

    function int twice(int n) {  // belongs to the class: Creeper.twice(4)
        return n + n;
    }
}
```

## Types

`int` (−32768 to 32767), `char`, `boolean` (`true` or `false`), and any
class: `Array`, `String`, `Creeper`. `null` means "no object".

## Statements

| Statement | Example |
|---|---|
| `var` (at the start of a subroutine) | `var int i, total;` |
| `let` | `let total = total + i;` and `let a[i] = 0;` |
| `do` (call, and throw the answer away) | `do Output.printInt(total);` |
| `if`, `else` | `if (x > 3) { ... } else { ... }` |
| `while` | `while (i < 10) { ... }` |
| `return` | `return;` or `return total;` |

Every subroutine ends with `return`, even a `void` one. Curly brackets
are always needed, even around one statement.

## Expressions

| Kind | Example |
|---|---|
| numbers, letters, words | `42`, `"Hello"` (there are no `'c'` letters: use 67) |
| arithmetic | `+ - * /` (whole numbers: `7 / 2` is 3) |
| comparing | `<`, `>`, `=` (not `==`, and there's no `<=`: use `~(a > b)`) |
| logic | `&` (and), `\|` (or), `~` (not) |
| negative | `-x` |
| arrays | `a[i]` |
| calls | `Math.max(a, b)`, `game.run()`, `move(1)` |

**Jack works strictly left to right.** `1 + 2 * 3` is 9, not 7. Use
brackets: `1 + (2 * 3)`.

## The operating system

| Class | Handy subroutines |
|---|---|
| `Output` | `printString(s)`, `printInt(n)`, `printChar(c)`, `println()`, `moveCursor(row, col)` (23 rows, 64 columns) |
| `Screen` | `clearScreen()`, `setColor(b)` (true is black), `drawPixel(x, y)`, `drawLine(x1, y1, x2, y2)`, `drawRectangle(x1, y1, x2, y2)`, `drawCircle(x, y, r)` |
| `Keyboard` | `keyPressed()` (0 if none), `readInt(message)`, `readLine(message)` |
| `Math` | `abs(x)`, `max(a, b)`, `min(a, b)`, `sqrt(x)`, `multiply`, `divide` |
| `String` | `new(maxLength)`, `length()`, `charAt(i)`, `appendChar(c)`, `intValue()`, `dispose()` |
| `Array` | `new(size)`, `dispose()` |
| `Memory` | `peek(address)`, `poke(address, value)`, `alloc(size)`, `deAlloc(o)` |
| `Sys` | `wait(milliseconds)`, `halt()` |

The screen is 512 × 256 pixels: x from 0 to 511 across, y from 0 to 255
down. Key codes: letters and numbers are ASCII (`A` is 65), space 32,
newline 128, backspace 129, left 130, up 131, right 132, down 133.

## The tools

- `jackc FOLDER` compiles every `.jack` file in the folder into a `.vm`
  file (Lesson 8.11).
- `vme` opens the VM Emulator. **Load Program**, choose the *folder*,
  answer **Yes** to "use the built-in implementation", set **Animate**
  to **No animation**, then Run. Click the keyboard bar under the screen
  before typing.
