from functools import wraps
from clirainbow import Colorizer, BRIGHT_BLUE, BRIGHT_GREEN, BRIGHT_RED, BRIGHT_YELLOW, sanitize
from quicktest.util import noun_number, terminal_width
from quicktest.summary import summarize

Colorizer = Colorizer()

_SEPARATOR = '=' * terminal_width()


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
def _print_labeled_list(label, lst, f=lambda x: x):
    print(label.upper())
    for x in lst:
        print(f(x))


def _repr(x):
    return sanitize(repr(x))


def _print_failures(failures):
    def print_failure(f):
        return Colorizer.format(
            f'Given <{f["inputs"]}>, expected <{_repr(f["expected"])}> but got <{_repr(f["actual"])}>',
            BRIGHT_BLUE, BRIGHT_GREEN, BRIGHT_YELLOW)

    if failures:
        _print_labeled_list('failures', failures, print_failure)


def _print_errors(errors):
    def print_error(e):
        return Colorizer.format(
            f'Given <{_repr(e["inputs"])}>, caught exception "<{_repr(e["error"])}>"', BRIGHT_BLUE, BRIGHT_RED)

    if errors:
        _print_labeled_list('errors', errors, print_error)


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
