

import pytest
from placer import Placer


@pytest.fixture
def placer():
    return Placer(1000, 1000)
