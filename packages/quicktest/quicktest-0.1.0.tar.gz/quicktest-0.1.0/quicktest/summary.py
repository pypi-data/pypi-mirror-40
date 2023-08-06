def summarize(results):
    summary = {
        'test_count': len(results),
        'success_count': 0,
        'failure_count': 0,
        'error_count': 0,
        'failures': [],
        'errors': []
    }
    for result in results:
        outcome = result['outcome']
        if outcome == 'success':
            summary['success_count'] += 1
        if outcome == 'failure':
            summary['failure_count'] += 1
            summary['failures'].append(result['info'])
        if outcome == 'error':
            summary['failure_count'] += 1
            summary['error_count'] += 1
            summary['errors'].append(result['info'])
    return summary
