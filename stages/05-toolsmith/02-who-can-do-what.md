# Lesson 5.2: Who Can Do What

**Time:** 2 sessions of 45 min · **You need:** the Sandbox; the lab
notebook; the binary dot cards from Stage 4 · **New words:**
permission, owner, group, others, read, write, execute, `chmod`, `adduser`

## Goal *(read this to the learner)*

> Why couldn't you read root's folder? Why couldn't you peek at other
> miners' homes in the Mineshaft? Every file on a Linux computer has a
> little label saying who owns it and who may read it, change it, or run
> it. Today you'll learn to read those labels, change them, make new
> users in the Sandbox, and set up a secret chest that only your team can
> open. And it turns out the labels are written in binary!

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check the Sandbox is up: `./sandbox.sh status` (in `labs/sandbox`).

## Warm-up (5 min)

"In binary, what's `111`?" *(7.)* "`110`?" *(6.)* "`101`?" *(5.)*
"`100`?" *(4.)* Keep those in mind: they're coming back.

## Activity

### Session 1: reading and changing permissions

1. **Make a secret.** Log in to the Sandbox. Then:
   ```
   echo "my secret diamond stash: 64" > secret.txt
   ls -l secret.txt
   ```
   **They should see:** something like
   `-rw-rw-r-- 1 sam sam 28 Oct 22 23:01 secret.txt`.

2. **Read the label.** Write the first part big on paper and split it up:

   ```
   -    rw-     rw-     r--      sam     sam
   |    owner   group   others   owner   group
   file
   ```

   **Say:** "The first character is `-` for a file or `d` for a folder.
   Then three sets of three: what the **owner** can do, what the
   **group** can do, and what everyone else (**others**) can do. `r` is
   **read**, `w` is **write** (change), and `x` is **execute** (run it as
   a program, or go into a folder). A `-` means 'not allowed'."

   Ask: "Who can change `secret.txt`?" *(sam, and anyone in the group
   called sam.)* "Can others read it?" *(Yes: there's an `r` at the
   start of the others part. Not very secret!)*

3. **Take away your own permission.**
   ```
   chmod u-r secret.txt
   ls -l secret.txt
   cat secret.txt
   ```
   **They should see:** `--w-rw-r--` and then `cat: secret.txt: Permission
   denied`. Even the owner is locked out! Put it back:
   ```
   chmod u+r secret.txt
   ```
   **Say:** "`chmod` means 'change mode'. `u` is the user who owns it, `g`
   is the group, `o` is others. `+` gives a permission and `-` takes it
   away."

4. **Permissions are binary!** Write the three letters as three bits,
   with the dot card values 4, 2 and 1:

   ```
   r  w  x
   4  2  1
   ```

   | Letters | Bits | Number |
   |---|---|---|
   | `rwx` | 111 | 7 |
   | `rw-` | 110 | 6 |
   | `r-x` | 101 | 5 |
   | `r--` | 100 | 4 |
   | `---` | 000 | 0 |

   **Say:** "So `rw-r--r--` is 6, 4, 4: `644`. Programmers set all three
   at once with numbers." Try:
   ```
   chmod 600 secret.txt
   ls -l secret.txt
   ```
   **They should see:** `-rw-------`: only the owner can read or change
   it. **Now** it's secret.

   Ask them to work out: `755`? *(`rwxr-xr-x`: programs.)* `700`? *(Only
   the owner can do anything.)* `777`? *(Everyone can do everything:
   dangerous!)*

5. **Folders.** `ls -ld /home/sam` (with their name). **They should see:**
   `drwxr-x---`. **Say:** "For a folder, `r` means 'can see the list of
   files', and `x` means 'can go in'. Others have no permissions at all on
   your home folder, so nobody else can look inside it. That's how the
   Mineshaft stopped you from looking ahead."

