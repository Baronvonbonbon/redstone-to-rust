# Lesson 10.11: Install Linux by Hand: Arch in a VM

**Time:** 3–4 sessions of 45 min · **You need:** a terminal; QEMU; **the
internet** for Sessions 1 and 2 (about 2.5 GB of downloads); about 10 GB
of free disk space; the guide · **New words:** virtual machine,
partition, file system, mount, package manager, chroot, bootloader,
snapshot

## Goal *(read this to the learner)*

> Pop!_OS came already installed. Today you'll install a whole Linux
> yourself, piece by piece, inside a **virtual machine**: a pretend
> computer that runs in a window. You'll cut up its disk, make a file
> system, download the kernel and the programs, set up a bootloader, and
> make a user account. Then you'll start it, log in, and it's yours: a
> computer you can break and fix without any danger to the real one.

## Before the lesson *(guide, 30 min, online)*

- [ ] Read this whole lesson once. This is the one Stage 10 lesson that
      needs the internet (Sessions 1 and 2).
- [ ] From your own account: `./scripts/install-packages.sh --later` (it
      installs QEMU).
- [ ] Let the learner's account use **KVM**, the part of the kernel that
      makes virtual machines fast:
      ```
      sudo usermod -aG kvm LEARNER
      ```
      Then the learner must log out and back in. Check, as the learner:
      `ls -l /dev/kvm` should show `kvm` as the group, and `id` should
      list `kvm`.
- [ ] The VM will have a root password and a user password. Choose them
      with the learner and write them in the lab notebook: they're only
      for the VM.

## Warm-up (5 min)

"What's PID 1 on this computer?" *(`systemd`.)* "Where did it come
from? Who put Linux on this computer?" *(Someone installed it.)* "Today
you're the someone."

## Activity

### Session 1: a pretend computer

1. **What's a virtual machine?** **Say:** "QEMU pretends to be a whole PC:
   CPU, memory, disk, screen, keyboard and network card. The 'disk' is
   just a file on the real disk. KVM lets the pretend CPU run on the real
   one at full speed, with the kernel keeping it fenced in, like a
   process." Draw the real computer, with a box inside it labelled *VM*
   that has its own little CPU, memory and disk.

2. **Download Arch Linux.** Arch is a Linux you build up yourself, with
   only what you choose. Its installer comes as an **ISO**: a file that
   holds a whole CD.
   ```
   mkdir -p ~/lab/os/arch
   cd ~/lab/os/arch
   curl -LO https://geo.mirror.pkgbuild.com/iso/latest/archlinux-x86_64.iso
   curl -LO https://geo.mirror.pkgbuild.com/iso/latest/sha256sums.txt
   sha256sum -c --ignore-missing sha256sums.txt
   ```
   **They should see** a progress bar for the big download (about
   1.6 GB), then `archlinux-x86_64.iso: OK`. **Say:** "`sha256sum` makes
   a fingerprint of the file. If even one bit was wrong, the fingerprint
   would be completely different. `OK` means ours matches Arch's."

3. **A disk for the VM.**
   ```
   qemu-img create -f qcow2 arch.qcow2 20G
   ls -lh
   ```
   **They should see:** `Formatting 'arch.qcow2', fmt=qcow2 ...
   size=21474836480 ...`, and `arch.qcow2` in the list at only about
   200K. **Ask:** "A 20 GB disk in 200 KB?" *(The file only grows when
   the VM writes to it: it's lazy, like Lesson 10.5's memory.)*

4. **Start the installer.**
   ```
   qemu-system-x86_64 -enable-kvm -m 2G -smp 2 -cdrom archlinux-x86_64.iso -drive file=arch.qcow2,if=virtio -nic user,model=virtio-net-pci -boot d
   ```
   **Say:** "2 GB of memory, 2 CPUs, the ISO in the pretend CD drive,
   our disk, a network card, and `-boot d`: start from the CD." A window
   opens. **They should see** a menu; the first line, `Arch Linux install
   medium (x86_64, BIOS)`, is chosen, so press Enter (or wait). Lots of
   messages scroll past, and then:
   ```
   root@archiso ~ #
   ```
   **Say:** "You're root, in the installer. Nothing here is saved: it's
   all in memory. The `#` means root." Click in the window to type in it.
   (Ctrl+Alt+G lets go of the mouse.)

