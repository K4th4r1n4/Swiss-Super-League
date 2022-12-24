import pytest

from src.utils.request import get_free_proxies


@pytest.fixture
def proxies():
    proxies = get_free_proxies()
    return proxies


def test_get_free_proxies(proxies):
    """Test `get_free_proxies` function."""
    assert len(proxies)
    assert isinstance(proxies[0], str)
    assert len(proxies[0].split(":")) == 2
    assert len(proxies[0].split("."))
