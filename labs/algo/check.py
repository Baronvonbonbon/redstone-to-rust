#!/usr/bin/env python3
"""The Stage 7 checker: tries your functions on lots of cases.

Run it in ~/lab/algo, next to your own files:

    python3 check.py          # lists the checks
    python3 check.py search   # checks searching.py

It never changes your files.
"""
import importlib
import os
import random
import signal
import sys
import traceback

sys.path.insert(0, os.getcwd())
sys.dont_write_bytecode = True


class Fail(Exception):
    """One case gave the wrong answer."""


class TooSlow(Exception):
    pass


def on_alarm(signum, frame):
    raise TooSlow()


def load(module_name, *names):
    """Imports the learner's file, and checks the functions are there."""
    filename = module_name + ".py"
    if not os.path.exists(filename):
        print(f"There's no {filename} in this folder ({os.getcwd()}).")
        print("Run the checker from the folder your file is in.")
        sys.exit(1)
    try:
        module = importlib.import_module(module_name)
    except Exception:
        print(f"{filename} has a problem before any checks could run:")
        print()
        traceback.print_exc(limit=-1, file=sys.stdout)
        sys.exit(1)
    missing = [n for n in names if not hasattr(module, n)]
    if missing:
        print(f"{filename} has no {' or '.join(missing)} yet.")
        print("Check the spelling: the names must match the lesson exactly.")
        sys.exit(1)
    return module


def show(value):
    text = repr(value)
    return text if len(text) <= 70 else text[:67] + "..."


def expect(call, got, want):
    if got != want:
        raise Fail(f"{call} gave {show(got)}, but it should be {show(want)}.")


# --- Counting helpers ----------------------------------------------------

class CountingList(list):
    """A list that counts how many items are looked at."""
    looks = 0

    def __getitem__(self, i):
        result = list.__getitem__(self, i)
        CountingList.looks += len(result) if isinstance(i, slice) else 1
        return result

    def __iter__(self):
        CountingList.looks += len(self)
        return list.__iter__(self)

    def __contains__(self, x):
        CountingList.looks += len(self)
        return list.__contains__(self, x)

    def index(self, *args):
        CountingList.looks += len(self)
        return list.index(self, *args)


class Num:
    """A number that counts how many times it's compared."""
    compares = 0

    def __init__(self, n):
        self.n = n

    def _count(self, other):
        Num.compares += 1
        return other.n if isinstance(other, Num) else other

    def __lt__(self, other): return self.n < self._count(other)
    def __le__(self, other): return self.n <= self._count(other)
    def __gt__(self, other): return self.n > self._count(other)
    def __ge__(self, other): return self.n >= self._count(other)
    def __eq__(self, other): return self.n == (other.n if isinstance(other, Num) else other)
    def __hash__(self): return hash(self.n)
    def __repr__(self): return repr(self.n)


def calls_itself(fn):
    return fn.__name__ in fn.__code__.co_names


# --- The checks ----------------------------------------------------------

def check_search():
    m = load("searching", "linear_search", "binary_search")
    for name in ["linear_search", "binary_search"]:
        fn = getattr(m, name)
        expect(f"{name}([5], 5)", fn([5], 5), 0)
        expect(f"{name}([], 5)", fn([], 5), None)
        expect(f"{name}([2, 4, 6, 8], 2)", fn([2, 4, 6, 8], 2), 0)
        expect(f"{name}([2, 4, 6, 8], 8)", fn([2, 4, 6, 8], 8), 3)
        expect(f"{name}([2, 4, 6, 8], 6)", fn([2, 4, 6, 8], 6), 2)
        expect(f"{name}([2, 4, 6, 8], 5)", fn([2, 4, 6, 8], 5), None)
        expect(f"{name}([2, 4, 6, 8], 1)", fn([2, 4, 6, 8], 1), None)
        expect(f"{name}([2, 4, 6, 8], 9)", fn([2, 4, 6, 8], 9), None)
        items = list(range(0, 300, 3))
        for target in range(-1, 301):
            want = target // 3 if target % 3 == 0 and 0 <= target < 300 else None
            expect(f"{name}(the multiples of 3 up to 297, {target})",
                   fn(items, target), want)
        print(f"  {name}: right every time.")
    expect("linear_search([7, 3, 9, 3], 3)", m.linear_search([7, 3, 9, 3], 3), 1)

    big = CountingList(range(1_000_000))
    for name in ["linear_search", "binary_search"]:
        CountingList.looks = 0
        getattr(m, name)(big, 999_999)
        print(f"  {name} found 999,999 in a million numbers"
              f" after {CountingList.looks:,} looks.")
        if name == "binary_search" and CountingList.looks > 100:
            raise Fail("binary_search looked at too many numbers: it should"
                       " need only about 20 halvings. Is it really halving?")


