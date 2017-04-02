

import pytest
import Placer


@pytest.fixture
def placer():
    return Placer(1000, 1000)
