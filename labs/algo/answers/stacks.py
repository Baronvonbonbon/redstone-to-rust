def brackets_ok(text):
    """True if every bracket is closed, in the right order."""
    partner = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if stack == []:
                return False
            if stack.pop() != partner[ch]:
                return False
    return stack == []
