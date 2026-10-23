// Test for Squares.asm (Redstone to Rust practice program, Stage 6 checkpoint).
// Squares puts R0 * R0 into R1, for R0 from 0 to 100.

load Squares.asm,
output-file Squares.out,
compare-to Squares.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2;

set RAM[0] 0, set RAM[1] -1;
repeat 100 { ticktock; }
set RAM[0] 0, output;

set PC 0, set RAM[0] 1, set RAM[1] -1;
repeat 100 { ticktock; }
set RAM[0] 1, output;

set PC 0, set RAM[0] 7, set RAM[1] -1;
repeat 500 { ticktock; }
set RAM[0] 7, output;

set PC 0, set RAM[0] 100, set RAM[1] -1;
repeat 5000 { ticktock; }
set RAM[0] 100, output;
