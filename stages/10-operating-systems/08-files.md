# Lesson 10.8: Files, Inodes and a Disk in a File

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; index cards and a pen; `~/lab/os` · **New words:** inode, hard
link, symbolic link, block, file system, `mkfs`, `debugfs`

## Goal *(read this to the learner)*

> The third of the kernel's big jobs is keeping things safe when the
> power goes off: **files**. A file turns out to be two things: a name,
> and an **inode**, the file's real self, which says where its blocks
> are on the disk. You'll give one file two names, and then make a whole
> disk inside a file, look at its insides, and discover that deleting a
> file doesn't wipe it.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Index cards: one for a "file's inode", and two or three for
      "names".

## Warm-up (5 min)

"What's the difference between a folder and a file?" Let them answer.
"Where's a file when the computer is switched off?" *(On the disk, as
magnetism or charges in memory chips: Stage 4's "persistence".)*

## Activity

### Session 1: names and inodes

1. **A file's number.**
   ```
   mkdir -p ~/lab/os/files
   cd ~/lab/os/files
   echo "Creepers are green" > notes.txt
   ls -i notes.txt
   stat notes.txt
   ```
   **They should see** a big number before `notes.txt`, and then from
   `stat` lines including:
   ```
     File: notes.txt
     Size: 19        	Blocks: 8          IO Block: 4096   regular file
   Device: 0,86	Inode: 21257693    Links: 1
   Access: (0644/-rw-r--r--)  Uid: ( 1001/     sam)   Gid: ( 1001/     sam)
   ```
   **Say:** "The big number is the file's **inode** number. The inode is
   the file's real self: it holds the size, the owner, the permissions,
   the times, and where the file's pieces are on the disk. What it
   *doesn't* hold is the name." Write "inode 21257693: 19 bytes, owner
   sam, blocks..." on one card.

2. **The name is in the folder.** **Say:** "A folder is just a list of
   names, each pointing to an inode number." On another card, write
   "folder `files`: notes.txt → 21257693" and draw the arrow to the
   inode card.

3. **Two names for one file.**
   ```
   ln notes.txt same.txt
   ls -li
   ```
   **They should see:** both names with the *same* inode number, and a
   `2` after the permissions:
   ```
   21257693 -rw-r--r-- 2 sam sam 19 Oct 23 23:12 notes.txt
   21257693 -rw-r--r-- 2 sam sam 19 Oct 23 23:12 same.txt
   ```
   **Say:** "`ln` made a **hard link**: a second name for the same inode.
   The 2 is the number of names." Add "same.txt → 21257693" to the folder
   card. Now:
   ```
   echo "and they go boom" >> same.txt
   cat notes.txt
   ```
   **They should see** both lines. **Ask:** "Why did `notes.txt`
   change?" *(It's the same file!)*

4. **Deleting a name.**
   ```
   rm notes.txt
   ls -li
   cat same.txt
   ```
   **They should see:** only `same.txt`, with `1` link now, and both
   lines still in it. **Say:** "`rm` doesn't delete files. It deletes a
   *name*. When a file has no names left (and nobody has it open), the
   kernel frees the inode and its blocks." Cross out the name on the
   card.

5. **A shortcut.**
   ```
   ln -s same.txt shortcut.txt
   ls -l
   cat shortcut.txt
   ```
   **They should see** `shortcut.txt -> same.txt`, and the two lines.
   **Say:** "That's a **symbolic link**: a tiny file whose content is
   the *name* of another file. Like a sign pointing the way." Now:
   ```
   rm same.txt
   cat shortcut.txt
   ```
   **They should see:** `cat: shortcut.txt: No such file or directory`.
   **Ask:** "Why? The shortcut's still there." *(It points to a name that
   doesn't exist any more: a broken sign.)*

### Session 2: everything is a file

6. **Devices.**
   ```
   ls -l /dev/null /dev/urandom /dev/sda /dev/nvme0n1
   ```
   (One of the last two will say `No such file or directory`: computers
   have one kind of disk or the other.) **They should see** lines that
   start with `c` or `b`, not `-`. **Say:** "These are *devices*,
   pretending to be files: `c` for character (a stream of bytes) and `b`
   for block (a disk). Reading or writing them talks to a driver in the
   kernel." Try:
   ```
   head -c 8 /dev/urandom | xxd
   echo "into the void" > /dev/null
   ```
   *(Eight random bytes, from the kernel's randomness; and `/dev/null`
   swallows everything.)*

7. **Your open files.**
   ```
   ls -l /proc/self/fd
   ```
   **They should see** `0`, `1` and `2` pointing at the terminal (like
   `/dev/pts/0`), and `3` pointing at a folder in `/proc`. **Say:** "The
   file descriptors from Lesson 10.2! This is `ls`'s list of open files,
   while it's running. 3 is the folder it's reading right now."

8. **Disks and mounting.**
   ```
   df -h /
   lsblk
   ```
   **They should see**, from `df`, the size of the main disk and how
   much is used; from `lsblk`, a tree of disks and their **partitions**
   (the pieces a disk is divided into). **Say:** "A partition holds a
   **file system**: the layout of inodes, folders and blocks. The kernel
   **mounts** it at a folder, and then the files appear there. `/` is
   the main one."

### Session 3: a disk in a file

9. **Make a disk.**
   ```
   cd ~/lab/os/files
   mkdir stuff
   echo "The diamonds are buried at 120, 12, -340" > stuff/secret.txt
   echo "Hello" > stuff/hello.txt
   mkfs.ext4 -q -d stuff disk.img 16M
   ls -l disk.img
   ```
   **They should see:** `Creating regular file disk.img`, and a 16 MB
   file (`16777216` bytes). **Say:** "`mkfs` makes a file system. Usually
   it's on a real disk, but it'll happily make one inside an ordinary
   file. `ext4` is the kind Linux uses, and `-d stuff` copies our folder
   into it."

10. **Look inside without mounting.** `debugfs` reads a file system
    directly:
    ```
    debugfs -R "ls -l" disk.img
    ```
    **They should see** (after a line `debugfs 1.47.0 (5-Feb-2023)`):
    ```
          2   40755 (2)      0      0    4096 23-Oct-2026 23:13 .
          2   40755 (2)      0      0    4096 23-Oct-2026 23:13 ..
         11   40700 (2)      0      0   16384 23-Oct-2026 23:13 lost+found
         12  100644 (1)   1001   1001       6 23-Oct-2026 23:13 hello.txt
         13  100644 (1)   1001   1001      41 23-Oct-2026 23:13 secret.txt
    ```
    **Say:** "The first number is the inode. In this little disk,
    `secret.txt` is inode 13." Now:
    ```
    debugfs -R "stat secret.txt" disk.img
    ```
    **They should see** a page about inode 13 (press `q` if it opens in
    a pager), ending with:
    ```
    EXTENTS:
    (0):1292
    ```
    **Say:** "The file's words are in block 1292 of the disk. Each block
    is 4096 bytes." (Your number may be different: use yours.) Read that
    block straight from the disk:
    ```
    dd if=disk.img bs=4096 skip=1292 count=1 status=none | strings
    ```
    **They should see:** `The diamonds are buried at 120, 12, -340`.
    **Ask:** "What does `skip=1292` do?" *(It jumps over 1292 blocks of
    4096 bytes: to byte 1292 × 4096.)*

11. **Delete it. Is it gone?**
    ```
    debugfs -w -R "rm secret.txt" disk.img
    debugfs -R "ls -l" disk.img
    dd if=disk.img bs=4096 skip=1292 count=1 status=none | strings
    ```
    **They should see:** `secret.txt` has gone from the list, but the
    `dd` line still prints the secret! **Say:** "Deleting took away the
    name, and marked the inode and the block as free. But nobody wiped
    the block. Until something new is written there, the words are still
    on the disk. That's how 'undelete' tools work, and why people who
    sell old computers wipe their disks properly." Commit what you wrote
    in the notebook (not `disk.img`: it's big).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `mkfs.ext4: command not found` or `debugfs: command not found` | They live in `/usr/sbin`, which isn't in the path here | Use `/usr/sbin/mkfs.ext4` and `/usr/sbin/debugfs`. |
| `ln: failed to create hard link 'same.txt': File exists` | There's already a `same.txt` | `rm same.txt`, or use another name. |
| `debugfs -R "stat secret.txt"` shows `File not found by ext2_lookup` | The name is wrong, or it's already deleted | Check with `debugfs -R "ls -l" disk.img`. |
| `dd` prints nothing | The block number is wrong | Use the number from *your* `EXTENTS:` line. |
| `The file disk.img does not exist and no size was specified.` | The size (`16M`) is missing | Add it at the end. |

## Talk about it

- What's an inode? What's *not* in it?
- What's the difference between a hard link and a symbolic link?
- Why doesn't `rm` really delete a file?
- What does "everything is a file" mean? Give three examples.

## Challenge *(if there's time, or for next time)*

- `debugfs -R "stat hello.txt" disk.img`: which block is it in? Read it
  with `dd`.
- What happens to a hard link's count when you `ln` a third name? Try
  it.
- `ls -id / /home ~`: what's special about the inode number of `/`?
  *(It's 2 on most ext4 disks, like the `.` in `disk.img`: the root
  folder.)*
- Make a disk with 100 small files in it (a `for` loop from Stage 5).
  Which inode numbers do they get?

## Checkpoint

The learner can, without help:
- [ ] Explain names and inodes with the cards
- [ ] Make a hard link and a symbolic link, and explain what `rm` does
      to each
- [ ] Make a file system in a file, and find a file's inode and block
      with `debugfs`
- [ ] Show that a deleted file's data can still be on the disk

## Lab notebook

Stick in the cards: the folder, the names and the inode. Write the
`EXTENTS` line and the `dd` command. Write, in one sentence, why
deleting isn't wiping. Commit. Add *inode*, *hard link*, *symbolic
link*, *block*, *file system*, *mkfs* and *debugfs* to `dictionary.md`.

## Guide's background *(optional reading)*

This covers OSTEP Chapters 39 ("Files and Directories") and 40 ("File
System Implementation"). OSTEP builds a tiny file system called vsfs
with the same parts: a superblock describing the disk, bitmaps of free
inodes and blocks, the inode table, and data blocks. ext4 adds
**extents** (a run of blocks described by its first block and length,
which is what `(0):1292` is: logical block 0 of the file is at disk
block 1292) and a **journal** that makes it safe to lose power in the
middle of a write (OSTEP Chapter 42).

`mkfs.ext4` and `debugfs` are in the `e2fsprogs` package, installed on
every Ubuntu-based system. Neither needs `sudo` here, because the "disk"
is an ordinary file the learner owns; mounting it *would* need `sudo`,
which is why this lesson uses `debugfs` instead.

Secure deletion is harder than it looks: on SSDs, the drive itself moves
data around behind the file system's back. Full-disk encryption (which
Pop!_OS offers when installing) is the reliable answer: without the
key, every block is noise.
