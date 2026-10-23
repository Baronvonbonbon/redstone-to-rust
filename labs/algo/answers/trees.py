class TreeNode:
    """A value, with a smaller tree on the left and a bigger one on the right."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def insert(root, value):
    """Puts value in the tree. Gives back the root."""
    if root is None:
        return TreeNode(value)
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    return root


def contains(root, value):
    if root is None:
        return False
    if value == root.value:
        return True
    if value < root.value:
        return contains(root.left, value)
    return contains(root.right, value)


def in_order(root):
    """All the values, smallest first."""
    if root is None:
        return []
    return in_order(root.left) + [root.value] + in_order(root.right)


def height(root):
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


def show(root, depth=0):
    """Prints the tree on its side: the right branch at the top."""
    if root is None:
        return
    show(root.right, depth + 1)
    print("    " * depth + str(root.value))
    show(root.left, depth + 1)
