# Lesson 0.10: Secret Messages

**Time:** 45 min · **You need:** two paper plates (one smaller, or cut one
down), a brass paper fastener or a pin, a marker, scissors · **New words:**
cipher, encrypt, decrypt, key

## Goal *(read this to the learner)*

> For thousands of years, people have hidden messages with secret codes
> called **ciphers**. Julius Caesar used one 2000 years ago! Today you'll
> build a cipher wheel and send secret messages that only someone with
> the **key** can read.

## Before the lesson *(guide, 10 min)*

- [ ] Make (or make together) the cipher wheel:
  1. Write the alphabet A to Z evenly around the edge of the big plate,
     like the numbers on a clock.
  2. Do the same on the smaller plate, lining the letters up under the
     big plate's letters.
  3. Push the fastener through both centres so the small plate spins.
- [ ] Encrypt this message with a key of **3** (explained below), to use
      in step 3: `MEET AT THE TREEHOUSE` becomes `PHHW DW WKH WUHHKRXVH`.

## Warm-up (5 min)

"Remember how a picture became numbers? Today, letters will turn into
*other* letters."

## Activity

1. **How the key works.** Line up A on the outer plate with A on the
   inner plate. Now turn the inner plate so that outer **A** sits over
   inner **D**. That's **key 3**: every letter moves 3 steps along.

2. **Encrypt.** Find each letter of your message on the *outer* plate,
   and write down the letter under it on the *inner* plate. Encrypt `HI`
   together. *(With key 3, it becomes `KL`.)*

3. **Decrypt.** Give them `PHHW DW WKH WUHHKRXVH` and tell them the key is
   3. Find each letter on the *inner* plate, and read the outer one.
   *(MEET AT THE TREEHOUSE.)*

4. **Send real messages.** They write a secret message with a key they
   choose, and give you only the scrambled message and the key. You
   decrypt it. Then swap.

5. **Crack it!** Give them a message without telling them the key:
   `KHOOR` (it's HELLO, with key 3). "There are only 25 possible keys.
   How could you crack it?" *(Try every key, one by one. Someone with a
   wheel and some patience can break this cipher!)*

## If something goes wrong

| What happens | What to do |
|---|---|
| Uses the wrong ring to look up letters | Colour the outer ring "PLAIN" and the inner ring "SECRET". |
| Mixes up encrypt and decrypt | Encrypt: outer to inner. Decrypt: inner to outer. Write it on the wheel. |
| What happens at the end, after Z? | It wraps around to A. That's why it's a wheel! |

## Talk about it

- What's the **key**? Why must it be secret? *(Anyone with the key can read
  your messages.)*
- How many different keys are there? *(25 useful ones; key 26 brings you
  back to the start.)*
- Is this a strong cipher? *(No. You can try every key in a few minutes.)*

## Challenge

- **Key 13** is special. Encrypt a word with key 13, then encrypt the
  *result* with key 13 again. What happens? *(You get your word back!
  It's called ROT13, and you'll meet it again in the Mineshaft.)*
- Make up your own cipher: maybe each letter becomes a number, or a
  symbol. Can your guide crack it?

## Checkpoint

The learner can, without help:
- [ ] Encrypt and decrypt a message with a given key
- [ ] Explain why the key must be kept secret

## Lab notebook

Write a secret message in your notebook, and hide the key somewhere else.
Write: "**Encrypt** = make it secret. **Decrypt** = turn it back. The
**key** unlocks it."

## Guide's background *(optional reading)*

This is the **Caesar cipher**. It's easy to crack, because there are only
25 keys to try (a "brute force" attack) and because common letters like
E still stand out. The Mineshaft wargame in Stages 1 and 5 includes ROT13
and base64, two ways of scrambling text that offer **no** real security.
In Stage 11, your learner will write a program that cracks Caesar ciphers
automatically, and learn how modern cryptography keeps real secrets safe.
