"""Validation helpers for the task manager."""

def validate_non_empty(value: str) -> bool:
    """Return True if `value` is a non-empty, non-whitespace string."""
    return bool(value and isinstance(value, str) and value.strip())


def validate_length(value: str, min_len: int = 1) -> bool:
    """Return True if `value` has length >= `min_len` after stripping."""
    if not validate_non_empty(value):
        return False
    return len(value.strip()) >= int(min_len)


def validate_index(idx, seq) -> bool:
    """Return True if `idx` is a valid index for sequence `seq` (0-based)."""
    try:
        i = int(idx)
    except (TypeError, ValueError):
        return False
    return 0 <= i < len(seq)


def validate_menu_choice(choice, valid_choices) -> bool:
    """Return True if `choice` is one of the integers in `valid_choices`."""
    try:
        c = int(choice)
    except (TypeError, ValueError):
        return False
    return c in valid_choices
