#!/usr/bin/env python3
"""Treasure Cave: a folder maze for practicing ls, cd, wildcards and find.

    python3 make_cave.py ~/cave            # new random cave
    python3 make_cave.py ~/cave --seed 3   # the same cave every time

Prints the answers to the quest questions for the guide.
"""
import argparse
import os
import random

ROOMS = ["entrance", "dark-tunnel", "lava-lake", "spider-den", "crystal-hall",
         "echo-chamber", "mushroom-grove", "underground-river", "bat-roost"]
ORES = ["coal", "iron", "gold", "redstone"]

QUEST = """\
TREASURE CAVE QUEST
===================

You are standing at the mouth of a cave. Every file in here is a block
of ore. The end of the name tells you what kind: coal, iron, gold,
redstone... and somewhere there is ONE diamond.

Answer these questions. Write your answers in your lab notebook.

1. How many coal blocks are in the entrance room?
   (Try: ls entrance/*.coal   The * means "anything".)

2. Which rooms are directly inside the cave? Which ones have rooms
   inside THEM?   (Try: ls, cd, and ls again. Or try: tree)

3. Where is the diamond? Give the whole path.
   (Try: find . -name "*.diamond")

4. How many gold blocks are in the WHOLE cave?
   (Try: find . -name "*.gold" | wc -l)

5. BONUS: Open the diamond with cat. What does it say?
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--seed", type=int)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    def room(path, depth, min_ore=0):
        os.makedirs(path, exist_ok=True)
        counts = {o: rng.randint(min_ore, 5) for o in ORES}
        for ore, k in counts.items():
            for i in range(k):
                open(os.path.join(path, f"block-{i + 1}.{ore}"), "w").write(f"A block of {ore}.\n")
        rooms = [path]
        if depth < 2:
            for name in rng.sample([r for r in ROOMS[1:] if r != os.path.basename(path)], rng.randint(1, 3)):
                rooms += room(os.path.join(path, name), depth + 1)
        return rooms

    top = [room(os.path.join(args.dir, "entrance"), 2, min_ore=2)]
    for name in rng.sample(ROOMS[1:], 3):
        top.append(room(os.path.join(args.dir, name), 0))
    all_rooms = [r for group in top for r in group]
    deepest = max(all_rooms, key=lambda p: p.count(os.sep))
    open(os.path.join(deepest, "shiny.diamond"), "w").write(
        "You found the DIAMOND! You are a master cave explorer.\n")
    open(os.path.join(args.dir, "QUEST.txt"), "w").write(QUEST)

    coal = len([f for f in os.listdir(os.path.join(args.dir, "entrance")) if f.endswith(".coal")])
    gold = sum(f.endswith(".gold") for _, _, fs in os.walk(args.dir) for f in fs)
    print(f"Cave created in {args.dir}\nFOR THE GUIDE: 1) {coal} coal   "
          f"3) {os.path.relpath(deepest, args.dir)}/shiny.diamond   4) {gold} gold")


if __name__ == "__main__":
    main()