5. **Look around.**
   ```
   lsblk
   pacman -Sy
   ```
   **They should see** from `lsblk` a disk called `vda`, 20G, and `loop0`
   and `sr0` (the CD); from `pacman -Sy`, lines about `core` and `extra`
   downloading. **Say:** "`vda` is our empty disk. `pacman` is Arch's
   **package manager**, like `apt` on Pop!_OS: it just fetched the list
   of every program it can install. That means the network works."

6. **Cut the disk into a partition.** **Say:** "A disk is divided into
   **partitions**. We need just one, the whole disk." Type `fdisk
   /dev/vda`, then answer each question:

   | fdisk asks | Type |
   |---|---|
   | `Command (m for help):` | `n` (new partition) |
   | `Select (default p):` | Enter |
   | `Partition number (1-4, default 1):` | Enter |
   | `First sector (2048-41943039, default 2048):` | Enter |
   | `Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-41943039, default 41943039):` | Enter |
   | `Command (m for help):` | `w` (write it, and quit) |

   **They should see** `Created a new partition 1 of type 'Linux' and of
   size 20 GiB.`, and at the end `Syncing disks.` Check with `lsblk`:
   now there's `vda1` under `vda`.

7. **Make the file system, and mount it.**
   ```
   mkfs.ext4 /dev/vda1
   mount /dev/vda1 /mnt
   ```
   **Say:** "`mkfs.ext4`, as in Lesson 10.8, but on a real (pretend)
   disk this time. `mount` makes it appear at `/mnt`." Shut down for
   now if the session is over: `poweroff`. Next time, start again from
   step 4, and do `mount /dev/vda1 /mnt` again (the partition and file
   system are saved on `arch.qcow2`, but the installer forgets
   everything else).

### Session 2: install

8. **Install the system.** First check the disk is mounted: `lsblk`
   should show `/mnt` at the end of the `vda1` line. (If not, `mount
   /dev/vda1 /mnt`.) Then:
   ```
   pacstrap -K /mnt base linux grub nano sudo dhcpcd
   ```
   **Say:** "`pacstrap` installs packages into `/mnt`: `base` (the basic
   programs, and `systemd`), `linux` (the kernel), `grub` (the
   bootloader), `nano` (the editor), `sudo`, and `dhcpcd` (which gets an
   internet address)." **They should see** lots of downloading and
   installing, for a few minutes, ending at the prompt.

9. **The file system table.**
   ```
   genfstab -U /mnt >> /mnt/etc/fstab
   cat /mnt/etc/fstab
   ```
   **They should see** a line starting `UUID=` with `/` and `ext4`.
   **Say:** "This tells the new system which disk to mount where, when
   it starts. The UUID is the file system's own name, so it's found
   even if the disk is renamed."

10. **Step inside.**
    ```
    arch-chroot /mnt
    ```
    **They should see** the prompt change to `[root@archiso /]#`.
    **Say:** "**chroot** means change root: now `/` is the new system's
    disk. Every command from here on changes the new system, not the
    installer."

11. **Settings.** One at a time (use your own region and city: `ls
    /usr/share/zoneinfo` shows the regions, and `ls
    /usr/share/zoneinfo/America` the cities in one):
    ```
    ln -sf /usr/share/zoneinfo/America/Chicago /etc/localtime
    hwclock --systohc
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
    locale-gen
    echo "LANG=en_US.UTF-8" > /etc/locale.conf
    echo redstone > /etc/hostname
    ```
    **Say:** "The time zone is a symbolic link (Lesson 10.8!). `locale`
    is the language. And `redstone` is the computer's name." **They
    should see**, from `locale-gen`, `Generating locales...` and
    `en_US.UTF-8... done`.

