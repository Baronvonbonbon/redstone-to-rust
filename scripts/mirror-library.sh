#!/bin/bash
# Download the course's free/open books, games and tools into one folder
# that every account on the computer can read, so lessons work offline.
#
#   sudo mkdir -p /srv/redstone-library && sudo chown "$USER" /srv/redstone-library
#   ./scripts/mirror-library.sh [/srv/redstone-library]
#
# Safe to re-run: existing downloads are skipped and git repos are updated.
# Some things can't be fetched by a script (OpenStax PDFs, for example);
# those are listed at the end for you to download by hand.
set -uo pipefail

LIB=${1:-/srv/redstone-library}
mkdir -p "$LIB"/{games,books,tools,repos} || { echo "Can't write to $LIB (see the comment at the top)."; exit 1; }
failed=()

clone() { # clone URL DIR
  local dest="$LIB/$2"
  if [[ -d "$dest/.git" ]]; then git -C "$dest" pull -q --ff-only || failed+=("$1")
  else git clone -q --depth 1 "$1" "$dest" || failed+=("$1"); fi
}
fetch() { # fetch URL FILE
  local dest="$LIB/$2"
  [[ -s "$dest" ]] && return
  curl -fsSL -o "$dest" "$1" || { rm -f "$dest"; failed+=("$1"); }
}

echo "Games (Stages 1, 5)..."
clone https://gitlab.com/slackermedia/bashcrawl.git          games/bashcrawl
clone https://github.com/mprat/Terminus.git                  games/terminus
clone https://github.com/veltman/clmystery.git               games/clmystery
clone https://github.com/NUKnightLab/sql-mysteries.git       games/sql-mysteries

echo "Tools (Stages 4, 6)..."
fetch https://github.com/hneemann/Digital/releases/download/v0.31/Digital.zip  tools/Digital.zip
fetch https://github.com/hneemann/Digital/releases/download/v0.31/Doc_English.pdf tools/Digital-manual.pdf
[[ -d "$LIB/tools/Digital" ]] || (cd "$LIB/tools" && unzip -q Digital.zip) || failed+=("unzip Digital.zip")

echo "Nand to Tetris software suite (Stages 6, 8)..."
# The desktop version (2.7), from the Google Drive link on nand2tetris.org/software.
N2T_ZIP="https://drive.usercontent.google.com/download?id=1xZzcMIUETv3u3sdpM_oTJSTetpVee3KZ&export=download&confirm=t"
if [[ ! -x "$LIB/tools/nand2tetris/tools/HardwareSimulator.sh" ]]; then
  fetch "$N2T_ZIP" tools/nand2tetris.zip
  if unzip -tq "$LIB/tools/nand2tetris.zip" >/dev/null 2>&1; then
    # The zip's scripts aren't marked as programs, so mark them.
    (cd "$LIB/tools" && unzip -qo nand2tetris.zip -x '__MACOSX/*' && chmod +x nand2tetris/tools/*.sh) \
      || failed+=("unzip nand2tetris.zip")
  else
    rm -f "$LIB/tools/nand2tetris.zip"; failed+=("Nand to Tetris zip (see the hand download list)")
  fi
fi

echo "Books (PDFs)..."
fetch https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download books/the-linux-command-line.pdf
fetch https://greenteapress.com/thinkpython2/thinkpython2.pdf books/think-python-2e.pdf
fetch https://richardhammack.github.io/BookOfProof/Main.pdf  books/book-of-proof.pdf
fetch https://courses.csail.mit.edu/6.042/spring18/mcs.pdf  books/mathematics-for-computer-science.pdf

echo "Books and courses (source repos)..."
clone https://github.com/missing-semester/missing-semester.git repos/missing-semester
clone https://github.com/rust-lang-nursery/rust-cookbook.git   repos/rust-cookbook
clone https://github.com/google/comprehensive-rust.git          repos/comprehensive-rust
clone https://github.com/rust-embedded/book.git                 repos/embedded-rust-book
clone https://github.com/phil-opp/blog_os.git                   repos/writing-an-os-in-rust
clone https://github.com/munificent/craftinginterpreters.git   repos/crafting-interpreters
clone https://github.com/SystemsApproach/book.git               repos/computer-networks-systems-approach
clone https://github.com/mit-pdos/xv6-riscv.git                 repos/xv6-riscv
clone https://github.com/ossu/computer-science.git              repos/ossu-computer-science

chmod -R a+rX "$LIB"

cat <<EOF

Library is in $LIB

Download these by hand (open the page, use its Download/PDF button) into $LIB/books:
  - OpenStax Introduction to Python Programming   openstax.org/details/books/introduction-python-programming
  - OpenStax Introduction to Computer Science     openstax.org/details/books/introduction-computer-science
  - OpenStax math books for the math track        see docs/MATH-TRACK.md
  - Invent Your Own Computer Games with Python    inventwithpython.com/invent4thed/  (free to read online)
  - Only if the Nand to Tetris download failed:   nand2tetris.org/software, "Software package" (desktop
    version). Unzip it in $LIB/tools/ so that $LIB/tools/nand2tetris/tools/ exists, then run
    chmod +x $LIB/tools/nand2tetris/tools/*.sh
  - OSTEP chapters (Stage 10)                     pages.cs.wisc.edu/~remzi/OSTEP/

The Rust books come with Rust itself: in Stage 9, 'rustup doc' opens them offline.
EOF

if ((${#failed[@]})); then
  echo; echo "These failed (check your connection and re-run):"; printf '  %s\n' "${failed[@]}"; exit 1
fi
