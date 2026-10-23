# Lesson 7.8: Why Should I Believe It? (Proof, Part 1)

**Time:** 2 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
building blocks, Numberblocks-style cubes or Lego (about 20); squared
paper · **New words:** claim, evidence, proof, counterexample,
invariant

## Goal *(read this to the learner)*

> The checker tried your binary search on hundreds of cases, and it
> passed. But there are *infinitely* many lists. How can anyone be sure
> it works on all of them? Mathematicians have an answer: a **proof**, an
> argument so careful that it works for every case at once, even the
> ones nobody has tried. Today you'll catch some claims that look true
> but aren't, write your first proofs with blocks and letters, and prove
> that binary search can't miss.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once, especially step 6.
- [ ] Optional reading for you: *Book of Proof* by Richard Hammack (in
      the offline library, `books/book-of-proof.pdf`), Chapter 4,
      "Direct Proof". This lesson is a
      gentle version of its first few pages.

## Warm-up (5 min)

"Is every number that ends in 0 even?" *(Yes.)* "How do you know? Did
you check them all?" *(You can't: there are infinitely many! You know
because of *why*: 10 is even, and they're all made of tens.)* "That
'because' is what a proof is."

## Activity

### Session 1: claims, evidence and counterexamples

1. **True or false?** **Say:** "A **claim** is something someone says is
   true. Let's test two." New file, `~/lab/algo/claims.py`:
   ```python
   def is_prime(n):
       if n < 2:
           return False
       d = 2
       while d * d <= n:
           if n % d == 0:
               return False
           d = d + 1
       return True


   # Claim 1: an even number plus an even number is always even.
   ok = True
   for a in range(0, 1000, 2):
       for b in range(0, 1000, 2):
           if (a + b) % 2 != 0:
               print("Claim 1 is wrong:", a, b)
               ok = False
   print("Claim 1 held for every pair I tried:", ok)

   # Claim 2: n × n + n + 41 is always prime.
   for n in range(100):
       if not is_prime(n * n + n + 41):
           print(f"Claim 2 is wrong when n is {n}: {n * n + n + 41} isn't prime.")
           break
   ```
   **Say:** "`is_prime` is the one from Lesson 3.6. `range(0, 1000, 2)`
   counts in twos: all the even numbers below 1000."

   **Before running it, ask:** "Try Claim 2 for n = 0, 1 and 2 on a
   calculator." *(41, 43 and 47: all prime! It looks true.)* Run it.
   **They should see:**
   ```
   Claim 1 held for every pair I tried: True
   Claim 2 is wrong when n is 40: 1681 isn't prime.
   ```
   **Say:** "1681 is 41 × 41. Claim 2 worked forty times in a row, then
   broke! One case where a claim fails is called a **counterexample**,
   and one is enough to prove a claim wrong. A famous mathematician,
   Leonhard Euler, found this formula nearly 300 years ago."

2. **Evidence isn't proof.** **Ask:** "Claim 1 worked for 250,000 pairs.
   Does that prove it?" *(No! Claim 2 worked 40 times, and it was
   wrong. Python tried lots of cases. That's **evidence**, not proof.)*
   **Say:** "To be sure, we need a reason that works for *every* even
   number, even the ones too big to type."

3. **A proof with blocks.** **Say:** "An even number is one you can
   build as two equal rows: all in pairs." Build 6 and 8 as two rows
   each, like a Numberblocks even number.

   **Ask:** "Push 6 and 8 together. Is it still two equal rows?" *(Yes:
   each row just got longer.)* "Would that work for *any* two even
   numbers?" *(Yes. Two-row shapes pushed together always make a
   two-row shape.)* **Say:** "That's a proof! It doesn't depend on which
   numbers you pick."

4. **The same proof with letters.** **Say:** "Algebra lets us write that
   proof down. Every even number is 2 times some whole number: 6 is
   2 × 3, and 8 is 2 × 4. Call our two even numbers 2 × a and 2 × b,
   where a and b can be *any* whole numbers." Write it out:

   > **Claim:** an even number plus an even number is even.
   >
   > **Proof:** Call the even numbers 2a and 2b. Then 2a + 2b = 2(a + b).
   > That's 2 times a whole number, so it's even. ∎

   **Say:** "The letters stand for *every* number at once. That's why one
   line of algebra beats a million tries in Python. The ∎ means 'proof
   finished'."

5. **Your turn: odd plus odd.** **Say:** "An odd number is two equal rows
   with one block left over." Build 5 and 7. **Ask:** "Is odd plus odd
   even, or odd?" Let the learner push them together and find the proof
   with blocks. *(The two leftover blocks make a pair, so it's two equal
   rows: even.)* Then with letters, with hints:
   - "An odd number is 2 × something, plus 1. How would you write two
     odd numbers?" *(2a + 1 and 2b + 1.)*
   - "Add them up." *(2a + 2b + 2.)*
   - "Can you write that as 2 times something?" *(2(a + b + 1).)*

   Write the proof in the notebook, in the same style as step 4, with ∎.

### Session 2: proving code is right

