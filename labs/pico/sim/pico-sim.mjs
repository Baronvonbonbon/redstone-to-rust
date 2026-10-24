// Run a Pico program (a .uf2 file) in the rp2040js emulator, and print what
// its LED and its USB connection do. For learners without a Pico, and for
// checking the course's own programs.
//
//   node pico-sim.mjs FILE.uf2 SECONDS [latch|fan]
//
// "latch" presses the buttons on GP14 (start) and GP15 (stop).
// "fan" warms and cools the chip's thermometer.
import { readFileSync } from 'fs';
import { ConsoleLogger, LogLevel, Simulator, USBCDC } from 'rp2040js';
import { bootromB1 } from './bootrom.mjs';

const [file, seconds = '3', scenario = ''] = process.argv.slice(2);
if (!file) {
  console.log('usage: node pico-sim.mjs FILE.uf2 SECONDS [latch|fan]');
  process.exit(1);
}

const sim = new Simulator();
const mcu = sim.rp2040;
mcu.logger = new ConsoleLogger(LogLevel.Error);
mcu.loadBootrom(bootromB1);

// A UF2 file is 512-byte blocks, each saying where its bytes go in flash.
const uf2 = readFileSync(file);
for (let i = 0; i + 512 <= uf2.length; i += 512) {
  const block = uf2.subarray(i, i + 512);
  const address = block.readUInt32LE(12);
  const size = block.readUInt32LE(16);
  mcu.flash.set(block.subarray(32, 32 + size), address - 0x10000000);
}

const now = () => sim.clock.nanos / 1e9;
const say = (text) => console.log(`${now().toFixed(3)} s  ${text}`);

// The LED is on GP25.
mcu.gpio[25].addListener((state) => {
  if (state === 0 || state === 1) say(`LED ${state === 1 ? 'on' : 'off'}`);
});

// Pretend to be the computer at the other end of the USB cable.
const cdc = new USBCDC(mcu.usbCtrl);
let text = '';
const show = (buffer) => {
  text += Buffer.from(buffer).toString('latin1');
  let end;
  while ((end = text.indexOf('\n')) >= 0) {
    const line = text.slice(0, end).replace(/[^\x20-\x7e]/g, '').trim();
    if (line) say(`USB: ${line}`);
    text = text.slice(end + 1);
  }
};
const cdcWrite = mcu.usbCtrl.onEndpointWrite;
mcu.usbCtrl.onEndpointWrite = (endpoint, buffer) => {
  cdcWrite(endpoint, buffer);
  if (endpoint !== 0) show(buffer);
};

// The thermometer: 0.706 V at 27 degrees, and 1.721 mV less for each degree more.
const setTemperature = (c) => {
  mcu.adc.channelValues[4] = Math.round(((0.706 - (c - 27) * 0.001721) / 3.3) * 4096);
};
setTemperature(22);
mcu.gpio[14].setInputValue(true); // buttons not pressed: pulled up, high
mcu.gpio[15].setInputValue(true);

const scenarios = {
  latch: [
    [0.5, 'press start', () => mcu.gpio[14].setInputValue(false)],
    [0.7, 'let go of start', () => mcu.gpio[14].setInputValue(true)],
    [1.5, 'press stop', () => mcu.gpio[15].setInputValue(false)],
    [1.7, 'let go of stop', () => mcu.gpio[15].setInputValue(true)],
  ],
  fan: [
    [3, 'finger on the chip: 23.5 degrees', () => setTemperature(23.5)],
    [6, 'warmer: 25 degrees', () => setTemperature(25)],
    [9, 'cooling: 24 degrees', () => setTemperature(24)],
    [12, 'cooler: 23 degrees', () => setTemperature(23)],
  ],
};
const events = [...(scenarios[scenario] ?? [])];

mcu.core.PC = 0x10000000;
sim.execute();
const check = setInterval(() => {
  while (events.length && now() >= events[0][0]) {
    const [, what, action] = events.shift();
    say(`(${what})`);
    action();
  }
  if (now() >= Number(seconds)) {
    sim.stop();
    clearInterval(check);
    say('stopped');
    process.exit(0);
  }
}, 1);
