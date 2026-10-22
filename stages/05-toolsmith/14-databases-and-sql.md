# Lesson 5.14: Databases and SQL

**Time:** 2 sessions of 45 min · **You need:** a terminal; `sqlite3`
(installed by setup); the Minecraft database (see below); Thonny ·
**New words:** database, table, row, column, query, SQL

## Goal *(read this to the learner)*

> In Stage 3 your Mob Book kept mobs in a Python dictionary. Big programs
> keep their information in a **database**: a program built for storing
> lots of facts and finding the right ones fast. Games, websites, banks
> and libraries all use them. Today you'll explore a Minecraft database by
> asking it questions in a special language called **SQL**: which mobs
> are hostile, which is the toughest, what does a creeper drop?

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] From **your own** account, in the course folder, give the learner
      the database file:
      ```
      ./scripts/give-lab.sh LEARNER sql
      ```
      It puts `minecraft.sql` in `~/lab/sql/` in their account.

## Warm-up (5 min)

"In your Mob Book, how did you look up a mob?" *(`mobs["creeper"]`.)*
"What if you wanted every mob with more than 20 health? Or all the
hostile ones, sorted by health?" *(A loop, with `if`s.)* "A database can
answer questions like that with one sentence."

## Activity

### Session 1: asking questions

1. **Build the database.**
   ```
   cd ~/lab/sql
   head -20 minecraft.sql
   sqlite3 minecraft.db < minecraft.sql
   ls -l
   ```
   **They should see:** the start of the file (commands in capital
   letters), then a new file, `minecraft.db`. **Say:** "The `.sql` file is
   a list of instructions. Feeding it to `sqlite3` with `<` followed them
   and built `minecraft.db`, the actual database."

2. **Open it.**
   ```
   sqlite3 minecraft.db
   ```
   **They should see:** a `sqlite>` prompt. Type these (they start with a
   dot: they're settings, not questions):
   ```
   .tables
   .headers on
   .mode column
   ```
   **They should see:** `drops  mobs`. **Say:** "A database is made of
   **tables**, like spreadsheets. Each **row** is one thing (one mob), and
   each **column** is one fact about it (its name, its health)."

3. **The first question.**
   ```sql
   SELECT * FROM mobs;
   ```
   **They should see:** all 23 mobs, in neat columns: name, behaviour,
   health, dimension and legs. **Say:** "`SELECT * FROM mobs` means 'show
   me everything from the mobs table'. The `;` at the end means 'that's
   the end of my question'. A question to a database is called a
   **query**, and the language is **SQL**, which most people say as
   'sequel'."

4. **Choosing columns, and choosing rows.**
   ```sql
   SELECT name, health FROM mobs;
   SELECT name, health FROM mobs WHERE behaviour = 'hostile';
   SELECT name FROM mobs WHERE health > 20;
   SELECT name FROM mobs WHERE dimension = 'nether' AND health > 15;
   ```
   **They should see:** just two columns; then only the eight hostile
   mobs; then the mobs with more than 20 health; then `piglin`, `blaze`
   and `wither`.

   **Say:** "`WHERE` is like `if`: only the rows where it's true. And
   there's AND from Stage 4 again. Words go in single quotes; numbers
   don't."

5. **Sorting and counting.**
   ```sql
   SELECT name, health FROM mobs ORDER BY health DESC LIMIT 3;
   SELECT COUNT(*) FROM mobs;
   SELECT behaviour, COUNT(*) FROM mobs GROUP BY behaviour;
   ```
   **They should see:** the three toughest (`warden` 500, `wither` 300,
   `ender dragon` 200); then `23`; then how many mobs of each behaviour
   (boss 2, hostile 8, neutral 6, passive 7).

   **Say:** "`DESC` means biggest first. `GROUP BY` puts the rows into
   groups and counts each one. Doing that in Python would take a loop and
   a dictionary, like counting votes in Lesson 3.8!"

6. **Question time.** The learner writes queries to answer these (answers
   for the guide in brackets):
   - Which mobs have no legs? *(`WHERE legs = 0`: ghast, blaze, wither.)*
   - Which mobs live in the End? *(enderman, ender dragon.)*
   - Which passive mob has the most health? *(`WHERE behaviour =
     'passive' ORDER BY health DESC LIMIT 1`: villager.)*
   - Which mobs' names start with `w`? *(`WHERE name LIKE 'w%'`: warden,
     witch, wither, wolf.)*

   Type `.quit` to leave sqlite3.

### Session 2: changing things, and joining tables

7. **Add a row.** Open the database again (`sqlite3 minecraft.db`, then
   `.headers on` and `.mode column`):
   ```sql
   INSERT INTO mobs VALUES ('sniffer', 'passive', 14, 'overworld', 6);
   SELECT * FROM mobs WHERE name = 'sniffer';
   ```
   Add a mob of their own choice too.

8. **Change a row.** **Say:** "You tamed a wolf! Tamed wolves have 40
   health and are friendly."
   ```sql
   UPDATE mobs SET health = 40, behaviour = 'passive' WHERE name = 'wolf';
   SELECT * FROM mobs WHERE name = 'wolf';
   ```

