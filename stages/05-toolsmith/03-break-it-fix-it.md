# Lesson 5.3: Packages, and Break It, Fix It

**Time:** 2 sessions of 45 min · **You need:** the Sandbox; the lab
notebook; the guide nearby with `./sandbox.sh reset` ready · **New
words:** package, package manager, `apt`, dependency, recovery

## Goal *(read this to the learner)*

> How does a program get onto a computer? On Linux, almost everything
> comes as a **package**, and a **package manager** installs it for you.
> Today you'll install programs into the Sandbox as its admin. Then comes
> the most fun lesson in the course: you'll **break** the Sandbox on
> purpose, five different ways, and work out how to fix it. One of them
> can't be fixed from the inside, and that's a lesson too.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Reset the Sandbox, so it starts fresh: `./sandbox.sh reset` (in
      `labs/sandbox`). The learner's password goes back to their name.
- [ ] Keep a terminal open in `labs/sandbox`, for step 9.

## Warm-up (5 min)

"How did cowsay get onto the family computer?" *(The guide installed it
with the setup script.)* "Why couldn't you install it yourself?" *(Not
an admin.)* "In the Sandbox, are you an admin?" *(Yes!)*

## Activity

### Session 1: packages

1. **It's not there yet.** Log in to the Sandbox (password: their name,
   after the reset). Then:
   ```
   which cowsay
   cowsay hi
   ```
   **They should see:** nothing from `which`, then `cowsay: command not
   found`.

2. **Try to install it without powers.**
   ```
   apt install cowsay
   ```
   **They should see:** `E: Could not open lock file
   /var/lib/dpkg/lock-frontend - open (13: Permission denied)` and `E:
   Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend),
   are you root?`. **Say:** "It even asks: are you root? Installing changes
   the whole computer, so only the admin may do it."

3. **Install it as admin.**
   ```
   sudo apt install cowsay
   ```
   It shows what it will install and asks `Do you want to continue? [Y/n]`.
   Type `y`. **They should see:** lines like `Setting up cowsay ...`. Then:
   ```
   which cowsay
   cowsay I installed this myself!
   ```

   **Say:** "`apt` is the **package manager**. A **package** is a program
   bundled up with everything it needs. Look at the list it showed:
   cowsay needed a little helper package too. Those are called
   **dependencies**, and `apt` finds them for you."

4. **Look inside a package.**
   ```
   dpkg -L cowsay | head
   apt show cowsay 2>/dev/null | head -3
   ```
   **They should see:** the files the package put on the computer
   (`/usr/games/cowsay` is the program), then the package's name and
   version.

5. **Install more, then remove one.** The Sandbox has `figlet`, `sl` and
   `toilet` saved ready to install. Install `sl` and `figlet` and try
   them (`sl`, `figlet Toolsmith`). Then remove one:
   ```
   sudo apt remove sl
   ```

   **Say:** "Normally `apt` downloads packages from the internet. The
   Sandbox has these four saved inside it, so it works even with the
   internet off. A package that isn't saved needs the internet."

### Session 2: break it, fix it

For each break: **predict** what will happen, **do** it, **look** at what
actually happens, then **fix** it. Write each one in the notebook as a
little table: break, what happened, fix.

6. **Break 1: lock yourself out of your own file.**
   ```
   echo "notes" > notes.txt
   chmod 000 notes.txt
   cat notes.txt
   ```
   *(Permission denied.)* Fix it: `chmod 644 notes.txt`, then `cat` again.

7. **Break 2: a program that won't run.**
   ```
   cp /usr/bin/ls ~/myls
   ./myls
   chmod -x myls
   ./myls
   ```
   **They should see:** the copy of `ls` works, then `-bash: ./myls:
   Permission denied`. Fix it: `chmod +x myls`.

   **Say:** "A program is just a file with the `x` permission. Take away
   the `x`, and it's just bytes."

8. **Break 3: break `ls` for everyone.** This one uses `sudo`, so read it
   twice before pressing Enter:
   ```
   sudo chmod -x /usr/bin/ls
   ls
   ```
   **They should see:** `-bash: /usr/bin/ls: Permission denied`. **Say:**
   "Now nobody on this computer can use `ls`! How can we see the files?"
   Try `echo *`. *(It lists the files: the shell does it by itself.)* Fix
   it: `sudo chmod +x /usr/bin/ls`.