12. **People.**
    ```
    passwd
    useradd -m -G wheel steve
    passwd steve
    echo '%wheel ALL=(ALL:ALL) ALL' > /etc/sudoers.d/wheel
    ```
    (Use the learner's own choice of name instead of `steve`, here and
    later.) `passwd` asks twice for the new password, and shows nothing
    while you type: that's normal. **Say:** "Root's password first, then
    a new user, in the group `wheel`, with their own password. The last
    line lets people in `wheel` use `sudo`."

13. **The network, and the bootloader.**
    ```
    systemctl enable dhcpcd
    grub-install --target=i386-pc /dev/vda
    grub-mkconfig -o /boot/grub/grub.cfg
    ```
    **They should see:** a `Created symlink` line; `Installation
    finished. No error reported.`; and from `grub-mkconfig`, `Found linux
    image: /boot/vmlinuz-linux` and, at the end, `done`. (A warning that
    `os-prober will not be executed` is fine: it looks for other
    operating systems, and this disk has none.) **Say:** "`systemctl enable`
    tells PID 1 to start `dhcpcd` at every boot. GRUB goes at the very
    start of the disk, where the firmware looks first."

14. **Out, and off.**
    ```
    exit
    umount -R /mnt
    poweroff
    ```
    The QEMU window closes.

### Session 3: your own Linux

15. **Boot it.** No CD this time:
    ```
    cd ~/lab/os/arch
    qemu-system-x86_64 -enable-kvm -m 2G -smp 2 -drive file=arch.qcow2,if=virtio -nic user,model=virtio-net-pci
    ```
    **They should see** the GRUB menu (`*Arch Linux`), kernel messages,
    `[  OK  ]` lines, and then:
    ```
    redstone login:
    ```
    Log in as `steve` (or their name). **They should see** the prompt
    `[steve@redstone ~]$`. **Say:** "You installed that. All of it."

16. **A script to start it.** Typing that long command every time is
    tiring. In a terminal on Pop!_OS, make `~/lab/os/arch/run-arch.sh`:
    ```
    #!/bin/bash
    cd ~/lab/os/arch
    qemu-system-x86_64 -enable-kvm -m 2G -smp 2 -drive file=arch.qcow2,if=virtio -nic user,model=virtio-net-pci
    ```
    and `chmod +x ~/lab/os/arch/run-arch.sh` (Stage 5).

