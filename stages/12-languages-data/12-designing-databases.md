# Lesson 12.12: Designing a Database

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; `sqlite3`; `~/lab/sql/minecraft.db`; paper · **New words:**
relation, primary key, foreign key, constraint, join, `NULL`,
transaction, index, query plan

## Goal *(read this to the learner)*

> In Stage 5 you asked questions of a database somebody else made.
> Today you'll design one: the Creeper Club's, with players, items and
> who has what, split into tables so that nothing is written twice.
> Then you'll build a pretend Minecraft world with 131,072 blocks, and
> make finding diamonds in it ten times faster with one line.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Lesson 5.14 is the learner's first SQL lesson; glance at it.
- [ ] As the learner: `mkdir -p ~/lab/lang/data && cd ~/lab/lang/data &&
      git init`.

## Warm-up (5 min)

"In Lesson 12.11, what was a table, in set words?" *(A set of rows.)*
"In Stage 5, how did you find which items a creeper drops?" *(A `JOIN`
between `mobs` and `drops`.)*

## Activity

### Session 1: designing tables

1. **The one-big-table mistake.** On paper, write the club's things in
   one table:

   | player | item | count |
   |---|---|---|
   | Steve | diamond | 3 |
   | Steve | torch | 64 |
   | Alex | diamond | 5 |
   | Alex | cookie | 12 |

   **Ask:** "We want to rename 'diamond' to 'shiny diamond'. How many
   places must we change?" *(Two, and if we miss one, the table
   disagrees with itself.)* "Sunny joins the club, but has nothing yet.
   Where does Sunny go?" *(Nowhere! There's no row without an item.)*
   **Say:** "The fix: one table for each kind of thing, and a table that
   connects them, using numbers."

2. **Three tables.** Draw them:
   ```
   players          items             inventory
   id | name        id | name         player | item | count
   1  | Steve       1  | diamond      1      | 1    | 3
   2  | Alex        2  | torch        1      | 2    | 64
   3  | Sunny       3  | cookie       2      | 1    | 5
                                      2      | 3    | 12
   ```
   **Say:** "Each player and item has an `id`, a number that's never
   repeated: its **primary key**. `inventory` just points at them by
   number: those are **foreign keys**. Now 'diamond' is written in one
   place, and Sunny can exist with no items." **Ask:** "What does the
   row `2 | 3 | 12` mean?" *(Alex has 12 cookies.)*

3. **Build it.** In `~/lab/lang/data`, make `club.sql`:
   ```sql
   -- The Creeper Club's database: who has what.
   CREATE TABLE players (
       id   INTEGER PRIMARY KEY,
       name TEXT NOT NULL UNIQUE
   );

   CREATE TABLE items (
       id   INTEGER PRIMARY KEY,
       name TEXT NOT NULL UNIQUE
   );

   CREATE TABLE inventory (
       player INTEGER REFERENCES players (id),
       item   INTEGER REFERENCES items (id),
       count  INTEGER CHECK (count > 0)
   );

   INSERT INTO players (name) VALUES ('Steve'), ('Alex'), ('Sunny');
   INSERT INTO items (name) VALUES ('diamond'), ('torch'), ('cookie');
   INSERT INTO inventory VALUES (1, 1, 3), (1, 2, 64), (2, 1, 5), (2, 3, 12);
   ```
   **Say:** "`NOT NULL` means it must have a name. `UNIQUE` means no two
   the same. `CHECK` is a rule every row must follow. These are
   **constraints**: the database refuses anything that breaks them.
   `INSERT INTO players (name)` leaves out the `id`, and SQLite numbers
   them 1, 2, 3 by itself." Then:
   ```
   sqlite3 club.db < club.sql
   sqlite3 -box club.db
   ```
   and `SELECT * FROM players;`. **They should see:**
   ```
   ┌────┬───────┐
   │ id │ name  │
   ├────┼───────┤
   │ 1  │ Steve │
   │ 2  │ Alex  │
   │ 3  │ Sunny │
   └────┴───────┘
   ```

### Session 2: joining it back together

