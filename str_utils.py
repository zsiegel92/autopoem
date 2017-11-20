def is_one_away(first, other):
    skip_difference = {
        -1: lambda i: (i, i+1),  # Delete
        1: lambda i: (i+1, i),  # Add
        0: lambda i: (i+1, i+1),  # Modify
    }
    try:
        skip = skip_difference[len(first) - len(other)]
    except KeyError:
        return False  # More than 2 letters of difference
    for i, (l1, l2) in enumerate(zip(first, other)):
        if l1 != l2:
            i -= 1  # Go back to the previous couple of identical letters
            break
    remain_first, remain_other = skip(i + 1)
    return first[remain_first:] == other[remain_other:]


def too_similar(new_word,taboo):
    if any(word in new_word for word in taboo) or any(word in new_word for word in taboo):
        return True
    else:
        return False
