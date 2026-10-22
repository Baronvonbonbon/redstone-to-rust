# Lesson 5.1: My Own Computer

**Time:** 2 sessions of 40 min · **You need:** the Sandbox running (see
below); a terminal; the lab notebook · **New words:** admin, root,
`sudo`, sandbox, container

## Goal *(read this to the learner)*

> On the family computer, you're not the boss: you can't install
> programs or change system files, and that's on purpose. Today you get a
> computer where you **are** the boss: the **Sandbox**. You'll be its
> admin, with the power to change anything at all, and even to break it.
> Breaking it is allowed! A Toolsmith learns how computers work by taking
> them apart, and the Sandbox can always be put back as new.

## Before the lesson *(guide, 20 min the first time)*

- [ ] Read this whole lesson once.
- [ ] **Once, while online**, from **your own** account, build the Sandbox
      (about 5 minutes). Use the learner's account name:
      ```
      cd labs/sandbox
      ./sandbox.sh build LEARNER
      ./sandbox.sh start
      ```
      **You should see:** `The Sandbox is on. Learner logs in with:  ssh
      LEARNER@localhost -p 2222`. It starts by itself after a reboot.
- [ ] Learn the one command that fixes everything:
      `./sandbox.sh reset` throws the Sandbox away and makes a brand-new
      one in a few seconds. Everything the learner changed inside it is
      gone, and the password goes back to the learner's name.
- [ ] If you have a Raspberry Pi or prefer a virtual machine, see
      [SETUP.md](../../docs/SETUP.md) ("A breakable computer"). The lessons
      work the same way on those; only the `ssh` command is different.

## Warm-up (5 min)

"In the Mineshaft, how did you get onto another computer?" *(`ssh`.)*
"What's your account on the family computer allowed to do? What isn't
it?" *(It can make its own files. It can't install programs or change
other people's files.)*

## Activity

### Session 1: logging in, and the keys to the kingdom

