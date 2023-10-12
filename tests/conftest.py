"""Test level wide changes for pytest to use"""
import pytest


def pytest_addoption(parser):
    """Adds flag to pytest CLI"""
    parser.addoption("--integration", action="store_true", help="run integration tests")


def pytest_runtest_setup(item):
    """Allows tests marked as integration to be skipped if flag not provided"""
    if "integration" in item.keywords and not item.config.getvalue("integration"):
        pytest.skip("need --integration option to run")
