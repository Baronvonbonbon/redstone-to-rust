def linear_search(items, target):
    """Looks at every item, from the start. Gives the position, or None."""
    for i in range(len(items)):
        if items[i] == target:
            return i
    return None


assert linear_search(["pig", "cow", "sheep"], "pig") == 0
assert linear_search(["pig", "cow", "sheep"], "sheep") == 2
assert linear_search(["pig", "cow", "sheep"], "ghast") is None
assert linear_search([], "pig") is None


def binary_search(items, target):
    """items must be sorted. Halves the part still to search each time."""
    low = 0
    high = len(items) - 1
    while low <= high:
        middle = (low + high) // 2
        if items[middle] == target:
            return middle
        elif items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return None


assert binary_search([2, 4, 6, 8, 10, 12, 14, 16], 12) == 5
assert binary_search([2, 4, 6, 8, 10, 12, 14, 16], 7) is None