17. **Explore.** In the VM:
    ```
    ps -p 1
    systemd-analyze
    lsblk
    free -h
    ip -brief address
    ```
    **They should see** `1 ?  00:00:00 systemd`, a line like `Startup
    finished in 1.2s (kernel) + 0.9s (initrd) + 2.3s (userspace) = ...`,
    `vda1` mounted at `/`, about 2 GB of memory, and an address like
    `10.0.2.15/24` on a network card called `ens3`. **Ask:** "What's PID
    1?" *(`systemd`.)* "How long did it take to start?" "How much memory does it think it has?" *(About 2 GB: what
    QEMU gave it.)* Then something fun:
    ```
    sudo pacman -S fastfetch
    fastfetch
    ```
    (The first time, `sudo` prints a short lecture, "Respect the privacy
    of others. Think before you type. With great power comes great
    responsibility.": read it together, it's the Hacker's Pledge in three
    lines. Then it asks for steve's password, and `pacman` asks `::
    Proceed with installation? [Y/n]`: press Enter.) **They should see**
    from `fastfetch` a summary of the VM, with the Arch logo: the
    operating system, the kernel, the memory and more.

18. **Snapshots: a save point.** `poweroff` the VM. On Pop!_OS:
    ```
    qemu-img snapshot -c fresh ~/lab/os/arch/arch.qcow2
    qemu-img snapshot -l ~/lab/os/arch/arch.qcow2
    ```
    **They should see** a table with one snapshot, `fresh`. **Say:**
    "That's a save point, like in a game. If you ever break the VM, go
    back to it with `qemu-img snapshot -a fresh ~/lab/os/arch/arch.qcow2`
    (with the VM off)." Write it in the notebook.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Could not access KVM kernel module: Permission denied` | The learner's account isn't in the `kvm` group yet | See "Before the lesson"; log out and back in. |
| `Could not access KVM kernel module: No such file or directory` | Virtualization is switched off in the computer's firmware | Ask the guide: it's a setting called VT-x, AMD-V or SVM in the firmware setup. Or leave out `-enable-kvm` (it works, but very slowly). |
| `archlinux-x86_64.iso: FAILED` | The download was damaged | Delete it and download it again. |
| Typing does nothing in the window | The window doesn't have the keyboard | Click inside it. Ctrl+Alt+G lets go again. |
| `error: failed retrieving file` or `Could not resolve host` | No internet in the VM | Check the internet on Pop!_OS; start QEMU with the `-nic` part exactly as shown. |
| `mount` gives an error about `/dev/vda1` | The partition wasn't made (or not written with `w`) | Check `lsblk`, and do step 6 again. |
| `grub-install: error: install device isn't specified.` | `/dev/vda` is missing from the end | Type the whole line. |
| The VM boots back into the installer | It was started with `-cdrom` and `-boot d` | Use the step 15 command. |
| GRUB shows `error: no such device` or `grub rescue>` | `grub-mkconfig` wasn't run, or ran outside the chroot | Boot the installer again, `mount /dev/vda1 /mnt`, `arch-chroot /mnt`, and do step 13 again. |
| `Login incorrect` | Wrong name or password (capitals count) | Try again; the notebook has them. |

## Talk about it

- What's a virtual machine? Why is it safe to break?
- What did each step make: the partition, the file system, `pacstrap`,
  the `fstab`, GRUB?
- What does chroot do?
- What's the difference between the installer and the installed system?

## Challenge *(if there's time, or for next time)*

- Install `htop` and `tree` in the VM with `pacman`. `pacman -Ss game`
  searches for packages: install one and play it in the VM.
- Look at the boot messages: `journalctl -b | less` (with `sudo`), and
  find where `systemd` started `dhcpcd`.
- Add a second user for someone else in the family.
- Make a snapshot, then do something drastic in the VM (delete
  `/etc/hostname` with `sudo rm /etc/hostname`, and reboot: what's the
  computer called now?), then go back to the snapshot.

## Checkpoint

The learner can, without help:
- [ ] Explain what a virtual machine is, and start one with QEMU
- [ ] Explain each install step: partition, file system, mount,
      `pacstrap`, `fstab`, chroot, settings, users, bootloader
- [ ] Boot and log in to their own Arch Linux
- [ ] Make a snapshot, and say how to go back to it

## Lab notebook

Write the VM's passwords (only for the VM!). Draw the disk: `vda`,
`vda1`, ext4, mounted at `/`. List the install steps in order, each with
one sentence. Stick in the snapshot commands. Commit (not the ISO or
`arch.qcow2`: they're huge). Add *virtual machine*, *partition*, *file
system*, *mount*, *package manager*, *chroot*, *bootloader* and
*snapshot* to `dictionary.md`.

## Guide's background *(optional reading)*

These steps follow the Arch Wiki's *Installation guide*, simplified for
a virtual machine: a BIOS-style (MBR) disk with one partition and no
swap, GRUB for BIOS, and `dhcpcd` for the network. The Arch Wiki is one
of the best Linux references there is, for any distribution. Arch is
"rolling": `pacman -Syu` updates everything to the latest, which is why
the ISO name has no version here and the lesson downloads `latest`.

The lesson leaves out `linux-firmware` (the files real hardware needs:
a VM doesn't) to save about 300 MB. The VM uses QEMU's "user mode"
network, which needs no setup and no `sudo`; the VM can reach the
internet, but nothing can reach the VM.

A VM is a strong fence: programs in it can't see or harm Pop!_OS. It's
the right place for experiments that might break things, and for the
system administration that Stage 11 builds on. The disk image grows as
it's used: after this lesson it's about 1.5 GB (`du -h arch.qcow2`).
The tested install was checked with the same commands, step by step,
in QEMU.