def check_sort(m, name, sizes=(1000,)):
    fn = getattr(m, name)
    cases = [[], [1], [2, 1], [1, 2], [3, 1, 2], [5, 5, 5], [4, 2, 4, 1, 2],
             [-3, 10, 0, -7], list(range(10)), list(range(10, 0, -1))]
    rng = random.Random(7)
    cases += [[rng.randint(-50, 50) for _ in range(rng.randint(5, 60))]
              for _ in range(40)]
    for case in cases:
        got = fn(list(case))
        expect(f"{name}({show(case)})", got, sorted(case))
    for n in sizes:
        for label, numbers in [("shuffled", rng.sample(range(n), n)),
                               ("already sorted", list(range(n)))]:
            Num.compares = 0
            try:
                got = fn([Num(x) for x in numbers])
            except RecursionError:
                raise Fail(f"{name} crashed with a RecursionError on {n:,}"
                           f" numbers that were {label}. Lesson 7.7 explains"
                           " why!")
            if [x.n if isinstance(x, Num) else x for x in got] != sorted(numbers):
                raise Fail(f"{name} got {n} {label} numbers wrong.")
            print(f"  {name}: {n:,} {label} numbers took"
                  f" {Num.compares:,} comparisons.")
    print(f"  {name}: right every time.")


def check_sorts():
    m = load("sorting", "selection_sort", "insertion_sort")
    check_sort(m, "selection_sort")
    check_sort(m, "insertion_sort")


def check_recursion():
    m = load("recursion", "factorial", "total", "reverse")
    for name in ["factorial", "total", "reverse"]:
        if not calls_itself(getattr(m, name)):
            raise Fail(f"{name} doesn't call itself. Today it has to be"
                       " recursive: no loops!")
    for n, want in [(0, 1), (1, 1), (2, 2), (3, 6), (5, 120), (10, 3628800)]:
        expect(f"factorial({n})", m.factorial(n), want)
    for items in [[], [7], [1, 2, 3], [10, -4, 5, 5], list(range(101))]:
        expect(f"total({show(items)})", m.total(items), sum(items))
    for text in ["", "a", "ab", "creeper", "racecar", "Captain Underpants"]:
        expect(f"reverse({text!r})", m.reverse(text), text[::-1])
    print("  factorial, total and reverse: right every time.")


def check_merge():
    m = load("sorting", "merge", "merge_sort")
    for a, b in [([], []), ([1], []), ([], [1]), ([1, 3], [2]), ([2], [1, 3]),
                 ([1, 4, 9], [2, 3, 10, 11]), ([5, 5], [5]), ([-2, 0], [-1])]:
        expect(f"merge({a}, {b})", m.merge(list(a), list(b)), sorted(a + b))
    print("  merge: right every time.")
    if not calls_itself(m.merge_sort):
        raise Fail("merge_sort doesn't call itself: it should sort each half"
                   " with merge_sort.")
    check_sort(m, "merge_sort", sizes=(1000, 100_000))


def check_quick():
    m = load("sorting", "quick_sort")
    check_sort(m, "quick_sort", sizes=(1000,))


def check_brackets():
    m = load("stacks", "brackets_ok")
    for text, want in [("", True), ("()", True), ("[]", True), ("{}", True),
                       ("([]{})", True), ("print(len([1, 2]))", True),
                       ("{[()()]}", True), ("(", False), (")", False),
                       ("(]", False), ("([)]", False), ("((", False),
                       ("())", False), ("print(len([1, 2])", False),
                       ("}{", False), ("no brackets at all", True)]:
        expect(f"brackets_ok({text!r})", m.brackets_ok(text), want)
    print("  brackets_ok: right every time.")


def check_linked():
    m = load("linked", "Node", "length", "to_list", "push_front", "contains")
    Node = m.Node
    chain = Node("creeper", Node("zombie", Node("skeleton")))
    expect("length(None)", m.length(None), 0)
    expect("length(creeper -> zombie -> skeleton)", m.length(chain), 3)
    expect("to_list(None)", m.to_list(None), [])
    expect("to_list(creeper -> zombie -> skeleton)", m.to_list(chain),
           ["creeper", "zombie", "skeleton"])
    expect("contains(None, 'zombie')", m.contains(None, "zombie"), False)
    expect("contains(creeper -> zombie -> skeleton, 'zombie')",
           m.contains(chain, "zombie"), True)
    expect("contains(creeper -> zombie -> skeleton, 'skeleton')",
           m.contains(chain, "skeleton"), True)
    expect("contains(creeper -> zombie -> skeleton, 'pig')",
           m.contains(chain, "pig"), False)
    head = None
    for x in [3, 2, 1]:
        head = m.push_front(head, x)
    if not isinstance(head, Node):
        raise Fail(f"push_front should give back the new first Node, but it"
                   f" gave {show(head)}.")
    expect("pushing 3, then 2, then 1, onto an empty list", m.to_list(head),
           [1, 2, 3])
    print("  Node, length, to_list, push_front and contains: right every time.")