9. **Break 4: delete a program.**
   ```
   sudo rm /usr/games/cowsay
   cowsay moo
   ```
   **They should see:** `-bash: /usr/games/cowsay: No such file or
   directory`. Fix it with the package manager:
   ```
   sudo apt install --reinstall cowsay
   cowsay I am back
   ```
   **Say:** "The package manager remembers what every package should
   contain, so it can put back anything that's missing."

10. **Break 5: fire yourself.** The big one. **Say:** "What happens if the
    admin takes away their own admin powers?" Predict first! Then:
    ```
    sudo deluser LEARNER sudo
    exit
    ```
    (With the learner's name.) Log in again, then:
    ```
    groups
    sudo ls
    ```
    **They should see:** only their own name in `groups`, and after their
    password, `sam is not in the sudoers file.`

    Can they fix it? Let them try. *(They can't: putting someone back in
    the `sudo` group needs `sudo`!)* **Say:** "Some mistakes lock the door
    behind you. On a real computer, fixing this means starting it in a
    special rescue mode, or asking whoever else is an admin. That's why
    careful admins keep **backups**, and why we can reset the Sandbox."

    The guide, in `labs/sandbox`: `./sandbox.sh reset`. **They should
    see:** the learner can log in again, with their name as the password,
    and `sudo` works. Everything else they changed is gone too.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `E: Unable to locate package cowsy` | A typo in the package name | Check the spelling. `apt search cow` searches for packages. |
| `Temporary failure resolving 'archive.ubuntu.com'` | That package isn't saved in the Sandbox, and the computer is offline | Use one of the saved ones: `cowsay`, `figlet`, `sl` or `toilet`. |
| `cowsay: command not found` after installing | The command was typed before installing finished, or it was removed | `which cowsay`; reinstall if needed. |
| `-bash: /usr/games/cowsay: No such file or directory` after reinstalling | The shell remembered the old location | Type `hash -r`, or log out and in again. |
| `Sorry, try again.` after a reset | After a reset, the password is the learner's name again | Use the name, then change it with `passwd` if you like. |
| Something's broken and nobody knows why | That's what the Sandbox is for | The guide runs `./sandbox.sh reset`. |

## Talk about it

- What does a package manager do for you?
- Which break was the scariest? Which was the easiest to fix?
- Why couldn't Break 5 be fixed from inside?
- Why is it good to make mistakes in a sandbox?

## Challenge *(if there's time, or for next time)*

- `apt list --installed | wc -l` counts the installed packages. How many
  does the Sandbox have? *(Ignore the warning.)*
- Install `toilet`, then try `toilet -f mono12 -F metal HELLO` and other
  options from `toilet --help`.
- Invent a sixth break, *predict* how to fix it, and try it. (Ask the
  guide first if it involves `sudo rm`.)

## Checkpoint

The learner can, without help:
- [ ] Install, look inside and remove a package with `apt` and `dpkg`
- [ ] Explain why installing needs admin powers
- [ ] Break and fix a file's permissions and a program's `x` permission
- [ ] Explain why some mistakes can't be fixed from the inside

## Lab notebook

Make the "break it, fix it" table, with all five breaks. Add *package*,
*package manager*, *dependency* and *recovery* to the dictionary.

## Guide's background *(optional reading)*

`apt` downloads `.deb` package files from Ubuntu's servers, checks them,
and unpacks them with the lower-level `dpkg`, which keeps a database of
which files belong to which package. That database is why
`apt install --reinstall` can restore a deleted file.

The Sandbox image keeps four small packages (and their dependencies)
already downloaded, and keeps the package lists, so this lesson works
with no internet. If your computer is online, the Sandbox can also
download any other package; that's fine, but no lesson needs it.

Break 5 is the classic admin mistake. On a real Linux machine it's fixed
by booting into recovery mode (which gives a root shell without
`sudo`), or by another admin. On a Raspberry Pi, the guide could swap in
the spare SD card. The lesson that matters: the power to change
everything includes the power to lock yourself out, so think before
pressing Enter, and have a way back.

These breaks are chosen to be safe and instructive. Please don't let the
learner try `sudo rm -rf` on anything, even in the Sandbox: it's a habit
not worth practising.
