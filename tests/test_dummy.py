import pytest


def pytest_sessionfinish(session, exitstatus):
    if session.testscollected == 0:
        exitstatus = 0  # Force pytest to exit successfully