def check_hash():
    m = load("hashtable", "HashTable")
    table = m.HashTable()
    for name in ["put", "get", "size"]:
        if not hasattr(table, name):
            raise Fail(f"HashTable has no method called {name} yet.")
    expect("a new table's size()", table.size(), 0)
    expect("get('creeper') on a new table", table.get("creeper"), None)
    table.put("creeper", 20)
    table.put("zombie", 20)
    table.put("iron golem", 100)
    expect("get('creeper')", table.get("creeper"), 20)
    expect("get('iron golem')", table.get("iron golem"), 100)
    expect("get('ghast')", table.get("ghast"), None)
    expect("size() after 3 puts", table.size(), 3)
    table.put("creeper", 25)
    expect("get('creeper') after changing it to 25", table.get("creeper"), 25)
    expect("size() after changing a value", table.size(), 3)

    table = m.HashTable()
    words = [f"block{i}" for i in range(5000)]
    for i, w in enumerate(words):
        table.put(w, i)
    for i, w in enumerate(words):
        if table.get(w) != i:
            raise Fail(f"after 5000 puts, get({w!r}) gave {show(table.get(w))},"
                       f" but it should be {i}.")
    expect("size() after 5000 different puts", table.size(), 5000)
    print("  put, get and size: right every time, even with 5000 keys.")
    buckets = getattr(table, "buckets", None)
    if isinstance(buckets, list) and buckets:
        longest = max(len(b) for b in buckets)
        empty = sum(1 for b in buckets if len(b) == 0)
        print(f"  {len(buckets)} buckets; the longest holds {longest} keys;"
              f" {empty} are empty.")


def check_bst():
    m = load("trees", "TreeNode", "insert", "contains", "in_order", "height")
    expect("in_order(None)", m.in_order(None), [])
    expect("height(None)", m.height(None), 0)
    expect("contains(None, 5)", m.contains(None, 5), False)
    root = None
    for x in [50, 30, 70, 20, 40, 60, 80, 30]:
        root = m.insert(root, x)
    if not isinstance(root, m.TreeNode):
        raise Fail("insert should give back the root TreeNode.")
    expect("in_order after inserting 50 30 70 20 40 60 80 30", m.in_order(root),
           [20, 30, 40, 50, 60, 70, 80])
    expect("height of that tree", m.height(root), 3)
    for x in [20, 30, 40, 50, 60, 70, 80]:
        expect(f"contains(that tree, {x})", m.contains(root, x), True)
    for x in [0, 25, 55, 90]:
        expect(f"contains(that tree, {x})", m.contains(root, x), False)
    rng = random.Random(3)
    numbers = rng.sample(range(10_000), 1000)
    root = None
    for x in numbers:
        root = m.insert(root, x)
    expect("in_order of 1000 random numbers", m.in_order(root), sorted(numbers))
    print("  insert, contains, in_order and height: right every time.")
    print(f"  1,000 random numbers made a tree {m.height(root)} levels tall.")
    root = None
    for x in range(1, 101):
        root = m.insert(root, x)
    print(f"  1 to 100, in order, made a tree {m.height(root)} levels tall.")


# --- Mazes ---------------------------------------------------------------

COST = {".": 1, "P": 1, "D": 1, "~": 5}


def maze_files():
    folder = "mazes"
    if not os.path.isdir(folder):
        print("There's no mazes folder here. Ask your guide for the Stage 7 lab.")
        sys.exit(1)
    return sorted(os.path.join(folder, f) for f in os.listdir(folder)
                  if f.endswith(".txt"))


def best(grid, start, goal, weighted):
    """The checker's own answer: the lowest cost (or steps), or None."""
    import heapq
    todo = [(0, start)]
    done = {}
    while todo:
        cost, (r, c) = heapq.heappop(todo)
        if (r, c) in done:
            continue
        done[(r, c)] = cost
        if (r, c) == goal:
            return cost
        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) \
                    and grid[nr][nc] in COST and (nr, nc) not in done:
                step = COST[grid[nr][nc]] if weighted else 1
                heapq.heappush(todo, (cost + step, (nr, nc)))
    return None


def check_path(grid, path, start, goal, name):
    if not isinstance(path, list) or not path:
        raise Fail(f"{name} should give a list of (row, col) spots, but it"
                   f" gave {show(path)}.")
    if tuple(path[0]) != start or tuple(path[-1]) != goal:
        raise Fail(f"{name}'s path should start at P {start} and end at D"
                   f" {goal}, but it goes from {show(path[0])} to {show(path[-1])}.")
    for a, b in zip(path, path[1:]):
        (r1, c1), (r2, c2) = a, b
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            raise Fail(f"{name}'s path jumps from {a} to {b}: each step must"
                       " be one square up, down, left or right.")
        if grid[r2][c2] not in COST:
            raise Fail(f"{name}'s path goes through a wall at {b}.")


