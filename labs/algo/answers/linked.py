class Node:
    """One link in the chain: a value, and the next Node (or None)."""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def length(head):
    count = 0
    node = head
    while node is not None:
        count = count + 1
        node = node.next
    return count


def to_list(head):
    result = []
    node = head
    while node is not None:
        result.append(node.value)
        node = node.next
    return result


def contains(head, value):
    node = head
    while node is not None:
        if node.value == value:
            return True
        node = node.next
    return False


def push_front(head, value):
    """Puts a new Node at the front. Gives back the new head."""
    return Node(value, head)
