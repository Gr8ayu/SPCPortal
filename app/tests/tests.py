
import pytest


@pytest.mark.django_db
def test_pytest_working():
    assert 2 + 2  == 4
