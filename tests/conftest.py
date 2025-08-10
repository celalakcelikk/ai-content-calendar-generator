"""
This module contains shared pytest fixtures used across the test suite.

Fixtures defined here provide common setup for environment variables and configuration dictionaries,
allowing tests to use consistent and reusable testing contexts.
"""

import os

import pytest


@pytest.fixture
def sample_env():
    """
    Fixture to temporarily set environment variables needed for the app.

    Sets environment variable 'OPENAI_API_KEY' for the duration
    of the test, and restores the original environment afterwards.

    Yields
    -------
    None
        This fixture does not return a value but sets environment variables for tests.
    """
    original_env = os.environ.copy()
    os.environ["OPENAI_API_KEY"] = "test_api_key"
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_config():
    """
    Fixture returning a sample configuration dictionary mimicking default app configuration.

    Returns
    -------
    dict
        A dictionary with keys 'topic', 'audience', 'frequency', 'duration', 'platform', and 'tone'
        filled with sample default values.
    """
    return {
        "topic": "technology",
        "audience": "developers",
        "frequency": "weekly",
        "duration": "1 month",
        "platform": "twitter",
        "tone": "informative",
    }
