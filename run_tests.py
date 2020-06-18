"""Module containing run tests function."""
import os
import coverage
import pytest


def test():
    """Run tests with coverage."""
    # Testing configurations
    COV = coverage.coverage(
        branch=True,
        omit=[
            '*/tests/*',
            '*/lib/*',
            '*/data/*',
            '*/migrations/*',
            '*/base.py',
            'manage.py',
            'config.py',
            '*/__init__.py',
            'run_tests.py'
        ]
    )
    COV.start()

    pytest.main(['-x', '-v', 'tests'])

    COV.stop()
    return 0


if __name__ == '__main__':
    test()