4. **Two joins.** `SELECT * FROM inventory;` is just numbers. Join it to
   both other tables:
   ```sql
   SELECT players.name AS player, items.name AS item, inventory.count
   FROM inventory
   JOIN players ON inventory.player = players.id
   JOIN items ON inventory.item = items.id
   ORDER BY player;
   ```
   **They should see:**
   ```
   ┌────────┬─────────┬───────┐
   │ player │  item   │ count │
   ├────────┼─────────┼───────┤
   │ Alex   │ diamond │ 5     │
   │ Alex   │ cookie  │ 12    │
   │ Steve  │ diamond │ 3     │
   │ Steve  │ torch   │ 64    │
   └────────┴─────────┴───────┘
   ```
   **Say:** "The one big table from step 1, made fresh whenever we ask.
   `AS` gives a column a nicer name."

5. **One change, everywhere.**
   ```sql
   UPDATE items SET name = 'shiny diamond' WHERE id = 1;
   ```
   Run the join again. **They should see** `shiny diamond` for both Steve
   and Alex. **Say:** "One change, and everyone's inventory agrees.
   Keeping each fact in one place is called **normalising** a
   database."

6. **Nobody's things: `LEFT JOIN` and `NULL`.**
   ```sql
   SELECT players.name AS player, SUM(inventory.count) AS total
   FROM players LEFT JOIN inventory ON players.id = inventory.player
   GROUP BY players.name;
   ```
   **They should see:**
   ```
   ┌────────┬───────┐
   │ player │ total │
   ├────────┼───────┤
   │ Alex   │ 17    │
   │ Steve  │ 67    │
   │ Sunny  │       │
   └────────┴───────┘
   ```
   **Say:** "A plain `JOIN` only keeps players who match something, so
   Sunny would vanish. `LEFT JOIN` keeps everyone from the left table,
   and fills the gaps with **`NULL`**: 'nothing here'. Sunny's total is
   `NULL`, shown as blank."

7. **The rules say no.** Try breaking each constraint:
   ```sql
   INSERT INTO players (name) VALUES ('Steve');
   INSERT INTO inventory VALUES (3, 2, 0);
   INSERT INTO players (name) VALUES (NULL);
   ```
   **They should see** three errors, ending `UNIQUE constraint failed:
   players.name (19)`, `CHECK constraint failed: count > 0 (19)` and
   `NOT NULL constraint failed: players.name (19)`. **Say:** "The
   database protects itself from mistakes, like Pickaxe's friendly
   errors, or the vault's checks in Lesson 11.6."

8. **Undo: transactions.**
   ```sql
   BEGIN;
   DELETE FROM inventory;
   SELECT COUNT(*) FROM inventory;
   ROLLBACK;
   SELECT COUNT(*) FROM inventory;
   ```
   **They should see** `0`, then `4`. **Say:** "`BEGIN` starts a
   **transaction**: a group of changes that happen all together, or not
   at all. `ROLLBACK` throws them away; `COMMIT` would keep them. A bank
   moving money uses one: take it from one account *and* add it to the
   other, never just half." `.quit`. Commit `club.sql` (not `club.db`:
   it can be made again from the `.sql`).

### Session 3: a world of blocks, and an index

