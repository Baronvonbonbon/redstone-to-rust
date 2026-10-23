// Test for Block.asm (Redstone to Rust practice program).
// Checks the first and last rows of the square, and the pixels around it.

load Block.asm,
output-file Block.out,
compare-to Block.cmp,
output-list RAM[16384]%D2.6.2 RAM[16385]%D2.6.2 RAM[16416]%D2.6.2 RAM[16864]%D2.6.2 RAM[16896]%D2.6.2;

repeat 500 { ticktock; }
output;
