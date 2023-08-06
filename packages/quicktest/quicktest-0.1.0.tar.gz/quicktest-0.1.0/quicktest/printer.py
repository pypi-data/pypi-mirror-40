from functools import wraps
from clirainbow import Colorizer, BRIGHT_BLUE, BRIGHT_GREEN, BRIGHT_RED, BRIGHT_YELLOW
from quicktest.utils import noun_number
from quicktest.summary import summarize


Colorizer = Colorizer()


_SEPARATOR = '=' * 50


def print_summary(results):
    summary = summarize(results)
    _print_summary_content(summary)
    _print_failures(summary['failures'])
    _print_errors(summary['errors'])


def _with_printed_prefix(sep):
    # This decorator isn't necessary at all, I'm just having fun
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(sep)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@_with_printed_prefix(_SEPARATOR)
def _print_summary_content(summary):
    _print_test_count(summary)
    _print_success_count(summary)
    _print_failure_count(summary)


@_with_printed_prefix(_SEPARATOR)
def _print_labeled_list(label, lst):
    print(label.upper())
    for x in lst:
        print(x)


def _print_failures(failures):
    if failures:
        _print_labeled_list('failures', failures)


def _print_errors(errors):
    if errors:
        _print_labeled_list('errors', errors)


def _print_test_count(summary):
    test_count = summary['test_count']
    Colorizer.print(f'<{test_count}> RAN', BRIGHT_BLUE)


def _print_success_count(summary):
    success_count = summary['success_count']
    Colorizer.print(f'<{success_count}> OK', BRIGHT_GREEN)


def _print_failure_count(summary):
    failure_count = summary['failure_count']
    error_count = summary['error_count']
    if failure_count:
        failure_ending = noun_number(failure_count).upper()
        error_ending = noun_number(error_count).upper()
        failure_part = Colorizer.format(
            f'<{failure_count}> FAILURE', BRIGHT_YELLOW) + failure_ending
        error_part = Colorizer.format(
            f' (<{error_count}> ERROR{error_ending})', BRIGHT_RED) if error_count else ''
        print(failure_part + error_part)