1. **Log in.** In a terminal:
   ```
   ssh LEARNER@localhost -p 2222
   ```
   (With the learner's name.) The first time, it asks `Are you sure you
   want to continue connecting (yes/no/[fingerprint])?`: type `yes`. The
   password is the learner's name. **They should see:** a welcome
   message that says `Welcome to the SANDBOX`, and a prompt like
   `sam@sandbox:~$`.

   **Say:** "Look at the prompt: you're `sam`, on a computer called
   `sandbox`. It's a little computer running inside this one, like the
   Mineshaft. A computer inside a computer like this is called a
   **container**."

2. **Make it yours: a new password.** Type `passwd`. It asks for the
   current password (the learner's name), then a new one, twice. Nothing
   shows while typing. **They should see:** `passwd: password updated
   successfully`.

   **Say:** "Pick a password you'll remember, but that's not your name. In
   the Sandbox, you need it a lot."

   Write it on the inside cover of the lab notebook. (If it's forgotten,
   the guide's `./sandbox.sh reset` sets it back to the learner's name.)

3. **Who am I here?**
   ```
   whoami
   hostname
   groups
   ```
   **They should see:** their name, `sandbox`, and `sam sudo`.

   **Say:** "You're in a group called `sudo`. That's the group of people
   allowed to be the **admin**: the boss of the computer."

4. **The locked room.** Every Linux computer has a super-user called
   **root**, who can do *anything*. Try:
   ```
   ls /root
   ```
   **They should see:** `ls: cannot open directory '/root': Permission
   denied`. That's root's home folder.

   Now:
   ```
   sudo ls /root
   ```
   It asks `[sudo] password for sam:` (their new password). **They should
   see:** nothing at all, because root's folder is empty. But this time,
   no "Permission denied"!

   ```
   sudo whoami
   ```
   **They should see:** `root`.

   **Say:** "`sudo` means '**s**uper-user **do**': do this one command as
   root. It asks for *your* password, to check it's really you at the
   keyboard. On the family computer, you're not in the `sudo` group, so it
   won't work there."

5. **The Toolsmith's rules.** Read these together, and write them in the
   notebook:
   1. In the Sandbox, you may change and break anything. That's what it's
      for.
   2. **Read the command before you press Enter**, especially with `sudo`.
      Root's commands never ask "are you sure?".
   3. Use `sudo` only when you need it, for one command at a time.
   4. Never use these powers on a computer that isn't yours, or without
      permission. (Like the Hacker's Pledge.)
   5. If something is broken and you can't fix it, tell the guide. A reset
      takes seconds, and broken is how we learn.

### Session 2: a tour of a whole computer

6. **The top of the tree.** In the Sandbox:
   ```
   cd /
   ls
   ```
   **They should see:** folders like `bin`, `etc`, `home`, `root`, `tmp`,
   `usr` and `var`. Visit some of them and write a one-line note for each:

   | Folder | What's in it |
   |---|---|
   | `/home` | Everyone's home folders. *(`ls /home`)* |
   | `/root` | Root's home folder. |
   | `/etc` | Settings for the whole computer. *(`ls /etc`, then `cat /etc/hostname`)* |
   | `/usr/bin` | Programs. *(`ls /usr/bin \| wc -l`: hundreds!)* |
   | `/tmp` | Temporary files, for anyone. |
   | `/var/log` | Logs: the computer's diary. *(`ls /var/log`)* |

   **Say:** "Every Linux computer, from a Raspberry Pi to a giant server,
   has this same tree. Once you know it, you can find your way around any
   of them."

7. **Who else lives here?**
   ```
   cat /etc/passwd
   ```
   **They should see:** lots of lines, one per account, with the
   learner's near the end, like `sam:x:1000:1000::/home/sam:/bin/bash`.
   **Say:** "Most of these aren't people. They're accounts that programs
   use, so each program only has the powers it needs. Despite the name,
   there are no passwords in this file. They're kept, scrambled, in
   `/etc/shadow`." Try `cat /etc/shadow` *(Permission denied)*, then
   `sudo cat /etc/shadow`. **Say:** "The scrambled passwords can't be
   unscrambled. That's Stage 11's story."

8. **How big is it?**
   ```
   df -h /
   free -h
   ```
   **Say:** "`df` shows disk space and `free` shows memory (the `h` means
   'human-friendly sizes'). These numbers are actually the *real*
   computer's: the Sandbox shares them."

9. **Leave.** Type `exit`. **They should see:** the family computer's
   prompt again.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ssh: connect to host localhost port 2222: Connection refused` | The Sandbox isn't running | The guide runs `./sandbox.sh start` (or `./sandbox.sh status` to check). |
| `Permission denied, please try again.` | Wrong password | It's the learner's name the first time, then their new password. Forgotten? The guide runs `./sandbox.sh reset`. |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | The guide rebuilt the Sandbox, so it has a new identity | Safe here: `ssh-keygen -R '[localhost]:2222'`, then log in again. |
| `sam is not in the sudoers file.` | The learner removed themselves from the `sudo` group | That can't be fixed from inside. The guide runs `./sandbox.sh reset`. |
| `passwd: Authentication token manipulation error` and `password unchanged` | The current password was typed wrong | Run `passwd` again, carefully. |
| `You must choose a longer password.` | The new password is too short | Type a longer one when it asks again. Eight or more characters is a good rule. |
| The prompt says the family computer's name | Not logged in to the Sandbox (or logged out) | Run the `ssh` command again. |

## Talk about it

- What's the difference between you and root?
- Why do you think the family computer doesn't let your account use
  `sudo`?
- Why is it OK to break the Sandbox, but not the family computer?

## Challenge *(if there's time, or for next time)*

- `cat /etc/os-release`: which Linux is the Sandbox?
- `ls -l /usr/bin | wc -l` counts programs. Which three have the funniest
  names?
- `sudo` remembers your password for about 15 minutes. Find out how to
  make it forget straight away. *(Read `sudo --help` and look for `-k`.)*

## Checkpoint

The learner can, without help:
- [ ] Log in to the Sandbox and change their password
- [ ] Explain what root is, and what `sudo` does
- [ ] Name five top-level folders and what's in them
- [ ] Say the Toolsmith's rules in their own words

## Lab notebook

Copy the Toolsmith's rules and the folder table. Add *admin*, *root*,
*sudo*, *sandbox* and *container* to the dictionary.

## Guide's background *(optional reading)*

The Sandbox is a **Docker container**: a sealed-off part of your
computer that looks to the learner like a whole separate Linux machine,
with its own users, files and root account. Being root inside it gives
no power over your real computer: it can't see your files, and nothing
it does survives `./sandbox.sh reset`. The learner never needs to be in
the `docker` group (which would be as powerful as being your admin);
they only `ssh` in, exactly like the Mineshaft.

It's built from Ubuntu 24.04, with the manual pages, `nano`, `vim`,
`git`, `python3` and `sqlite3`, and a few packages saved for Lesson 5.3,
so it works with no internet. If your computer *is* online, the Sandbox
can download packages too; nothing in the lessons depends on that.

A Raspberry Pi or a virtual machine is an even more "real" breakable
computer (it boots, has its own kernel, and you can pull the plug). If
you have one, the lessons work the same; see SETUP.md. Many families
start with the Sandbox and add a Pi later.

`sudo` asking for the user's own password (not root's) is a Ubuntu and
Raspberry Pi OS convention. The point is to make admin actions
deliberate: one command at a time, by someone who's proved they're at
the keyboard.
