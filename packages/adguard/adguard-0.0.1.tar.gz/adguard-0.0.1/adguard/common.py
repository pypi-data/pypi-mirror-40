"""Common functions."""


def get_percentage(part, whole):
    """Return percentage."""
    percentage = 100 * float(part)/float(whole)
    return int(percentage)
