-- A small Minecraft database for Lesson 5.14.
-- Make the database file with:   sqlite3 minecraft.db < minecraft.sql
-- Health is in half-hearts, like the game (20 = 10 hearts).

CREATE TABLE mobs (
    name      TEXT PRIMARY KEY,
    behaviour TEXT,      -- passive, neutral, hostile or boss
    health    INTEGER,
    dimension TEXT,      -- overworld, nether or end
    legs      INTEGER
);

INSERT INTO mobs VALUES
    ('chicken',      'passive', 4,   'overworld', 2),
    ('cow',          'passive', 10,  'overworld', 4),
    ('pig',          'passive', 10,  'overworld', 4),
    ('sheep',        'passive', 8,   'overworld', 4),
    ('villager',     'passive', 20,  'overworld', 2),
    ('axolotl',      'passive', 14,  'overworld', 4),
    ('fox',          'passive', 10,  'overworld', 4),
    ('wolf',         'neutral', 8,   'overworld', 4),
    ('bee',          'neutral', 10,  'overworld', 6),
    ('panda',        'neutral', 20,  'overworld', 4),
    ('iron golem',   'neutral', 100, 'overworld', 2),
    ('enderman',     'neutral', 40,  'end',       2),
    ('piglin',       'neutral', 16,  'nether',    2),
    ('zombie',       'hostile', 20,  'overworld', 2),
    ('skeleton',     'hostile', 20,  'overworld', 2),
    ('creeper',      'hostile', 20,  'overworld', 4),
    ('spider',       'hostile', 16,  'overworld', 8),
    ('witch',        'hostile', 26,  'overworld', 2),
    ('ghast',        'hostile', 10,  'nether',    0),
    ('blaze',        'hostile', 20,  'nether',    0),
    ('warden',       'hostile', 500, 'overworld', 2),
    ('wither',       'boss',    300, 'nether',    0),
    ('ender dragon', 'boss',    200, 'end',       4);

CREATE TABLE drops (
    mob  TEXT,
    item TEXT
);

INSERT INTO drops VALUES
    ('chicken', 'feather'), ('chicken', 'raw chicken'),
    ('cow', 'leather'), ('cow', 'raw beef'),
    ('pig', 'raw porkchop'),
    ('sheep', 'wool'), ('sheep', 'raw mutton'),
    ('zombie', 'rotten flesh'),
    ('skeleton', 'bone'), ('skeleton', 'arrow'),
    ('creeper', 'gunpowder'),
    ('spider', 'string'), ('spider', 'spider eye'),
    ('enderman', 'ender pearl'),
    ('blaze', 'blaze rod'),
    ('ghast', 'ghast tear'), ('ghast', 'gunpowder'),
    ('witch', 'glass bottle'), ('witch', 'redstone'),
    ('iron golem', 'iron ingot'), ('iron golem', 'poppy'),
    ('wither', 'nether star'),
    ('ender dragon', 'dragon egg');
