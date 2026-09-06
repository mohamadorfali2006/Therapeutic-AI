"""Test fixtures: ensure the baseline artifact exists before the suite runs."""

import pytest


@pytest.fixture(scope="session", autouse=True)
def ensure_artifact():
    from ml.baseline import DEFAULT_ARTIFACT, train_and_persist

    if not DEFAULT_ARTIFACT.exists():
        train_and_persist()
    yield