9. **A big table.** In `~/lab/lang/data`, make `world.py`:
   ```python
   # Make a pretend Minecraft world, 64 x 64 x 32 blocks, in a database.
   import random
   import sqlite3

   random.seed(1)
   db = sqlite3.connect("world.db")
   db.execute("CREATE TABLE blocks (x INTEGER, y INTEGER, z INTEGER, block TEXT)")
   rows = []
   for x in range(64):
       for z in range(64):
           for y in range(32):
               if y > 28:
                   block = "air"
               elif y == 28:
                   block = "grass"
               elif y > 24:
                   block = "dirt"
               else:
                   block = random.choice(["stone"] * 60 + ["coal", "iron", "gravel"] * 3 + ["diamond"])
               rows.append((x, y, z, block))
   db.executemany("INSERT INTO blocks VALUES (?, ?, ?, ?)", rows)
   db.commit()
   print(len(rows), "blocks")
   ```
   `python3 world.py`. **They should see:** `131072 blocks`. **Ask:** "Why
   131072?" *(64 × 64 × 32, which is 2¹⁷.)* "Why is `diamond` so rare?"
   *(It's 1 choice in a list of 70.)* `random.seed(1)` makes everyone's
   world the same.

10. **Count, and time it.** `sqlite3 -box world.db`, then:
    ```sql
    .timer on
    SELECT block, COUNT(*) FROM blocks GROUP BY block ORDER BY COUNT(*) DESC;
    SELECT COUNT(*) FROM blocks WHERE block = 'diamond';
    EXPLAIN QUERY PLAN SELECT x, y, z FROM blocks WHERE block = 'diamond';
    ```
    **They should see** stone first (87749), down to `diamond` (1482);
    then `1482`, with a line like `Run Time: real 0.011`; then:
    ```
    QUERY PLAN
    `--SCAN blocks
    ```
    **Say:** "`SCAN` means SQLite looked at every one of the 131,072
    rows to find the diamonds. That's linear search, from Stage 7. The
    **query plan** is SQLite saying how it will answer."

11. **An index.**
    ```sql
    CREATE INDEX by_block ON blocks (block);
    SELECT COUNT(*) FROM blocks WHERE block = 'diamond';
    EXPLAIN QUERY PLAN SELECT x, y, z FROM blocks WHERE block = 'diamond';
    ```
    **They should see** `1482` again, but with a time like `real 0.001`,
    and:
    ```
    QUERY PLAN
    `--SEARCH blocks USING INDEX by_block (block=?)
    ```
    **Say:** "About ten times faster. An **index** is a sorted list of
    every block type, with where to find each row, kept in a tree. Like
    the index at the back of a book, or binary search in Stage 7:
    SQLite jumps straight to `diamond`." `.quit`, and `ls -l world.db`.
    **Ask:** "The file was about 2.4 MB before. What's the cost of an
    index?" *(Space: now about 4.2 MB. And every `INSERT` has to update
    the index too.)* Commit `world.py`, but not `world.db`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Parse error near line 2: table players already exists` | `club.sql` was run twice into the same `club.db` | Delete `club.db` and run it again. |
| A join gives 36 rows instead of 4 | The `JOIN`s are missing their `ON`s, so every row is matched with every other (4 × 3 × 3) | Every `JOIN` needs `ON` to say which rows match. |
| `Parse error: ambiguous column name: name` | Both tables have a `name` column | Say which: `players.name`. |
| `WHERE drops.item = NULL` finds nothing | Nothing is ever equal to `NULL`, not even `NULL` | Use `IS NULL`. |
| `sqlite3.OperationalError: table blocks already exists` | `world.py` was run twice | Delete `world.db` first. |
| The times are both `0.000` | A very fast computer | Look at `SCAN` and `SEARCH` instead; or make the world bigger. |

## Talk about it

- What went wrong with one big table?
- What are primary and foreign keys for?
- What's the difference between `JOIN` and `LEFT JOIN`?
- What's a transaction? Why do banks need them?
- What does an index cost, and what does it buy?

## Challenge *(if there's time, or for next time)*

- Add a `trades` table: who gave what to whom. Write a join with
  `players` twice (`JOIN players AS giver ...`).
- In the world, find the highest diamond (`ORDER BY y DESC LIMIT 1`).
  Does `EXPLAIN QUERY PLAN` still use the index?
- Join `mobs` and `drops` with `LEFT JOIN`, and find every mob that
  drops nothing. *(`WHERE drops.item IS NULL`: 8 mobs, from axolotl to
  wolf.)*

## Checkpoint

The learner can, without help:
- [ ] Explain why one big table causes problems, and split it into
      tables with keys
- [ ] Write a three-table join, and a `LEFT JOIN`
- [ ] Explain constraints and transactions, with examples
- [ ] Show `SCAN` turn into `SEARCH` with an index, and explain the cost

## Lab notebook

Draw the three club tables with arrows from `inventory` to the others.
Write the diamond times before and after the index. Commit. Add
*primary key*, *foreign key*, *constraint*, *NULL*, *transaction* and
*index* to `dictionary.md`.

## Guide's background *(optional reading)*

Splitting tables so that each fact is stored once is called
**normalisation** (the "normal forms" of database theory); step 1 shows
the update and insertion anomalies it prevents. SQLite enforces `CHECK`,
`UNIQUE` and `NOT NULL` always, but checks `REFERENCES` (foreign keys)
only after `PRAGMA foreign_keys = ON;`, for historical reasons: try
inserting an inventory row for player 99 with and without it.

`NULL` uses **three-valued logic** (true, false and unknown), which is
why `= NULL` is never true: it's "unknown". SQLite's indexes are
**B-trees**, wide, shallow trees designed for disks; *Let's Build a
Simple Database* (in the offline library, `repos/db-tutorial`, Parts 7
onwards) builds one in C for an older learner. Timings vary a lot by
computer; the `SCAN`/`SEARCH` change is the reliable evidence.