6. **The system's secrets.**
   ```
   ls -l /etc/passwd /etc/shadow
   ```
   **They should see:** `/etc/passwd` is `-rw-r--r--` (everyone can read
   it), and `/etc/shadow` is `-rw-r-----` with group `shadow` (others
   can't). Owner `root` for both.

### Session 2: users and groups

7. **Make a new user.** **Say:** "As admin, you can make new accounts. Who
   should live in your Sandbox?" (A sibling? A Minecraft friend? Steve?)
   ```
   sudo adduser steve
   ```
   It asks for a new password for steve (type it twice), then a full name
   (type `Steve`), then Room Number, Work Phone, Home Phone and Other:
   press **Enter** to skip each one. Then `Is the information correct?
   [Y/n]`: type `y`.

   **They should see:** messages starting `info:`, including ``Creating
   home directory `/home/steve' ...``. Check: `tail -2 /etc/passwd` and
   `ls /home`.

8. **Be steve.**
   ```
   su - steve
   ```
   (`su` means "switch user". It asks for **steve's** password.) **They
   should see:** the prompt change to `steve@sandbox:~$`. Now try:
   ```
   whoami
   ls /home/sam
   cat /home/sam/secret.txt
   sudo ls
   ```
   **They should see:** `steve`, then `Permission denied` twice, and
   finally, after steve's password, `steve is not in the sudoers file.`

   **Say:** "Steve is an ordinary user, like you are on the family
   computer. He can't see your files, and he isn't an admin." Type `exit`
   to be yourself again.

9. **Groups: a secret chest for a team.** **Say:** "What if you *want*
   steve to share some files with you, but nobody else? You make a
   **group**."
   ```
   sudo addgroup miners
   sudo adduser steve miners
   sudo adduser sam miners
   sudo mkdir /srv/chest
   sudo chgrp miners /srv/chest
   sudo chmod 770 /srv/chest
   ls -ld /srv/chest
   ```
   (With the learner's name instead of `sam`.) **They should see:**
   `drwxrwx--- 2 root miners ... /srv/chest`.

   Now try `touch /srv/chest/hello.txt`. **They should see:** `touch:
   cannot touch '/srv/chest/hello.txt': Permission denied`!

   **Say:** "Why? Type `groups`." *(It doesn't show `miners` yet.)* "Your
   groups are decided when you log in. Log out and back in." Type `exit`,
   log in again with `ssh`, then:
   ```
   groups
   echo "Meet at the nether portal" > /srv/chest/note.txt
   su - steve -c "cat /srv/chest/note.txt"
   ```
   **They should see:** `miners` in the list, then (after steve's
   password) `Meet at the nether portal`. Steve can read it, but a user
   who isn't a miner couldn't.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `chmod: cannot access 'secret.txt': No such file or directory` | Wrong folder, or a typo | `ls` to check, and `cd ~`. |
| `chmod: changing permissions of '/etc/passwd': Operation not permitted` | Only the owner (or root) can change a file's permissions | That's root's file. Use `sudo` only if you really mean it. |
| ``fatal: The user `steve' already exists.`` | Steve's already been made | Use a different name, or carry on with steve. |
| `su: Authentication failure` | The password typed was the learner's, not steve's | `su` wants the password of the user you're switching *to*. |
| Still `Permission denied` in `/srv/chest` | Groups only update when you log in | `exit`, then `ssh` in again, and check `groups`. |
| `adduser` asks lots of questions | That's normal | Press Enter to skip the ones you don't need. |

## Talk about it

- What do `r`, `w` and `x` mean for a file? For a folder?
- Why is `chmod 777` a bad idea?
- How is a group like a team or a club?
- In the Mineshaft, why couldn't miner5 read miner6's home?

## Challenge *(if there's time, or for next time)*

- Make a folder `/srv/library` that everyone can read but only the
  `miners` can change. *(Group `miners`, mode `775`.)*
- Make a script file, and find out which `chmod` lets you run it with
  `./script`. *(It needs `x`: `chmod 755` or `chmod u+x`.)*
- Look at `ls -l /usr/bin/passwd`. There's an `s` where you'd expect an
  `x`. That's a special permission that lets ordinary users change their
  own password in `/etc/shadow`. Mineshaft level 13 uses the same trick
  (Lesson 5.8).

## Checkpoint

The learner can, without help:
- [ ] Read a permission label like `-rw-r--r--` and say who can do what
- [ ] Use `chmod` with letters (`u+x`) and with numbers (`644`)
- [ ] Explain why permissions are binary numbers
- [ ] Add a user and a group, and set up a folder only a group can use

## Lab notebook

Draw the permission label, split into its parts. Copy the `rwx` to
number table. Add *permission*, *owner*, *group*, *others*, *read*,
*write* and *execute* to the dictionary.

## Guide's background *(optional reading)*

Unix permissions are nine bits: read, write and execute for the owner,
the group and everyone else. Writing them as three octal (base 8) digits
is a direct use of Stage 4's binary, and it's why the numbers only go up
to 7. On Ubuntu, new files are usually `rw-rw-r--` (664) because each
user has their own private group; home folders are `rwxr-x---` (750).

`adduser` (a friendly front-end) asks questions; `useradd` is the
lower-level tool that doesn't. A user's groups are fixed when they log
in, which surprises everyone the first time; the learner meets that
here on purpose.

Everything done in this lesson disappears on `./sandbox.sh reset`, so
there's no harm in experimenting. The family computer works the same
way, which is why the learner's account there can't change system files.
