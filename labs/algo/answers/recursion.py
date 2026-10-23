def factorial(n):
    """n × (n - 1) × ... × 1. factorial(0) is 1."""
    if n == 0:
        return 1
    return n * factorial(n - 1)


def total(items):
    """Adds up a list: the first item, plus the total of the rest."""
    if items == []:
        return 0
    return items[0] + total(items[1:])


def reverse(text):
    """The reverse of the rest, then the first letter on the end."""
    if text == "":
        return ""
    return reverse(text[1:]) + text[0]
