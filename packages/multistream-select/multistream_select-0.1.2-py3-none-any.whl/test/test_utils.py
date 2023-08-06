import pytest
from multistream_select import utils


@pytest.mark.parametrize(
    "test_in, test_out", [
        ("hello, world", '0x0d68656c6c6f2c20776f726c640a'),
        ("na", '0x036e610a'), ("ls", '0x036c730a')
    ]
)
def test_str_to_hex(test_in, test_out):
    assert utils.hexify(test_in) == test_out
