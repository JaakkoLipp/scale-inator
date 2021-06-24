import pytest
from scale_inator.main import setup_serial

class ArgsPretend:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.fixture
def main_setup():
    arguments = ArgsPretend(pretend=1,no_gui=1)
    setup_serial(arguments)
    return arguments
