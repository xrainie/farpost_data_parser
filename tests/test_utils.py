from src.utils import PromoData
import pytest

@pytest.fixture(autouse=True)
def main_data():
    return PromoData().load()

@pytest.mark.parametrize('keys', 
                         [
                             ('authorr', 'title', 'viewss')
                         ])
def test_main_data(main_data, keys):
    assert keys == tuple(main_data.items().keys())