"""Test fixtures: ensure all model artifacts exist before the suite runs."""

import pytest


@pytest.fixture(scope="session", autouse=True)
def ensure_artifacts():
    from ml.baseline import PROPERTIES
    from ml.baseline import train_and_persist

    for prop in PROPERTIES:
        if not PROPERTIES[prop]["artifact"].exists():
            train_and_persist(prop)
    yield