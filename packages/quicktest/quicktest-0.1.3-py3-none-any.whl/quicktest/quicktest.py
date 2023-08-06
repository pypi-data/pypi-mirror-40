from quicktest.tester import run_test
from quicktest.printer import print_summary


def test(f, cases):
    """
    For each case in `cases`, applies `f` to the inputs and evaluates whether
    `f` returns the correct output or produces an error.
    `cases` is assumed to be an iterable of iterables, each of which
    has length at least 2, with the expected output in last position.
    Other elements are considered to be inputs, in the order `f` is expecting them.
    """
    results = [run_test(f, case) for case in cases]
    print_summary(results)