def draw(grid, path):
    rows = [list(row) for row in grid]
    for r, c in path[1:-1]:
        rows[r][c] = "o"
    for row in rows:
        print("    " + "".join(row))


def check_maze(weighted):
    name = "cheapest_path" if weighted else "shortest_path"
    m = load("mazes", "read_maze", "find", name)
    for filename in maze_files():
        grid = m.read_maze(filename)
        if not isinstance(grid, list) or not grid:
            raise Fail(f"read_maze({filename!r}) should give a list of rows.")
        if any(row.endswith("\n") for row in grid):
            raise Fail(f"read_maze({filename!r}) left the newlines on the rows.")
        start, goal = m.find(grid, "P"), m.find(grid, "D")
        for letter, spot in [("P", start), ("D", goal)]:
            r, c = spot
            if grid[r][c] != letter:
                raise Fail(f"find(grid, {letter!r}) gave {spot}, but that"
                           f" square is {grid[r][c]!r}.")
        start, goal = tuple(start), tuple(goal)
        want = best(grid, start, goal, weighted)
        result = getattr(m, name)(grid, start, goal)
        if weighted:
            if want is None:
                expect(f"{name} in {filename}", result, None)
                print(f"  {filename}: no way through, and {name} knew it.")
                continue
            if not (isinstance(result, tuple) and len(result) == 2):
                raise Fail(f"{name} should give (cost, path), but in"
                           f" {filename} it gave {show(result)}.")
            cost, path = result
            check_path(grid, path, start, goal, name)
            real = sum(COST[grid[r][c]] for r, c in path[1:])
            if real != cost:
                raise Fail(f"in {filename}, {name} said the cost was {cost},"
                           f" but its path really costs {real}.")
            if cost != want:
                raise Fail(f"in {filename}, {name} found a path costing {cost},"
                           f" but there's one costing only {want}.")
            print(f"  {filename}: cost {cost}, the cheapest there is.")
        else:
            if want is None:
                expect(f"{name} in {filename}", result, None)
                print(f"  {filename}: no way through, and {name} knew it.")
                continue
            check_path(grid, result, start, goal, name)
            steps = len(result) - 1
            if steps != want:
                raise Fail(f"in {filename}, {name} took {steps} steps, but"
                           f" it can be done in {want}.")
            print(f"  {filename}: {steps} steps, the shortest there is.")
        if len(grid) <= 12:
            draw(grid, result if not weighted else result[1])


CHECKS = {
    "search":   ("7.2",  "linear_search and binary_search, in searching.py", check_search),
    "sorts":    ("7.4",  "selection_sort and insertion_sort, in sorting.py", check_sorts),
    "recursion": ("7.5", "factorial, total and reverse, in recursion.py", check_recursion),
    "merge":    ("7.6",  "merge and merge_sort, in sorting.py", check_merge),
    "quick":    ("7.7",  "quick_sort, in sorting.py", check_quick),
    "brackets": ("7.10", "brackets_ok, in stacks.py", check_brackets),
    "linked":   ("7.11", "Node and friends, in linked.py", check_linked),
    "hash":     ("7.12", "HashTable, in hashtable.py", check_hash),
    "bst":      ("7.13", "TreeNode and friends, in trees.py", check_bst),
    "bfs":      ("7.14", "shortest_path, in mazes.py", lambda: check_maze(False)),
    "dijkstra": ("7.15", "cheapest_path, in mazes.py", lambda: check_maze(True)),
}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in CHECKS:
        print("Usage: python3 check.py NAME. The checks are:")
        for name, (lesson, what, _) in CHECKS.items():
            print(f"  {name:10} Lesson {lesson:5} {what}")
        sys.exit(1 if len(sys.argv) > 1 else 0)
    lesson, what, check = CHECKS[sys.argv[1]]
    print(f"Checking {what}...")
    signal.signal(signal.SIGALRM, on_alarm)
    signal.alarm(10)
    try:
        check()
    except Fail as problem:
        print(f"NOT YET: {problem}")
        sys.exit(1)
    except TooSlow:
        print("NOT YET: that took more than 10 seconds. Is there a loop that"
              " never stops?")
        sys.exit(1)
    except RecursionError:
        print("NOT YET: RecursionError. A function called itself too many"
              " times. Does it have a base case that stops it?")
        sys.exit(1)
    except Exception:
        print("NOT YET: your code crashed during a check:")
        print()
        traceback.print_exc(limit=-1, file=sys.stdout)
        sys.exit(1)
    print("ALL GOOD!")


if __name__ == "__main__":
    main()