6. **The promise.** **Say:** "Binary search has a promise that it keeps
   all the time: *if the target is in the list, it's somewhere from
   position `low` to position `high`*. A promise like that, which stays
   true every time round a loop, is called an **invariant**." Prove it
   in three steps, talking it through with the sorted cards from
   Lesson 7.2:
   - **It's true at the start.** `low` is 0 and `high` is the last
     position: the whole list. If the target is anywhere, it's there.
   - **Each time round the loop keeps it true.** Say the middle card is
     too small. The list is *sorted*, so every card to the left of the
     middle is smaller still: the target can't be any of them. So moving
     `low` to `middle + 1` keeps the promise. The same goes for "too big"
     and `high`.
   - **So when the loop stops, the answer is right.** It stops either
     because it found the target (right!), or because `low` went past
     `high`. Then there are no positions left between them, so by the
     promise, the target isn't in the list. `None` is right too.

   **Ask:** "Where did the proof use 'sorted'?" *(The second step.)*
   "And why can't the loop go on forever?" *(Each time round, `low` goes
   up or `high` goes down, so the gap between them shrinks. It can't
   shrink forever.)*

7. **Check the promise as the program runs.** New file,
   `~/lab/algo/invariant.py`:
   ```python
   def binary_search(items, target):
       low = 0
       high = len(items) - 1
       while low <= high:
           assert target not in items[:low], "it's to the left of low!"
           assert target not in items[high + 1:], "it's to the right of high!"
           middle = (low + high) // 2
           if items[middle] == target:
               return middle
           elif items[middle] < target:
               low = middle + 1
           else:
               high = middle - 1
       return None


   numbers = list(range(0, 200, 2))
   for target in range(-1, 201):
       binary_search(numbers, target)
   print("The promise was kept every time round the loop.")
   binary_search([1, 9, 4, 6, 2], 2)
   ```
   **Say:** "The two `assert`s check the promise every time round the
   loop: the target isn't to the left of `low`, or to the right of
   `high`. The last line tries a list that *isn't* sorted."

   Run it. **They should see:** `The promise was kept every time round
   the loop.`, then an error ending:
   ```
   AssertionError: it's to the right of high!
   ```
   **Say:** "On the unsorted list, the promise broke, just where the
   proof said it needed 'sorted'. The `assert`s are evidence; the proof
   is the reason." Commit both files.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NameError: name 'is_prime' is not defined` | The `is_prime` function isn't at the top of `claims.py` | Copy it in, above the claims. |
| Claim 2 never says it's wrong | The loop doesn't reach 40 | `range(100)`. |
| `invariant.py` stops with an `AssertionError` before the "promise" line | The `binary_search` in this file is different from the lesson's | Compare it line by line: a broken binary search breaks the promise. That's the asserts doing their job! |
| The learner wants to "prove" it by trying more numbers | Very natural! | Ask: "Claim 2 worked 40 times. Would 40 tries have convinced you?" |

## Talk about it

- What's the difference between evidence and proof?
- How many counterexamples does it take to show a claim is false?
- What's binary search's invariant? Where does the proof need the list
  to be sorted?

## Challenge *(if there's time, or for next time)*

- Prove that even × any whole number is even. *(2a × b = 2(ab).)*
- True or false? "Every odd number bigger than 1 is prime." Find a
  counterexample. *(9.)*
- True or false? "Every whole number bigger than 1 is prime, or can be
  made by multiplying primes." Try lots of numbers in Python. Can you
  find a counterexample? (Mathematicians have proved it's true: it's
  called the Fundamental Theorem of Arithmetic.)
- Write the invariant for linear search, and prove it. *(The target
  isn't in any position before `i`.)*

## Checkpoint

The learner can, without help:
- [ ] Explain the difference between evidence and a proof
- [ ] Find a counterexample with a Python loop
- [ ] Prove "odd plus odd is even" with blocks and with algebra
- [ ] Explain binary search's invariant, and why it needs a sorted list

## Lab notebook

Write the two proofs (even plus even, odd plus odd), with ∎ at the end
of each. Write binary search's invariant, and the three steps of its
proof. Commit. Add *claim*, *evidence*, *proof*, *counterexample* and
*invariant* to `dictionary.md`.

## Guide's background *(optional reading)*

A **direct proof** starts from definitions ("even means 2 times a whole
number") and reasons step by step to the conclusion. It's the first
method in *Book of Proof*, Chapter 4. The block pictures are real
proofs too, as long as the argument works for every case and not just
the ones on the table.

Proving programs correct uses exactly these ideas. A **loop invariant**
is a statement that's true before the loop and stays true after each
time round it; together with the loop's stopping condition, it shows
the answer is right. Showing the loop *stops* is a separate proof,
usually by finding something that shrinks each time (here, the gap from
`low` to `high`). Remember the Collatz puzzle from Lesson 3.7: nobody
has managed to prove that its loop always stops.

The Euler polynomial n² + n + 41 is a famous example of why mathematicians
don't trust patterns, however long. Lesson 7.9 adds the second big proof
method, **induction**, which is how most facts about recursive programs
are proved.
