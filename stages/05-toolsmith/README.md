# Stage 5: Toolsmith

**Badge:** Toolsmith · **Needs first:** Stage 4 · **Lessons:** 16

The learner stops being a visitor on a computer and becomes its admin.
On the **Sandbox**, a small Linux computer of their own, they use
`sudo`, read and set permissions (which turn out to be the binary from
Stage 4), install packages, and break the system on purpose to learn
how to fix it. Then they make their own tools: shell scripts with
arguments, decisions and loops, kept in `~/bin`; the `vim` editor; and
**git**, which from now on holds the lab notebook and every project.
They meet processes and ports, talk to servers by hand, ask a database
questions in SQL, and finish the Mineshaft by writing a program that
beats a guard no human can. The stage ends with a tool of their own,
tested, documented and in git.

Every lesson is fully scripted. The commands, error messages, scripts,
git sessions and SQL queries in this stage were all run in containers,
and the lessons say what really appears. The Mineshaft levels are
checked by `labs/mineshaft/test_solutions.sh`.

## Tools

- **The Sandbox** (`labs/sandbox`), the breakable computer, for Lessons
  5.1–5.3, the 5.11 challenge and the checkpoint. The guide builds it
  once while online, from their own account:
  `./sandbox.sh build LEARNER`, then `./sandbox.sh start`. The learner
  logs in with `ssh LEARNER@localhost -p 2222`. `./sandbox.sh reset`
  makes a brand-new one in seconds. The
  [Sandbox handbook](../../labs/sandbox/README.md) has everything else.
  A Raspberry Pi or a virtual machine also works: see
  [docs/SETUP.md](../../docs/SETUP.md).
- **The Mineshaft**, levels 10–19, from Stage 1, for Lessons 5.4, 5.8,
  5.13 and 5.15. The learner's saved passwords are in
  `~/lab/mineshaft.txt`. The [guide's handbook](../../labs/mineshaft/README.md)
  has hints and solutions.
- **vim**, **git**, **sqlite3** and **nc**, all installed by setup.
- **The Minecraft database**, for Lesson 5.14: from your own account,
  `./scripts/give-lab.sh LEARNER sql`.
- **(Optional) Oh My Git!**, a card game about git, for Lesson 5.10.
  It's a hand download from its itch.io page (linked from ohmygit.org),
  with no account needed; it wasn't tested by the course's checks.
  **(Online, optional, no account):** *learngitbranching.js.org*.
- **(Optional) The Command Line Murder Mystery** and **SQL Murder
  Mystery**, in the offline library under `games/`. Both are detective
  stories about a murder, with no gore. **Preview them first** and
  decide whether they suit your learner.
- References for the guide: *The Linux Command Line* by William Shotts
  (in the offline library, `books/the-linux-command-line.pdf`), chapters
  9–10 (permissions, processes) and 24–36 (shell scripts); and *Pro Git*
  (free online at git-scm.com/book).

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 5.1 | [My Own Computer](01-my-own-computer.md) | Logging in to the Sandbox, a new password, `sudo` and root, the Toolsmith's rules, a tour of the folders | admin, root, containers |
| 5.2 | [Who Can Do What](02-who-can-do-what.md) | Permission labels, `chmod` with letters and binary numbers, a new user, a group-only chest | permissions, octal |
| 5.3 | [Packages, and Break It, Fix It](03-break-it-fix-it.md) | `apt` offline, inside a package, five things to break and fix, and one that needs a reset | package managers, recovery |
| 5.4 | [Back to the Mineshaft (Levels 10–12)](04-mineshaft-10-12.md) | ROT13 with `tr`, unpacking in a scratch folder, `find` by size | `tr`, `tar`, `find` |
| 5.5 | [Vim, the Editor That Never Dies](05-vim.md) | `vimtutor`, modes, saving and quitting, the escape card | modal editing |
| 5.6 | [Shell Scripts, Part 1](06-scripts-1.md) | `~/bin`, shebangs, `PATH`, arguments, `read`, a dice roller | scripts, variables |
| 5.7 | [Shell Scripts, Part 2](07-scripts-2.md) | Exit codes, `if`, loops, a backup script and a restore drill | conditions, loops, backups |
| 5.8 | [The Mineshaft, Levels 13–15](08-mineshaft-13-15.md) | A setuid door, environment variables, `diff` | setuid, environment |
| 5.9 | [Git, Part 1: Save Points](09-git-save-points.md) | `init`, `add`, `commit`, `log`; the notebook moves into git | version control |
| 5.10 | [Git, Part 2: Time Travel and Branches](10-git-time-travel-and-branches.md) | `restore`, old versions, `.gitignore`, a pink-world branch and a merge | branches, history |
| 5.11 | [Git, Part 3: Conflicts and Remotes](11-git-conflicts-and-remotes.md) | A merge conflict, a bare remote, `push`, `clone`, `pull` | collaboration |
| 5.12 | [Processes and Ports](12-processes-and-ports.md) | `ps`, `top`, jobs and `kill`; ports, an `nc` chat, a web server, HTTP by hand | processes, client/server |
| 5.13 | [The Mineshaft, Levels 16–18](13-mineshaft-16-18.md) | A gatekeeper on a port, a leaked command line, git history that remembers | real security mistakes |
| 5.14 | [Databases and SQL](14-databases-and-sql.md) | A Minecraft database: `SELECT`, `WHERE`, `INSERT`, `UPDATE`, `JOIN`, and SQL from Python | databases, queries |
| 5.15 | [The Final Vault](15-the-final-vault.md) | A Python network client beats Mineshaft level 19; the trophy | protocols, sockets, automation |
| 5.16 | [Project: My Own Tool](16-my-own-tool.md) | A command with a usage message, tests, a README, branches and a remote; demo day; Stage 5 checkpoint | putting it together |

## Free play for this stage

- The Sandbox: it's theirs. Make users for the family, write a message
  of the day (`sudo nano /etc/motd`), install and try `figlet` and
  `toilet`.
- More commands in `~/bin`: anything they type often is a script
  waiting to happen.
- `vimtutor` again, to get faster.
- SQL questions about the Minecraft database, asked by the family.
- An `nc` chat between two terminals, with a sibling.

## Habits to build now

- **Read before you press Enter**, especially with `sudo`, `rm`, `>`,
  `DELETE` and `UPDATE`.
- **Commit early, commit often**, with messages that say what changed
  and why. The lab notebook is in git from Lesson 5.9 on.
- **Try big ideas on a branch.**
- **Back up, and prove the backup works** by restoring it somewhere else.
- **Secrets stay out of command lines and out of git.**
- **Read the error message**, then `man` and `--help`, before asking.

## Checkpoint

The learner can, without help:
- [ ] Use `sudo` carefully, and explain what root is
- [ ] Read and set permissions, with letters and with numbers
- [ ] Install and remove packages with `apt`
- [ ] Edit a file in vim, save, and quit
- [ ] Write a shell script with arguments, `if`, loops and exit codes,
      and run it from `~/bin`
- [ ] Use git to commit, look back, branch, merge, fix a conflict and push
- [ ] Find and stop processes, and explain ports, servers and clients
- [ ] Ask a database questions in SQL

They can also:
- [ ] Reach the bottom of the Mineshaft, with a program they wrote
- [ ] Build, test and document a tool of their own (Lesson 5.16)
