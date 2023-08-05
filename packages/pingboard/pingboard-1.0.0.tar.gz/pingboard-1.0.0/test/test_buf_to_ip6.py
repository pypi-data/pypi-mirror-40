import pytest
import socket

from hypothesis import given
from hypothesis.strategies import binary

from pingboard.util import buf_to_ip6
from pingboard.const import ICMPV6_ECHO_REPLY, AF_INET6


def test_decode_not_v6():
    with pytest.raises(RuntimeError) as e:
        buf_to_ip6(b'\x00'*40)
    assert 'Expected IPv6 packet' in str(e.value)


def test_decode_missing_headers():
    with pytest.raises(RuntimeError) as e:
        buf_to_ip6(b'\x60' + b'\x00'*39)
    assert 'Ran out of buffer' in str(e.value)


def test_decode_short():
    with pytest.raises(RuntimeError) as e:
        buf_to_ip6(b'\x60' + b'\x00'*20)
    assert 'buffer to short' in str(e.value)


def test_decode_no_next_header():
    source_addr = b'\x00'*15 + b'\x01'
    dest_addr = b'\x00'*15 + b'\x01'
    buf = b'\x60\x00\x00\x00\x00\x10\x3b\x40' + source_addr + dest_addr
    with pytest.raises(RuntimeError) as e:
        buf_to_ip6(buf)

    assert "Got the 'No Next Header'" in str(e.value)


@given(
    binary(min_size=16, max_size=16),  # source address
    binary(min_size=16, max_size=16),  # destination address
    binary(min_size=2, max_size=2),  # identifier
    binary(min_size=2, max_size=2),  # sequence
    binary(min_size=1, max_size=1),  # data
)
def test_decode_random_v6(source_addr, dest_addr, identifier, sequence, data):

    buf = b'\x60\x00\x00\x00\x00\x10\x3a\x40' + source_addr + dest_addr \
        + b'\x81\x00\xad\x0e' + identifier + sequence + data

    packet = buf_to_ip6(buf)
    assert isinstance(packet, dict)
    assert packet['destination'] == socket.inet_ntop(AF_INET6, dest_addr)
    assert packet['type'] == ICMPV6_ECHO_REPLY
    assert packet['code'] == 0
    assert packet['data'] == data
