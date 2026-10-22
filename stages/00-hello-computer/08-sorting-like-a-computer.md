# Lesson 0.8: Sorting Like a Computer

**Time:** 40 min · **You need:** 8 identical paper cups, coins or pebbles,
sticky notes, a pencil. No computer · **New words:** algorithm, compare,
sort

## Goal *(read this to the learner)*

> A computer can't look at a whole pile of things and "just see" which is
> biggest. It can only compare **two things at a time**. Today you'll
> sort hidden things into order using only that power, and invent your
> own **algorithm**.

## Before the lesson *(guide, 10 min)*

- [ ] Put a different number of coins or pebbles under each of the 8 cups
      (for example 1, 3, 4, 7, 9, 12, 15, 20). Mix the cups up so you
      don't know which is which.
- [ ] Label the cups A to H with sticky notes.

## Warm-up (5 min)

Ask them to put 5 numbers written on paper in order (say 8, 2, 9, 4, 1).
Easy! "But how did you do it? Could you explain it to the sandwich robot?"

## Activity

1. **The rule.** Explain: "You're a computer now. You can't look under the
   cups. You can only pick up **two** cups at a time, feel which is
   heavier, and put them down. Your job is to line them up from lightest
   to heaviest." (Coins: they can peek under just those two cups, then
   put them back.)

2. **Sort them** however they like. Keep a tally of how many
   comparisons they make (every time two cups are compared, make a mark).

3. **Check.** Lift all the cups. Are they in order? How many comparisons
   did it take?

4. **Learn one famous way: Bubble Sort.** Mix the cups up again. Teach it:
   - Start at the left. Compare cup 1 and cup 2. If the left one is
     heavier, swap them.
   - Move one step right: compare cups 2 and 3, and swap if needed.
     Keep going to the end.
   - The heaviest cup has now "bubbled" to the right end!
   - Go back to the start and do it again (you can stop one cup earlier
     each time).
   - When you go all the way along with **no swaps**, you're done.

   Count the comparisons again.

5. **Write the algorithm.** On paper, they write Bubble Sort as steps the
   sandwich robot could follow. Run it once with you as the robot.

## If something goes wrong

| What happens | What to do |
|---|---|
| Peeks at all the cups | "Computers can't do that! Only two at a time." |
| Loses track of where they are | Put a pencil next to the pair being compared, and move it along. |
| Bored with 8 cups | Use 5 cups to learn it, then 8 to race. |

## Talk about it

- Was your own way faster or slower than Bubble Sort? (Count!)
- A list of steps that solves a problem is called an **algorithm**. Was
  your own way an algorithm?
- What if there were 1000 cups? Would Bubble Sort be fast?
  *(No! It gets VERY slow. There are cleverer algorithms, and you'll
  learn them in Stage 7.)*

## Challenge

**Selection Sort.** Find the lightest cup by comparing it against all the
others, and put it first. Then find the lightest of the rest, and put it
second... Count the comparisons. Better or worse than Bubble Sort?

## Checkpoint

The learner can, without help:
- [ ] Sort the cups, comparing two at a time
- [ ] Explain the steps of Bubble Sort

## Lab notebook

Write the Bubble Sort steps. Record: "My way: ___ comparisons. Bubble
Sort: ___ comparisons."

## Guide's background *(optional reading)*

Sorting is one of the most studied problems in computer science, because
computers sort constantly: search results, contact lists, high-score
tables. The rule "compare only two things at a time" is exactly how
real sorting algorithms work. Bubble Sort is simple but slow; for 1000
items it can take about half a million comparisons. Merge Sort, which
your learner will meet in Stage 7, needs only about 10,000.

Counting comparisons is the seed of **Big-O**, the way computer
scientists measure how fast an algorithm is. This activity is adapted
from CS Unplugged's sorting activities.
