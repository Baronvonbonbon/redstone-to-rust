def selection_sort(items):
    """Finds the smallest, puts it first; then the next smallest..."""
    items = items.copy()
    for i in range(len(items)):
        smallest = i
        for j in range(i + 1, len(items)):
            if items[j] < items[smallest]:
                smallest = j
        items[i], items[smallest] = items[smallest], items[i]
    return items


def insertion_sort(items):
    """Like sorting a hand of cards: each new card slides left into place."""
    items = items.copy()
    for i in range(1, len(items)):
        card = items[i]
        j = i - 1
        while j >= 0 and items[j] > card:
            items[j + 1] = items[j]
            j = j - 1
        items[j + 1] = card
    return items


def merge(left, right):
    """Two sorted lists in, one sorted list out."""
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1
    result = result + left[i:] + right[j:]
    return result


def merge_sort(items):
    """Sort each half, then merge them."""
    if len(items) <= 1:
        return items
    middle = len(items) // 2
    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])
    return merge(left, right)


def quick_sort(items):
    """Split around a pivot: the smaller ones, the same ones, the bigger ones."""
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]
    smaller = []
    same = []
    bigger = []
    for x in items:
        if x < pivot:
            smaller.append(x)
        elif x == pivot:
            same.append(x)
        else:
            bigger.append(x)
    return quick_sort(smaller) + same + quick_sort(bigger)
