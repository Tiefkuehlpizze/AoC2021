import dataclasses
import typing
from collections import deque

LENGTH_TYPE_TOTAL_LENGTH = '0'
LENGTH_TYPE_NUM_SUB_PACKETS = '1'

PACKET_TYPE_SUM = 0
PACKET_TYPE_MUL = 1
PACKET_TYPE_MIN = 2
PACKET_TYPE_MAX = 3
PACKET_TYPE_LITERAL = 4
PACKET_TYPE_GT = 5
PACKET_TYPE_LT = 6
PACKET_TYPE_EQ = 7


class TransmissionReader:
    _transmission: deque[str]

    def __init__(self, binary_transmission: str):
        """
        Reads a binary string represented as string with '0' and '1' characters.
        Each character represents a single bit.

        :param binary_transmission: a string containing only 0 and 1 characters
        """
        self._transmission = deque(binary_transmission)

    def _read(self, bits: int) -> str:
        return ''.join(self._transmission.popleft() for _ in range(bits))

    def _read_literal(self) -> int:
        number = 0
        while True:
            chunk = int(self._read(5), 2)
            number <<= 4
            number |= chunk & 0b1111
            if chunk & 0b10000 == 0:
                break
        return number

    @property
    def eof(self) -> bool:
        return not bool(self._transmission)

    def read_packet(self):
        # first 3 bits are packet version
        packet_version = int(self._read(3), 2)
        # second 3 bits are packet type
        packet_type = int(self._read(3), 2)

        # variable initialization for later
        literal = -1
        packets = ()

        if packet_type == PACKET_TYPE_LITERAL:
            literal = self._read_literal()
        else:
            length_type = self._read(1)

            if length_type == LENGTH_TYPE_TOTAL_LENGTH:
                # total length reads a 15 bits number with the length of the sub packages
                # this length is used to read the input for a sub-TransmissionReader
                sub_packet_length = int(self._read(15), 2)
                sub_packet_transmission = self._read(sub_packet_length)

                reader = TransmissionReader(sub_packet_transmission)
                sub_packets = []
                while not reader.eof:
                    sub_packets.append(reader.read_packet())
                packets = tuple(sub_packets)
            elif length_type == LENGTH_TYPE_NUM_SUB_PACKETS:
                # Num Sub Packets reads a 11 bit number with and reads the specified amount of packets
                num_sub_packets = int(self._read(11), 2)
                sub_packets = []

                for _ in range(num_sub_packets):
                    sub_packets.append(self.read_packet())
                packets = tuple(sub_packets)

        return Packet(packet_version, packet_type, literal, packets)


@dataclasses.dataclass
class Packet:
    packet_version: int
    packet_type: int
    literal: int
    packets: typing.Tuple['Packet', ...]


def get_input() -> str:
    with open('input') as f:
        return f.read().rstrip()


def hex_to_bin(hex_str: str) -> str:
    return ''.join(['{0:04b}'.format(int(c, 16)) for c in hex_str])


def calc_value(packet: Packet) -> int:
    result = 0
    if packet.packet_type == PACKET_TYPE_SUM:
        result = sum(calc_value(s_packet) for s_packet in packet.packets)
    elif packet.packet_type == PACKET_TYPE_MUL:
        result = 1
        for s_packet in packet.packets:
            result *= calc_value(s_packet)
    elif packet.packet_type == PACKET_TYPE_MIN:
        result = min(calc_value(s_packet) for s_packet in packet.packets)
    elif packet.packet_type == PACKET_TYPE_MAX:
        result = max(calc_value(s_packet) for s_packet in packet.packets)
    elif packet.packet_type == PACKET_TYPE_LITERAL:
        return packet.literal
    elif packet.packet_type == PACKET_TYPE_GT:
        # always have exact two sub-packets
        result = int(
            calc_value(packet.packets[0]) >
            calc_value(packet.packets[1])
        )
    elif packet.packet_type == PACKET_TYPE_LT:
        # always have exact two sub-packets
        result = int(
            calc_value(packet.packets[0]) <
            calc_value(packet.packets[1])
        )
    elif packet.packet_type == PACKET_TYPE_EQ:
        # always have exact two sub-packets
        result = int(
            calc_value(packet.packets[0]) ==
            calc_value(packet.packets[1])
        )
    return result


def part1():
    reader = TransmissionReader(hex_to_bin(get_input()))
    packet_q = [reader.read_packet()]

    version_sum = 0
    while packet_q:
        packet = packet_q.pop()
        version_sum += packet.packet_version
        packet_q.extend(packet.packets)
    print(version_sum)


def part2():
    reader = TransmissionReader(hex_to_bin(get_input()))
    root_packet = reader.read_packet()
    print(calc_value(root_packet))


if __name__ == '__main__':
    from timeit import timeit

    runs = 10
    print(timeit(part1, number=runs) / runs)
    print(timeit(part2, number=runs) / runs)
