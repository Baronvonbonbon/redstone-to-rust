# Sprite Maker

Turns text pixel art into PNG pictures that Pygame Zero games can use.
It's Lesson 0.7's "pictures made of numbers" idea, for real.
Standard-library Python only.

Give it to the learner (Lesson 3.13):

```bash
./scripts/give-lab.sh LEARNER sprites    # copies it to ~/lab/sprite-maker
```

The learner uses it like this:

```bash
python3 ~/lab/sprite-maker/make_sprite.py diamond.txt            # makes diamond.png
python3 ~/lab/sprite-maker/make_sprite.py diamond.txt --size 8   # bigger pixels
```

The colour letters and how to add new colours are at the top of
`make_sprite.py`. `examples/` has a miner, a diamond and a creeper.
`test_sprites.sh` checks that it works.
