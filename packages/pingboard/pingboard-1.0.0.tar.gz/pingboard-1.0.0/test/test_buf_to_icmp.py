import pytest
import socket
import struct


from hypothesis import given, assume
from hypothesis.strategies import binary, just

from pingboard.util import buf_to_icmp4, buf_to_icmp
from pingboard.const import ICMP_ECHO_REQUEST, ICMP_ECHO_REPLY, \
    ICMP_TIME_EXCEEDED


def test_decode_short():
    with pytest.raises(RuntimeError) as e:
        buf_to_icmp(b'\x00'*2, socket.AF_INET)
    assert 'buffer to short' in str(e.value)


def test_decode_short2():
    with pytest.raises(RuntimeError) as e:
        buf_to_icmp(b'\x00'*6, socket.AF_INET)
    assert 'buffer to short' in str(e.value)


def test_decode_short3():
    '''Check the expected exception is thrown for buffers with icmp type
    ICMP_DEST_UNREACH (3) and that are too short.'''
    with pytest.raises(RuntimeError) as e:
        buf_to_icmp(b'\x03\x00\x00\x00\x00\x00\x00\x00', socket.AF_INET)
    assert 'Expected more data' in str(e.value)


def test_decode_short4():
    '''Check the expected exception is thrown for buffers with icmp type
    ICMP_TIME_EXCEEDED (11) and that are too short.'''
    with pytest.raises(RuntimeError) as e:
        buf_to_icmp(b'\x0b\x00\x00\x00\x00\x00\x00\x00', socket.AF_INET)
    assert 'Expected more data' in str(e.value)


def test_decode_inner_not_v4():
    '''Check suitable exception raised when type ICMP_DEST_UNREACH (3) and
    inner packet is doesn't have correct IPv4 version'''
    with pytest.raises(RuntimeError) as e:
        buf_to_icmp(b'\x03' + b'\x00'*27, socket.AF_INET)
    assert 'expected version 4' in str(e.value)


def test_decode_echo():
    packet = buf_to_icmp(b'\x08\x00\x00\x00\xFE\xFF\xEF\xEE', socket.AF_INET)
    assert packet['type'] == ICMP_ECHO_REQUEST
    assert packet['code'] == 0
    assert packet['ID'] == 0xFEFF
    assert packet['sequence'] == 0xEFEE


def test_decode_real_echo():
    '''Test what happens when data from a real packet is sent to
    buf_to_icmp. I've captured an echo reply, and extracted the ICMP
    headeers and payload from it'''
    packet = buf_to_icmp(
        b'\x00\x00\x67\xbb\x08\x1b\x00\x00\x5a\x02\x2d\xaf\x00' +
        b'\x05\x1d\x70\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11' +
        b'\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e' +
        b'\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b' +
        b'\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37',
        socket.AF_INET)
    assert packet['type'] == ICMP_ECHO_REPLY
    assert packet['code'] == 0
    assert packet['ID'] == 0x081b
    assert packet['sequence'] == 0x0000


def test_decode_real_ttl_exceeded():
    # Test a ICMP Time Exceeded packet, this buf comes from a packet
    # capture.
    buf = b'\x0b\x00\xbf\x89\x00\x00\x00\x00\x45\x00\x00\x54\xca' + \
        b'\x05\x40\x00\x01\x01\xf0\xc8\xac\x1f\x02\xac\x08\x08' + \
        b'\x08\x08\x08\x00\xf6\xc4\x36\xb0\x00\x01'
    packet = buf_to_icmp(buf, socket.AF_INET)
    assert packet['type'] == ICMP_TIME_EXCEEDED
    assert packet['original']['type'] == ICMP_ECHO_REQUEST
    assert packet['original']['destination'] \
        == socket.inet_ntop(socket.AF_INET, b'\x08\x08\x08\x08')

    # Take that same buf, but create an invalid IHL field.
    buf = b'\x0b\x00\xbf\x89\x00\x00\x00\x00\x43\x00\x00\x54\xca' + \
        b'\x05\x40\x00\x01\x01\xf0\xc8\xac\x1f\x02\xac\x08\x08' + \
        b'\x08\x08\x08\x00\xf6\xc4\x36\xb0\x00\x01'
    with pytest.raises(RuntimeError) as e:
        packet = buf_to_icmp(buf, socket.AF_INET)
    assert 'IHL field smaller than legal' in str(e.value)


@given(binary(min_size=8), just(socket.AF_INET))
def test_decode_random_v4(binary_data, family):

    # Filter out buffers with icmp type ICMP_DEST_UNREACH (3),
    # ICMP_TIME_EXCEEDED (11) that are too short.
    assume(not(binary_data[0:1] in (b'\x0b', b'\x03')
           and len(binary_data) < 28))

    # Filter out buffers with icmp type ICMP_DEST_UNREACH (3) or
    # ICMP_TIME_EXCEEDED (11) that have an inner packet that has the wrong
    # IP version field.
    assume(not(
        binary_data[0:1] in (b'\x0b', b'\x03')
        and ((struct.unpack("B", binary_data[8:9])[0] & 0xf0) >> 4) != 4))

    packet = buf_to_icmp(binary_data, family)
    assert isinstance(packet, dict)


@given(binary(min_size=12), just(socket.AF_INET6))
def test_decode_random_v6(binary_data, family):
    # Filter out buffers with icmp type ICMPV6_DEST_UNREACH (1),
    # ICMPV6_TIME_EXCEEDED (3) that are too short.
    assume(not(binary_data[0:1] in (b'\x01', b'\x03')
           and len(binary_data) < 48))

    packet = buf_to_icmp(binary_data, family)
    assert isinstance(packet, dict)


def test_decode_not_ip4():
    '''Check suitable exception raised when calling buf_to_icmp4, but we
    pass in a packet that is not an IPv4 packets.'''

    with pytest.raises(RuntimeError) as e:
        buf_to_icmp4(b'\x03' + b'\x00'*27)
    assert 'not a version 4 IP packet' in str(e.value)


def test_decode_ihl_to_small():
    '''Check suitable exception raised when calling buf_to_icmp4, but we
    pass in a packet that has an ihl field with a value that is too small'''

    with pytest.raises(RuntimeError) as e:
        buf_to_icmp4(b'\x43' + b'\x00'*27)
    assert 'IHL field smaller than legal' in str(e.value)


def test_decode_ip4_to_short():
    '''Check suitable exception raised when calling buf_to_icmp4, but we
    pass in a packet that is too short'''

    with pytest.raises(RuntimeError) as e:
        buf_to_icmp4(b'E\x00\x00\x00\x00\x00\x00\x00')
    assert 'buffer to short' in str(e.value)


@given(binary(min_size=28))
def test_decode_random_v4_whole_packet(binary_data):

    # Filter out packets that aren't IPv4
    assume(((struct.unpack("!B", binary_data[0:1])[0] & 0xf0) >> 4) == 4)

    ihl = struct.unpack("!B", binary_data[0:1])[0] & 0x0f

    # Filter out packets that have an IHL that is too small
    assume(ihl >= 5)

    # Filter out packets where the IHL dictates a packet of a certain
    # length, but the packet isn't that length.
    assume(len(binary_data) >= (ihl*4+8))

    packet = buf_to_icmp4(binary_data)
    assert isinstance(packet, dict)