9. **The dangerous one.** **Say:** "`UPDATE` and `DELETE` without a
   `WHERE` change *every* row. Read every query before you press Enter,
   like with `sudo`." Try it on purpose:
   ```sql
   DELETE FROM mobs WHERE name = 'sniffer';
   DELETE FROM mobs;
   SELECT COUNT(*) FROM mobs;
   ```
   **They should see:** `0`: every mob is gone! **Say:** "No undo button.
   Luckily, we have the recipe." `.quit`, then rebuild it from the `.sql`
   file:
   ```
   rm minecraft.db
   sqlite3 minecraft.db < minecraft.sql
   ```
   **Say:** "That's why real databases have backups."

10. **Two tables together.** The `drops` table lists what each mob drops.
    Look at it: `SELECT * FROM drops;`. Then join the two tables:
    ```sql
    SELECT mobs.name, drops.item FROM mobs JOIN drops ON mobs.name = drops.mob WHERE mobs.behaviour = 'hostile';
    ```
    **They should see:** each hostile mob next to each thing it drops:
    `creeper gunpowder`, `spider string`, `witch redstone`...

    **Say:** "`JOIN` matches rows from two tables where the mob's name is
    the same. Keeping drops in their own table means a mob can drop many
    things, without repeating its health every time."

11. **SQL from Python.** New file in Thonny,
    `~/lab/sql/toughest.py`:
    ```python
    import sqlite3

    db = sqlite3.connect("minecraft.db")
    for name, health in db.execute("SELECT name, health FROM mobs ORDER BY health DESC LIMIT 5"):
        print(f"{name}: {health // 2} hearts")
    db.close()
    ```
    Run it. **They should see:** `warden: 250 hearts`, `wither: 150
    hearts`, and so on. **Say:** "Python can ask the database questions,
    and get the answers back as rows to loop over. Lots of real programs
    are exactly this: a program, talking to a database."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The prompt changes to `   ...>` and nothing happens | The `;` at the end is missing | Type `;` and press Enter. |
| `Parse error: no such column: behavior` | A spelling difference: the column is `behaviour` | Check names with `.schema mobs`. |
| `Parse error: no such table: mob` | The table is called `mobs` | `.tables` lists them. |
| `Parse error: no such column: hostile` | Words need single quotes | `WHERE behaviour = 'hostile'` |
| `Parse error near line 5: table mobs already exists` | `minecraft.sql` was run into a database that was already built | `rm minecraft.db` first, then build it again. |
| Everything is squashed together with `\|` between | The settings weren't typed this time | `.headers on` and `.mode column` (they're needed each time). |
| Python: `sqlite3.OperationalError: no such table: mobs` (or `unable to open database file`) | The program ran in a different folder, so Python couldn't find `minecraft.db` (and may have made a new, empty one) | Run the program from `~/lab/sql`, next to `minecraft.db`. Save it there in Thonny. |

## Talk about it

- What's a table, a row and a column?
- How is `WHERE` like an `if`?
- Why is `DELETE FROM mobs;` dangerous?
- Why are the drops in a separate table?

## Challenge *(if there's time, or for next time)*

- Make a new table for your own Minecraft world: `CREATE TABLE builds
  (name TEXT, blocks INTEGER, finished TEXT);` and add your builds.
- Which items are dropped by more than one mob? *(`SELECT item, COUNT(*)
  FROM drops GROUP BY item HAVING COUNT(*) > 1;`)*
- Rewrite the Mob Book from Lesson 3.8 to keep its mobs in a database
  instead of a JSON file.
- **SQL Murder Mystery** *(for the guide to preview first: it's a
  detective story about a murder, with no gore, but decide whether it
  suits your learner).* It's in the offline library at
  `/srv/redstone-library/games/sql-mysteries/`; open its
  `sql-murder-mystery.db` with `sqlite3` and follow the instructions in
  its `prompt_beginner.pdf`.

## Checkpoint

The learner can, without help:
- [ ] Build a database from a `.sql` file and open it with `sqlite3`
- [ ] Write queries with `SELECT`, `WHERE`, `ORDER BY` and `COUNT`
- [ ] Add and change rows with `INSERT` and `UPDATE`, and explain why
      `DELETE` needs `WHERE`
- [ ] Run a query from Python

## Lab notebook

Write the three queries they're proudest of in the notebook, and commit
it. Add *database*, *table*, *row*, *column*, *query* and *SQL* to
`dictionary.md`.

## Guide's background *(optional reading)*

SQL (Structured Query Language, from the 1970s) is the standard way to
work with **relational databases**, which store information in tables
that can be joined together. SQLite is a complete SQL database in a
single file, with no server; it's built into Python, every phone and
every web browser, which makes it the most widely used database in the
world.

The ideas map onto what the learner already knows: a table is like a
list of dictionaries, `WHERE` is a filter, `GROUP BY` with `COUNT` is the
vote-counting pattern from Stage 3, and `JOIN` matches up two lists. The
big difference is that SQL says *what* you want, and the database works
out *how* to find it.

The mob facts (health in half-hearts) are from the game, simplified;
Minecraft fans in the family will happily argue about them, which is a
good excuse to practise `UPDATE`.
