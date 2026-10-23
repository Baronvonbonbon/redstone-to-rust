# HDL Card

A one-page reminder of the hardware description language used in Nand to
Tetris. Print it and keep it next to the keyboard.

## A chip

```
CHIP CreeperAlarm {           // the name: the same as the file's name
    IN creeper, night, inside; // input pins
    OUT alarm;                 // output pins

    PARTS:                     // the chips inside, one per line
    And(a=creeper, b=night, out=danger);
    Not(in=inside, out=outside);
    And(a=danger, b=outside, out=alarm);
}
```

- In `And(a=creeper, ...)`, the **left** side is the part's own pin, and
  the **right** side is a wire in *this* chip.
- A new name on the right (`danger`) makes an **internal pin**: a wire
  inside the chip.
- Every part line ends with `;`. Comments start with `//`.
- The order of the lines doesn't matter: all the parts work at once.

## Rules

- Each wire is driven by **one** part's output, no more.
- A chip's own output pin (like `alarm`) can't be used as an input to
  another part. Use an internal pin, and see "Several outputs" below.
- Input pins that aren't connected are 0.

## Buses: many wires at once

```
IN a[16];                   // a 16-wire bus: a[0] is the right-hand bit, a[15] the left
Not(in=a[3], out=out[3]);   // one wire of a bus
Or8Way(in=a[0..7], out=x);  // wires 0 to 7 of an input bus
Mux16(a=a, b=b, sel=s, out=out);  // a whole bus: the widths must match
```

- `true` and `false` are wires that are always 1 or 0:
  `Mux16(a=x, b=false, ...)`, or one wire of a bus: `b[0]=true`.
- You can take part of an **input** bus (`a[0..7]`), but not part of an
  **internal** one. Instead, name the parts where they come out (below).

## Several outputs from one part

A part's output can be connected to several wires at once:

```
Mux16(a=x, b=y, sel=s, out=out, out=copy, out[15]=top, out[0..7]=low);
```

This is how to use a chip's output inside the chip as well, or to split
a bus.

## Chips and their pins

The first ones are built-in; the rest you build, in this order. Each
project folder has the files for its chips.

| Chip | Inputs | Outputs |
|---|---|---|
| Nand | a, b | out |
| Not | in | out |
| And, Or, Xor | a, b | out |
| Mux | a, b, sel | out |
| DMux | in, sel | a, b |
| Not16 | in[16] | out[16] |
| And16, Or16 | a[16], b[16] | out[16] |
| Mux16 | a[16], b[16], sel | out[16] |
| Or8Way | in[8] | out |
| Mux4Way16 | a[16], b[16], c[16], d[16], sel[2] | out[16] |
| Mux8Way16 | a[16] ... h[16], sel[3] | out[16] |
| DMux4Way | in, sel[2] | a, b, c, d |
| DMux8Way | in, sel[3] | a, b, c, d, e, f, g, h |
| HalfAdder | a, b | sum, carry |
| FullAdder | a, b, c | sum, carry |
| Add16 | a[16], b[16] | out[16] |
| Inc16 | in[16] | out[16] |
| ALU | x[16], y[16], zx, nx, zy, ny, f, no | out[16], zr, ng |
| DFF *(built-in, clocked)* | in | out |
| Bit | in, load | out |
| Register | in[16], load | out[16] |
| RAM8 | in[16], load, address[3] | out[16] |
| RAM64 | in[16], load, address[6] | out[16] |
| RAM512 | in[16], load, address[9] | out[16] |
| RAM4K | in[16], load, address[12] | out[16] |
| RAM16K | in[16], load, address[14] | out[16] |
| PC | in[16], inc, load, reset | out[16] |
| Screen *(built-in)* | in[16], load, address[13] | out[16] |
| Keyboard *(built-in)* | | out[16] |
| ARegister, DRegister *(built-in)* | in[16], load | out[16] |
| ROM32K *(built-in)* | address[15] | out[16] |
| Memory | in[16], load, address[15] | out[16] |
| CPU | inM[16], instruction[16], reset | outM[16], writeM, addressM[15], pc[15] |
| Computer | reset | |

## Testing

```
hardware Not.tst          # run a test in the terminal
diff Not.out Not.cmp      # after a failure: the last line of .out is the wrong one
hardware                  # open the simulator's window
```

In the window: **Load Chip** (chip button), double-click an input's
value to change it, **Eval** (calculator) to work out the outputs,
**tick-tock** (clock) for chips with memory, **Load Script** (scroll),
then **Run** (double arrow). Set **Animate** to **No animation** to run
tests quickly.
