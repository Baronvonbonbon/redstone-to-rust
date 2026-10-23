// Test for Sum.asm (Redstone to Rust practice program).
// Sum adds up 1 + 2 + ... + R0 and puts the answer in R1.

load Sum.asm,
output-file Sum.out,
compare-to Sum.cmp,
output-list RAM[1]%D2.6.2;

set RAM[0] 0, set RAM[1] 99;   // 99 checks that R1 starts at 0
repeat 100 { ticktock; }
output;

set PC 0, set RAM[0] 1, set RAM[1] 99;
repeat 100 { ticktock; }
output;

set PC 0, set RAM[0] 4, set RAM[1] 99;
repeat 200 { ticktock; }
output;

set PC 0, set RAM[0] 100, set RAM[1] 99;
repeat 2000 { ticktock; }
output;
