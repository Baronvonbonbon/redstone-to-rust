// Test for CreeperAlarm.hdl (Redstone to Rust practice chip).

load CreeperAlarm.hdl,
output-file CreeperAlarm.out,
compare-to CreeperAlarm.cmp,
output-list creeper%B3.1.3 night%B2.1.2 inside%B2.1.3 alarm%B2.1.2;

set creeper 0, set night 0, set inside 0, eval, output;
set creeper 0, set night 0, set inside 1, eval, output;
set creeper 0, set night 1, set inside 0, eval, output;
set creeper 0, set night 1, set inside 1, eval, output;
set creeper 1, set night 0, set inside 0, eval, output;
set creeper 1, set night 0, set inside 1, eval, output;
set creeper 1, set night 1, set inside 0, eval, output;
set creeper 1, set night 1, set inside 1, eval, output;
