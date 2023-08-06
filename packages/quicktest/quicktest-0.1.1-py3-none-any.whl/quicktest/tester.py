def run_test(f, case):
    *inputs, expected_result = case
    try:
        result = f(*inputs)
        return _result(inputs, result, expected_result)
    except Exception as e:
        return _error_result(inputs, e)


def _result(inputs, result, expected):
    if result == expected:
        return _success_result()
    else:
        return _failure_result(inputs, result, expected)


def _success_result():
    return {
        'outcome': 'success'
    }


def _failure_result(inputs, result, expected):
    return {
        'outcome': 'failure',
        'info': f'Given {inputs}, expected {repr(expected)} but got {repr(result)}'
    }


def _error_result(inputs, e):
    return {
        'outcome': 'error',
        'info': f'Given {inputs}, caught exception "{e}"'
    }
